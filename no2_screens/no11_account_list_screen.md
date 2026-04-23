# 帳戶列表: AccountListScreen

## 畫面目標

- 提供查看、排序與管理所有帳戶的介面，並作為新增或編輯帳戶的入口

---

## 線框圖

```text
+--------------------------------+
| < Back      Accounts     Merge |
+--------------------------------+
| My Accounts        [+ Add]     |
| [Icon] Account Name      [=]   |
|        Type                    |
| [Icon] Account Name      [=]   |
|        Type                    |
+--------------------------------+
```

---

## 佈局

### 導覽列

- 返回按鈕
- 帳戶管理 標題
- 合併按鈕

### 帳戶區

- 我的帳戶 標題
- 新增按鈕
- 帳戶列表
  - **IF** 列表為空:
    - 顯示尚未建立任何帳戶提示
  - 帳戶列表項目
    - 圖示
    - 名稱
    - 帳戶類型
    - 拖拉圖示
    - **IF** 已停用:
      - 顯示灰色文字

---

## 互動

- **點按返回按鈕:**
  - 返回上一頁

- **點按合併按鈕:**
  - 以帳戶模式導航至 MergeEditorScreen

- **點按新增按鈕:**
  - 呼叫 canUserPerformAction，動作識別碼 createAccount
  - **IF** 回傳禁止:
    - 導航至 PaywallScreen
  - **ELSE:**
    - 導航至 AccountEditorScreen

- **點按帳戶列表項目:**
  - 導航至 AccountEditorScreen

- **拖拉帳戶列表項目:**
  - 呼叫 reorderAccounts
