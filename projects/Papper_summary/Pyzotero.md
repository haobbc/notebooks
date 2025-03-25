# 使用 Pyzotero 從 PDF 提取元數據

## 概述
Pyzotero 是一個 Python 套件，用於與 Zotero API 互動。此筆記記錄如何利用 Pyzotero 從 PDF 檔案中提取元數據（例如標題、作者、出版年份等），並將其整理為結構化格式（例如 YML），以便後續整合至 Obsidian 或其他工具。

## 注意事項
1. **API 金鑰**：
   - `local = true` 則不用
2. **PDF 品質**：
   - PDF 必須包含可識別的元數據（例如 DOI 或標題），否則提取可能失敗。
   - 掃描版 PDF（純圖片）無法直接提取，需 OCR 處理。
3. **網路連線**：
   - Pyzotero 依賴 Zotero API，要開啟本地端API，並且開啟程式。
4. **檔案路徑**：
   - 提供正確的 PDF 檔案路徑，否則程式會報錯。
5. **依賴套件**：
   - 安裝 `pyzotero` 和相關工具（如 `requests`），建議使用虛擬環境。

## 安裝與設定
### 安裝 Pyzotero
```bash
pip install pyzotero
```

### 基本配置
- 取得 Zotero 用戶 ID：在 Zotero 設定頁面查看。
- 生成 API 金鑰：前往 [Zotero API 設定](https://www.zotero.org/settings/keys)。

## 常用語法與代碼範例

### 1. 初始化 Pyzotero
```python
from pyzotero import zotero

# 替換為你的實際資訊
library_id = '你的用戶ID'  # e.g., 1234567 ，本地端設定為0
api_key = '你的API金鑰'    # e.g., abcdefghijklmnopqrstuvwx，1本地端不用
library_type = 'user'      # 或 'group' 如果是群組庫

# 初始化 Zotero 物件
zot = zotero.Zotero(library_id='000000', library_type = 'user', local=True) # local=True for read access to local Zotero
```

### 2. 搜尋 PDF 同名文件
```python
# 搜尋所有附件
attachments = zot.items(itemType='attachment', linkMode='linked_file', limit="none") #預設上限可能只有20

for attachment in attachments:
    attachment_data = attachment['data']
    if attachment_data.get('title') == target_filename:
        parent_key = attachment_data.get('parentItem')
        if parent_key:
            parent_item = zot.item(parent_key)
            parent_data = parent_item['data']
                
            # 提取所需資訊
            title = parent_data.get('title', 'No Title')
            # 處理作者（假設有多位作者，取第一位）
            author = parent_data.get('creators', [])
            author_names = [f"{a['firstName']} {a['lastName']}" for a in author]
            journal = parent_data.get('publicationTitle', 'No Journal')
            date = parent_data.get('date', 'No Date')
                
            print(f"找到匹配的附件 '{target_filename}'，父項目資料：{parent_key}")
            
            # 生成 YAML 前置元數據
            yaml_header = f"""---
title: "{title}"
author: "{author_names}"
journal: "{journal}"
publish_date: "{str(date)}"
---
"""
```

### 3. 檢查'data'項目
```python
items = zot.all_top(level=1, limit=1000)

item = items[0]
item_data = item['data']
print(item_data)
```

## 常見問題與解決方案
1. **錯誤：無法連接到 Zotero API**
   - 檢查 `library_id` 和 `api_key` 是否正確。
   - 確認網路連線是否正常。
2. **元數據提取失敗**
   - 確保 PDF 已成功上傳並被 Zotero 識別。
   - 嘗試手動在 Zotero 中「Retrieve Metadata for PDF」。
3. **中文字符亂碼**
   - 在寫入檔案時使用 `encoding='utf-8'`。
   - 確認 YAML 輸出時設定 `allow_unicode=True`。

## 進階應用
- **批量處理**：遍歷資料夾中的多個 PDF，上傳並提取元數據。
```python
import os

pdf_folder = '/path/to/pdf/folder'
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        item = zot.attachment_simple([pdf_path])
        # 後續處理...
```
- **整合雲端**：將 YML 檔案同步至 OneDrive 或 Google Drive。

## 參考資源
- [Pyzotero 官方文件](https://pyzotero.readthedocs.io/)
- [Zotero API 文件](https://www.zotero.org/support/dev/web_api/v3/start)

---
*最後更新日期：2025年3月11日*
