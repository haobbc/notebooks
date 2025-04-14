# dicom_metadata_stable.py
import os
import sqlite3
import pydicom
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import sys
import time # For simple progress timing

# --- 設定 ---
DEFAULT_MAX_WORKERS = os.cpu_count() or 4
# Batch size for database insertion (matches user's 5000-10000 range)
DB_BATCH_SIZE = 8000
# Progress reporting frequency (every N files processed in parallel phase)
PROGRESS_REPORT_INTERVAL = 10000

# --- 要提取的元數據欄位 ---
# (與之前的版本相同)
metadata_fields = {
    "file_path": lambda ds, fp: str(fp), # File path is special, comes from argument
    "study_date": lambda ds, fp: ds.get((0x0008, 0x0020), "N/A").value if (0x0008, 0x0020) in ds else "N/A",
    "series_date": lambda ds, fp: ds.get((0x0008, 0x0021), "N/A").value if (0x0008, 0x0021) in ds else "N/A",
    "acquisition_date": lambda ds, fp: ds.get((0x0008, 0x0022), "N/A").value if (0x0008, 0x0022) in ds else "N/A",
    "content_date": lambda ds, fp: ds.get((0x0008, 0x0023), "N/A").value if (0x0008, 0x0023) in ds else "N/A",
    "study_time": lambda ds, fp: ds.get((0x0008, 0x0030), "N/A").value if (0x0008, 0x0030) in ds else "N/A",
    "series_time": lambda ds, fp: ds.get((0x0008, 0x0031), "N/A").value if (0x0008, 0x0031) in ds else "N/A",
    "acquisition_time": lambda ds, fp: ds.get((0x0008, 0x0032), "N/A").value if (0x0008, 0x0032) in ds else "N/A",
    "modality": lambda ds, fp: ds.get((0x0008, 0x0060), "N/A").value if (0x0008, 0x0060) in ds else "N/A",
    "manufacturer": lambda ds, fp: ds.get((0x0008, 0x0070), "N/A").value if (0x0008, 0x0070) in ds else "N/A",
    "institution_name": lambda ds, fp: ds.get((0x0008, 0x0080), "N/A").value if (0x0008, 0x0080) in ds else "N/A",
    "study_description": lambda ds, fp: ds.get((0x0008, 0x1030), "N/A").value if (0x0008, 0x1030) in ds else "N/A",
    "series_description": lambda ds, fp: ds.get((0x0008, 0x103E), "N/A").value if (0x0008, 0x103E) in ds else "N/A",
    "patient_id": lambda ds, fp: ds.get((0x0010, 0x0020), "N/A").value if (0x0010, 0x0020) in ds else "N/A",
    "patient_sex": lambda ds, fp: ds.get((0x0010, 0x0040), "N/A").value if (0x0010, 0x0040) in ds else "N/A",
    "patient_age": lambda ds, fp: ds.get((0x0010, 0x1010), "N/A").value if (0x0010, 0x1010) in ds else "N/A",
    "slice_thickness": lambda ds, fp: ds.get((0x0018, 0x0050), "N/A").value if (0x0018, 0x0050) in ds else "N/A",
    "study_instance_uid": lambda ds, fp: ds.get((0x0020, 0x000D), "N/A").value if (0x0020, 0x000D) in ds else "N/A",
    "series_instance_uid": lambda ds, fp: ds.get((0x0020, 0x000E), "N/A").value if (0x0020, 0x000E) in ds else "N/A"
}
# 預先產生 INSERT 語句
INSERT_COLUMNS = ", ".join(metadata_fields.keys())
INSERT_PLACEHOLDERS = ", ".join(["?"] * len(metadata_fields))
INSERT_SQL = f"INSERT OR IGNORE INTO dicom_metadata ({INSERT_COLUMNS}) VALUES ({INSERT_PLACEHOLDERS})"

# --- Helper Functions ---

def scan_all_dicom_files(dicom_dirs):
    """Phase 1: Scan all directories and return a list of all potential DICOM file paths."""
    all_files = []
    print(f"[{datetime.now()}] Phase 1: Scanning directories...")
    for directory in dicom_dirs:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or is not a directory, skipping: {directory}")
            continue
        print(f"Scanning: {directory}")
        count = 0
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".dcm"):
                    all_files.append(os.path.join(root, file))
                    count += 1
        print(f"Found {count} potential DICOM files in {directory}.")
    print(f"[{datetime.now()}] Phase 1: Scan complete. Total potential files found: {len(all_files)}")
    return all_files

