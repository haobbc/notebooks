# Git 備份到 GitHub 與 MD 筆記管理

## 概述
此筆記記錄如何使用 Git 將本地的 Markdown (MD) 筆記備份到 GitHub，實現版本控制與遠端儲存，並確保筆記在多設備間同步與安全管理。

## 目的
- 透過 Git 追蹤 MD 筆記的修改歷史。
- 將 Obsidian 筆記備份至 GitHub，防止資料遺失。
- 支援多人協作或跨設備存取。

## 前置條件
1. **Git 已安裝**：確認本地已安裝 Git（運行 `git --version` 檢查）。
2. **GitHub 帳戶與儲存庫**：
   - 在 GitHub 上建立一個儲存庫（例如 `research-notes`）。
   - 可選擇公開或私有儲存庫。
3. **Obsidian 資料夾**：已有一個包含 MD 筆記的本地資料夾（例如 `obsidian-vault`）。

## 操作步驟

### 1. 初始化 Git 儲存庫
在本地 Obsidian 資料夾中初始化 Git：
```bash
cd /path/to/obsidian-vault
git init
```

### 2. 添加筆記檔案
將所有 MD 檔案加入 Git 追蹤：
```bash
git add *.md
```
- 如果資料夾中有子資料夾，使用 `git add .` 添加所有檔案。
- 注意：避免添加大型二進位檔案（如 PDF），建議使用 `.gitignore` 排除。

### 3. 提交變更
提交當前檔案至本地儲存庫：
```bash
git commit -m "初次提交：備份 MD 筆記"
```

### 4. 連結到 GitHub 遠端儲存庫
將本地儲存庫連結至 GitHub：
```bash
git remote add origin https://github.com/你的用戶名/你的儲存庫.git
```
- 替換 URL 為您實際的 GitHub 儲存庫地址。

### 5. 推送至 GitHub
將本地內容推送至 GitHub：
```bash
git push -u origin main
```
- 如果使用 `master` 作為主分支，替換 `main` 為 `master`。
- 首次推送可能需要 GitHub 身份驗證（例如個人存取令牌 PAT）。

### 6. 更新與同步
每次修改 MD 筆記後，重複以下步驟：
```bash
git add .
git commit -m "更新：新增或修改筆記"
git push
```

## MD 筆記管理建議
1. **檔案命名**：
   - 使用有意義的名稱，例如 `2025-03-11_Pyzotero.md`。
   - 避免特殊字符，以免跨平台問題。
2. **資料夾結構**：
   - 建議分隔筆記類型，例如：
     - `docs/`：文獻筆記
     - `project/`：專案相關筆記
     - `personal/`：個人想法
3. **連結筆記**：
   - 使用相對路徑連結其他 MD 檔案，例如 `[Pyzotero筆記](../project/Pyzotero.md)`。
   - 在 Obsidian 中可直接使用 `[[Pyzotero]]`（需確認檔案名稱一致）。

## 注意事項
1. **忽略大型檔案**：
   - 建立 `.gitignore` 檔案，避免推送 PDF 或其他非必要檔案：
     ```
     *.pdf
     *.zip
     /temp/
     ```
2. **衝突處理**：
   - 若多人協作或多設備使用，推送前先拉取更新：
     ```bash
     git pull origin main
     ```
   - 解決衝突後再推送。
3. **儲存庫大小**：
   - GitHub 對免費帳戶有檔案大小限制（單檔不超過 100MB），保持 MD 筆記輕量化。

## 常用 Git 指令
- 查看狀態：`git status`
- 查看歷史：`git log`
- 還原修改：`git restore <檔案名稱>`
- 分支管理：`git branch` / `git checkout -b <分支名稱>`

## 進階應用
- **自動化推送**：
  - 撰寫簡單腳本（例如 Bash 或 Python），定時執行 `git add/commit/push`。
- **GitHub Actions**：
  - 設定工作流，自動檢查 MD 語法或生成索引。

## 參考資源
- [Git 官方文件](https://git-scm.com/doc)
- [GitHub 快速入門](https://docs.github.com/en/get-started)

---
*最後更新日期：2025年3月11日*
