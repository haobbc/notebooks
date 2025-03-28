
### 背景知識
1. **JupyterLab 的運作機制**：
   - JupyterLab 是一個前端界面，負責顯示和編輯 Notebook，但實際執行程式碼的是後端的 **kernel**。
   - Kernel 是獨立的執行環境，負責運行 Python（或其他語言）程式碼。JupyterLab 透過 `jupyter_server` 與 kernel 通信。

2. **Kernel 的來源**：
   - 默认情况下，安装 JupyterLab 時會附帶一個預設的 Python kernel（通常是安裝 JupyterLab 的環境）。
   - 你可以添加其他 kernel，例如來自不同 Conda 環境、虛擬環境，甚至其他 Python 安裝。

3. **乾淨環境假設**：
   - 你提到「乾淨 Python 3.12.9 環境」，假設只有 Python 3.12.9 和 JupyterLab，沒有其他套件（如 `numpy`、`pandas`）。

---

### 問題解答

#### **Q1: 純安裝 JupyterLab 後，使用其他 kernel 時需要額外安裝套件嗎？**
- **不需要在 JupyterLab 環境中額外安裝套件**，但 **取決於你使用的 kernel 是否已經包含所需套件**。
- 詳細說明：
  - JupyterLab 本身只負責界面和 kernel 管理，不執行程式碼，因此它不需要知道你的程式碼依賴哪些套件。
  - 當你切換到其他 kernel（例如另一個 Conda 環境的 Python kernel），程式碼會在該 kernel 的環境中運行，使用的套件來自該 kernel 的環境，而不是 JupyterLab 的環境。
  - 如果該 kernel 的環境缺少運行程式碼所需的套件（例如 `numpy`），你需要在該 kernel 的環境中安裝這些套件，而不是在 JupyterLab 的環境中。

#### **Q2: JupyterLab 是使用 kernel 來跑 Python 嗎？**
- **是的**，JupyterLab 完全依賴 kernel 來運行 Python 程式碼。
- 流程：
  1. 你在 JupyterLab 的 Notebook 中輸入程式碼。
  2. JupyterLab 將程式碼發送到當前選定的 kernel。
  3. Kernel 執行程式碼並將結果返回給 JupyterLab 顯示。
- 因此，JupyterLab 本身不包含 Python 執行環境，所有執行邏輯都由 kernel 提供。

---

### 額外注意
- **Python 3.12 的相容性**：
  - 如前所述，Python 3.12 是較新版本，某些套件（例如舊版 `jupyter_server`）可能有相容性問題。如果遇到錯誤（如 `pysqlite2`），考慮降級到 Python 3.11。
- **Kernel 清單管理**：
  - 查看已註冊的 kernel：
    ```bash
    jupyter kernelspec list
    ```
  - 移除不需要的 kernel：
    ```bash
    jupyter kernelspec remove ml_env
    ```


---

### 在 JupyterLab 中使用其他環境

- 你已經安裝了 JupyterLab（例如在一個名為 `jupyter_env` 的 Conda 環境中）。
- 你有其他環境（例如 `data_env`、`ml_env`），這些環境包含你想使用的套件或特定 Python 版本。

---

### 步驟：將其他環境加入 JupyterLab

#### **步驟 1: 在目標環境中安裝 `ipykernel`**
- 每個你想用作 kernel 的環境都需要安裝 `ipykernel`，這樣它才能與 JupyterLab 通信。

1. 啟動目標環境：
   ```bash
   conda activate data_env
   ```

2. 安裝 `ipykernel`：
   ```bash
   conda install -c conda-forge ipykernel
   ```

#### **步驟 2: 註冊環境作為 kernel**
- 使用 `ipykernel` 將該環境註冊到 Jupyter 的 kernel 清單中。

1. 在目標環境中運行以下命令：
   ```bash
   python -m ipykernel install --user --name data_env --display-name "Data Env (Python 3.11)"
   ```
   - `--user`：將 kernel 安裝到使用者層級（`~/.local/share/jupyter/kernels/`）。
   - `--name data_env`：kernel 的內部名稱（建議與環境名稱一致）。
   - `--display-name "Data Env (Python 3.11)"`：JupyterLab 中顯示的名稱（可自訂）。

