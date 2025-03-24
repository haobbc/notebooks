### 關鍵要點
- Marp 支援圖片調整和排版，包括調整大小、背景圖片和定位。
- 幻燈片過場設定可在 HTML 輸出中使用，支援內建和自訂過場效果，但不支援 PDF 或 PPTX。
- 動畫功能有限，主要透過 CSS 實現元素之間的轉換。

---

### 圖片調整和排版
Marp 提供多種方式來調整和排版圖片，讓您的幻燈片更具視覺吸引力。以下是具體方法：

#### 調整圖片大小
您可以使用關鍵字在圖片後指定寬度和高度，例如：
- 調整寬度：`![width:300px](image.jpg)`
- 調整高度：`![height:200px](image.jpg)`
- 同時調整：`![width:300px height:200px](image.jpg)`

#### 背景圖片
將圖片設為幻燈片背景，使用 `![bg](url)` 語法：
- 基本用法：`![bg](https://example.com/background.jpg)`
- 調整大小：`![bg 150%](https://example.com/background.jpg)`
- 應用濾鏡：`![bg blur:3px](https://example.com/background.jpg)`

#### 定位和多圖排版
- 分割背景：使用 `left` 或 `right` 定位，例如 `![bg left](https://example.com/background.jpg)`。
- 多層背景：使用多個 `bg` 關鍵字，例如 `![bg](image1.jpg) ![bg](image2.jpg)`，可使用 `vertical` 設定垂直堆疊。

---

### 動畫和過場設定
Marp 的動畫和過場設定主要適用於 HTML 輸出，需使用支援 View Transition API 的瀏覽器（如 Chrome 111+、Edge 111+、Safari 18.2+）。以下是具體方法：

#### 過場設定
- 使用 `transition` 指令設定過場效果，例如：
  ```
  --- transition: fade ---
  # 帶有淡入淡出效果的幻燈片
  ```
- 內建過場包括 `none`、`clockwise`、`fade` 等，完整列表可參考 Marp 文件。
- 自訂過場：透過 CSS `@keyframes` 定義自訂動畫，需編輯 HTML 輸出。

#### 動畫功能
- 支援元素之間的轉換動畫，使用 `view-transition-name` CSS 屬性實現。
- 例如，在元素上添加 `view-transition-name: my-element`，可在切換幻燈片時實現平滑轉換。
- 動畫效果僅適用於 HTML 輸出，且需相容瀏覽器支援。

---

---

### 調查報告：Marp 的圖片調整、排版與動畫/過場設定詳解

Marp 是一款基於 Markdown 的幻燈片製作工具，允許使用者透過簡單的語法創建專業的演示文稿。以下是對圖片調整和排版，以及動畫和過場設定的詳細分析，特別針對講座或技術分享場景的適用性。

#### 圖片調整和排版的技術細節

Marp 擴展了標準 Markdown 的圖片語法，提供了多種圖片調整和排版選項，適合不同視覺需求。以下是具體實現方式：

1. **圖片大小調整**：
   - Marp 允許在圖片語法中指定寬度和高度，使用關鍵字 `width` 和 `height`。例如：
     - `![width:300px](image.jpg)`：將圖片寬度設為 300 像素。
     - `![height:200px](image.jpg)`：將圖片高度設為 200 像素。
     - `![width:300px height:200px](image.jpg)`：同時設定寬度和高度。
   - 支援單位包括像素（px），但不支援視窗相對單位（如 vw、vh、vmin、vmax），適合固定尺寸的展示。
   - 表 1 列出圖片大小調整的支援情況：

     | 功能                     | 內聯圖片 | 背景圖片 | 進階背景 | 備註                                      |
     |--------------------------|----------|----------|----------|------------------------------------------|
     | 按關鍵字調整大小         | 僅 `auto` | ✔️       | ✔️       | -                                        |
     | 按百分比調整大小         | ❌       | ✔️       | ✔️       | 例如 `![bg 150%](https://example.com/background.jpg)` |
     | 按長度調整大小           | ✔️       | ✔️       | ✔️       | 例如 `![width:200px](image.jpg)`，不支援 vw/vh 等 |

