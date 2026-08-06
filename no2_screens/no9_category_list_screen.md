# 類別列表: CategoryListScreen

## 畫面目標

- 提供查看、排序與管理所有收入及支出類別的介面，並作為新增或編輯類別的入口

---

## 線框圖

```text
+--------------------------------+
| <      Categories  [Merge][+]  |
+--------------------------------+
| [Icon] Category Name           |
| [Icon] Category Name           |
|                                |
| [Icon] Category Name           |
| [Icon] Category Name           |
+--------------------------------+
```

---

## 佈局

### 導覽列

- Header 模式: A
- 返回按鈕
- 類別管理 標題
- 合併按鈕
- 新增按鈕

### 支出區

- List 模式: D
- 類別列表
  - 類別列表項目
    - 圖示
    - 名稱
    - **IF** 已停用:
      - 以停用樣式呈現

### 收入區

- List 模式: D
- 類別列表
  - 類別列表項目
    - 圖示
    - 名稱
    - **IF** 已停用:
      - 以停用樣式呈現

---

## 互動

- **點按返回按鈕:**
  - 返回上一頁

- **點按合併按鈕:**
  - 以類別模式導航至 MergeEditorScreen

- **點按新增按鈕:**
  - 呼叫 canUserPerformAction，動作識別碼 createCategory
  - **IF** 回傳禁止:
    - 導航至 PaywallScreen
  - **ELSE:**
    - 導航至 CategoryEditorScreen，不帶類別類型參數
    - 類別類型由 CategoryEditorScreen 的類別類型選擇器預設為支出

- **點按類別列表項目:**
  - 導航至 CategoryEditorScreen

- **拖拉類別列表項目:**
  - 以所在分區的有序類別清單呼叫 reorderCategories
