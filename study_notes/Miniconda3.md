
### **1.下載 Miniconda 安裝檔案**
1. 前往 Miniconda 官方下載頁面：[https://www.anaconda.com/docs/getting-started/miniconda/install](https://www.anaconda.com/docs/getting-started/miniconda/install)。
2. 根據目標系統選擇合適的版本：
   - **Linux**: 例如 `Miniconda3-latest-Linux-x86_64.sh`
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
   - **macOS**: 例如 `Miniconda3-latest-MacOSX-x86_64.sh`
   - **Windows**: 例如 `Miniconda3-latest-Windows-x86_64.exe`
3. 下載檔案並儲存到可移動儲存設備（如 USB 隨身碟）或本地硬碟。

---

### 2. 將檔案傳輸到離線機器
- 使用 USB 隨身碟、硬碟或其他方式將以下檔案傳到目標離線機器：
  - Miniconda 安裝檔案（例如 `Miniconda3-latest-Linux-x86_64.sh`）。
  - （可選）套件快取檔案（例如 `jupyterlab-4.0.9-pyhd8ed1ab_0.tar.bz2`）。

---

### 3. 離線安裝 Miniconda

#### **Linux/macOS**
1. **進入檔案所在目錄**  
   假設檔案在 `/path/to/installer/`：
   ```bash
   cd /path/to/installer/
   ```

2. **執行安裝腳本**  
   運行以下命令：
   ```bash
   bash Miniconda3-latest-Linux-x86_64.sh
   ```
   - 如果是 macOS，檔案名可能不同，例如 `bash Miniconda3-latest-MacOSX-x86_64.sh`。
   - 按提示操作：
     - 輸入 `yes` 同意許可協議。
     - 指定安裝路徑（預設是 `~/miniconda3`，可自訂，例如 `/opt/miniconda3`）。
     - 選擇是否初始化 Conda（建議 `yes`，會修改 `~/.bashrc`）。

3. **啟動 Conda**  
   安裝完成後，啟動新的終端機，或手動載入 Conda：
   ```bash
   source ~/miniconda3/bin/activate
   ```
   Or refresh the terminal:
   ```bash
   source ~/.bashrc
   ```
   - 如果自訂了安裝路徑，改為 `source /opt/miniconda3/bin/activate`。
   - 檢查是否成功：
     ```bash
     conda --version
     ```

---

### 4. （可選）離線安裝套件
如果準備了套件檔案，可以在離線環境中安裝：

1. **創建環境並安裝套件**  
   啟動 Conda：
   ```bash
   source ~/miniconda3/bin/activate
   ```
2. 創建新環境：
   ```bash
   conda create -n myenv python=3.11
   conda activate myenv
   ```
   安裝套件（使用本地檔案）：
   ```bash
   conda install --offline /path/to/pkgs/jupyterlab-4.0.9-pyhd8ed1ab_0.tar.bz2
   ```
   - `--offline`：強制使用本地快取，不連線網路。
   - 指定套件檔案的完整路徑。

---

### 5. 注意事項

#### **系統相容性**
- 確保下載的 Miniconda 版本與目標系統匹配（例如，Linux 64-bit 不能用於 Windows）。
- 如果目標機器是舊系統，檢查 `glibc` 版本（Linux），可能需要下載較舊的 Miniconda 版本。

#### **套件依賴**
- 如果套件有未下載的依賴，離線安裝會失敗。建議在有網路的機器上測試完整環境，然後打包所有依賴（或使用 `conda-pack`，如前述問題所述）。

#### **啟動問題**
- 如果 `source activate` 無效，檢查路徑是否正確，或直接運行：
  ```bash
  /path/to/miniconda3/bin/conda init
  ```

---

![[Conda_pack]]

