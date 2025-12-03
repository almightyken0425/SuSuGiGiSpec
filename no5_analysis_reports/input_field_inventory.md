# 輸入欄位盤點清單 Input Field Inventory

本文件盤點 Accounting App 中所有使用者輸入欄位，並對照 `input_field_limits_strategy.md` 檢視現狀與缺口。

## 1. 文字輸入欄位 (Text Inputs)

需重點評估字數上限與 UI 截斷策略。

| 欄位名稱 | 所屬畫面 | 規格現狀 (Spec) | 策略文件 (Strategy) | 狀態/缺口 |
| :--- | :--- | :--- | :--- | :--- |
| **帳戶名稱** | AccountEditor | 必填, TextInput | 255 chars | ✅ 符合 |
| **類別名稱** | CategoryEditor | 必填, TextInput | 255 chars | ✅ 符合 |
| **交易備註** | TransactionEditor | 選填, TextInput | 1000 chars | ✅ 符合 |
| **轉帳備註** | TransferEditor | 選填, TextInput | 1000 chars | ✅ 符合 |
| **搜尋關鍵字** | SearchScreen | TextInput | 未定義 | ⚠️ 需定義上限 (建議 100) |
| **帳戶描述** | AccountEditor | **❌ 未定義** | 500 chars | 🔴 規格缺漏 (Spec 未包含此欄位) |
| **類別說明** | CategoryEditor | **❌ 未定義** | 500 chars | 🔴 規格缺漏 (Spec 未包含此欄位) |
| **週期交易名稱** | RecurringSetting | **❌ 未定義** | 255 chars | 🔴 規格缺漏 (Spec 未包含此欄位) |
| **標籤名稱** | (未見 Tag 相關畫面) | **❌ 未定義** | 100 chars | 🔴 規格缺漏 (無 Tag 編輯畫面) |

## 2. 特殊格式輸入 (Special Inputs)

需評估格式驗證與鍵盤類型。

| 欄位名稱 | 所屬畫面 | 規格現狀 | 驗證規則 |
| :--- | :--- | :--- | :--- |
| **兌換序號** | RedeemCodeScreen | 12 位數, 自動格式化 | 限制 14 chars (含分隔線), 僅限英數大寫 |
| **電子郵件** | LoginScreen (Google) | Google SDK 處理 | 依賴 Google 驗證 |

## 3. 數值輸入欄位 (Numeric Inputs)

需評估最大數值限制 (Max Value) 與小數位數 (Decimal Places)，而非字元長度。

| 欄位名稱 | 所屬畫面 | 類型 | 備註 |
| :--- | :--- | :--- | :--- |
| **初始餘額** | AccountEditor | 金額 | 需定義最大金額 (e.g., 999,999,999) |
| **交易金額** | TransactionEditor | 金額 | 同上 |
| **轉出金額** | TransferEditor | 金額 | 同上 |
| **轉入金額** | TransferEditor | 金額 | 同上 |
| **匯率** | Account/Transfer Editor | 匯率 | 需定義小數位數 (e.g., 4位) |
| **週期頻率** | RecurringSetting | 數字 (間隔) | 最小 1, 需定義最大值 (e.g., 999) |

## 4. 建議行動

1.  **補齊規格缺口**: 確認 `AccountEditor` 與 `CategoryEditor` 是否需要加入「描述/說明」欄位，或從策略文件中移除。
2.  **定義搜尋限制**: 為 `SearchScreen` 的搜尋框設定合理的字數上限 (建議 100)。
3.  **確認 Tag 功能**: 確認目前版本是否包含標籤 (Tag) 功能，若無則暫時從策略文件中隱藏。
4.  **數值限制策略**: 另立文件或章節定義金額與匯率的輸入限制 (非字元長度，而是數值範圍)。