def filter_unprocessed_files(all_files, conn):
    """Phase 2: Query DB to find files that haven't been processed yet."""
    files_to_process = []
    processed_count = 0
    total_files = len(all_files)
    print(f"[{datetime.now()}] Phase 2: Filtering {total_files} files against database...")
    c = conn.cursor()
    start_time = time.time()
    for i, file_path in enumerate(all_files):
        c.execute("SELECT 1 FROM dicom_metadata WHERE file_path = ?", (file_path,))
        if c.fetchone() is None:
            files_to_process.append(file_path)
        else:
            processed_count += 1

        if (i + 1) % 20000 == 0: # Progress update for filtering
             elapsed = time.time() - start_time
             rate = (i + 1) / elapsed if elapsed > 0 else 0
             print(f"Checked: {i+1}/{total_files} | Found processed: {processed_count} | Rate: {rate:.0f} files/sec")

    end_time = time.time()
    print(f"[{datetime.now()}] Phase 2: Filtering complete in {end_time - start_time:.2f} seconds.")
    print(f"Total files checked: {total_files}")
    print(f"Already processed: {processed_count}")
    print(f"Files to process : {len(files_to_process)}")
    return files_to_process

def extract_metadata_only(file_path):
    """Phase 3 Task: Read DICOM and extract metadata. No DB interaction."""
    try:
        # Use force=True to try reading slightly non-compliant files
        ds = pydicom.dcmread(file_path, stop_before_pixels=True, force=True)
        # Basic check if it's a DICOM file with some common identifier
        if (0x0008, 0x0016) not in ds:
            # print(f"Warning: Missing SOPClassUID: {file_path}") # Optional warning
            return None

        metadata = {}
        for key, func in metadata_fields.items():
            metadata[key] = func(ds, file_path)

        # Convert special types (like UID) to strings for database compatibility
        for key, value in metadata.items():
            if not isinstance(value, (str, int, float, type(None))):
                metadata[key] = str(value)
        return metadata # Return the dictionary
    except pydicom.errors.InvalidDicomError:
        # print(f"Skipping invalid DICOM file: {file_path}") # Optional warning
        return None
    except Exception as e:
        print(f"Error reading/extracting {file_path}: {e}")
        return None # Return None on error

def insert_batch(conn, metadata_tuples):
    """Helper to insert batch, returns number of rows attempted."""
    if not metadata_tuples:
        return 0
    try:
        c = conn.cursor()
        c.executemany(INSERT_SQL, metadata_tuples)
        # Note: executemany doesn't reliably return row count in sqlite3
        return len(metadata_tuples)
    except sqlite3.Error as e:
        print(f"Database batch insert error: {e}")
        # Consider logging the failed batch data here if needed
        return 0 # Indicate failure / 0 inserted on error


def process_files_parallel_and_insert(files_to_process, conn, max_workers, batch_size):
    """Phase 3 & 4: Process files in parallel, collect results, and insert into DB in batches."""
    total_to_process = len(files_to_process)
    if total_to_process == 0:
        print(f"[{datetime.now()}] Phase 3 & 4: No new files to process.")
        return 0

    print(f"[{datetime.now()}] Phase 3: Starting parallel metadata extraction for {total_to_process} files using {max_workers} workers...")
    start_time = time.time()
    processed_count = 0
    inserted_count = 0
    batch_results = [] # Accumulate results for batch insertion

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create futures for all files to process
        future_to_file = {executor.submit(extract_metadata_only, f): f for f in files_to_process}

        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                metadata_dict = future.result() # Get the result dictionary (or None)
                if metadata_dict:
                    # Convert dict to ordered tuple for insertion
                    metadata_tuple = tuple(metadata_dict[key] for key in metadata_fields.keys())
                    batch_results.append(metadata_tuple)
                    processed_count += 1 # Count successful extractions

                    # Check if batch is ready to be inserted
                    if len(batch_results) >= batch_size:
                        print(f"[{datetime.now()}] Inserting batch of {len(batch_results)} records...")
                        inserted = insert_batch(conn, batch_results)
                        inserted_count += inserted
                        batch_results = [] # Clear batch

            except Exception as e:
                print(f"Error processing future for {file_path}: {e}")
                # processed_count is not incremented for errors

            # Progress reporting
            current_completed = processed_count + (total_to_process - len(future_to_file) - processed_count) # Estimate completed tasks
            if current_completed % PROGRESS_REPORT_INTERVAL == 0 and current_completed > 0 :
                 elapsed = time.time() - start_time
                 rate = current_completed / elapsed if elapsed > 0 else 0
                 print(f"Progress: {current_completed}/{total_to_process} | Successful: {processed_count} | Rate: {rate:.0f} files/sec")


    # Insert any remaining results after the loop finishes
    if batch_results:
        print(f"[{datetime.now()}] Inserting final batch of {len(batch_results)} records...")
        inserted = insert_batch(conn, batch_results)
        inserted_count += inserted

    # --- Commit once after all processing is done ---
    try:
        print(f"[{datetime.now()}] Phase 4: Committing all changes...")
        conn.commit()
        print(f"[{datetime.now()}] Commit successful.")
    except sqlite3.Error as e:
        print(f"FATAL: Database commit error: {e}")
        # Consider rollback? Might lose work.

    end_time = time.time()
    print(f"[{datetime.now()}] Phase 3 & 4: Processing and Insertion complete in {end_time - start_time:.2f} seconds.")
    print(f"Successfully extracted metadata for: {processed_count}/{total_to_process} files.")
    print(f"Attempted to insert records: {inserted_count} (due to INSERT OR IGNORE, actual new rows might be slightly less if duplicates somehow occurred)")
    return processed_count

