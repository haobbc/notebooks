#!/bin/bash

# --- 配置 ---
CONDA_ENV_NAME="haobbc"
PYTHON_SCRIPT_PATH="/home/user/scrips/dicom_metadata.py"
TARGET_DICOM_DIR="/DICOM/xxxx"
DB_FILE_PATH="/home/user/dicom_metadata.db"
LOG_FILE="dicom_metadata_run.log"
# WORKER_COUNT=8 # 可選

# --- 功能函數 ---
log_message() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# --- 主腳本邏輯 ---
log_message "Script started (using multi-threaded Python script)."

# ... (檢查目錄和腳本存在的邏輯) ...
if [ ! -d "$TARGET_DICOM_DIR" ]; then # ... 省略檢查 ...
  exit 1
fi
if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then # ... 省略檢查 ...
  exit 1
fi

# --- 使用 conda run ---
log_message "Executing Python script within Conda environment: $CONDA_ENV_NAME"
log_message "Target directory: $TARGET_DICOM_DIR"
log_message "Output database: $DB_FILE_PATH"

# 準備 Python 命令參數
PYTHON_ARGS="\"$PYTHON_SCRIPT_PATH\" \"$TARGET_DICOM_DIR\" -o \"$DB_FILE_PATH\""
if [ ! -z "$WORKER_COUNT" ]; then
  log_message "Setting worker count to: $WORKER_COUNT"
  PYTHON_ARGS="$PYTHON_ARGS -w $WORKER_COUNT"
fi

# 使用 conda run 執行命令
CONDA_RUN_CMD="conda run -n \"$CONDA_ENV_NAME\" python $PYTHON_ARGS"
log_message "Executing: $CONDA_RUN_CMD"

# eval 確保帶有引號的參數被正確處理
eval $CONDA_RUN_CMD
SCRIPT_EXIT_CODE=$?
# --- conda run 結束 ---


if [ ${SCRIPT_EXIT_CODE} -eq 0 ]; then
  log_message "Python script finished successfully via conda run."
else
  log_message "Error: Python script executed via conda run exited with status code ${SCRIPT_EXIT_CODE}."
fi

log_message "Script finished."
exit ${SCRIPT_EXIT_CODE}
