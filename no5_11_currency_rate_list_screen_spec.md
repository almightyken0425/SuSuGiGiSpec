# 設定 - 匯率管理 (CurrencyRateListScreen)

_(本文件定義「匯率管理」畫面的 UI、流程與邏輯，此為付費功能)_

## 畫面目標 (Screen Objective)

- 提供一個中心化的儀表板，讓使用者可以**查看**並**更新**他們所使用的各個貨幣對的**最新有效匯率**。
- 清楚地向使用者溝通匯率的計算與應用規則。

## UI 佈局與元件 (UI Layout & Components)

- **頂部導航列 (Top Navigation Bar):**
    - **左側:** 「返回」按鈕，導航回設定主頁 (`SettingsScreen`)。
    - **中間:** 畫面標題，顯示「匯率管理」。

- **說明文字區 (Info Text Area):**
    - **UI:** 在「匯率列表」的上方，應有一個清晰的說明區塊。
    - **內容:**
        > 「此處顯示各貨幣對的**最新有效匯率**。當您進行跨幣別轉帳時，系統會自動記錄當下的匯率。所有報表在計算總資產時，將統一採用您在此處設定的最新匯率進行換算。您可以點擊下方的匯率項目來手動更新。」

- **匯率列表 (Rate List):**
    - **UI:** 一個列表 (`FlatList`)，**僅顯示**使用者所有使用過的貨幣對及其**最新一筆**的有效匯率。
    - **項目內容 (每筆):**
        - 顯示類似「1 USD = 32.5 TWD」的文字。
        - 顯示該匯率的最後更新日期 (`rateDate`)。
    - **空狀態 (Empty State):** 如果使用者尚未使用任何外幣帳戶，則顯示提示文字，例如「當您新增外幣帳戶或進行跨幣別轉帳時，相關匯率將會顯示於此。」

- **新增按鈕 (Add Button):**
    - **UI:** 一個懸浮操作按鈕 (FAB)，圖示為「+」。
    - **邏輯:** 點擊後導航至 `CurrencyRateEditorScreen` 的「新增」模式。

## 核心邏輯

- **資料載入邏輯:**
    - 畫面載入時，直接查詢 `CurrencyRates` 表來取得資料：
        - 將 `CurrencyRates` 表中的所有記錄按 (`currencyFromId`, `currencyToId`) 貨幣對進行分組。
        - 在每個分組中，找出 `rateDate` **最新**的一筆記錄。
        - 將這些找出的「最新有效匯率」記錄顯示在列表中。

- **互動邏輯:**
    - **點擊列表項目 (設定新匯率):** 點擊列表項目應被視為「更新匯率」。此操作會導航至匯率編輯器畫面 (`CurrencyRateEditorScreen`)，並傳入該貨幣對資訊以「新增」一筆新的匯率記錄。

- **付費牆檢查 (Paywall Check):**
    - 由於此畫面為付費功能，在從設定主頁 (`SettingsScreen`) 導航至此畫面之前，就應檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser` 狀態。若為免費版使用者，則直接導向付費牆畫面 (`PaywallScreen`)。

## 狀態管理 (State Management)

- 使用 `useState` 管理從 `CurrencyRates` 讀取並處理過的匯率列表 `latestRates: Rate[]`。

## 導航 (Navigation)

- **進入:** 從設定主頁 (`SettingsScreen`) 的「匯率管理」項目點擊進入。
- **退出:** 點擊頂部導航列的「返回」按鈕。
- **導出:** 點擊列表項目或新增按鈕，導航至匯率編輯器畫面 (`CurrencyRateEditorScreen`)。
