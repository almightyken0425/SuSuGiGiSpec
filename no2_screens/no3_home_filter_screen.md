# 首頁篩選: HomeFilterScreen

## 畫面目標

- 提供首頁報表的篩選設定

---

## 觸發情境

- 由 HomeScreen 以 Modal 呈現

---

## 線框圖

```text
+---------------------------------------+
| [x]           Filter Report           |
+---------------------------------------+
| Time Granularity:                     |
| [Day] [Week] [Month] [Year] [All]    |
|                                       |
| Chart Source:                         |
| [Expense] [Income]                    |
|                                       |
| Group By:                             |
| [Category] [Date]                     |
|                                       |
| Accounts (3 selected)   Select All    |
| [x] Account A                         |
| [x] Account B                         |
| [ ] Account C                         |
+---------------------------------------+
```

---

## 佈局

### 導覽列

- 篩選報表標題
- 關閉按鈕

### 篩選設定

- 時間粒度 Segmented Control
  - 日、週、月、年、全部
- 圖表來源 Segmented Control
  - 支出、收入
- 列表分組 Segmented Control
  - 類別分組、日期分組
- 帳戶篩選
  - 已選帳戶數量標題與全選/取消全選切換文字按鈕
  - Checkbox 列表，列出所有啟用中的帳戶
  - **IF** 僅剩一個帳戶被選取:
    - 該帳戶列為不可點按狀態，半透明顯示
  - **IF** 無可用帳戶:
    - 顯示無帳戶提示文字

---

## 互動

- **變更任一篩選條件:**
  - HomeScreen 報表即時更新

- **點按全選/取消全選切換文字按鈕:**
  - **IF** 目前為全選狀態:
    - 取消全選
  - **ELSE:**
    - 全選所有帳戶

- **點按關閉按鈕:**
  - 關閉 Modal

- **向下滑動:**
  - 關閉 Modal
