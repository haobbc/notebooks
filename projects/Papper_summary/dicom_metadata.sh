#!/bin/bash

# --- 配置 ---
CONDA_ENV_NAME="haobbc"                             # Conda 環境名稱
PYTHON_SCRIPT_PATH="/home/user/scrips/dicom_metadata.py" # Python 腳本的絕對路徑
TARGET_DICOM_DIR="/DICOM/xxxx"                      # 要處理的 DICOM 目錄的絕對路徑
DB_FILE_PATH="/home/user/dicom_metadata.db"         # SQLite 資料庫檔案的絕對路徑
LOG_FILE="dicom_metadata_run.log"                   # 執行的日誌檔案 (與 Python 腳本的輸出分開)
# 可以考慮將日誌檔案放在與資料庫相同或更合適的位置，例如：
# LOG_FILE="/home/user/dicom_metadata_run.log"

# --- 功能函數 ---
log_message() {
  # 同時輸出到控制台和日誌檔案
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# --- 主腳本邏輯 ---
log_message "Script started."

# 檢查目標目錄是否存在
if [ ! -d "$TARGET_DICOM_DIR" ]; then
  log_message "Error: Target DICOM directory '$TARGET_DICOM_DIR' not found or is not a directory."
  exit 1
fi

# 檢查 Python 腳本是否存在
if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then
  log_message "Error: Python script '$PYTHON_SCRIPT_PATH' not found."
  exit 1
fi

# 啟動 Conda 環境
log_message "Activating Conda environment: $CONDA_ENV_NAME..."
# 使用 source 或者 conda run 來確保環境正確啟動
# source $(conda info --base)/etc/profile.d/conda.sh # 可能需要這行，取決於你的 conda 初始化設置
conda activate "$CONDA_ENV_NAME"
if [ $? -ne 0 ]; then
  log_message "Error: Failed to activate Conda environment '$CONDA_ENV_NAME'."
  exit 1
fi
log_message "Conda environment activated."

# 執行 Python 腳本
log_message "Starting metadata extraction for directory: $TARGET_DICOM_DIR"
log_message "Output database: $DB_FILE_PATH"

# 使用 python 執行腳本，並傳遞參數
# 注意：TARGET_DICOM_DIR 和 DB_FILE_PATH 加了引號，以處理路徑中可能存在的空格
python "$PYTHON_SCRIPT_PATH" "$TARGET_DICOM_DIR" -o "$DB_FILE_PATH"

# 檢查 Python 腳本的退出狀態碼
SCRIPT_EXIT_CODE=$?
if [ ${SCRIPT_EXIT_CODE} -eq 0 ]; then
  log_message "Python script finished successfully."
else
  log_message "Error: Python script exited with status code ${SCRIPT_EXIT_CODE}."
  # 即使 Python 腳本失敗，仍然嘗試停用 Conda 環境
fi

# 停用 Conda 環境
log_message "Deactivating Conda environment..."
conda deactivate
log_message "Conda environment deactivated."

log_message "Script finished."

# 根據 Python 腳本的結果退出 Shell 腳本
exit ${SCRIPT_EXIT_CODE}