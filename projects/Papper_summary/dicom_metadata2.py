# dicom_metadata.py
import os
import sqlite3
from pathlib import Path # Pathlib is imported but less used than os.path, consider consolidating usage if desired.
import pydicom
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys # For exiting on error

# --- 設定 ---
# 執行緒數量，可根據 CPU 核心數和 I/O 狀況調整
# 如果 I/O 是瓶頸 (例如慢速硬碟)，過多的執行緒可能幫助不大
DEFAULT_MAX_WORKERS = os.cpu_count() or 4 # Use CPU count as a default, fallback to 4

# --- 要提取的元數據欄位 ---
# 使用 lambda 函數安全地提取值，如果標籤不存在則返回 "N/A"
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
# 預先產生 INSERT 語句的欄位和問號部分
INSERT_COLUMNS = ", ".join(metadata_fields.keys())
INSERT_PLACEHOLDERS = ", ".join(["?"] * len(metadata_fields))
INSERT_SQL = f"INSERT OR IGNORE INTO dicom_metadata ({INSERT_COLUMNS}) VALUES ({INSERT_PLACEHOLDERS})"

def extract_metadata(file_path_str, conn):
    """
    提取單個 DICOM 檔案的元數據。
    先檢查資料庫中是否已存在該檔案路徑，若存在則跳過。
    Args:
        file_path_str (str): DICOM 檔案的完整路徑。
        conn (sqlite3.Connection): 資料庫連接物件。
    Returns:
        dict or None: 包含提取元數據的字典，如果檔案已存在、讀取錯誤或非 DICOM 則返回 None。
    """
    c = conn.cursor()
    # 檢查檔案是否已存在於資料庫
    c.execute("SELECT 1 FROM dicom_metadata WHERE file_path = ?", (file_path_str,))
    if c.fetchone():
        # print(f"Skipping already processed file: {file_path_str}") # 可選：取消註解以顯示跳過的檔案
        return None  # 已存在，跳過

    try:
        # stop_before_pixels=True 極大地加快讀取速度，因為我們不需要像素數據
        ds = pydicom.dcmread(file_path_str, stop_before_pixels=True, force=True) # force=True 嘗試讀取一些輕微損壞的檔案

        # 檢查是否有必要的 DICOM 標頭 (例如 SOPClassUID)，確認是 DICOM 檔案
        if (0x0008, 0x0016) not in ds:
             print(f"Warning: Missing SOPClassUID or not a standard DICOM file: {file_path_str}")
             return None # 可能不是有效的 DICOM 檔案

        metadata = {}
        for key, func in metadata_fields.items():
            metadata[key] = func(ds, file_path_str) # 傳遞 ds 和 file_path_str 給 lambda

        # pydicom 讀取的數據可能是特殊類型 (如 pydicom.uid.UID)，轉換為字串以便儲存
        for key, value in metadata.items():
            if not isinstance(value, (str, int, float, type(None))):
                metadata[key] = str(value)
            # 處理日期和時間，確保格式一致 (如果需要)
            # if key.endswith('_date') and isinstance(value, str) and len(value) == 8:
            #     try:
            #         metadata[key] = f"{value[:4]}-{value[4:6]}-{value[6:]}" # 轉成 YYYY-MM-DD
            #     except: pass # 忽略格式錯誤
            # elif key.endswith('_time') and isinstance(value, str) and '.' in value:
            #      metadata[key] = value.split('.')[0] # 去掉毫秒

        return metadata
    except pydicom.errors.InvalidDicomError:
        # print(f"Skipping invalid DICOM file: {file_path_str}") # 可選：顯示無效檔案
        return None # 不是有效的 DICOM 檔案
    except Exception as e:
        print(f"Error reading DICOM file {file_path_str}: {e}")
        return None

def scan_dicom_files(directory):
    """
    遞迴掃描指定目錄及其子目錄下的所有檔案，生成 DICOM 檔案的路徑。
    Args:
        directory (str): 要掃描的目錄路徑。
    Yields:
        str: 找到的 DICOM 檔案的完整路徑 (.dcm 結尾，不區分大小寫)。
    """
    print(f"Scanning for DICOM files in: {directory}")
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".dcm"):
                count += 1
                yield os.path.join(root, file)
    print(f"Found {count} potential DICOM files in {directory}.")


