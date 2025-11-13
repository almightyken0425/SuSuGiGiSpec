# 資料結構

_(本文件定義 App 的核心資料模型與靜態定義)_

## 使用者自訂資料結構 (未來 DB Table)

_(現況: 這些是 App 的核心動態資料，將儲存在 Firestore 中並與 UserId 關聯。)_

### 帳戶 (Accounts)

- **欄位:**
    
    - `id`: String (UUID/GUID) - Primary Key
        
    - `userId`: String (Email) - Foreign Key (Users), Not Null, Index
        
    - `name`: String - Not Null
        
    - `icon`: Number - Foreign Key (IconDefinitions)
        
    - `initialBalanceCents`: BigInt - Not Null, Default 0
        
    - `currencyId`: Number - Foreign Key (Currencies), Not Null
        
    - `standardAccountTypeId`: Number | Null - Foreign Key (StandardAccountTypes), Nullable
        
    - `sortOrder`: Number - Not Null, Default 0 (用於使用者自訂排序，數字越小越前面)
        
    - `createdOn`: Number (Unix Timestamp ms) - Not Null (資料建立的系統時間)
        
    - `updatedOn`: Number (Unix Timestamp ms) - Not Null (資料最後更新時間，同步依據)
        
    - `disabledOn`: Number | Null (Unix Timestamp ms) - Nullable
        
    - `deletedOn`: Number | Null (Unix Timestamp ms) - Nullable, Index (用於軟刪除)
        

### 類別 (Categories)

- **欄位:**
    
    - `id`: String (UUID/GUID) - Primary Key
        
    - `userId`: String (Email) - Foreign Key (Users), Not Null, Index
        
    - `name`: String - Not Null
        
    - `icon`: Number - Foreign Key (IconDefinitions)
        
    - `categoryType`: Number - Not Null (0: 收入, 1: 支出)
        
    - `standardCategoryId`: Number | Null - Foreign Key (StandardCategory), Nullable (關聯到標準類別)
        
    - `sortOrder`: Number - Not Null, Default 0 (用於使用者自訂排序，數字越小越前面)
        
    - `createdOn`: Number (Unix Timestamp ms) - Not Null
        
    - `updatedOn`: Number (Unix Timestamp ms) - Not Null (資料最後更新時間，同步依據)
        
    - `disabledOn`: Number | Null (Unix Timestamp ms) - Nullable
        
    - `deletedOn`: Number | Null (Unix Timestamp ms) - Nullable, Index
                

### 交易紀錄 (Transactions)

- **欄位:**
    
    - `id`: String (UUID/GUID) - Primary Key
        
    - `userId`: String (Email) - Foreign Key (Users), Not Null, Index
        
    - `categoryId`: String - Foreign Key (Categories), Not Null
        
    - `accountId`: String - Foreign Key (Accounts), Not Null
        
    - `amountCents`: BigInt - Not Null (支出為正值，收入也為正值，由 categoryType 決定收支)
        
    - `transactionDate`: Number (Unix Timestamp ms) - Not Null (交易發生日，由使用者選擇，用於報表統計)
        
    - `createdOn`: Number (Unix Timestamp ms) - Not Null (資料建立的系統時間)
        
    - `updatedOn`: Number (Unix Timestamp ms) - Not Null (資料最後更新時間，同步依據)
        
    - `note`: String | Null - Nullable (用於搜尋)
        
    - `scheduleId`: String | Null - Foreign Key (Schedules), Nullable (標記此筆為定期交易產生)
        
    - `scheduleInstanceDate`: Number | Null (Unix Timestamp ms) - Nullable (標記此筆交易對應的排程日期錨點，此欄位永不應被使用者修改，僅供系統檢查重複用)
        
    - `deletedOn`: Number | Null (Unix Timestamp ms) - Nullable, Index
        

### 轉帳紀錄 (Transfers)

- **欄位:**
    
    - `id`: String (UUID/GUID) - Primary Key
        
    - `userId`: String (Email) - Foreign Key (Users), Not Null, Index
        
    - `accountFromId`: String - Foreign Key (Accounts), Not Null
        
    - `accountToId`: String - Foreign Key (Accounts), Not Null
        
    - `amountFromCents`: BigInt - Not Null (轉出帳戶的金額，以該帳戶幣別計)
        
    - `amountToCents`: BigInt - Not Null (轉入帳戶的金額，以該帳戶幣別計)
        
    - `impliedRateScaled`: BigInt - Not Null- Nullable (儲存匯率 * 1,000,000 後的整數)
        
    - `transactionDate`: Number (Unix Timestamp ms) - Not Null (轉帳發生日，用於報表篩選)
        
    - `createdOn`: Number (Unix Timestamp ms) - Not Null (資料建立的系統時間)
        
    - `updatedOn`: Number (Unix Timestamp ms) - Not Null (資料最後更新時間，同步依據)
        
    - `note`: String | Null - Nullable (用於搜尋)
        
    - `scheduleId`: String | Null - Foreign Key (Schedules), Nullable
        
    - `scheduleInstanceDate`: Number | Null (Unix Timestamp ms) - Nullable
        
    - `deletedOn`: Number | Null (Unix Timestamp ms) - Nullable, Index
                

### 貨幣匯率 (CurrencyRates)

