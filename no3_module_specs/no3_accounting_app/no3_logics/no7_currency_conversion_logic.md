# 匯率轉換邏輯: CurrencyConversionLogic

## 邏輯目標

- **定義:** 系統如何處理多幣別之間的金額轉換與報表彙整
- **確保:** 報表數據的一致性與可預測性
- **限制:** 避免因多重路徑轉換 Multi-path conversion 造成的計算誤差

---

## 核心規則

### 1. 基礎貨幣規則 Base Currency Rule

- **定義:** 所有全域報表 Global Reports 與總資產計算，**必須** 統一轉換為使用者的 **基礎貨幣 Base Currency**。
- **來源:** `Settings.baseCurrencyId`

### 2. 直接匯率要求 Direct Rate Requirement

- **規則:** 系統僅使用 **直接對應** 基礎貨幣的匯率進行轉換。
- **禁止事項:** 嚴格禁止 **多重跳轉 Multi-hop** 或 **遞迴查找 Recursive Lookup**。
- **範例:**
    - **情境:** 基礎貨幣為 TWD。交易貨幣為 USD。
    - **合法轉換:** 讀取 `USD -> TWD` 的匯率。
    - **非法轉換:** 若缺少 `USD -> TWD`，**禁止** 嘗試 `USD -> JPY -> TWD` 的路徑。
- **例外處理:**
    - **IF** 缺少直接匯率:
        - 該金額在報表中視為無法計算，或依各畫面定義處理。
        - **不** 自動推算或是使用近似值。

### 3. 匯率選擇策略 Rate Selection Strategy

- **基準時間:** 以交易發生的日期 `transactionDate` 為準。
- **查找邏輯:**
    - 使用 `CurrencyRates` 表中，`rateDate` 小於等於 `transactionDate` 的 **最新一筆** 紀錄。
    - **SQL 概念:** `SELECT * FROM CurrencyRates WHERE currencyFrom = 'USD' AND currencyTo = 'TWD' AND rateDate <= transactionDate ORDER BY rateDate DESC LIMIT 1`

---

## 轉帳隱含匯率 Transfer Implied Rate

- **定義:** 在 `Transfers` 表中 `impliedRateScaled` 欄位所紀錄的匯率。
- **用途:**
    - 用於顯示該筆轉帳交易在當下的換匯比例。
    - **作為全域匯率:** 轉帳時**會**自動將此隱含匯率寫入 `CurrencyRates` 表。
- **限制:**
    - 雖然匯率被寫入了，但報表計算仍受「直接匯率要求」限制。
    - **範例:** 若轉帳產生了 `USD -> JPY` 的匯率紀錄，但用戶的基礎貨幣是 `TWD`，這筆 `USD -> JPY` 的紀錄**不會**被用於計算 `USD` 資產在報表上的 `TWD` 價值，因為不支援多重跳轉。
    - **有效場景:** 若轉帳剛好是 `USD -> TWD` 即 Base，則此自動產生的紀錄**會**被報表採用。
