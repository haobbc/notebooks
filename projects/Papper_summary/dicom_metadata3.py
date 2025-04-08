# dicom_metadata_from_filelist.py
import os
import sqlite3
import pydicom
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import sys
import time

# --- 設定 ---
DEFAULT_MAX_WORKERS = os.cpu_count() or 4
DB_BATCH_SIZE = 8000
PROGRESS_REPORT_INTERVAL = 10000

# --- 元數據欄位和 SQL (與之前相同) ---
metadata_fields = {
    "file_path": lambda ds, fp: str(fp),
    # ... (其他欄位定義不變) ...
    "series_instance_uid": lambda ds, fp: ds.get((0x0020, 0x000E), "N/A").value if (0x0020, 0x000E) in ds else "N/A"
}
INSERT_COLUMNS = ", ".join(metadata_fields.keys())
INSERT_PLACEHOLDERS = ", ".join(["?"] * len(metadata_fields))
INSERT_SQL = f"INSERT OR IGNORE INTO dicom_metadata ({INSERT_COLUMNS}) VALUES ({INSERT_PLACEHOLDERS})"

# --- Helper Functions (大部分與之前相同) ---

def read_file_list(file_path):
    """Phase 1 (Modified): Read file paths from a text file."""
    all_files = []
    print(f"[{datetime.now()}] Phase 1: Reading file list from: {file_path}")
    try:
        with open(file_path, 'r') as f:
            for line in f:
                path = line.strip()
                if path: # Ensure not adding empty lines
                    # Optional: Add basic check like os.path.exists(path) here if needed
                    all_files.append(path)
        print(f"[{datetime.now()}] Phase 1: Read complete. Found {len(all_files)} paths in the list.")
        return all_files
    except FileNotFoundError:
        print(f"Error: Input file list '{file_path}' not found.")
        return [] # Return empty list on error
    except Exception as e:
        print(f"Error reading file list '{file_path}': {e}")
        return []

def filter_unprocessed_files(all_files, conn):
    """Phase 2: Filter using In-Memory Set (與之前相同)."""
    files_to_process = []
    processed_paths = set()
    total_files = len(all_files)
    if total_files == 0:
        print(f"[{datetime.now()}] Phase 2: Input file list is empty. No files to filter.")
        return []

    print(f"[{datetime.now()}] Phase 2: Fetching existing paths from database...")
    start_time_fetch = time.time()
    try:
        c = conn.cursor()
        # Fetch all paths at once - make sure this fits reasonably in RAM along with all_files
        processed_paths = set(row[0] for row in c.execute("SELECT file_path FROM dicom_metadata"))
        fetch_time = time.time() - start_time_fetch
        print(f"Fetched {len(processed_paths)} existing paths in {fetch_time:.2f} seconds.")
    except sqlite3.Error as e:
        print(f"Error fetching existing paths from DB: {e}")
        print("Proceeding without filtering - may re-process files.")
        processed_paths = set() # Continue without filtering if DB read fails

    print(f"Filtering {total_files} scanned paths against {len(processed_paths)} existing paths...")
    start_time_filter = time.time()
    # Use list comprehension for efficient filtering
    files_to_process = [f for f in all_files if f not in processed_paths]
    filter_time = time.time() - start_time_filter
    print(f"[{datetime.now()}] Phase 2: Filtering complete in {filter_time:.2f} seconds.")
    print(f"Files to process: {len(files_to_process)}")
    return files_to_process

# --- extract_metadata_only (與之前相同) ---
def extract_metadata_only(file_path):
    """Phase 3 Task: Read DICOM and extract metadata. No DB interaction."""
    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True, force=True)
        if (0x0008, 0x0016) not in ds: return None
        metadata = {}
        for key, func in metadata_fields.items():
            metadata[key] = func(ds, file_path)
        for key, value in metadata.items():
            if not isinstance(value, (str, int, float, type(None))):
                metadata[key] = str(value)
        return metadata
    except Exception: # Catch broad exception here
        # print(f"Error reading/extracting {file_path}: {e}") # Can be too verbose
        return None

# --- insert_batch (與之前相同) ---
def insert_batch(conn, metadata_tuples):
    """Helper to insert batch, returns number of rows attempted."""
    if not metadata_tuples: return 0
    try:
        c = conn.cursor()
        c.executemany(INSERT_SQL, metadata_tuples)
        return len(metadata_tuples)
    except sqlite3.Error as e:
        print(f"Database batch insert error: {e}")
        return 0

