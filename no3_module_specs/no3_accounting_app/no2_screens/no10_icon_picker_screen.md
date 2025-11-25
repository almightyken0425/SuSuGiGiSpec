# 圖標選擇器規格: IconPickerScreen

## 畫面目標

- **提供:** 一個圖標網格介面供使用者選擇
- **返回:** 所選圖標的 ID

## UI 佈局

- **UI:** 顯示圖標網格

---

## 核心邏輯

- **資料來源:**
    - **讀取:** `IconDefinition.json`
- **過濾:**
    - **條件:** 依 `types` 相符
    - **備註:** types 包含 expense, income, account, general
- **互動:**
    - **觸發:** 點選圖標
    - **行為:** 返回 `id`

---

## 導航

- **進入:**
    - **來源:** AccountEditorScreen, CategoryEditorScreen
- **退出:**
    - **觸發:** 點選圖標
    - **行為:** `navigation.goBack()` 並返回 `id`