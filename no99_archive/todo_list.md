# 待辦事項清單

## 規格文件更新

- [ ] 因應 `theme.ts` 的色碼與結構調整，需變更 `no1_design_tokens.md` 規格文件
    - **程式碼來源:** `SuSuGiGiApp/src/constants/theme.ts`
    - **規格文件:** `no3_module_specs/no3_accounting_app/no5_design_system/no1_design_tokens.md`
    - **待辦內容:** 比對程式碼與規格文件的差異，將規格文件更新至與程式碼一致

- [ ] 將圖示系統從 Expo Vector Icons 遷移至自訂 SVG
    - **程式碼來源:** `SuSuGiGiApp/assets/definitions/IconDefinition.json`
    - **待辦內容:**
        - 建立 `assets/icons/` 資料夾存放 SVG 檔案
        - 調整 `IconDefinition.json` 結構，移除 `library` 與 `glyph` 欄位
        - 新增 `svgPath` 欄位指向對應的 SVG 檔案路徑
        - 更新圖示渲染元件以支援 SVG 載入

---

## 功能實作

- [ ] 實作正式版預設資料初始化邏輯
    - **程式碼位置:** `SuSuGiGiApp/src/database/helpers/seed.ts`
    - **目前狀態:** 暫時呼叫 `mockData.ts` 的 `generateMockData()` 產生測試資料
    - **待辦內容:**
        - 定義 7 個預設類別清單及對應圖示
        - 實作建立 1 個預設帳戶邏輯，使用裝置 Locale 幣別
        - 實作建立 7 個預設類別邏輯
        - 將 `seed.ts` 的 `seedInitialData()` 改為呼叫正式邏輯

- [ ] 實作時區切換支援
    - **UI 調整:** `TransactionEditor` 內的 Date Picker 需支援 `YYYYMMDD HHMMSS` 格式選擇
    - **連動邏輯:** 修改 `Preference` 時區設定時，`HomeScreen` 需即時更新顯示
    - **影響範圍:** 時間區間計算、交易時間顯示

- [ ] 修正所有頁面的 modal & segue

- [ ] 實作 HomeFilter 帳戶選擇的 Universal Logic
    - **背景:** 目前在 merge 或 delete 帳戶後，若導致篩選列表為空，系統不做任何自動選取。
    - **目標:** 定義並實作一個通用的預設選取邏輯（例如：當沒有任何選取時，自動選取排序第一的帳戶，或是顯示特定提示）。
    - **實作位置:** `SuSuGiGiApp/src/contexts/HomeFilterContext.tsx`
    - **相關檔案:**
        - `SuSuGiGiApp/src/contexts/HomeFilterContext.tsx` (核心邏輯)
        - `SuSuGiGiApp/src/screens/Home/HomeFilterScreen.tsx` (篩選器 UI)
        - `SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no2_home_screen.md` (規格定義)

## 待修復問題

- [ ] 修復首頁 Filter 切換 Group By Category 到 Date 的延遲問題
    - **問題描述:** 使用者回報在 `HomeScreen` 切換顯示分組從 `Category` 變成 `Date` 時有明顯延遲
    - **待辦內容:** 檢查 `PeriodDataStore` 的資料處理效率，優化重新分組的邏輯

---

## [Archived] 實作 SearchScreen (2025-12-16)

### Tasks
- [x] 分析需求與現有程式碼 <!-- id: 0 -->
- [x] Create Implementation Plan <!-- id: 1 -->
- [x] Implement SearchScreen UI/UX <!-- id: 2 -->
- [x] Implement Search Logic <!-- id: 3 -->
- [ ] 驗證實作 <!-- id: 4 -->

### Implementation Plan
#### 目標描述
實作 `SearchScreen` 功能，允許使用者透過 `note` 欄位內容搜尋 `Transactions`（交易）與 `Transfers`（轉帳）。搜尋結果將顯示符合的紀錄，並高亮顯示關鍵字。

#### 擬定變更
##### [新功能] SearchScreen
###### [修改] [SearchScreen.tsx](file:///Users/kenchio/Documents/GitHub/SuSuGiGiApp/src/screens/Search/SearchScreen.tsx)
- 實作 UI 佈局，包含頂部導航列（返回按鈕、文字輸入框）與 FlatList。
- 使用 WatermelonDB 查詢 `transactions` 與 `transfers` 資料表以實作搜尋邏輯。
    - 過濾 `note` 包含關鍵字的紀錄（不分大小寫）。
    - 排除已刪除的紀錄。
    - 依日期降冪排序。
- 實作 `renderItem` 以顯示紀錄細節：
    - 圖示（類別圖示或轉帳圖示）。
    - 標題（類別名稱或「轉帳」）。
    - 備註（關鍵字高亮顯示）。
    - 金額與日期。
- 加入導航至 `TransactionEditorScreen` 或 `TransferEditorScreen` 的功能。
- 為搜尋輸入框加入 Debounce 機制（300ms）。

#### 驗證計畫
##### 手動驗證
1.  **導航至搜尋頁面**: 前往首頁 -> 點擊頂部導航列的搜尋圖示。
2.  **空狀態**: 驗證初始顯示「請輸入關鍵字以搜尋交易備註...」訊息。
3.  **搜尋邏輯**:
    -   輸入存在於某些交易備註中的關鍵字。
    -   驗證結果正確顯示。
    -   驗證結果包含 Transactions 與 Transfers（若有）。
    -   驗證結果依日期降冪排序（最新的在最上面）。
4.  **高亮顯示**: 檢查備註欄位中的關鍵字是否被高亮顯示（粗體或不同顏色）。
5.  **無搜尋結果**: 輸入隨機字串，驗證顯示「找不到符合 [關鍵字] 的紀錄」訊息。
6.  **導航**: 點擊搜尋結果，驗證是否開啟正確的編輯頁面。