# 貨幣格式列表: CurrencyListScreen

## 畫面目標

- 提供選擇要調整顯示格式之貨幣的介面

---

## 線框圖

```text
+--------------------------------+
| < Back      Currencies         |
+--------------------------------+
| [ Search Currency... ]         |
+--------------------------------+
| USD  United States Dollar   >  |
| TWD  New Taiwan Dollar      >  |
| JPY  Japanese Yen           >  |
| ...                            |
+--------------------------------+
```

---

## 佈局

### 導覽列

- 返回 按鈕
- 貨幣格式列表 標題

### 搜尋列

- 貨幣關鍵字輸入框

### 貨幣列表

- 貨幣項目
  - `alphabeticCode`
  - `name`
  - 右側導航箭頭

---

## 互動

- **點按返回按鈕:**
  - 返回上一頁

- **輸入搜尋文字:**
  - 依貨幣代碼或名稱即時篩選列表

- **點按貨幣項目:**
  - 導航至 CurrencyDetailConfigScreen