- **欄位:**
    
    - `id`: String (UUID/GUID) - Primary Key
        
    - `userId`: String (Email) - Foreign Key (Users), Not Null (因為是手動輸入)
        
    - `currencyFromId`: Number - Foreign Key (Currencies), Not Null
        
    - `currencyToId`: Number - Foreign Key (Currencies), Not Null
        
    - `rateCents`: BigInt - Not Null (儲存匯率 * 1,000,000 後的整數)
        
    - `rateDate`: Number (Unix Timestamp ms) - Not Null (匯率生效日期，儲存該日 00:00:00 UTC)
        
    - `createdOn`: Number (Unix Timestamp ms) - Not Null
        
    - `updatedOn`: Number (Unix Timestamp ms) - Not Null (資料最後更新時間，同步依據)
        

### 定期交易排程 (Schedules)

- **欄位:**
    
    - `id`: String (UUID/GUID) - Primary Key
        
    - `userId`: String (Email) - Foreign Key (Users), Not Null
        
    - `scheduleType`: String - Not Null (e.g., 'daily', 'weekly', 'monthly', 'yearly')
        
    - `startOn`: Number (Unix Timestamp ms) - Not Null (排程開始日期，基於使用者時區的 00:00:00 轉存 UTC)
        
    - `endOn`: Number | Null (Unix Timestamp ms) - Nullable (排程結束日期)
        
    - `isTransfer`: Boolean - Not Null (true: 轉帳排程, false: 收支排程)
        
    - `templateAmountCents`: BigInt | Null (收支金額)
        
    - `templateCategoryId`: String | Null (收支類別 ID)
        
    - `templateAccountId`: String | Null (收支帳戶 ID)
        
    - `templateAmountFromCents`: BigInt | Null (轉出金額)
        
    - `templateAccountFromId`: String | Null (轉出帳戶 ID)
        
    - `templateAmountToCents`: BigInt | Null (轉入金額)
        
    - `templateAccountToId`: String | Null (轉入帳戶 ID)
        
    - `templateNote`: String | Null
        
    - `createdOn`: Number (Unix Timestamp ms) - Not Null
        
    - `updatedOn`: Number (Unix Timestamp ms) - Not Null (資料最後更新時間，同步依據)
        
    - `deletedOn`: Number | Null (Unix Timestamp ms) - Nullable, Index
        

### 使用者設定 (Settings)

- **說明:** 用於儲存使用者特定的偏好設定，採用 Key-Value 結構。
    
- **欄位:**
    
    - `id`: String (UUID/GUID) - Primary Key
        
    - `userId`: String (Email) - Foreign Key (Users), Not Null
        
    - `settingKey`: String - Not Null (e.g., 'baseCurrencyId', 'timeZone', 'language', 'isPremiumUser', 'lastRecurringCheckDate')
        
    - `settingValue`: String - Not Null (儲存 JSON 字串或簡單值)
        
    - `createdOn`: Number (Unix Timestamp ms) - Not Null
        
    - `updatedOn`: Number (Unix Timestamp ms) - Not Null (資料最後更新時間，同步依據)
        

## App 標準定義資料 (Definitions)

_(現況: 這些是 App 內建的靜態參考資料，將打包在 App 中或從遠端載入。)_

### 標準收支類別 (StandardCategory)

- **說明:** 統一管理標準的收支大類，使用者自訂類別需映射到此。
- **檔案:** `assets/definitions/StandardCategory.json`
- **欄位 (fields):**
    - `id`: `Number`
    - `categoryType`: `Number` - (0: 收入, 1: 支出)
    - `translationKey`: `String`
    - `defaultName`: `String`
    

### 標準帳戶類型 (StandardAccountType)

- **說明:** 定義帳戶的金融本質分類 (支付、投資、貸款、其他)。
- **檔案:** `assets/definitions/StandardAccountType.json`
- **欄位 (fields):**
    - `id`: `Number`
    - `translationKey`: `String`
    - `defaultName`: `String`
    

### 圖標定義 (IconDefinition)

- **說明:** 定義 App 內預選的 Feather 圖標及其適用場景 (expense, income, account, general, ui)。使用者資料中只儲存 `id`。
- **檔案:** `assets/definitions/IconDefinition.json`
- **欄位 (fields):**
    - `id`: `Number`
    - `featherName`: `String`
    - `types`: `Array<String>`
    - `tags`: `Array<String> | Null` - Optional
    

### 貨幣 (Currencies)

- **說明:** 定義支援的貨幣及其基本資訊。
- **檔案:** `assets/definitions/Currency.json`
- **欄位 (fields):**
    - `id`: `Number` - ISO Numeric
    - `name`: `String`
    - `alphabeticCode`: `String` - ISO Alpha
    - `numericCode`: `Number`
    - `minorUnits`: `Number`
    - `symbol`: `String | Null`
    

## 時間格式標準

- **儲存標準:**
    - 所有在資料結構中與時間相關的欄位 (如 `transactionDate`, `createdOn`, `updatedOn`, `deletedOn`, `rateDate`, `startOn`, `endOn`, `scheduleInstanceDate`) **必須** 儲存為 **UTC Unix Timestamp (毫秒)** (`number` 型別)。
- **計算與顯示標準:**
    - 所有時間的計算（如判斷「今天」、報表區間）和顯示，都**必須**基於使用者在 `Settings` 中設定的**「主要時區 (timeZone)」** 來進行轉換。