2. **背景圖片與濾鏡**：
   - 背景圖片使用 `![bg](url)` 語法設定，可進一步調整大小和應用 CSS 濾鏡。例如：
     - `![bg 150%](https://example.com/background.jpg)`：放大 150%。
     - `![bg blur:3px](https://example.com/background.jpg)`：應用模糊效果。
   - 支援的濾鏡包括亮度（brightness）、灰度（grayscale）、懷舊（sepia）等，參考 [CSS 濾鏡文件](https://developer.mozilla.org/en-US/docs/Web/CSS/filter)。
   - 內聯圖片也支援濾鏡，例如 `![brightness:.8 sepia:50%](https://example.com/image.jpg)`。

3. **圖片定位與多圖排版**：
   - 分割背景：使用 `left` 或 `right` 關鍵字實現 Deckset 風格的分割背景，例如 `![bg left](https://picsum.photos/720?image=29)`，可指定比例如 `left:33%`。
   - 多層背景：允許多個背景圖片堆疊，預設水平排列，可使用 `vertical` 關鍵字切換為垂直排列。例如：
     - `![bg](image1.jpg) ![bg](image2.jpg)`：水平堆疊。
     - `![bg vertical](image1.jpg) ![bg vertical](image2.jpg)`：垂直堆疊。
   - 這些功能適合創建複雜的視覺效果，例如講座中的多圖比較或背景層次設計。

#### 動畫與過場設定的技術細節

Marp 的動畫和過場設定主要針對 HTML 輸出，基於 View Transition API 實現。以下是具體功能和限制：

1. **過場設定**：
   - Marp CLI 的 `bespoke` 模板支援幻燈片過場動畫，使用 `transition` 本地指令設定。例如：
     - `--- transition: fade ---`：設定淡入淡出過場。
     - `--- transition: fade 1s ---`：設定 1 秒的淡入淡出過場。
   - 內建過場效果包括 33 種，如 `none`、`clockwise`、`counterclockwise`、`cover` 等，完整列表可參考 [Marp CLI 過場展示](https://marp-cli-page-transitions.glitch.me/)。
   - 自訂過場：使用者可透過 CSS `@keyframes` 定義自訂動畫，命名規則為 `marp-transition-XXXXXXXX` 等，並在 Markdown 中引用。
   - 過場持續時間預設為 0.5 秒，可透過指令調整（如 `1s` 或 `1000ms`）。
   - 表 2 列出瀏覽器支援情況：

     | 瀏覽器  | 支援 | 版本範圍       |
     |----------|------|----------------|
     | Chrome   | ✅   | 111 及以上     |
     | Edge     | ✅   | 111 及以上     |
     | Safari   | ✅   | 18.2 及以上    |
     | Firefox  | ❌   | -              |

2. **動畫功能**：
   - 支援元素之間的轉換動畫（morphing animations），使用 `view-transition-name` CSS 屬性標記元素。例如：
     - 在 HTML 中添加 `style="view-transition-name: my-element"`，在切換幻燈片時實現平滑轉換。
   - 這功能適用於 Chrome 和 Edge，Safari 可能因 WebKit 長久存在的 Bug 而效果不穩定，需使用 [marpit-svg-polyfill](https://github.com/marp-team/marpit-svg-polyfill) 修補。
   - 要求每個幻燈片中 `view-transition-name` 名稱唯一，否則轉換動畫可能失效。
   - 動畫僅在 HTML 輸出中有效，PDF 和 PPTX 格式不支援動畫。

3. **限制與注意事項**：
   - 過場和動畫僅適用於 HTML 輸出，需在支援 View Transition API 的瀏覽器中查看（如 Chrome 111+）。
   - 若觀眾啟用「減少動畫」模式（prefers-reduced-motion），過場會自動降級為簡單的 `fade` 效果，參考 [web.dev 文章](https://web.dev/prefers-reduced-motion/)。
   - 使用 CLI 可選擇禁用過場：`--bespoke.transition=false`。

#### 適用場景與建議

- **圖片調整與排版**：適合技術講座或教育簡報，特別是需要展示圖表、圖片比較或背景設計的場景。建議使用相對單位（如百分比）以適應不同螢幕尺寸。
- **動畫與過場**：適合 HTML 格式的線上分享或現場演示，增強視覺效果。但需提前測試瀏覽器兼容性，特別是 Safari 的潛在 Bug。
- **備案方案**：若需離線或跨平台使用，考慮匯出 PDF，接受無動畫的限制。

#### 結論

Marp 提供強大的圖片調整和排版功能，透過關鍵字和 CSS 濾鏡實現靈活的視覺設計。動畫和過場設定主要適用於 HTML 輸出，支援內建和自訂效果，但受限於瀏覽器兼容性和輸出格式。建議根據講座需求選擇適當的輸出格式，並提前測試以確保效果。

---

### 關鍵引用
- [Marp 圖片語法文件](https://marpit.marp.app/image-syntax)
- [Marp CLI 自訂過場文件](https://github.com/marp-team/marp-cli/blob/main/docs/bespoke-transitions/README.md)
- [Marp Blog 自訂過場文章](https://marp.app/blog/how-to-make-custom-transition)
- [CSS 濾鏡文件](https://developer.mozilla.org/en-US/docs/Web/CSS/filter)
- [Marp CLI 過場展示](https://marp-cli-page-transitions.glitch.me/)
- [web.dev 減少動畫文章](https://web.dev/prefers-reduced-motion/)# MARP

Marp 是一款基於 Markdown 的幻燈片製作工具，專為需要快速創建美觀幻燈片的使用者設計。以下是關於其語法、與 Markdown 的整合、相關應用以及範例的全面分析，適合希望深入了解的讀者。

#### Marp 的概述與功能
Marp，全稱為 Markdown Presentation Ecosystem，提供了一個直觀的體驗，讓使用者專注於內容編寫，而非格式設計。它的核心是基於 CommonMark，一個標準化的 Markdown 規範，確保與一般 Markdown 文件的兼容性。研究顯示，Marp 的設計特別適合技術人員、教育工作者和會議演講者，原因在於其簡單性和靈活性。

#### 幻燈片語法與 Markdown 整合
Marp 的語法以 Markdown 為基礎，允許使用者使用標準 Markdown 語法來編寫內容，包括：
- 標題：使用 `#` 表示，例如 `# 標題`。
- 列表：使用 `-` 或 `*` 創建項目列表，例如：
  ```
  - 項目 1
  - 項目 2
  ```
- 代碼塊：使用三個反引號（```）包圍代碼，例如：
  ```
  ```python
  print("Hello, Marp!")
  ```
- 超連結：使用 `[文字](URL)` 格式，例如 `[Marp 官網](https://marp.app/)`。

幻燈片的分隔是 Marp 與標準 Markdown 的主要差異，使用水平分隔線 `---` 來區分每一張幻燈片。例如：
```
# 第一張幻燈片
內容。

---
# 第二張幻燈片
更多內容。
```
此外，Marp 提供了擴展語法，增強幻燈片的功能：
- **主題設定**：透過前置事項（front-matter）設定主題，例如：
  ```
  ---
  theme: default
  ---
  ```
  內建主題包括 `default`、`gaia` 和 `uncover`，每個主題提供不同的視覺風格。
- **背景圖片與顏色**：使用 `bg` 指令設定背景，例如：
  ```
  ![bg](https://example.com/image.jpg)
  ```
  或設定背景顏色，例如 `backgroundColor: #000000`。
- **幻燈片大小**：使用 `size` 指令設定比例，例如：
  ```
  ---
  size: 4:3
  ---
  ```
  支援常見比例如 16:9 和 4:3。
- **數學公式**：支援 Pandoc 風格的數學公式，例如 `$E = mc^2$`。
- **自動縮放**：代碼塊和數學公式會自動調整大小，以適應幻燈片布局。

這些擴展語法與 Markdown 的整合，使得 Marp 成為一個強大的工具，能夠在簡單的文本編輯中實現複雜的視覺效果。

#### 相關應用與工具
Marp 的生態系統提供了多種工具，增強其實用性：
- **VS Code 整合**：Marp 提供了一個 VS Code 擴展套件，允許使用者在編輯 Markdown 文件時即時預覽幻燈片。安裝後，僅需按 `Ctrl+Shift+V`（Windows/Linux）或 `Cmd+Shift+V`（macOS）即可查看效果，特別適合開發者和學生使用。
- **命令列工具（CLI）**：Marp CLI 是一個強大的工具，可將 Markdown 文件轉換為多種格式，包括 HTML、PDF、PPTX 和圖像。使用方法如下：
  - 安裝 Node.js 後，執行 `npm install --save-dev @marp-team/marp-cli`。
  - 轉換文件，例如 `npx @marp-team/marp-cli ./slide.md --html --pdf`。
  - 這適合需要自動化工作流程的使用者，例如與 GitHub Actions 整合，自動生成和部署幻燈片。
- **主題自訂**：使用者可以透過 CSS 創建自訂主題，控制幻燈片的外觀。例如，添加類別後，可在 CSS 中定義：
  ```
  section.title { background-color: red; }
  ```
  這為企業或個人化需求提供了靈活性。

這些工具的整合使得 Marp 成為一個多功能的平台，特別適合技術演講、教育簡報和會議展示。

#### 範例與實際應用
為了幫助理解，下面提供一個詳細的 Marp 幻燈片範例，展示多種語法的使用：
```
---
theme: gaia
size: 16:9
---

# 歡迎使用 Marp
這是第一張幻燈片。

---

# 內容清單
- 介紹
- 功能
- 結論

---

![bg](https://example.com/background.jpg)
# 背景圖片範例
這張幻燈片有背景圖片。

---

# 代碼展示
以下是一個 Python 範例：
```python
def hello():
    print("Hello, Marp!")
hello()
```
```
這個範例展示了：
- 使用 `theme: gaia` 和 `size: 16:9` 設定主題和比例。
- 使用 `---` 分隔幻燈片。
- 包含列表、背景圖片和代碼塊。

實際應用中，Marp 被廣泛用於教育場景，例如教師創建帶有直播代碼的互動式課程，或開發者準備技術會議的幻燈片。它的簡單性也適合學生快速製作報告。

---

**關鍵引用**：
- [Marp: Markdown Presentation Ecosystem 官方網站](https://marp.app/)
- [GitHub - marp-team/marpit 幻燈片框架](https://github.com/marp-team/marpit)
- [Write your tech talk slides rapidly with Marp DEV Community 文章](https://dev.to/andyhaskell/write-your-tech-talk-slides-rapidly-with-marp-2c7g)
- [Creating Slides with Marp: Custom Themes Medium 文章](https://medium.com/@75py/creating-slides-with-marp-13dc35e36e4c)
- [GitHub - hahnec/marp-recipes 範例和模板](https://github.com/hahnec/marp-recipes)
- [4 Markdown-powered slide generators Opensource.com 文章](https://opensource.com/article/18/5/markdown-slide-generators)

---

### 圖片調整和排版
Marp 提供多種方式來調整和排版圖片，讓您的幻燈片更具視覺吸引力。以下是具體方法：

#### 調整圖片大小
您可以使用關鍵字在圖片後指定寬度和高度，例如：
- 調整寬度：`![width:300px](image.jpg)`
- 調整高度：`![height:200px](image.jpg)`
- 同時調整：`![width:300px height:200px](image.jpg)`

#### 背景圖片
將圖片設為幻燈片背景，使用 `![bg](url)` 語法：
- 基本用法：`![bg](https://example.com/background.jpg)`
- 調整大小：`![bg 150%](https://example.com/background.jpg)`
- 應用濾鏡：`![bg blur:3px](https://example.com/background.jpg)`

#### 定位和多圖排版
- 分割背景：使用 `left` 或 `right` 定位，例如 `![bg left](https://example.com/background.jpg)`。
- 多層背景：使用多個 `bg` 關鍵字，例如 `![bg](image1.jpg) ![bg](image2.jpg)`，可使用 `vertical` 設定垂直堆疊。

---

### 動畫和過場設定
Marp 的動畫和過場設定主要適用於 HTML 輸出，需使用支援 View Transition API 的瀏覽器（如 Chrome 111+、Edge 111+、Safari 18.2+）。以下是具體方法：

#### 過場設定
- 使用 `transition` 指令設定過場效果，例如：
  ```
  --- transition: fade ---
  # 帶有淡入淡出效果的幻燈片
  ```
- 內建過場包括 `none`、`clockwise`、`fade` 等，完整列表可參考 Marp 文件。
- 自訂過場：透過 CSS `@keyframes` 定義自訂動畫，需編輯 HTML 輸出。

#### 動畫功能
- 支援元素之間的轉換動畫，使用 `view-transition-name` CSS 屬性實現。
- 例如，在元素上添加 `view-transition-name: my-element`，可在切換幻燈片時實現平滑轉換。
- 動畫效果僅適用於 HTML 輸出，且需相容瀏覽器支援。

---

---

### 調查報告：Marp 的圖片調整、排版與動畫/過場設定詳解

Marp 是一款基於 Markdown 的幻燈片製作工具，允許使用者透過簡單的語法創建專業的演示文稿。以下是對圖片調整和排版，以及動畫和過場設定的詳細分析，特別針對講座或技術分享場景的適用性。

#### 圖片調整和排版的技術細節

Marp 擴展了標準 Markdown 的圖片語法，提供了多種圖片調整和排版選項，適合不同視覺需求。以下是具體實現方式：

1. **圖片大小調整**：
   - Marp 允許在圖片語法中指定寬度和高度，使用關鍵字 `width` 和 `height`。例如：
     - `![width:300px](image.jpg)`：將圖片寬度設為 300 像素。
     - `![height:200px](image.jpg)`：將圖片高度設為 200 像素。
     - `![width:300px height:200px](image.jpg)`：同時設定寬度和高度。
   - 支援單位包括像素（px），但不支援視窗相對單位（如 vw、vh、vmin、vmax），適合固定尺寸的展示。
   - 表 1 列出圖片大小調整的支援情況：

     | 功能                     | 內聯圖片 | 背景圖片 | 進階背景 | 備註                                      |
     |--------------------------|----------|----------|----------|------------------------------------------|
     | 按關鍵字調整大小         | 僅 `auto` | ✔️       | ✔️       | -                                        |
     | 按百分比調整大小         | ❌       | ✔️       | ✔️       | 例如 `![bg 150%](https://example.com/background.jpg)` |
     | 按長度調整大小           | ✔️       | ✔️       | ✔️       | 例如 `![width:200px](image.jpg)`，不支援 vw/vh 等 |

2. **背景圖片與濾鏡**：
   - 背景圖片使用 `![bg](url)` 語法設定，可進一步調整大小和應用 CSS 濾鏡。例如：
     - `![bg 150%](https://example.com/background.jpg)`：放大 150%。
     - `![bg blur:3px](https://example.com/background.jpg)`：應用模糊效果。
   - 支援的濾鏡包括亮度（brightness）、灰度（grayscale）、懷舊（sepia）等，參考 [CSS 濾鏡文件](https://developer.mozilla.org/en-US/docs/Web/CSS/filter)。
   - 內聯圖片也支援濾鏡，例如 `![brightness:.8 sepia:50%](https://example.com/image.jpg)`。

3. **圖片定位與多圖排版**：
   - 分割背景：使用 `left` 或 `right` 關鍵字實現 Deckset 風格的分割背景，例如 `![bg left](https://picsum.photos/720?image=29)`，可指定比例如 `left:33%`。
   - 多層背景：允許多個背景圖片堆疊，預設水平排列，可使用 `vertical` 關鍵字切換為垂直排列。例如：
     - `![bg](image1.jpg) ![bg](image2.jpg)`：水平堆疊。
     - `![bg vertical](image1.jpg) ![bg vertical](image2.jpg)`：垂直堆疊。
   - 這些功能適合創建複雜的視覺效果，例如講座中的多圖比較或背景層次設計。

#### 動畫與過場設定的技術細節

Marp 的動畫和過場設定主要針對 HTML 輸出，基於 View Transition API 實現。以下是具體功能和限制：

1. **過場設定**：
   - Marp CLI 的 `bespoke` 模板支援幻燈片過場動畫，使用 `transition` 本地指令設定。例如：
     - `--- transition: fade ---`：設定淡入淡出過場。
     - `--- transition: fade 1s ---`：設定 1 秒的淡入淡出過場。
   - 內建過場效果包括 33 種，如 `none`、`clockwise`、`counterclockwise`、`cover` 等，完整列表可參考 [Marp CLI 過場展示](https://marp-cli-page-transitions.glitch.me/)。
   - 自訂過場：使用者可透過 CSS `@keyframes` 定義自訂動畫，命名規則為 `marp-transition-XXXXXXXX` 等，並在 Markdown 中引用。
   - 過場持續時間預設為 0.5 秒，可透過指令調整（如 `1s` 或 `1000ms`）。
   - 表 2 列出瀏覽器支援情況：

     | 瀏覽器  | 支援 | 版本範圍       |
     |----------|------|----------------|
     | Chrome   | ✅   | 111 及以上     |
     | Edge     | ✅   | 111 及以上     |
     | Safari   | ✅   | 18.2 及以上    |
     | Firefox  | ❌   | -              |

2. **動畫功能**：
   - 支援元素之間的轉換動畫（morphing animations），使用 `view-transition-name` CSS 屬性標記元素。例如：
     - 在 HTML 中添加 `style="view-transition-name: my-element"`，在切換幻燈片時實現平滑轉換。
   - 這功能適用於 Chrome 和 Edge，Safari 可能因 WebKit 長久存在的 Bug 而效果不穩定，需使用 [marpit-svg-polyfill](https://github.com/marp-team/marpit-svg-polyfill) 修補。
   - 要求每個幻燈片中 `view-transition-name` 名稱唯一，否則轉換動畫可能失效。
   - 動畫僅在 HTML 輸出中有效，PDF 和 PPTX 格式不支援動畫。

3. **限制與注意事項**：
   - 過場和動畫僅適用於 HTML 輸出，需在支援 View Transition API 的瀏覽器中查看（如 Chrome 111+）。
   - 若觀眾啟用「減少動畫」模式（prefers-reduced-motion），過場會自動降級為簡單的 `fade` 效果，參考 [web.dev 文章](https://web.dev/prefers-reduced-motion/)。
   - 使用 CLI 可選擇禁用過場：`--bespoke.transition=false`。

#### 適用場景與建議

- **圖片調整與排版**：適合技術講座或教育簡報，特別是需要展示圖表、圖片比較或背景設計的場景。建議使用相對單位（如百分比）以適應不同螢幕尺寸。
- **動畫與過場**：適合 HTML 格式的線上分享或現場演示，增強視覺效果。但需提前測試瀏覽器兼容性，特別是 Safari 的潛在 Bug。
- **備案方案**：若需離線或跨平台使用，考慮匯出 PDF，接受無動畫的限制。

#### 結論

Marp 提供強大的圖片調整和排版功能，透過關鍵字和 CSS 濾鏡實現靈活的視覺設計。動畫和過場設定主要適用於 HTML 輸出，支援內建和自訂效果，但受限於瀏覽器兼容性和輸出格式。建議根據講座需求選擇適當的輸出格式，並提前測試以確保效果。

---

### 關鍵引用
- [Marp 圖片語法文件](https://marpit.marp.app/image-syntax)
- [Marp CLI 自訂過場文件](https://github.com/marp-team/marp-cli/blob/main/docs/bespoke-transitions/README.md)
- [Marp Blog 自訂過場文章](https://marp.app/blog/how-to-make-custom-transition)
- [CSS 濾鏡文件](https://developer.mozilla.org/en-US/docs/Web/CSS/filter)
- [Marp CLI 過場展示](https://marp-cli-page-transitions.glitch.me/)
- [web.dev 減少動畫文章](https://web.dev/prefers-reduced-motion/)

---
# 置底footer

在 Marp 中，`<!--_footer: "Reference" -->` 是一種局部指令（local directive），用來為單張幻燈片設定頁腳內容。這種語法非常適合您的需求（例如置底參考文獻），而且比全局 `footer` 更靈活。以下是關於如何使用此語法增加多個頁腳內容或實現換行的詳細說明。

---

### 基本語法說明
- `<!--_footer: "內容" -->` 是 Marp 的註解式指令，僅影響其所在幻燈片。
- 它支援 Markdown 和 HTML 語法，因此可以用來添加多行文字或格式化內容。

---

### 增加多個頁腳內容
若您想在同一張幻燈片中顯示多個參考文獻（例如 `[1]` 和 `[2]`），可以直接在 `<!--_footer: -->` 中撰寫多項內容，並使用 HTML 或 Markdown 格式分隔。

#### 方法 1：使用空格或分隔符
- **範例**：
  ```
  # 幻燈片標題
  研究內容 [1] 和 [2]
  <!--_footer: "[1] Kochanek PM et al., *Pediatric Critical Care Medicine*, 2019;20(3):269–279.   [2] Smith J et al., *Journal of Science*, 2020;15(4):123–130." -->
  ```
- **效果**：頁腳顯示為單行，兩條參考文獻用空格分隔。
- **注意**：若內容過長，可能被截斷，需調整字體大小或幻燈片布局。

#### 方法 2：使用 HTML 列表
- **範例**：
  ```
  # 幻燈片標題
  研究內容 [1] 和 [2]
  <!--_footer: "<ol><li>Kochanek PM et al., <i>Pediatric Critical Care Medicine</i>, 2019;20(3):269–279.</li><li>Smith J et al., <i>Journal of Science</i>, 2020;15(4):123–130.</li></ol>" -->
  ```
- **效果**：
  - 頁腳顯示為有序列表：
    ```
    1. Kochanek PM et al., Pediatric Critical Care Medicine, 2019;20(3):269–279.
    2. Smith J et al., Journal of Science, 2020;15(4):123–130.
    ```
- **優點**：結構清晰，適合多個參考文獻。

---

### 實現換行
若要在頁腳中換行，可以使用 HTML 的 `<br>` 標籤或 CSS 自訂樣式。

#### 方法 1：使用 `<br>` 換行
- **範例**：
  ```
  # 幻燈片標題
  研究內容 [1] 和 [2]
  <!--_footer: "[1] Kochanek PM et al., <i>Pediatric Critical Care Medicine</i>, 2019;20(3):269–279.<br>[2] Smith J et al., <i>Journal of Science</i>, 2020;15(4):123–130." -->
  ```
- **效果**：
  - 頁腳顯示為兩行：
    ```
    [1] Kochanek PM et al., Pediatric Critical Care Medicine, 2019;20(3):269–279.
    [2] Smith J et al., Journal of Science, 2020;15(4):123–130.
    ```
- **注意**：`<br>` 是 HTML 換行符，Marp 會正確解析。

#### 方法 2：使用 CSS 控制換行
若需要更靈活的排版，可以結合 `<style>` 標籤調整頁腳樣式。

- **範例**：
  ```
  # 幻燈片標題
  研究內容 [1] 和 [2]
  <!--_footer: "<div class='ref'>[1] Kochanek PM et al., <i>Pediatric Critical Care Medicine</i>, 2019;20(3):269–279.</div><div class='ref'>[2] Smith J et al., <i>Journal of Science</i>, 2020;15(4):123–130.</div>" -->

  <style>
  .ref {
    display: block; /* 每個 div 獨立一行 */
    font-size: 12px;
  }
  </style>
  ```
- **效果**：頁腳顯示為兩行，並可透過 CSS 調整字體大小、顏色等。

---

### 進階應用：多張幻燈片與動態頁腳
若不同幻燈片需要不同的參考文獻，可以為每張幻燈片單獨設定 `<!--_footer: -->`。

- **範例**：
  ```
  ---
  theme: gaia
  ---

  # 第一張幻燈片
  研究內容 [1]
  <!--_footer: "[1] Kochanek PM et al., <i>Pediatric Critical Care Medicine</i>, 2019;20(3):269–279. <a href='https://doi.org/10.1097/PCC.0000000000001737'>DOI</a>" -->

  ---

  # 第二張幻燈片
  另一個觀點 [2]
  <!--_footer: "[2] Smith J et al., <i>Journal of Science</i>, 2020;15(4):123–130." -->
  ```
- **效果**：
  - 第一張幻燈片頁腳顯示 `[1]` 的參考文獻。
  - 第二張幻燈片頁腳顯示 `[2]` 的參考文獻。

---

### 注意事項與優化
1. **字體大小**：
   - 頁腳預設字體較小，若內容過多，可用 `<style>` 調整：
     ```
     <style>
     footer {
       font-size: 10px;
     }
     </style>
     ```
2. **超連結**：
   - 在 HTML 輸出中，`<a href="...">` 可點擊；在 PDF 中，需確保轉換工具（如 Chrome）支援。
3. **內容長度**：
   - 若頁腳過長，可能超出幻燈片底部，建議限制每行字數或使用縮寫。
4. **Markdown 限制**：
   - `<!--_footer: -->` 中的內容若包含純 Markdown（如 `*斜體*`），可能不會正確解析，建議使用 HTML（如 `<i>斜體</i>`）。

---

### 綜合範例
以下是結合多個參考文獻和換行的完整範例：
```
---
theme: gaia
---

# 研究概述
研究顯示重要結果 <sup>[1]</sup>，進一步分析見 <sup>[2]</sup>。

<!--_footer: "<ol><li>Kochanek PM et al., <i>Pediatric Critical Care Medicine</i>, 2019;20(3):269–279. <a href='https://doi.org/10.1097/PCC.0000000000001737'>DOI</a></li><li>Smith J et al., <i>Journal of Science</i>, 2020;15(4):123–130.</li></ol>" -->

<style>
footer {
  font-size: 12px;
  padding-bottom: 10px;
}
</style>
```
- **轉換命令**：
  ```
  npx marp slides.md -o slides.html
  ```
- **效果**：
  - 內容中使用上標 `[1]` 和 `[2]`。
  - 頁腳顯示為有序列表，兩條參考文獻分行排列。

---

### 結論與建議
- **增加多個頁腳內容**：使用 HTML 列表（`<ol>` 或 `<ul>`）或簡單的分隔符。
- **實現換行**：使用 `<br>` 或 CSS 的 `display: block`。
- **講座應用**：推薦使用 `<ol>` 格式，結構化且符合學術規範；若需超連結，確保 HTML 輸出環境支援。

---
# 部屬到 GitHub Pages

以下將詳細指導您如何使用 Marp 將幻燈片輸出為 HTML，並介紹部署到 GitHub Pages 的方法，以及其他可能的部署方案。這些方法特別適合講座或公開分享使用。

---

### 使用 Marp 輸出為 HTML 的方案

Marp 提供簡單的方式將 Markdown 文件轉換為 HTML 文件，您可以使用 Marp CLI（命令列工具）來完成。以下是步驟：

#### 步驟 1：安裝 Marp CLI
1. 確保您的電腦已安裝 **Node.js**（建議最新 LTS 版本，例如 v18 或 v20）。
2. 在終端機中全局安裝 Marp CLI：
   ```
   npm install -g @marp-team/marp-cli
   ```
   或若不想全局安裝，可在專案目錄中局部安裝：
   ```
   npm install --save-dev @marp-team/marp-cli
   ```

#### 步驟 2：撰寫 Marp Markdown 文件
創建一個 Markdown 文件（例如 `slides.md`），內容如下：
```
---
theme: gaia
---

# 第一張幻燈片
歡迎使用 Marp！

---

# 第二張幻燈片
- 項目 1
- 項目 2
```

#### 步驟 3：轉換為 HTML
1. 在終端機中，進入包含 `slides.md` 的目錄。
2. 執行以下命令將其轉換為 HTML：
   ```
   npx marp slides.md -o slides.html
   ```
   - `npx marp`：調用 Marp CLI。
   - `-o slides.html`：指定輸出文件為 `slides.html`。
3. 檢查輸出：打開 `slides.html` 文件，確認內容正確顯示。

#### 進階選項
- **預覽模式**：若想即時預覽並編輯：
  ```
  npx marp --preview slides.md
  ```
  這會啟動一個本地伺服器（通常在 `http://localhost:8080`），可用瀏覽器查看。
- **添加轉場效果**：若需要動態效果，可手動編輯輸出的 HTML，加入 CSS 和 JavaScript（見前文範例）。
- **多文件輸出**：若有多個 Markdown 文件，可使用通配符：
  ```
  npx marp *.md -o output/
  ```

---

### 部署到 GitHub Pages

GitHub Pages 是一個免費的靜態網站托管服務，非常適合部署 Marp 生成的 HTML 幻燈片。以下是部署步驟：

#### 步驟 1：創建 GitHub 儲存庫
1. 登錄 GitHub，點擊右上角「+」 > 「New repository」。
2. 輸入儲存庫名稱（例如 `marp-slides`），選擇公開（Public）或私有（Private），然後點擊「Create repository」。

#### 步驟 2：準備文件並推送
1. 在本地創建一個專案資料夾（例如 `marp-slides`）。
2. 將 `slides.md` 和生成的 `slides.html` 放入該資料夾。
3. 若有圖片或其他資源（如 `img/` 資料夾），也一併放入並確保路徑正確（建議使用相對路徑，例如 `![圖片](./img/image.jpg)`）。
4. 初始化 Git 並推送：
   ```
   cd marp-slides
   git init
   git add .
   git commit -m "Initial commit with Marp slides"
   git remote add origin https://github.com/您的用戶名/marp-slides.git
   git push -u origin main
   ```

#### 步驟 3：啟用 GitHub Pages
1. 在 GitHub 儲存庫頁面，點擊「Settings」。
2. 滾動至「Pages」部分。
3. 在「Source」下拉選單中，選擇 `main` 分支（或您使用的分支），根目錄設為 `/ (root)`，然後點擊「Save」。
4. 等待幾分鐘，GitHub Pages 會生成一個 URL，例如：
   ```
   https://您的用戶名.github.io/marp-slides/
   ```
5. 訪問該 URL，確認 `slides.html` 可正常顯示。若檔案名稱不是 `index.html`，需在 URL 中指定，例如：
   ```
   https://您的用戶名.github.io/marp-slides/slides.html
   ```

#### 步驟 4：優化（可選）
- **將 `slides.html` 改名為 `index.html`**：
  - 這樣訪問根 URL（`https://您的用戶名.github.io/marp-slides/`）即可直接顯示幻燈片。
  - 修改後重新推送：
    ```
    mv slides.html index.html
    git add .
    git commit -m "Rename to index.html"
    git push
    ```
- **自動化部署**：
  - 使用 GitHub Actions 自動轉換並部署：
    1. 在儲存庫根目錄創建 `.github/workflows/deploy.yml`：
       ```yaml
       name: Deploy Marp Slides to GitHub Pages
       on:
         push:
           branches: [main]
       jobs:
         build-and-deploy:
           runs-on: ubuntu-latest
           steps:
             - uses: actions/checkout@v3
             - name: Setup Node.js
               uses: actions/setup-node@v3
               with:
                 node-version: '18'
             - name: Install Marp CLI
               run: npm install -g @marp-team/marp-cli
             - name: Build Slides
               run: npx marp slides.md -o index.html
             - name: Deploy to GitHub Pages
               uses: peaceiris/actions-gh-pages@v3
               with:
                 github_token: ${{ secrets.GITHUB_TOKEN }}
                 publish_dir: ./
       ```
    2. 提交此文件並推送，之後每次推送 `slides.md` 時，GitHub Actions 會自動生成並部署 HTML。

---

### 其他部署方案

除了 GitHub Pages，還有以下替代方案，根據您的需求選擇：

#### 1. Netlify
- **步驟**：
  1. 將 `slides.html`（建議改名為 `index.html`）上傳至一個本地資料夾。
  2. 註冊 Netlify 帳號，拖曳資料夾至 Netlify 的「Sites」頁面，或連結 GitHub 儲存庫。
  3. 部署完成後，獲得一個 URL（例如 `https://your-site.netlify.app`）。
- **優點**：
  - 簡單拖放部署，支援自訂域名。
  - 提供預覽部署功能，適合測試。
- **講座適用性**：
  - 適合快速分享，無需手動配置伺服器。

#### 2. Vercel
- **步驟**：
  1. 安裝 Vercel CLI：
     ```
     npm install -g vercel
     ```
  2. 在專案資料夾中執行：
     ```
     vercel
     ```
  3. 按提示配置並部署，獲得 URL（例如 `https://your-site.vercel.app`）。
- **優點**：
  - 支援自動化部署，與 Git 整合。
  - 提供免費 HTTPS 和自訂域名。
- **講座適用性**：
  - 適合技術講座，部署快速且可靠。

#### 3. 本地伺服器（離線使用）
- **步驟**：
  1. 將 `slides.html` 儲存至 USB 或電腦。
  2. 使用簡單的 HTTP 伺服器（如 Python）運行：
     ```
     python -m http.server 8000
     ```
  3. 在瀏覽器訪問 `http://localhost:8000/slides.html`。
- **優點**：
  - 無需網路，適合現場講座。
- **講座適用性**：
  - 適合離線環境，但需自備設備。

#### 4. 雲端儲存（如 Google Drive/Dropbox）
- **步驟**：
  1. 上傳 `slides.html` 至 Google Drive 或 Dropbox。
  2. 生成公開分享連結。
  3. 使用連結訪問（需確保檔案可公開下載並在瀏覽器中打開）。
- **優點**：
  - 簡單分享，無需部署。
- **講座適用性**：
  - 適合小型分享，但可能因檔案格式限制而不穩定。

---

### 針對講座使用的建議

- **推薦方案**：
  - **GitHub Pages**：免費、穩定，適合公開講座並長期存取。
  - **Netlify/Vercel**：若需要更專業的部署體驗或自訂域名。
  - **本地伺服器**：若講座現場無網路，作為備案。

- **注意事項**：
  - **圖片路徑**：部署前確認所有圖片使用相對路徑（例如 `./img/image.jpg`），並包含在儲存庫中。
  - **測試**：部署後在不同設備上測試，確保幻燈片顯示正常。
  - **備份**：保留 PDF 版本作為應急方案。

- **GitHub Pages 自動化範例**：
  使用上述 GitHub Actions 配置後，您只需編輯 `slides.md` 並推送，幻燈片會自動更新並部署到 GitHub Pages，非常適合講座前的即時調整。

---

### 結論

使用 Marp 輸出 HTML 簡單高效，透過 Marp CLI 即可完成。部署到 GitHub Pages 是最推薦的方式，因其免費且與 Git 整合良好；其他方案如 Netlify、Vercel 或本地伺服器則視需求補充。若您需要進一步協助（例如具體的 GitHub Actions 配置或某方案的細節），請告訴我，我可以提供更詳細的指導！