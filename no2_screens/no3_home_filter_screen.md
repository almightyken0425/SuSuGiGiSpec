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
|             Filter Report       Done  |
+---------------------------------------+
| Time Granularity:                     |
| [Day] [Week] [Month] [Year] [All]     |
|                                       |
| Chart Source:                         |
| [Expense] [Income]                    |
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

## 佈局

### 導覽列

- 篩選報表 標題
- 完成按鈕

### 篩選設定

- 時間粒度 Segmented Control
  - 日、週、月、年、全部
- 圖表來源 Segmented Control
  - 支出、收入
- 帳戶篩選 Checkbox 列表
  - 全選
  - 帳戶名稱
- 列表分組 Segmented Control
  - 日期分組、類別分組

---

## 互動

- **變更任一篩選條件:**
  - HomeScreen 報表即時更新

- **點按完成按鈕:**
  - 關閉 Modal

- **向下滑動:**
  - 關閉 Modal
