# AI 台灣旅遊情報員 × 智慧行程推薦網站

以官方旅遊情報為基礎的台灣旅行提案原型。專案整理旅遊研究、每週情報、簡報與影片素材，並提供一頁式網站，讓親子、情侶及熟齡旅客依偏好探索主題。

## 快速預覽

- **旅遊推薦網站：**直接在瀏覽器開啟 [`index.html`](index.html)。網站使用原生 HTML、CSS 與 JavaScript，不需安裝套件或設定 API Key。
- **簡報網頁：**開啟 [`slides.html`](slides.html)。
- **PowerPoint：**使用 PowerPoint 開啟 `presentations/taiwan-travel-weekly-2026-11-21.pptx`。
- **影片：**預覽 `video/taiwan-travel-promo-30s.mp4`；分鏡與素材說明見 `video/storyboard.md`。

## 網站目前狀態

`index.html` 是靜態前端原型，包含品牌首頁、週報情報、三類旅客入口、偏好篩選、規則式推薦、理由與來源、無結果提示及複製諮詢需求。偏好僅在當次頁面互動中使用，不寫入網址或瀏覽器儲存空間；目前沒有後端、會員、即時交通／天氣、付款、訂位或正式旅行社聯絡表單。

研究資料尚未提供旅行社正式商品、價格、團位或服務條款。網站中的行程與價格為醒目標示的**模擬資料**；官方景點及活動資訊只作旅遊情報，不代表可售套裝商品。活動日期與景點營運狀況可能變動，請出發前重新查核來源。

## 專案目錄

- `docs/`：CCI、SIPOC、產品需求及每週旅遊情報。
- `research/`：結構化旅遊資料、來源索引、查詢日期及使用限制。
- `weekly-reports/`：週報工作目錄。
- `presentations/`：簡報大綱與 PowerPoint 成品。
- `video/`：影片分鏡、提示詞、建置腳本及成品素材。
- `website/`：後續網站工程工作目錄；目前首頁檔案位於專案根目錄 `index.html`。
- `handoffs/`：角色交接紀錄。
- `qa/`：功能及來源抽查紀錄。
- `templates/`：研究、週報、交接與驗收模板。
- `skills/travel-content-factory/`：旅遊內容工作流程 Skill 原始檔。

## 建議閱讀順序

1. 閱讀 [專案協作規範](AGENTS.md)。
2. 閱讀 [產品需求](docs/PRD.md)、[週報](docs/weekly-report.md) 及 [來源索引](research/sources.md)。
3. 在瀏覽器預覽 `index.html`，再查看 [網站驗收紀錄](qa/website-prototype-2026-11-21.md)。
5. 檢視 [簡報大綱](presentations/slide-outline.md)、[影片分鏡](video/storyboard.md) 及角色交接紀錄。

## 旅遊資料與隱私

現有旅遊研究查詢日期為 2026-11-21；可核實事實附來源連結，客群配對建議、開放狀況、票價、交通及其他未確認項目均須依文件標示。資料來源、開放資料授權與媒體使用限制見 `research/sources.md`。

不要提交密碼、API Key、存取權杖、真實 `.env`、客戶個資或未授權媒體。`.gitignore` 排除常見環境設定、憑證、個資資料夾、下載依賴及本機建置產物；提交前仍須檢查 Git 暫存檔案清單與差異。`.env.example` 若新增，只能使用假值或留空欄位。

## Git 與遠端發布

此工作目錄目前已有 Git 提交 `Initial project files`。提交前先查看將納入的追蹤檔案及差異；忽略規則只影響尚未追蹤的檔案，已追蹤檔案即使新增至 `.gitignore` 仍會留在提交內。

檢查本次準備提交的檔案及差異：

```bash
git status --short
git diff --cached --name-only
git diff --cached
```

建立後續本機提交：

```bash
git add README.md .gitignore
git diff --cached --name-only
git diff --cached
git commit -m "docs: 整理專案說明與忽略規則"
```

設定遠端前，先確認儲存庫網址、可見性及將上傳的提交內容。此專案目前沒有設定遠端；遠端目標尚未確認前不要執行 `git push`。推送前再次檢查將上傳的提交及檔案，確認沒有 `.env`、憑證、帳號密碼或旅客個資。
