
### 1. 常用影像分析與機器學習庫

#### **影像分析相關**
- **OpenCV (`opencv-python`)**: 影像處理基礎庫，支援圖像讀取、轉換、濾波等。
- **Pillow (`pillow`)**: 簡單的圖像處理庫，適合讀寫圖像檔案。
- **scikit-image**: 高級影像處理，包含分割、特徵提取等功能。
- **imageio**: 圖像檔案的讀寫，支援多種格式。
- **matplotlib**: 視覺化工具，用於顯示圖像或分析結果。

#### **機器學習相關**
- **NumPy**: 數值計算基礎庫，幾乎所有機器學習庫的依賴。
- **Pandas**: 數據處理與分析，適合處理結構化數據。
- **scikit-learn**: 傳統機器學習演算法（分類、回歸、聚類等）。
- **TensorFlow** 或 **PyTorch**: 深度學習框架（根據需求選擇其一或兩者）。
- **Keras**: 高層次深度學習 API（若使用 TensorFlow，可內含）。
- **SciPy**: 科學計算，支援優化、線性代數等。

#### **其他實用工具**
- **JupyterLab**: 互動式開發環境，用於測試和展示程式碼。
- **tqdm**: 進度條工具，方便監控訓練或處理進度。
- **h5py**: 處理 HDF5 格式數據，常見於模型儲存。

---

### 2. 在有網路的機器上準備環境並打包

#### **步驟 1: 安裝 Miniconda（若尚未安裝）**
![[Miniconda3#**Linux/macOS**]]

#### **步驟 2: 創建並配置環境**
1. **創建新環境**  
   ```bash
   conda create -n ml_env python=3.11
   conda activate ml_env
   ```

2. **安裝常用庫**  
   使用 `conda` 和 `pip` 安裝（部分套件在 `conda-forge` 更穩定）：
   ```bash
   # 基礎工具
   conda install -c conda-forge numpy pandas scipy matplotlib jupyterlab tqdm h5py

   # 影像分析
   conda install -c conda-forge opencv scikit-image pillow imageio

   # 機器學習
   conda install -c conda-forge scikit-learn

   # 深度學習（選擇 TensorFlow 或 PyTorch，或兩者）
   conda install -c conda-forge tensorflow  # TensorFlow
   conda install -c conda-forge pytorch torchvision  # PyTorch
   ```

   - **注意**：
     - TensorFlow 和 PyTorch 可能需要 GPU 版本，若離線機器有 GPU，需確保版本與硬體相容（例如 `tensorflow-gpu`）。
     - 如果 `conda` 安裝過慢，可用 `pip` 補充：
       ```bash
       pip install opencv-python pillow scikit-image
       ```

#### **步驟 3: 使用 `conda-pack` 打包**
1. **安裝 `conda-pack`**  
   ```bash
   conda install -c conda-forge conda-pack
   ```

2. **打包環境**  
   ```bash
   conda pack -n ml_env -o ml_env.tar.gz
   ```
   - 這會生成一個 `ml_env.tar.gz` 檔案，包含所有套件和依賴。

3. **（可選）下載 Miniconda 安裝檔案**  
- ![[Miniconda3#**下載 Miniconda 安裝檔案**]]

---

### 3. 傳輸到離線機器並部署

#### **步驟 1: 傳輸檔案**
- 將以下檔案複製到離線機器（例如透過 USB）：
  - `ml_env.tar.gz`
  - （若需要）`Miniconda3-latest-Linux-x86_64.sh`

#### **步驟 2: 安裝 Miniconda（若未安裝）**
- 參考前述離線安裝步驟：
[[Miniconda3#**Linux/macOS**]]

#### **步驟 3: 解壓並啟動環境**
1. **解壓環境**  
   ```bash
   mkdir -p /path/to/ml_env
   tar -xzf ml_env.tar.gz -C /path/to/ml_env
   ```

2. **啟動環境**  
   ```bash
   source /path/to/ml_env/bin/activate
   ```

3. **測試運行**  
   ```bash
   jupyter lab --no-browser --port=8888
   ```
   - 如果是遠端伺服器，搭配 SSH 隧道：
     ```bash
     ssh -L 8888:localhost:8888 user@remote_server
     ```

---

### 4. 注意事項

#### **套件版本衝突**
- 在安裝時可能遇到依賴衝突（例如 TensorFlow 和 PyTorch 的 CUDA 版本要求）。建議先測試完整環境，確保所有庫相容。
- 示例解決衝突：
  ```bash
  conda install tensorflow=2.10 pytorch=1.12 -c conda-forge
  ```

#### **硬體相容性**
- 如果離線機器有 GPU，確保打包的 TensorFlow/PyTorch 支援 GPU（需要 CUDA 和 cuDNN）。在有網路的機器上測試 GPU 可用性：
  ```python
  import tensorflow as tf
  print(tf.config.list_physical_devices('GPU'))
  import torch
  print(torch.cuda.is_available())
  ```

#### **檔案大小**
- 包含深度學習庫的環境可能很大（數 GB），確保儲存設備和目標機器有足夠空間。

#### **離線模型**
- 如果需要預訓練模型（例如 PyTorch 的 `torchvision.models`），提前下載並打包到環境中：
  ```python
  import torchvision.models as models
  model = models.resnet50(pretrained=True)  # 會下載到本地快取
  ```
  快取路徑（Linux）：`~/.cache/torch/hub/`，將其一併複製。

---

`conda-pack` 打包後的環境並**不會自動加入 `conda env list`**，因為它只是打包一份可攜的資料夾，而非註冊到 conda 的環境管理中。

---

### 5. 出現在 `conda env list` 中方法：

#### **手動複製到 conda 的 envs 資料夾**

```bash
# 假設你解壓後的環境在 /home/user/jlab_env
mv /home/user/jlab_env ~/miniconda3/envs/
```

然後就會自動出現在：

```bash
conda env list
```

接著即可：

```bash
conda activate jlab_env
```