2. 重複此步驟，為每個想使用的環境註冊 kernel。例如：
   ```bash
   conda activate ml_env
   conda install -c conda-forge ipykernel
   python -m ipykernel install --user --name ml_env --display-name "ML Env (Python 3.10)"
   ```

#### **步驟 3: 啟動 JupyterLab**
- 返回安裝 JupyterLab 的環境（例如 `jupyter_env`）：
  ```bash
  conda activate jupyter_env
  jupyter lab
  ```

#### **步驟 4: 在 JupyterLab 中選擇其他環境**
1. **新建 Notebook**：
   - 在 JupyterLab 界面中，點擊左上角的「+」按鈕，選擇「Notebook」。

2. **選擇 Kernel**：
   - 彈出窗口會顯示可用的 kernel 清單。
   - 選擇你剛註冊的 kernel，例如 "Data Env (Python 3.11)" 或 "ML Env (Python 3.10)"。
   - 點擊「Select」。

3. **切換現有 Notebook 的 Kernel**：
   - 如果已經打開一個 Notebook：
     - 點擊頂部菜單的「Kernel」 > 「Change Kernel」。
     - 從下拉清單中選擇目標 kernel（例如 "Data Env (Python 3.11)"）。
     - 確認後，Notebook 會重新連接到新 kernel。

4. **驗證**：
   - 在 Notebook 中運行：
     ```python
     import sys
     print(sys.executable)  # 顯示當前 kernel 的 Python 路徑
     import numpy  # 測試套件是否可用
     ```
   - 如果路徑指向 `data_env`（例如 `/home/user/miniconda3/envs/data_env/bin/python`），且套件正常導入，說明成功使用該環境。

---

### 管理 Kernel

#### **查看已註冊的 Kernel**
```bash
jupyter kernelspec list
```
- 輸出示例：
  ```
  Available kernels:
    data_env    /home/user/.local/share/jupyter/kernels/data_env
    ml_env      /home/user/.local/share/jupyter/kernels/ml_env
    python3     /home/user/miniconda3/envs/jupyter_env/share/jupyter/kernels/python3
  ```

#### **移除不需要的 Kernel**
- 如果不再需要某個 kernel：
  ```bash
  jupyter kernelspec remove data_env
  ```

---

### 注意事項

1. **JupyterLab 環境無需包含所有套件**：
   - 如前所述，JupyterLab 的環境（例如 `jupyter_env`）只需安裝 `jupyterlab`，無需安裝其他 kernel 環境中的套件（例如 `numpy`、`tensorflow`）。

2. **Kernel 環境必須獨立完整**：
   - 每個 kernel 環境（例如 `data_env`）需要包含運行程式碼所需的套件。如果缺少，會報錯（如 `ModuleNotFoundError`）。

3. **跨系統移植**：
   - 如果你在 WSL 或其他系統打包環境並移植到新機器，kernel 的註冊資訊不會隨 `conda-pack` 一起移動，需在新機器上重新運行 `python -m ipykernel install`。

4. **多版本 Python**：
   - 你可以用不同 Python 版本的環境作為 kernel（例如 Python 3.11、3.12），只要它們都安裝了 `ipykernel`。

---

### 完整範例
假設你有以下環境：
- `jupyter_env`：Python 3.12，只安裝 JupyterLab。
- `data_env`：Python 3.11，包含 `numpy` 和 `pandas`。

#### 配置流程：
```bash
# 配置 JupyterLab 環境
conda create -n jupyter_env python=3.12
conda activate jupyter_env
conda install -c conda-forge jupyterlab

# 配置數據分析環境
conda create -n data_env python=3.11
conda activate data_env
conda install -c conda-forge numpy pandas ipykernel
python -m ipykernel install --user --name data_env --display-name "Data Env (Python 3.11)"

# 啟動 JupyterLab
conda activate jupyter_env
jupyter lab
```

#### 在 JupyterLab 中：
- 新建 Notebook，選擇 "Data Env (Python 3.11)"。
- 運行：
  ```python
  import numpy as np
  print(np.__version__)
  ```
- 成功輸出版本號，證明使用的是 `data_env` 的 kernel。

