# 圖示選擇器畫面: IconPickerScreen

## 畫面目標

- **提供:** 圖示網格介面供使用者選擇
- **返回:** 所選圖示的 ID

```text
+--------------------------------+
| <           Select Icon        |
+--------------------------------+
| [Icon] [Icon] [Icon] [Icon]    |
| [Icon] [Icon] [Icon] [Icon]    |
| [Icon] [Icon] [Icon] [Icon]    |
| [Icon] [Icon] [Icon] [Icon]    |
|                                |
|                                |
+--------------------------------+
```

---

## UI 佈局

- **頂部導航列:**
    - `返回按鈕`(圖示 <)
    - `標題` 選擇圖示
- **圖示網格:**
    - **UI:** Grid 佈局顯示所有可用圖示

---

## 核心邏輯

- **資料來源:**
    - **讀取:** `IconDefinition.json`
    - **過濾:** 依 `types` 相符
        - types 包含 expense, income, account, general
- **互動:**
    - **點選圖示:**
        - **行為:** 返回 `id` 並關閉畫面

---

## 導航

- **進入:**
    - **來源:** AccountEditorScreen 或 CategoryEditorScreen
    - **必要參數:** type 用於過濾圖示
- **退出:**
    - **觸發:** 點選圖示
    - **導航:** 返回上一頁
    - **回傳:** 所選圖示的 `id`