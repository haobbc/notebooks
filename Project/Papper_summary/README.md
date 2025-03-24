# 專案名稱：研究筆記與文獻管理流程

## 專案概述
此專案旨在建立一個高效的研究筆記與文獻管理流程，結合 Obsidian、GitHub、Zotero 與自動化工具，實現文獻搜尋、備份與筆記生成的最佳化工作流。

## 思考流程

### 1. 開啟 Obsidian 資料夾
- 在本地端建立一個專屬的 Obsidian 資料夾，用於存放 Markdown 格式的筆記。
- 設定資料夾結構以便後續管理，例如分隔文獻筆記與個人想法。

### 2. [Git 備份到 GitHub](./Project/git.md)
- 初始化 Git 儲存庫，將 Obsidian 資料夾中的筆記同步至 GitHub。
- 確保版本控制，方便追蹤筆記修改並實現遠端備份。

### 3. PubMed 搜尋文章，導入 Zotero
- 在 PubMed 上搜尋相關研究文章。
- 將搜尋結果（包含元數據）匯入 Zotero 文獻管理軟體。

### 4. 全文搜尋或自動導入 PDF
- 使用 Zotero 搜尋文章全文，或手動上傳 PDF。
- 透過 **Zotmoov** 外掛將 PDF 連結至指定雲端資料夾（例如 OneDrive 或 Google Drive）。
  - 優勢：節省 Zotero 本地儲存空間，並避免將大型 PDF 檔案上傳至 GitHub。

### 5. 使用自動化程式生成 YML 及快速個人筆記
#### 5-1. [使用 Pyzotero 利用 PDF 找到元數據](./Project/Pyzotero.md)
- 透過 Pyzotero 套件，從 PDF 檔案中提取元數據（例如標題、作者、出版年份等）。
- 將元數據轉換為 YML 格式，儲存於 Obsidian 資料夾中。

#### 5-2. [使用 LLM 生成快速筆記](./Project/LLM.md)
- 利用 LLM（大型語言模型），根據 PDF 全文生成簡要筆記。
- 要求：需提供文章全文作為輸入。

#### 5-3. [使用CitationKey版本](./Project/PDF2MD.md)
 - 使用Better BibTex pluging 生成的citationKey
 - 克服標題多樣性造成檔名不一致的問題
 - 未來快速整合Pandoc套用引用格式

### 6. 在 Obsidian 閱讀 MD 筆記
- 開啟 Obsidian，閱讀生成的 Markdown 筆記。
- 快速標記關鍵字、整理文章重點，建立個人知識網絡。

## 下一步計畫
- 優化自動化腳本，提升元數據提取與筆記生成的準確性。
- 整合更多雲端服務，增強備份彈性。
- 測試不同 LLM 模型，找出最適合學術筆記生成的方案。

## 工具與技術
- **Obsidian**: 筆記撰寫與知識管理
- **Git/GitHub**: 版本控制與遠端備份
- **Zotero**: 文獻管理
- **Zotmoov**: PDF 檔案連結與雲端同步
- **Pyzotero**: 元數據提取
- **LLM**: 自動化筆記生成
- **雲端服務**: OneDrive/Google Drive

## 注意事項
- 確保雲端資料夾與 GitHub 儲存庫的同步設定，避免檔案衝突。
- LLM 生成筆記時，需校對內容以確保準確性。

---
*最後更新日期：2025年3月11日*