def process_file_batch(file_paths, conn):
    """
    處理一批檔案並將元數據插入資料庫。
    Args:
        file_paths (list): 包含多個檔案路徑的列表。
        conn (sqlite3.Connection): 資料庫連接物件。
    Returns:
        int: 成功處理並插入資料庫的檔案數量。
    """
    processed_count = 0
    metadata_list = []
    for file_path in file_paths:
        metadata = extract_metadata(file_path, conn)
        if metadata:
            # 將字典的值按照 metadata_fields 的順序排列
            ordered_values = tuple(metadata[key] for key in metadata_fields.keys())
            metadata_list.append(ordered_values)

    if metadata_list:
        try:
            c = conn.cursor()
            # 使用 executemany 進行批量插入，效率更高
            c.executemany(INSERT_SQL, metadata_list)
            # 注意：Commit 不在這裡做，由調用者 (process_directory) 控制
            processed_count = len(metadata_list)
        except sqlite3.Error as e:
            print(f"Database error during batch insert: {e}")
            # 可以考慮在這裡加入錯誤處理，例如記錄失敗的批次
    return processed_count


def process_directory(dicom_dir, db_file, conn, max_workers):
    """
    處理單個目錄中的所有 DICOM 檔案。
    Args:
        dicom_dir (str): DICOM 檔案所在的目錄路徑。
        db_file (str): SQLite 資料庫檔案路徑 (主要用於記錄)。
        conn (sqlite3.Connection): 資料庫連接物件。
        max_workers (int): 線程池的最大工作線程數。
    Returns:
        tuple: (成功處理的檔案數, 掃描到的總檔案數)
    """
    print(f"[{datetime.now()}] Starting processing directory: {dicom_dir}")
    start_time = datetime.now()

    # 使用生成器掃描檔案，避免一次性載入所有路徑到記憶體
    file_generator = scan_dicom_files(dicom_dir)

    total_processed_in_dir = 0
    files_scanned = 0 # 用來估計總數，雖然生成器無法預知總數

    # 批量處理檔案以減少資料庫寫入次數
    batch_size = 1000 # 每 1000 個檔案處理一次並檢查進度

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        file_batch = []
        for file_path in file_generator:
            files_scanned += 1
            file_batch.append(file_path)

            if len(file_batch) >= batch_size:
                # 提交一批檔案給線程池處理
                # 傳遞當前的 conn 物件，因為 SQLite 在多線程寫入時需要謹慎處理
                # 我們的策略是讀取並行，寫入通過 process_file_batch 批量串行化
                futures.append(executor.submit(process_file_batch, file_batch, conn))
                file_batch = [] # 清空批次

            # 定期檢查已完成的 future 並更新進度
            # 這有助於及早發現錯誤並釋放記憶體
            completed_futures = [f for f in futures if f.done()]
            for future in completed_futures:
                try:
                    result = future.result() # 獲取批次處理結果 (成功數量)
                    total_processed_in_dir += result
                except Exception as e:
                    print(f"Error in processing batch: {e}") # 處理執行緒中的錯誤
                futures.remove(future) # 從列表中移除已處理的 future

            # 每處理 N 個檔案打印一次進度 (基於掃描到的檔案)
            if files_scanned % (batch_size * 5) == 0: # 每 5 個批次的大小打印一次
                 print(f"[{datetime.now()}] Scanned: {files_scanned}, Batches submitted: {len(futures)}, Approx processed: {total_processed_in_dir} in {dicom_dir}")

        # 處理剩餘不足一個批次的檔案
        if file_batch:
            futures.append(executor.submit(process_file_batch, file_batch, conn))

        # 等待所有剩餘的任務完成
        print(f"[{datetime.now()}] Waiting for remaining batches ({len(futures)}) to complete for {dicom_dir}...")
        for future in futures: # 使用 as_completed 可能更優，但直接迭代也可以
            try:
                result = future.result()
                total_processed_in_dir += result
            except Exception as e:
                print(f"Error processing final batch: {e}")

    # --- 優化：在處理完一個目錄的所有檔案後進行一次 commit ---
    try:
        print(f"[{datetime.now()}] Committing changes for directory: {dicom_dir}")
        conn.commit()
        print(f"[{datetime.now()}] Commit successful for {dicom_dir}.")
    except sqlite3.Error as e:
        print(f"Database commit error for {dicom_dir}: {e}")
        # 可以考慮在這裡回滾或採取其他錯誤處理措施
        # conn.rollback()

    end_time = datetime.now()
    print(f"[{datetime.now()}] Completed processing {dicom_dir} in {end_time - start_time}")
    print(f"[{datetime.now()}] Total files scanned in {dicom_dir}: {files_scanned}")
    print(f"[{datetime.now()}] Total files successfully processed and potentially inserted in {dicom_dir}: {total_processed_in_dir}")
    # 注意：total_processed_in_dir 是成功讀取並嘗試插入的數量，由於 INSERT OR IGNORE，實際新增的行數可能較少

    return total_processed_in_dir, files_scanned # 返回處理數和掃描數

