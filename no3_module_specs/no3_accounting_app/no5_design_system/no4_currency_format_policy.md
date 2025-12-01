# 金額顯示規範

---

## 核心策略

- **原則:** 顯示幣別符號 (Symbol) 以符合使用者直覺，金額格式跟隨系統語系 Locale Aware
- **技術實作:** 封裝全域函式 formatAppCurrency
- **模式:** 支援 3 種標準格式 Standard, Compact, ExchangeRate

---

## 支援格式

### Standard

- **用途:** 列表、餘額、詳情、編輯器顯示
- **範例:** NT$1,234.00 或 $10.50
- **Intl 設定:**
    - style: currency
    - currency: [ISO Code]
    - currencyDisplay: symbol
    - minimumFractionDigits: 2 (或依幣別定義)
    - maximumFractionDigits: 2 (或依幣別定義)

### Compact

- **用途:** 圖表 (Pie Chart)、空間極度受限處
- **範例:** NT$1.2k 或 $5M
- **Intl 設定:**
    - style: currency
    - currency: [ISO Code]
    - currencyDisplay: symbol
    - notation: compact
    - compactDisplay: short

### Exchange Rate

- **用途:** 匯率列表、跨幣別轉帳匯率
- **範例:** 1 USD ≈ 30.5000 TWD
- **邏輯:** 顯示 1 單位來源貨幣等於多少目標貨幣
- **Intl 設定 (目標金額):**
    - style: decimal
    - minimumFractionDigits: 0
    - maximumFractionDigits: 6 (確保精確度)

---

**文件結束**