def create_db_table(conn):
    """Creates the database table if it doesn't exist."""
    try:
        c = conn.cursor()
        column_defs = ",\n".join([f"    {key} TEXT" for key in metadata_fields.keys()])
        column_defs = column_defs.replace("file_path TEXT", "file_path TEXT PRIMARY KEY")
        create_table_sql = f'''CREATE TABLE IF NOT EXISTS dicom_metadata (
{column_defs}
)'''
        c.execute(create_table_sql)
        # Add index on other commonly queried fields if needed for performance
        # c.execute("CREATE INDEX IF NOT EXISTS idx_study_uid ON dicom_metadata(study_instance_uid);")
        # c.execute("CREATE INDEX IF NOT EXISTS idx_series_uid ON dicom_metadata(series_instance_uid);")
        # c.execute("CREATE INDEX IF NOT EXISTS idx_patient_id ON dicom_metadata(patient_id);")
        conn.commit()
        print("Database table 'dicom_metadata' checked/created successfully.")
    except sqlite3.Error as e:
        print(f"Fatal: Could not create database table: {e}")
        sys.exit(1)


# --- Main Execution ---
def main(dicom_dirs, db_file, max_workers, batch_size):
    """Main function orchestrating the stable workflow."""
    print(f"[{datetime.now()}] Starting stable metadata extraction process...")
    print(f"Database file: {db_file}")
    print(f"Target directories: {', '.join(dicom_dirs)}")
    print(f"Max worker threads: {max_workers}")
    print(f"Database batch size: {batch_size}")
    overall_start_time = datetime.now()

    conn = None
    try:
        # Connect to DB - check_same_thread=False is NOT needed now as DB access is sequential
        conn = sqlite3.connect(db_file, timeout=30.0)
        print(f"Connected to database: {db_file}")
        create_db_table(conn)
    except sqlite3.Error as e:
        print(f"Fatal: Could not connect to or initialize database {db_file}: {e}")
        if conn: conn.close()
        sys.exit(1)

    try:
        # Phase 1: Scan all files
        all_files = scan_all_dicom_files(dicom_dirs)
        print("-" * 30)

        # Phase 2: Filter unprocessed files
        files_to_process = filter_unprocessed_files(all_files, conn)
        print("-" * 30)

        # Phase 3 & 4: Process in parallel and insert results
        successfully_processed_count = process_files_parallel_and_insert(
            files_to_process, conn, max_workers, batch_size
        )

    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        # Optionally rollback if commit hasn't happened?
        # if conn: conn.rollback()
    finally:
        # Ensure connection is closed
        if conn:
            try:
                conn.close()
                print(f"Database connection closed.")
            except sqlite3.Error as e:
                print(f"Error closing database connection: {e}")

    overall_end_time = datetime.now()
    print("=" * 50)
    print(f"[{datetime.now()}] Overall process finished.")
    print(f"Total execution time: {overall_end_time - overall_start_time}")
    print(f"Processed and attempted insert for {successfully_processed_count} new files in this run.")
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stable DICOM metadata extraction: Scan, Filter, Process in Parallel, Insert Sequentially.")
    parser.add_argument("dicom_dirs", type=str, nargs="+",
                        help="One or more absolute paths to DICOM directories.")
    parser.add_argument("-o", "--output", type=str, default="dicom_metadata.db",
                        help="Path to the output SQLite database file.")
    parser.add_argument("-w", "--workers", type=int, default=DEFAULT_MAX_WORKERS,
                        help=f"Number of worker threads for parallel extraction (default: {DEFAULT_MAX_WORKERS}).")
    parser.add_argument("-b", "--batchsize", type=int, default=DB_BATCH_SIZE,
                        help=f"Number of records to insert into DB per batch (default: {DB_BATCH_SIZE}).")

    args = parser.parse_args()

    db_file_path = os.path.abspath(args.output)
    absolute_dicom_dirs = [os.path.abspath(d) for d in args.dicom_dirs]

    main(absolute_dicom_dirs, db_file_path, args.workers, args.batchsize)
    
