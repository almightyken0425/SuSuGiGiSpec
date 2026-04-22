# 類別列表: CategoryListScreen

## 畫面目標

- 提供查看、排序與管理所有收入及支出類別的介面，並作為新增或編輯類別的入口

---

## 線框圖

```text
+--------------------------------+
| < Back      Categories   Merge |
+--------------------------------+
| Expense            [+ Add]     |
| [Icon] Category Name     [=]   |
| [Icon] Category Name     [=]   |
|                                |
| Income             [+ Add]     |
| [Icon] Category Name     [=]   |
| [Icon] Category Name     [=]   |
+--------------------------------+
```

---

## 佈局

### 導覽列

- 返回按鈕
- 類別管理 標題
- 合併按鈕

### 支出區

- 支出 標題
- 新增按鈕
- 類別列表
  - **IF** 列表為空:
    - 顯示尚未建立任何支出類別提示
  - 類別列表項目
    - 圖示
    - 名稱
    - 拖拉圖示
    - **IF** 已停用:
      - 顯示灰色文字與已停用標籤

### 收入區

- 收入 標題
- 新增按鈕
- 類別列表
  - **IF** 列表為空:
    - 顯示尚未建立任何收入類別提示
  - 類別列表項目
    - 圖示
    - 名稱
    - 拖拉圖示
    - **IF** 已停用:
      - 顯示灰色文字與已停用標籤

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
    - 導航至 CategoryEditorScreen

- **點按類別列表項目:**
  - 導航至 CategoryEditorScreen

- **拖拉類別列表項目:**
  - 依所在分區的分類類型呼叫 reorderCategories
