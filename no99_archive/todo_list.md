# 待辦事項清單

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


- [ ] 實作 HomeFilter 帳戶選擇的 Universal Logic
    - **背景:** 目前在 merge 或 delete 帳戶後，若導致篩選列表為空，系統不做任何自動選取。
    - **目標:** 定義並實作一個通用的預設選取邏輯（例如：當沒有任何選取時，自動選取排序第一的帳戶，或是顯示特定提示）。
    - **實作位置:** `SuSuGiGiApp/src/contexts/HomeFilterContext.tsx`
    - **相關檔案:**
        - `SuSuGiGiApp/src/contexts/HomeFilterContext.tsx` (核心邏輯)
        - `SuSuGiGiApp/src/screens/Home/HomeFilterScreen.tsx` (篩選器 UI)
        - `SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no2_home_screen.md` (規格定義)

幣別要可以選擇報表顯示位數