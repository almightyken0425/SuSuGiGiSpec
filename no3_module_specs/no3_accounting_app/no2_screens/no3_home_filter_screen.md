# 首頁篩選畫面: HomeFilterScreen

## 畫面目標

- **提供:** 首頁報表的篩選與檢視設定
- **允許:** 切換時間粒度、篩選特定帳戶、切換列表分組模式

```text
+---------------------------------------+
| Cancel      Filter Report      Done   |
+---------------------------------------+
| Time Granularity:                     |
| [Day] [Week] [Month] [Year] [All]     |
|                                       |
| Accounts:                             |
| [x] Select All                        |
| [x] Account A                         |
| [ ] Account B                         |
|                                       |
| Group By:                             |
| [Date] [Category]                     |
+---------------------------------------+
```

---

## UI 佈局

- **呈現方式:** Modal Bottom Sheet
- **頂部導航列:**
    - **內部元件:**
        - **取消按鈕:** 行為 關閉 Modal，不儲存
        - **標題:** 內容 篩選報表
        - **完成按鈕:** 行為 關閉 Modal，觸發 `HomeScreen` 重新查詢
- **內容 - 時間粒度:**
    - **UI:** Segmented Control
    - **選項:** 日, 週, 月, 年, 全部
        - **屬性:** 單選
- **內容 - 帳戶篩選:**
    - **UI:** 多選 Checkbox 列表 + 全選
- **內容 - 列表分組:**
    - **UI:** Segmented Control
    - **選項:** 按日期分組, 按類別分組

---

## 核心邏輯

- **篩選邏輯:**
    - **帳戶篩選:** 排除 `deletedOn` 或 `disabledOn` 非 `null` 的帳戶
- **預設值:**
    - **時間粒度:** 當日 daily
    - **帳戶篩選:** 僅選取 `sortOrder` 最高的帳戶
    - **列表分組:** 按類別分組
- **限制:** 不可選擇未來期間

---

## 狀態管理

- **本地狀態:**
    - `selectedTimeGranularity`
    - `selectedAccountIds`
    - `selectedGroupBy`

---

## 導航

- **進入:**
    - **來源:** HomeScreen 頂部 Header 篩選按鈕
- **退出:**
    - **觸發:** 點擊 取消 或 完成
    - **行為:** `navigation.goBack()`
    - **回傳:** (若點擊完成) 篩選條件參數