def create_db_table(conn):
    """創建資料庫表格 (如果不存在)"""
    try:
        c = conn.cursor()
        # 生成 CREATE TABLE 語句的欄位定義部分
        column_defs = ",\n".join([f"    {key} TEXT" for key in metadata_fields.keys()])
        # 將 file_path 設為主鍵
        column_defs = column_defs.replace("file_path TEXT", "file_path TEXT PRIMARY KEY")

        create_table_sql = f'''CREATE TABLE IF NOT EXISTS dicom_metadata (
{column_defs}
)'''
        # print("Executing SQL:\n", create_table_sql) # Debug: 查看SQL語句
        c.execute(create_table_sql)
        conn.commit()
        print("Database table 'dicom_metadata' checked/created successfully.")
    except sqlite3.Error as e:
        print(f"Fatal: Could not create database table: {e}")
        sys.exit(1) # 無法創建表格，退出程序


def main(dicom_dirs, db_file, max_workers):
    """主函數，處理所有指定的 DICOM 目錄"""
    print(f"[{datetime.now()}] Starting metadata extraction process...")
    print(f"Database file: {db_file}")
    print(f"Target directories: {', '.join(dicom_dirs)}")
    print(f"Max worker threads: {max_workers}")
    overall_start_time = datetime.now()

    conn = None # 初始化 conn
    try:
        # 連接到 SQLite 資料庫 (如果檔案不存在，會自動創建)
        # isolation_level=None 可以讓 commit 手動控制，但這裡我們使用預設級別並手動 commit
        # timeout 增加等待鎖的時間，以防萬一
        conn = sqlite3.connect(db_file, timeout=30.0)
        print(f"Connected to database: {db_file}")

        # 創建表格 (如果不存在)
        create_db_table(conn)

    except sqlite3.Error as e:
        print(f"Fatal: Could not connect to or initialize database {db_file}: {e}")
        sys.exit(1) # 連接失敗，退出

    overall_processed = 0
    overall_scanned = 0

    # 依序處理每個指定的目錄
    for dicom_dir in dicom_dirs:
        if not os.path.isdir(dicom_dir):
            print(f"Warning: Directory not found or is not a directory, skipping: {dicom_dir}")
            continue # 跳過無效的目錄

        # 為每個目錄調用處理函數
        processed, scanned = process_directory(dicom_dir, db_file, conn, max_workers)
        overall_processed += processed
        overall_scanned += scanned
        print("-" * 30) # 分隔不同目錄的輸出

    # 所有目錄處理完畢後關閉資料庫連接
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
    print(f"Total directories processed: {len(dicom_dirs)}")
    print(f"Total files scanned across all directories: {overall_scanned}")
    print(f"Total files successfully processed and potentially inserted: {overall_processed}")
    print("=" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract DICOM metadata from specified directories and save to an SQLite database.")
    parser.add_argument("dicom_dirs", type=str, nargs="+",
                        help="One or more absolute paths to DICOM directories (space-separated).")
    parser.add_argument("-o", "--output", type=str, default="dicom_metadata.db",
                        help="Path to the output SQLite database file (default: dicom_metadata.db in the current directory).")
    parser.add_argument("-w", "--workers", type=int, default=DEFAULT_MAX_WORKERS,
                        help=f"Number of worker threads for parallel processing (default: {DEFAULT_MAX_WORKERS}).")

    args = parser.parse_args()

    # 確保輸出路徑是絕對路徑或相對於腳本執行位置
    db_file_path = os.path.abspath(args.output)
    # 確保輸入目錄是絕對路徑
    absolute_dicom_dirs = [os.path.abspath(d) for d in args.dicom_dirs]

    # 執行主函數
    main(absolute_dicom_dirs, db_file_path, args.workers)