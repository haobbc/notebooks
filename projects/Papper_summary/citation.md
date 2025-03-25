# 在 Obsidian 中撰寫論文並插入參考文獻的方案

## 概述
此筆記提供一個在 Obsidian 中撰寫論文時插入參考文獻的流程，利用已整理的筆記（如元數據或快速筆記），並在完稿時轉換為 BibTeX 格式以符合學術引用標準。目標是保持撰寫過程順暢，最後輸出正統引用。

## 需求
- **Obsidian 筆記**：包含文獻元數據（如 YML 格式）或快速筆記（如 LLM 生成）。
- **工具**：
  - Obsidian（撰寫與管理筆記）。
  - Zotero（匯出 BibTeX）。
  - Pandoc（轉換 Markdown 為論文格式，例如 LaTeX 或 Word）。
- **最終輸出**：帶有 BibTeX 引用的論文文件。

## 方案流程

### 1. 在 Obsidian 中準備文獻筆記
- **來源**：
  - 使用 [Pyzotero 筆記](../project/Pyzotero.md) 提取的元數據（儲存為 YML）。
  - 使用 [LLM 快速筆記](./LLM_Notes.md) 生成的摘要或關鍵點。
- **格式建議**：
  - 每篇文獻一個 MD 檔案，例如 `Smith_2020.md`。
  - 文件開頭包含 YML 前置元數據：
    ```yaml
    ---
    title: "Sample Article Title"
    authors: ["Smith, John", "Doe, Jane"]
    year: 2020
    doi: "10.1000/xyz123"
    ---
    ```
  - 正文可加入 LLM 生成的筆記或個人註解。

### 2. 撰寫論文時插入臨時引用
- **方法**：
  - 在 Obsidian 中撰寫論文（例如 `Thesis.md`），使用簡單標記插入引用。
  - 引用格式：`[@檔案名]`，例如 `[@Smith_2020]`。
  - 範例：
    ```markdown
    研究顯示某些現象 [@Smith_2020]。此外，其他研究也支持這一點 [@Jones_2019]。
    ```
- **優點**：
  - 直接連結至文獻筆記（Obsidian 支援 `[[Smith_2020]]` 跳轉）。
  - 避免繁瑣的 BibTeX 鍵管理，保持撰寫流暢。

### 3. 建立參考文獻索引
- **手動索引**：
  - 在 `Thesis.md` 末尾添加參考文獻區塊，列出所有引用的筆記：
    ```markdown
    ## 參考文獻
    - [[Smith_2020]]
    - [[Jones_2019]]
    ```
  - 可使用 Obsidian 的嵌入功能顯示筆記內容：
    ```markdown
    ![[Smith_2020]]
    ```
- **自動化輔助**：
  - 使用插件（如 `Obsidian Citation Plugin`）掃描文中引用，生成索引。

### 4. 完稿時轉換為 BibTeX 格式
- **步驟**：
  1. **匯出 BibTeX**：
     - 將引用的文獻從 Zotero 匯出為 `.bib` 檔案（包含所有元數據）。
     - 範例 BibTeX 條目：
       ```bibtex
       @article{smith2020,
         title = {Sample Article Title},
         author = {Smith, John and Doe, Jane},
         year = {2020},
         doi = {10.1000/xyz123}
       }
       ```
  2. **映射引用鍵**：
     - 將文中 `[@Smith_2020]` 替換為 BibTeX 鍵（例如 `[@smith2020]`）。
     - 可手動編輯，或使用腳本自動替換（見下方範例）。
  3. **轉換文件**：
     - 使用 Pandoc 將 Markdown 轉為 LaTeX 或 Word，並套用 BibTeX：
       ```bash
       pandoc Thesis.md -o Thesis.tex --bibliography=references.bib --citeproc
       ```
     - 或生成 Word 文件：
       ```bash
       pandoc Thesis.md -o Thesis.docx --bibliography=references.bib --citeproc
       ```

### 5. 驗證與調整
- 檢查生成的論文文件，確保引用格式符合目標期刊或學校要求（例如 APA、MLA）。
- 若需調整 BibTeX 樣式，修改 `.csl` 文件並重新運行 Pandoc。

## 實現代碼範例
- **替換引用鍵的 Python 腳本**：
  ```python
  import re

  # 讀取 Thesis.md
  with open("Thesis.md", "r", encoding="utf-8") as f:
      content = f.read()

  # 映射表：Obsidian 文件名 -> BibTeX 鍵
  mapping = {
      "Smith_2020": "smith2020",
      "Jones_2019": "jones2019"
  }

  # 替換 [@Smith_2020] 為 [@smith2020]
  for obsidian_key, bib_key in mapping.items():
      content = content.replace(f"[@{obsidian_key}]", f"[@{bib_key}]")

  # 儲存更新後的文件
  with open("Thesis_updated.md", "w", encoding="utf-8") as f:
      f.write(content)
  ```

## 注意事項
1. **一致性**：
   - 確保 Obsidian 文件名與 Zotero 中的文獻條目一致，便於映射。
2. **插件支援**：
   - 安裝 `Obsidian Citation Plugin` 或 `Zotero Integration`，可直接從 Zotero 插入引用。
3. **版本控制**：
   - 參考 [Git 備份筆記](./GitBackup.md)，定期提交論文與筆記至 GitHub。
4. **Pandoc 配置**：
   - 確認 Pandoc 已安裝，並測試 BibTeX 與 CSL 檔案是否正確。

## 優點與限制
- **優點**：
  - 撰寫階段專注內容，無需管理複雜引用。
  - 利用 Obsidian 的連結功能，提升筆記與論文的互動性。
  - 最終輸出符合學術標準。
- **限制**：
  - 需手動或腳本映射引用鍵，初期設定稍繁瑣。
  - 長篇論文可能需分段管理引用。

## 下一步
- 測試 `Obsidian Citation Plugin` 與 Zotero 的整合，減少手動步驟。
- 開發自動化工具，從 YML 元數據生成 BibTeX 條目。

---
*最後更新日期：2025年3月11日*
