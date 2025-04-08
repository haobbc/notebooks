#!/bin/bash

# --- 配置 ---
CONDA_ENV_NAME="haobbc"
# !! 修改 Python 腳本名稱 (如果需要) !!
PYTHON_SCRIPT_PATH="/home/user/scrips/dicom_metadata_from_filelist.py" # <--- 新檔名?
# !! TARGET_DICOM_DIRS 可以是多個，用空格分隔 !!
TARGET_DICOM_DIRS="/DICOM/xxxx /ANOTHER/DICOM/DIR" # <--- 修改為實際要掃描的目錄(們)
DB_FILE_PATH="/home/user/dicom_metadata.db"
LOG_FILE="dicom_metadata_run.log"
TEMP_FILE_LIST="dicom_paths_temp.txt" # <--- find 命令輸出的臨時檔名
# WORKER_COUNT=8 # 可選
# BATCH_SIZE=8000 # 可選

# --- 功能函數 ---
log_message() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# --- 主腳本邏輯 ---
log_message "Script started (using find + Python)."

# 檢查目標目錄是否存在 (檢查第一個即可，find 會處理不存在的路徑)
first_dir=$(echo $TARGET_DICOM_DIRS | cut -d' ' -f1)
if [ ! -d "$first_dir" ]; then
    log_message "Warning: First target DICOM directory '$first_dir' not found. Continuing scan..."
    # 不退出，讓 find 命令處理
fi
# 檢查 Python 腳本是否存在
if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then
  log_message "Error: Python script '$PYTHON_SCRIPT_PATH' not found."
  exit 1
fi

# --- 步驟 1: 使用 find 命令產生檔案列表 ---
log_message "Phase 1: Generating file list using 'find' for directories: $TARGET_DICOM_DIRS"
# 使用 -iname 進行不區分大小寫的 .dcm 匹配
# 將 TARGET_DICOM_DIRS 作為參數傳遞給 find
find $TARGET_DICOM_DIRS -iname '*.dcm' -type f > "$TEMP_FILE_LIST"
FIND_EXIT_CODE=$?
if [ ${FIND_EXIT_CODE} -ne 0 ]; then
    log_message "Error: 'find' command failed with exit code ${FIND_EXIT_CODE}."
    # 可選擇是否在此處退出
    # exit 1
fi
# 檢查文件是否為空
if [ ! -s "$TEMP_FILE_LIST" ]; then
    log_message "Warning: 'find' command did not find any '.dcm' files or the output file is empty."
    # 可以選擇退出或繼續執行 Python (Python 會處理空列表)
    # exit 0
fi
log_message "Phase 1: File list generated: $TEMP_FILE_LIST"
# --- find 命令結束 ---


# --- 步驟 2: 使用 conda run 執行 Python 腳本 ---
log_message "Executing Python script with environment: $CONDA_ENV_NAME"
log_message "Input file list: $TEMP_FILE_LIST"
log_message "Output database: $DB_FILE_PATH"

# 準備 Python 命令參數
# !! 新增 --input-list 參數 !!
PYTHON_ARGS="\"$PYTHON_SCRIPT_PATH\" --input-list \"$TEMP_FILE_LIST\" -o \"$DB_FILE_PATH\"" # <--- 修改點
# 添加可選參數
if [ ! -z "$WORKER_COUNT" ]; then
  PYTHON_ARGS="$PYTHON_ARGS -w $WORKER_COUNT"
fi
if [ ! -z "$BATCH_SIZE" ]; then
  PYTHON_ARGS="$PYTHON_ARGS -b $BATCH_SIZE"
fi

# 使用 conda run 執行命令
CONDA_RUN_CMD="conda run -n \"$CONDA_ENV_NAME\" python $PYTHON_ARGS"
log_message "Executing: $CONDA_RUN_CMD"

# eval 確保帶有引號的參數被正確處理
eval $CONDA_RUN_CMD
SCRIPT_EXIT_CODE=$?
# --- conda run 結束 ---


if [ ${SCRIPT_EXIT_CODE} -eq 0 ]; then
  log_message "Python script finished successfully."
  # --- 步驟 3 (可選): 清理臨時檔案 ---
  log_message "Cleaning up temporary file list: $TEMP_FILE_LIST"
  rm -f "$TEMP_FILE_LIST"
  # --- 清理結束 ---
else
  log_message "Error: Python script exited with status code ${SCRIPT_EXIT_CODE}."
  log_message "Temporary file list $TEMP_FILE_LIST was kept for inspection."
fi

log_message "Script finished."
exit ${SCRIPT_EXIT_CODE}