## 專案名稱
**PDF to Markdown Generator with Dual-Language TL;DR**

## 概述
此專案是一個 Python 工具，用於將 Zotero 中的 PDF 文件轉換為 Markdown 文件，並可選擇使用 xAI 的 Grok 2 模型生成英文和繁體中文的 TL;DR（概要）摘要。程式支援動態路徑（基於 OneDrive 同步）、Zotero 本地 API，並在重複執行時避免不必要的 LLM 調用，以節省 Token 成本。

## 功能
1. **PDF 轉 Markdown**：
   - 從 Zotero PDF 文件生成 Markdown，包含 YAML 元數據、PDF 連結和 Citation。
   - 支援相對路徑映射（例如 `Reference/seizure/pdf1.pdf` -> `recieved_notes/seizure/pdf1.md`）。
2. **雙語 TL;DR**：
   - 使用 Grok 2 生成結構化的英文和繁體中文摘要（`# TL;DR (Summary)` 和 `# 中文摘要 (TL;DR)`）。
   - 每項支援最多 2-3 條簡潔條目。
3. **重複執行邏輯**：
   - **無 MD 檔**：
     - 無 LLM：建立 YAML 和基本內容，添加分隔符 `***`。
     - 有 LLM：在分隔符下添加雙語摘要。
   - **有 MD 檔**：
     - 無 LLM：更新分隔符上方內容，下方不動。
     - 有 LLM：若分隔符下無摘要則生成，否則跳過。
4. **跨裝置支援**：
   - 使用 OneDrive 相對路徑，適配不同電腦。

## 工作流總結
1. **初始化**：
   - 載入 Zotero 附件資料至 DataFrame（透過本地 API）。
   - 讀取 `.bib` 文件建立文獻字典。
2. **PDF 處理**：
   - 遍歷 Zotero PDF 資料夾，獲取每個 PDF 的相對路徑。
   - 根據路徑生成對應的 Markdown 文件。
3. **內容生成**：
   - 從 `.bib` 提取元數據，生成 YAML。
   - 使用 Zotero item key 生成 PDF 連結。
   - 若啟用 LLM，檢查是否需生成摘要（跳過已有 Summary）。
4. **輸出**：
   - 將 Markdown 寫入對應目錄，保留分隔符 `***` 下方的現有內容。

## 快速上手指南
### 安裝依賴
```bash
pip install bibtexparser pyyaml pdfplumber openai pyzotero pandas
```

### 配置
1. **API Key**：
   - 將 `XAI_API_KEY` 設為您的 xAI API Key（程式碼第 19 行）。
2. **路徑檢查**：
   - 確保 OneDrive 已同步，且以下路徑存在：
     - `文件/Reference`（Zotero PDF 資料夾）
     - `文件/論文筆記/recieved_notes`（Markdown 輸出資料夾）
     - `文件/Reference/Zotero_lib.bib`（BibTeX 文件）
3. **Zotero**：
   - 確保 Zotero 7 運行，程式使用本地 API（`ZOTERO_USER_ID = "0"`）。

### 執行程式
- **不使用 LLM（預設）**：
  ```bash
  python pdf_to_md_chinese.py
  ```
- **使用 LLM 生成摘要**：
  ```bash
  python pdf_to_md_chinese.py -l y
  ```

### 範例輸出
假設 PDF 為 `Glioma and Sleep/rangel-castilla2015NormalPerfusionPressure.pdf`：
```markdown
---
title: "Normal Perfusion Pressure Breakthrough Theory: A Reappraisal after 35 Years"
author: "Rangel-Castilla, Leonardo and Spetzler, Robert F. and Nakaji, Peter"
year: "2015"
journal: "Neurosurgical Review"
doi: "10.1007/s10143-014-0600-4"
citekey: "rangel-castilla2015NormalPerfusionPressure"
aliases:
  - "(Rangel-Castilla et al., 2015)"
date_added: "2025-03-23"
---
# Normal Perfusion Pressure Breakthrough Theory: A Reappraisal after 35 Years
- [PDF Link](zotero://open-pdf/library/items/6N2B7D8Q)

Citation: [@rangel-castilla2015NormalPerfusionPressure]
***
# TL;DR (Summary)
- Key findings from 35 years of research.
- Updated theory insights.

# 中文摘要 (TL;DR)
- 35 年研究的關鍵發現。
- 更新理論洞見。
```
檔案位於：`OneDrive/文件/論文筆記/recieved_notes/Glioma and Sleep/rangel-castilla2015NormalPerfusionPressure.md`

## 注意事項
- **Zotero 運行**：程式需 Zotero 啟動以存取本地 API。
- **Token 節省**：重複執行時，若已有 Summary，會跳過 LLM 生成。
- **路徑同步**：確保 OneDrive 在不同電腦上的資料夾結構一致。

## 目前進度
- **功能實現**：
  - 相對路徑映射完成。
  - 雙語 TL;DR（英文+繁體中文）支援多項輸出（每項 2-3 條）。
  - 重複執行邏輯優化，使用 `***` 分隔符避免 YAML 衝突。
- **已解決問題**：
  - 重複執行時標題和連結重複的問題。
  - 語言不一致（現為英文+繁體中文）。
- **待確認**：
  - 使用者滿意度與進一步微調需求。
