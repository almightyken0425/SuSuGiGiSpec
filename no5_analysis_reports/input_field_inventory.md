# 輸入欄位盤點清單 Input Field Inventory

本文件盤點 Accounting App 中所有使用者輸入欄位，並對照 `input_field_limits_strategy.md` 檢視現狀與缺口。

## 1. 文字輸入欄位 (Text Inputs)

| 欄位名稱 | 畫面規格現狀 (Screen Spec) | 策略文件現狀 (Strategy Doc) | 狀態 |
| :--- | :--- | :--- | :--- |
| **帳戶名稱** | ✅ **有** (AccountEditor) | ✅ **有** (上限 255) | **一致** |
| **類別名稱** | ✅ **有** (CategoryEditor) | ✅ **有** (上限 255) | **一致** |
| **交易備註** | ✅ **有** (TransactionEditor) | ✅ **有** (上限 255) | **一致** |
| **轉帳備註** | ✅ **有** (TransferEditor) | ✅ **有** (上限 255) | **一致** |
| **搜尋關鍵字** | ✅ **有** (SearchScreen) | ✅ **有** (上限 255) | **一致** |

*(已移除: 帳戶描述、類別說明、週期交易名稱、標籤名稱)*

## 2. 數值輸入欄位 (Numeric Inputs)

需評估最大數值限制 (Max Value) 與小數位數 (Decimal Places)。

| 欄位名稱 | 所屬畫面 | 類型 | 備註 |
| :--- | :--- | :--- | :--- |
| **初始餘額** | AccountEditor | 金額 | Max: 999,999,999, Decimal: 2 |
| **交易金額** | TransactionEditor | 金額 | Max: 999,999,999, Decimal: 2 |
| **轉出金額** | TransferEditor | 金額 | Max: 999,999,999, Decimal: 2 |
| **轉入金額** | TransferEditor | 金額 | Max: 999,999,999, Decimal: 2 |
| **匯率** | Account/Transfer Editor | 匯率 | Decimal: 4 |
| **週期頻率** | RecurringSetting | 數字 (間隔) | 整數 |

*(特殊格式輸入如兌換序號、Email 無需定義策略)*