# --- process_files_parallel_and_insert (與之前相同) ---
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
    batch_results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(extract_metadata_only, f): f for f in files_to_process}
        for i, future in enumerate(as_completed(future_to_file)):
            # file_path = future_to_file[future] # Less useful now maybe
            try:
                metadata_dict = future.result()
                if metadata_dict:
                    metadata_tuple = tuple(metadata_dict[key] for key in metadata_fields.keys())
                    batch_results.append(metadata_tuple)
                    processed_count += 1
                    if len(batch_results) >= batch_size:
                        # print(f"[{datetime.now()}] Inserting batch of {len(batch_results)} records...")
                        inserted = insert_batch(conn, batch_results)
                        inserted_count += inserted
                        batch_results = [] # Clear batch
            except Exception: # Ignore errors from futures for now, already logged inside task ideally
                 pass # Or log file_path if needed: print(f"Error processing future for {file_path}: {e}")

            # Progress reporting based on completed futures
            if (i + 1) % PROGRESS_REPORT_INTERVAL == 0:
                 elapsed = time.time() - start_time
                 rate = (i + 1) / elapsed if elapsed > 0 else 0
                 print(f"Progress: {i+1}/{total_to_process} futures completed | Successful: {processed_count} | Rate: {rate:.0f} tasks/sec")

    if batch_results: # Final batch
        # print(f"[{datetime.now()}] Inserting final batch of {len(batch_results)} records...")
        inserted = insert_batch(conn, batch_results)
        inserted_count += inserted

    try: # Final Commit
        print(f"[{datetime.now()}] Phase 4: Committing all changes ({inserted_count} attempted inserts)...")
        conn.commit()
        print(f"[{datetime.now()}] Commit successful.")
    except sqlite3.Error as e:
        print(f"FATAL: Database commit error: {e}")

    end_time = time.time()
    print(f"[{datetime.now()}] Phase 3 & 4: Processing and Insertion complete in {end_time - start_time:.2f} seconds.")
    print(f"Successfully extracted metadata for: {processed_count}/{total_to_process} files.")
    print(f"Attempted to insert records: {inserted_count}")
    return processed_count

# --- create_db_table (與之前相同) ---
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
        # Optional: Add other indices here if needed
        # c.execute("CREATE INDEX IF NOT EXISTS idx_study_uid ON dicom_metadata(study_instance_uid);")
        conn.commit()
        print("Database table 'dicom_metadata' checked/created successfully.")
    except sqlite3.Error as e:
        print(f"Fatal: Could not create database table: {e}")
        sys.exit(1)

# --- Main Execution ---
def main(input_list_file, db_file, max_workers, batch_size):
    """Main function using file list input."""
    print(f"[{datetime.now()}] Starting metadata extraction from file list...")
    print(f"Input file list: {input_list_file}")
    print(f"Database file: {db_file}")
    print(f"Max worker threads: {max_workers}")
    print(f"Database batch size: {batch_size}")
    overall_start_time = datetime.now()

    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=30.0)
        print(f"Connected to database: {db_file}")
        create_db_table(conn) # Ensure table exists
    except sqlite3.Error as e:
        print(f"Fatal: Could not connect to or initialize database {db_file}: {e}")
        if conn: conn.close()
        sys.exit(1)

    successfully_processed_count = 0
    try:
        # Phase 1: Read file list from file
        all_files = read_file_list(input_list_file)
        print("-" * 30)

        if all_files: # Only proceed if list is not empty
            # Phase 2: Filter unprocessed files using in-memory set
            files_to_process = filter_unprocessed_files(all_files, conn)
            print("-" * 30)

            # Phase 3 & 4: Process in parallel and insert results
            successfully_processed_count = process_files_parallel_and_insert(
                files_to_process, conn, max_workers, batch_size
            )
        else:
            print("No files found in the input list to process.")

    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        # import traceback
        # traceback.print_exc() # Uncomment for detailed traceback
    finally:
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
    parser = argparse.ArgumentParser(description="Stable DICOM metadata extraction using an input file list.")
    # !! Changed positional argument to --input-list !!
    parser.add_argument("-i", "--input-list", type=str, required=True,
                        help="Path to the text file containing the list of DICOM file paths (one per line).")
    parser.add_argument("-o", "--output", type=str, default="dicom_metadata.db",
                        help="Path to the output SQLite database file.")
    parser.add_argument("-w", "--workers", type=int, default=DEFAULT_MAX_WORKERS,
                        help=f"Number of worker threads for parallel extraction (default: {DEFAULT_MAX_WORKERS}).")
    parser.add_argument("-b", "--batchsize", type=int, default=DB_BATCH_SIZE,
                        help=f"Number of records to insert into DB per batch (default: {DB_BATCH_SIZE}).")

    args = parser.parse_args()

    db_file_path = os.path.abspath(args.output)
    input_list_file_path = os.path.abspath(args.input_list) # Get absolute path for input list

    main(input_list_file_path, db_file_path, args.workers, args.batchsize)