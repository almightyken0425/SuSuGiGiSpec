# 交易編輯器: TransactionEditorScreen

## 畫面目標

- 提供新增與編輯收入或支出交易的介面，並作為建立定期收支排程的入口

---

## 線框圖

```text
+--------------------------------+
| Cancel      Title       Done   |
+--------------------------------+
|  Date: Oct 25, 2024            |
+--------------------------------+
| [ $ Amount Input    ] [Recur]  |
|                                |
| [Category Selector]            |
| [Account Selector]             |
| [Note Input]                   |
|                                |
|           [Delete]             |
+--------------------------------+
```

---

## 佈局

### Header

- 取消按鈕
- 標題
  - **IF** 支出:
    - 支出
  - **IF** 收入:
    - 收入
- 完成按鈕
  - **IF** 必填欄位未填妥:
    - 不可點按

### 日期選擇區

- 日期標題列
  - **IF** 收合:
    - 顯示日期與時間文字
  - **IF** 展開:
    - 日曆選擇器
    - 時間選擇器

### 欄位區

- 類別選擇器
- 帳戶選擇器
- 備註輸入框

### 金額輸入區

- 金額輸入框
- 定期交易按鈕

### 操作區

- **IF** 編輯模式:
  - 刪除按鈕

---

## 互動

- **點按取消按鈕:**
  - 返回上一頁

- **點按日期標題列:**
  - 展開或收合日期時間選擇器

- **點按定期交易按鈕:**
  - **IF** 為 LEVEL_0:
    - 導航至 PaywallScreen
  - **ELSE:**
    - 導航至 RecurringSettingScreen

- **點按完成按鈕:**
  - **IF** 定期交易:
    - **IF** 新增模式:
      - 呼叫 createSchedule
    - **IF** 編輯模式:
      - 呼叫 deleteTransaction
      - 呼叫 createSchedule
  - **IF** 一般交易:
    - **IF** 新增模式:
      - 呼叫 createTransaction
    - **IF** 編輯模式:
      - 呼叫 updateTransaction
  - **IF** 操作成功:
    - 返回上一頁
  - **IF** 操作失敗:
    - 顯示錯誤提示

- **點按刪除按鈕:**
  - **IF** 定期交易:
    - 呼叫 deleteSchedule
  - **IF** 一般交易:
    - 呼叫 deleteTransaction
  - **IF** 操作成功:
    - 返回上一頁
  - **IF** 操作失敗:
    - 顯示錯誤提示
