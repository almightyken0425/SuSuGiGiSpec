# 轉帳編輯器: TransferEditorScreen

## 畫面目標

- 提供新增與編輯轉帳記錄的介面，並作為建立定期轉帳排程的入口

---

## 線框圖

```text
+--------------------------------+
| Cancel    Transfer      Done   |
+--------------------------------+
|  Date: Oct 25, 2024            |
+--------------------------------+
| From: [Account Selector]       |
| To:   [Account Selector]       |
| Note: [Note Input]             |
+--------------------------------+
| Amount From: [ $ Input ] [Recur]|
| Rate & Arrow if Cross-Currency |
| Amount To:   [ $ Input ]       |
|                                |
|           [Delete]             |
+--------------------------------+
```

---

## 佈局

### Header

- 取消按鈕
- 轉帳 標題
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

### 帳戶選擇區

- 轉出帳戶選擇器
- 轉入帳戶選擇器
- 備註輸入框

### 金額輸入區

- 轉出金額輸入框
- 定期轉帳按鈕
- **IF** 跨幣別轉帳:
  - 隱含匯率與箭頭
  - 轉入金額輸入框

### 操作區

- **IF** 編輯模式:
  - 刪除按鈕

---

## 互動

- **點按取消按鈕:**
  - 返回上一頁

- **點按日期標題列:**
  - 展開或收合日期時間選擇器

- **點按定期轉帳按鈕:**
  - **IF** = Tier0:
    - 導航至 PaywallScreen
  - **IF** > Tier0:
    - 導航至 RecurringSettingScreen

- **點按完成按鈕:**
  - **IF** 定期轉帳:
    - **IF** 新增模式:
      - 呼叫 createSchedule
    - **IF** 編輯模式:
      - 呼叫 updateSchedule
  - **IF** 一般轉帳:
    - **IF** 新增模式:
      - 呼叫 createTransfer
    - **IF** 編輯模式:
      - 呼叫 updateTransfer
  - **IF** 操作成功:
    - 返回上一頁
  - **IF** 操作失敗:
    - 顯示錯誤提示

- **點按刪除按鈕:**
  - **IF** 定期轉帳:
    - 呼叫 deleteSchedule
  - **IF** 一般轉帳:
    - 呼叫 deleteTransfer
  - **IF** 操作成功:
    - 返回上一頁
  - **IF** 操作失敗:
    - 顯示錯誤提示
