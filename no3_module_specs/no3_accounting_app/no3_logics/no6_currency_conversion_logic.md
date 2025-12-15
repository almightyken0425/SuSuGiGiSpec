# 匯率轉換邏輯: CurrencyConversionLogic

## 邏輯目標

- **定義:** 說明系統如何處理多幣別之間的金額轉換與報表彙整
- **目的:** 確保使用者在不同介面看到的金額一致且符合直覺

---

## 核心規則

### 基礎貨幣 Base Currency

- **定義:** 總資產與全域報表統一使用的計價單位。
- **來源:** 設定中的基礎貨幣。

### 匯率來源與更新

- **來源:** 取自匯率設定列表。
- **範圍:** 系統僅讀取屬於當前使用者的匯率設定。
- **更新:** 當匯率變更或新增轉帳時，系統會即時重新計算所有相關金額，無需手動重新整理。

### 匯率使用規則

- **策略:** 系統一律使用 **最新的交易對** 進行換算。
- **查找邏輯:**
    - 系統將 原始幣別與基礎幣別 的所有交易對，包含正向與反向，合併並依時間倒序排列。
    - **唯一基準:** 僅採用 **時間最新** 的那一筆匯率紀錄。
- **處理方式:**
    - **若最新紀錄為正向:** 原始幣別 換算至 基礎幣別，則直接使用該匯率。
    - **若最新紀錄為反向:** 基礎幣別 換算至 原始幣別，則取匯率倒數進行換算。
    - **無有效匯率:** 若查無任何紀錄，系統將顯示原始金額。

### 轉帳與匯率連動

- **自動建立:** 當使用者建立跨幣別轉帳時，系統會自動根據輸入的轉出與轉入金額，計算並建立一筆當下的匯率紀錄。
- **影響:** 這筆自動建立的匯率，等同於使用者手動新增的匯率，會立即影響全域的資產換算結果。

---

## 轉帳紀錄顯示規則 Transfer Display Rules

- **說明:** 本表詳列在不同 **錢包篩選 (Filter)** 情境下，系統應如何呈現轉帳紀錄。
- **符號:**
    - **Amount From:** 轉出金額
    - **Amount To:** 轉入金額
    - **Base:** 基礎幣別 (假設為 TWD)

### 1. 單選錢包情境 (Single Wallet Filter)

| 當前篩選 Filter | 交易情境 Transfer Pair | 命中角色 Role | 顯示類型 Type | 取用欄位 Field | 邏輯與幣別 Logic |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **USD** | **USD -> TWD** (轉出) | 轉出方 | 支出 Expense | Amount From | **USD** 不轉換 |
| **USD** | **TWD -> USD** (轉入) | 轉入方 | 收入 Income | Amount To | **USD** 不轉換 |
| **USD** | **USD -> JPY** (轉出) | 轉出方 | 支出 Expense | Amount From | **USD** 不轉換 |
| **USD** | **JPY -> USD** (轉入) | 轉入方 | 收入 Income | Amount To | **USD** 不轉換 |

### 2. 多選錢包情境 (Multi-Wallet Filter)
- **假設:** 使用者同時勾選了 **USD** 與 **JPY** 兩個錢包。

| 當前篩選 Filter | 交易情境 Transfer Pair | 命中角色 Role | 顯示類型 Type | 取用欄位 Field | 邏輯與幣別 Logic |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **USD & JPY** | **USD -> TWD** (轉出至未選) | 轉出方 (USD) | 支出 Expense | Amount From | **USD** 不轉換 |
| **USD & JPY** | **TWD -> JPY** (自未選轉入) | 轉入方 (JPY) | 收入 Income | Amount To | **JPY** 不轉換 |
| **USD & JPY** | **USD -> JPY** (內部互轉) | 轉出方 (USD) | 支出 Expense | Amount From | **USD** 不轉換 (列表呈現第1筆) |
| **USD & JPY** | **USD -> JPY** (內部互轉) | 轉入方 (JPY) | 收入 Income | Amount To | **JPY** 不轉換 (列表呈現第2筆) |

### 3. 全域情境 (Global / All Wallets)

| 當前篩選 Filter | 交易情境 Transfer Pair | 命中角色 Role | 顯示類型 Type | 取用欄位 Field | 邏輯與幣別 Logic |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **全域 Global** | **USD -> TWD** | 總覽 | 支出 Expense | Amount From | 轉為 **Base (TWD)** |
| **全域 Global** | **TWD -> USD** | 總覽 | 支出 Expense | Amount From | 轉為 **Base (TWD)** |
| **全域 Global** | **USD -> JPY** | 總覽 | 支出 Expense | Amount From | 轉為 **Base (TWD)** |
| **全域 Global** | **TWD -> TWD** | 總覽 | 支出 Expense | Amount From | **TWD** 不轉換 |
| **全域 Global** | **USD -> USD** | 總覽 | 支出 Expense | Amount From | 轉為 **Base (TWD)** |

- **全域補充:** 在全域視角下，轉帳通常視為一種「流動」，為了統計方便與版面一致，系統統一呈現 **轉出方** 的視角，並將金額換算為 **基礎幣別**。
