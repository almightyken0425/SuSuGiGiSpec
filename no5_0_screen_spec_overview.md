# 畫面規格總覽

_(本文件用來規劃 MVP 範圍內所有需要詳細定義規格的 App 畫面 (Screen))_

## 畫面列表 (MVP)

根據 MVP 範圍和檔案結構計劃，我們至少需要為以下 MVP 範圍內的畫面定義詳細規格（包含 UI 佈局、元件、互動流程、資料來源、錯誤處理等）：

- **登入畫面 (LoginScreen)**
    - UI 佈局 (Logo, 價值主張, Google 登入按鈕)
    - 認證流程 (呼叫 `authService` 執行 Google 登入)
    - 錯誤處理 (登入失敗、網路錯誤)
    - 導航邏輯 (登入成功後導航至首頁，觸發「首次登入流程」)

- **首頁 (HomeScreen)**
    - UI 佈局 (控制列、摘要視圖、列表視圖)
    - 狀態管理 (viewMode, currentDate, selectedAccounts)
    - 核心互動 (視圖切換、時間區間滑動/選擇、帳戶篩選)
    - 摘要視圖資料邏輯 (總計、圖表聚合、水平滾動摘要)
    - 列表視圖資料邏輯 (交易讀取、日期/類別分組)
    - 導航 (點擊設定、點擊交易項目)

- **交易編輯器畫面 (TransactionEditorScreen)**
    - UI 佈局 (收支切換、金額輸入、類別/帳戶/日期選擇、備註)
    - 共用元件 (帳戶選擇器、類別選擇器、日期選擇器)
    - 資料邏輯 (新增/編輯/刪除 `Transaction` 記錄)
    - 狀態管理 (表單資料)
    - 導航 (接收交易 ID 進入編輯模式、儲存後返回)
    - (付費功能) 包含用於**建立**定期交易的 Modal/Sheet 介面入口

- **轉帳編輯器畫面 (TransferEditorScreen)**
    - UI 佈局 (來源/目標帳戶選擇、轉出/轉入金額輸入、日期、備註)
    - 共用元件 (帳戶選擇器 x2, 日期選擇器)
    - 多幣別邏輯 (處理跨幣別轉帳，顯示參考匯率)
    - 資料邏輯 (新增/編輯/刪除 `Transfer` 記錄，儲存 `AmountFrom/To`)
    - 狀態管理 (表單資料)
    - 導航 (接收轉帳 ID 進入編輯模式、儲存後返回)
    - (付費功能) 包含用於**建立**定期交易的 Modal/Sheet 介面入口

- **設定 - 主頁 (SettingsScreen)**
    - UI 佈局 (導航列表)
    - 導航項目 (連結至後續子畫面)
    - 登出邏輯 (呼叫 `authService` 登出)
    - (付費功能) 顯示/連結至付費牆
- **設定 - 類別列表 (CategoryListScreen)**
    - UI: 依 `CategoryType` (收/支) 分頁顯示類別列表、新增按鈕。
    - 互動: **支援拖拉排序**，更新 `SortOrder` 欄位。點擊項目導航至 `CategoryEditorScreen`。
    - 資料: 讀取 `Categories`。

- **設定 - 類別編輯器 (CategoryEditorScreen)**
    - UI: 名稱、圖標 (IconPicker)、`CategoryType` (不可修改)、`StandardCategoryId` 映射 (必要)。
    - 資料: 讀寫 `Categories`。
    - 邏輯: 檢查免費版 10 個類別限制 (觸發付費牆)。

- **設定 - 帳戶列表 (AccountListScreen)**
    - UI: 顯示所有帳戶列表。列表應根據 SortOrder 排序並支援拖拉。
    - 互動:
        - **支援拖拉排序:** 支援拖拉排序，更新其 `SortOrder` 欄位。
        - 點擊項目導航至 `AccountEditorScreen` 進行編輯。
        - 點擊「新增」按鈕導航至 `AccountEditorScreen` 進行建立。
    - 資料: 讀取 `Accounts`。

- **設定 - 帳戶編輯器 (AccountEditorScreen)**
    - UI: 名稱、圖標 (IconPicker)、幣別、初始餘額 (僅限新增)、標準帳戶類型映射。
    - 資料: 讀寫 `Accounts`。
    - 邏輯: 檢查免費版 3 個帳戶限制 (觸發付費牆)、(付費功能) 建立外幣帳戶時觸發匯率輸入。

- **設定 - 圖標選擇器 (IconPickerScreen)**
    - UI: 顯示 `IconDefinition.json` 中 `types` 相符的圖標網格 (e.g., 'expense', 'income', 'account', 'general')。

- **設定 - 匯率管理 (CurrencyRateListScreen)** (付費功能)
    - UI: 顯示各貨幣對的**最新有效匯率**列表，並包含說明文字。
    - 資料: 讀取 `CurrencyRates`。
    - 邏輯: 允許使用者點擊列表項目來**更新**現有貨幣對的匯率（實質為新增記錄），或手動新增一個新的貨幣對匯率。

- **設定 - 匯率編輯器 (CurrencyRateEditorScreen)** (付費功能)
    - UI: 貨幣對選擇器、匯率輸入框。
    - 資料: 寫入 `CurrencyRates` (僅新增)。
    - 邏輯: 處理匯率 (1 From = ? To) 的輸入與儲存。

- **設定 - 偏好設定 (PreferenceScreen)**
    - UI: 語系選擇器、主要貨幣選擇器、時區選擇器。
    - 資料: 讀寫 `Settings` (Key-Value)。
    - 邏輯: 變更後需觸發 App 重新載入設定 (e.g., i18n, 報表重算)。

- **搜尋畫面 (SearchScreen)**
    - UI: 搜尋輸入框、交易結果列表。
    - 資料: 查詢 `Transactions` 和 `Transfers` 的 `Note` 欄位。
    - 互動: 點擊結果導航至編輯畫面。
- **匯入畫面 (ImportScreen)**
    - UI: 檔案選擇器 (CSV)、欄位映射介面、匯入預覽。
    - 邏輯: CSV 解析、資料驗證、寫入 `Transactions` 表。
    - 錯誤處理: 顯示匯入失敗的行數與原因。
- **付費牆畫面 (PaywallScreen)**
    - UI: 顯示免費版限制、付費版功能列表 (多幣別、定期交易、無限帳戶/類別等)。
    - 互動: 顯示訂閱選項 (月/年)、購買按鈕、恢復購買按鈕。
    - 邏輯: 串接 RevenueCat (或 App Store/Google Play) 處理購買流程、驗證收據、更新 `Settings` 中的 `isPremiumUser` 狀態。

## 全域設計原則

- **編輯器的呈現方式:** 所有用於「新增」或「編輯」的獨立畫面 (如 `CategoryEditorScreen`, `TransactionEditorScreen`, `AccountEditorScreen` 等)，都應統一採用 **Sheet 形式的 Modal** 進行呈現，而非全螢幕或 Segue (Push) 導航。