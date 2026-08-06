# 類別核心邏輯: CategoryLogic

## createCategory 建立類別

- **輸入:**
  - 類別資料，含 type、name、iconId、disabledOn
- **IF** 類別名稱去除前後空白後長度超過名稱長度上限:
  - **回傳:** 驗證失敗，原因為名稱過長
  - 作為畫面即時長度上限的後備，涵蓋繞過畫面的匯入路徑
- **寫入 Category:**
  - **條件:**
    - `type` 為必填，須為 `expense` 或 `income`
    - `iconId` 必須引用 `tags` 含 `category` 的 `IconDefinitions` 記錄
  - **執行:**
    - 新增一筆記錄至 `Categories` 表

## updateCategory 更新類別

- **輸入:**
  - 類別識別碼、類別資料
- **IF** 類別名稱去除前後空白後長度超過名稱長度上限:
  - **回傳:** 驗證失敗，原因為名稱過長
  - 作為畫面即時長度上限的後備，涵蓋繞過畫面的匯入路徑
- **更新 Category:**
  - **欄位:**
    - `name`、`iconId`、`disabledOn` 可更新
  - **行為:**
    - `type` 不可更新
  - **理由:**
    - 避免改變已建立類別的類型，導致歷史交易分類錯亂
  - **執行:**
    - 更新 `Categories` 表中的記錄

## deleteCategory 刪除類別

- **輸入:**
  - 類別識別碼
- **軟刪除 Category:**
  - **執行:**
    - 更新 `Categories` 表
- **串聯軟刪除 Transaction:**
  - **執行:**
    - 更新該類別所屬的 `Transactions` 表記錄

## reorderCategories 重排類別

- 重排單一類型分區內的類別順序，分區歸屬由清單成員決定
- **輸入:**
  - 有序的類別識別碼清單
- **更新 Category:**
  - **執行:**
    - 批次更新 `Categories` 表的排序欄位
