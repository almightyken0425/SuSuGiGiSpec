# 產品定義與使用者故事

## 核心產品矩陣

-  **記帳 App + Firestore, Accounting App**
-  **Web 複雜報表, Web Console**
-  **AI 個人化建議, AI Advisor**
-  **總經分析報表與 API, Macro Data Service**

---

## 記帳 App + Firestore, Accounting App

**定位:** 核心基礎設施，提供極速記帳與雲端同步服務。
**價值:** 工具價值, Utility, 安全價值, Security

### User Stories

#### 交易與自動化, Transaction & Automation
- **支出管理, Expense CRUD:** 作為使用者，我想要新增、編輯、刪除一筆支出紀錄，以便追蹤我的花費。
- **收入管理, Income CRUD:** 作為使用者，我想要新增、編輯、刪除一筆收入紀錄，以便追蹤我的進帳。
- **轉帳管理, Transfer CRUD:** 作為使用者，我想要在不同帳戶間進行轉帳，以便管理資金流動。
- **定期交易, Recurring Transaction:** 作為付費使用者，我想要設定自動重複的交易, 如房租，以便省去重複輸入的時間。

#### 資產管理, Asset Management
- **帳戶管理, Account CRUD:** 作為使用者，我想要建立、編輯、刪除我的資產帳戶, 如現金、銀行。
- **類別管理, Category CRUD:** 作為使用者，我想要自訂交易類別與子類別，以便更精確地分類。
- **預設資料初始化, Onboarding Data:** 作為新使用者，我想要在首次開啟 App 時自動建立預設的幣別、帳戶與類別，以便立即開始使用。
- **多幣別支援, Multi-Currency:** 作為付費使用者，我想要管理外幣帳戶並進行跨幣別轉帳。
- **解除限制, Unlimited Access:** 作為付費使用者，我想要解除免費版的帳戶與類別數量限制。

#### 資料與同步, Data & Sync
- **離線支援, Offline Architecture:** 作為使用者，我想要在無網路時也能完整操作 CRUD，並在連網後自動同步。
- **雲端同步引擎, Sync Engine:** 作為付費使用者，我想要我的資料能自動備份到雲端，並在多裝置間同步。
- **資料匯入, CSV Import:** 作為付費使用者，我想要匯入外部 CSV 檔案，以便遷移舊資料。

#### 儀表板與體驗, Dashboard & Experience
- **首頁儀表板, Home Dashboard:** 作為使用者，我想要在首頁查看當月收支摘要與列表，以便快速掌握財務狀況。
- **搜尋功能, Local Search:** 作為使用者，我想要透過關鍵字搜尋備註欄位，以便找到特定的歷史交易。
- **多語言支援, i18n:** 作為使用者，我想要切換 App 語言, 如繁中、英文，以便使用我熟悉的介面。
- **配色主題系統, Theme System:** 作為開發團隊，我想要建立設計代幣與變數架構，以便 App 可支援多套配色主題。
- **主題切換介面, Theme Switcher:** 作為使用者，我想要在設定中切換不同的配色主題，以便客製化我的介面外觀。
- **新增配色主題, New Theme:** 作為設計團隊，我想要為系統新增一套完整的配色組合，以便提供使用者更多選擇。

#### 共用帳本, Shared Ledger
- **預設帳本, Default Book:** 作為使用者，我擁有一本預設的帳本，所有的交易都記錄在其中。
- **帳本切換, Book Switcher:** 作為使用者，我想要切換不同的帳本, 如個人、家庭，以便區隔不同場景的帳務。
- **成員邀請, Member Invitation:** 作為帳本管理者，我想要邀請其他使用者加入我的帳本，以便共同記帳。
- **協作權限, Collaboration:** 作為帳本成員，我想要在共用帳本中新增交易，並即時同步給其他成員。

---

## Web 複雜報表, Web Console

**定位:** 進階管理工具，提供桌面級的大螢幕操作與複雜邏輯處理。
**價值:** 管理價值, Management, 效率價值, Efficiency

### User Stories

#### 高密度資料瀏覽, Data Browsing
- **桌面版表格視圖, Data Grid:** 作為進階使用者，我想要在電腦大螢幕上以 Excel 般的表格介面瀏覽所有帳務。
- **進階匯出, Advanced Export:** 作為進階使用者，我想要匯出完整的 CSV/Excel 報表以供備份或外部分析。

#### 進階篩選與查詢, Advanced Query
- **JQL 查詢介面, JQL Interface:** 作為進階使用者，我想要使用類似 SQL 的語法進行複雜篩選。
- **自訂視圖儲存, Saved Views:** 作為進階使用者，我想要保存常用的篩選條件，以便下次快速存取。

#### 客製化報表, Custom Reporting
- **自訂維度分析, Custom Charts:** 作為進階使用者，我想要自定義 X/Y 軸維度來產生專屬分析圖表。
- **報表匯出, Report Export:** 作為進階使用者，我想要將分析圖表數據匯出為 CSV。

---

## AI 個人化建議, AI Advisor

**定位:** 智慧顧問，提供主動式的財務洞察與預測。
**價值:** 預知價值, Foresight, 顧問價值, Consultancy


### User Stories

#### 預測與診斷, Forecast & Diagnosis
- **現金流預測, Cashflow Forecast:** 作為使用者，我想要看到依目前消費速度推算的月底結餘預測。
- **財務健康評分, Health Score:** 作為使用者，我想要獲得每月的財務健康分數與改善建議。
- **自然語言問答, AI Chat:** 作為使用者，我想要用對話方式詢問財務問題並獲得即時回答。

---

## 總經分析報表與 API, Macro Data Service

**定位:** B 端數據服務，提供市場洞察與總體經濟指標。
**價值:** 情報價值, Intelligence, 決策價值, Decision

### User Stories

#### B 端數據服務, B2B Data Services
- **市場情資儀表板, Market Dashboard:** 作為市場研究員，我想要查詢特定受眾的聚合消費數據。
- **競品趨勢分析, Competitor Analysis:** 作為品牌商，我想要查看競品在特定時間點的消費熱度。
- **總經 API 串接, Macro API:** 作為量化交易員，我想要透過 API 獲取即時的民間消費力指數。
- **隱私合規處理, Privacy Compliance:** 作為平台管理者，我想要確保所有輸出數據皆經過 K-Anonymity 去識別化處理。
