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
- [ ] 修復所有 `timeZoneOffsetInMinutes` 棄用警告
    - **問題:** `DateTimePicker` 的 `timeZoneOffsetInMinutes` 屬性已棄用，即將移除。
    - **解法:** 改用 `timeZoneName` 屬性。
    - **待辦內容:** 檢查並更新專案中所有使用 `DateTimePicker` 的頁面。