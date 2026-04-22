# 分類核心邏輯: CategoryLogic

## createCategory 建立分類

- **輸入:**
  - 分類資料
- **寫入 Category:**
  - **執行:**
    - 新增一筆記錄至 `Categories` 表

## updateCategory 更新分類

- **輸入:**
  - 分類資料
- **更新 Category:**
  - **執行:**
    - 更新 `Categories` 表中的記錄

## deleteCategory 刪除分類

- **輸入:**
  - 分類識別碼
- **軟刪除 Category:**
  - **執行:**
    - 更新 `Categories` 表
- **串聯軟刪除 Transaction:**
  - **執行:**
    - 更新該分類所屬的 `Transactions` 表記錄

## reorderCategories 重排分類

- **輸入:**
  - 分類類型
  - 有序的分類識別碼清單
- **更新 Category:**
  - **執行:**
    - 批次更新 `Categories` 表的排序欄位
