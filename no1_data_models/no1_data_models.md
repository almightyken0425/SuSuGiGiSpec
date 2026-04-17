# 資料結構

## 使用者自訂資料結構

### 設定 Settings

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key, 通常只有一筆記錄
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index
  - `language`: String - Not Null, 介面語言代碼，例如 en
  - `baseCurrencyId`: Number - Foreign Key to Currencies, Not Null, 主要貨幣
  - `timeZone`: String - Not Null, IANA Timezone ID，例如 Asia/Taipei
  - `theme`: String - Not Null, 主題設定，例如 light、dark、system
  - `lastSyncedAt`: Number, Unix Timestamp ms - Not Null, 上次完成同步的時間
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據

**與 User Management 的關係**: 此表為 `users/{uid}/preferences` 的本地快取。
- `language`、`timeZone`、`theme` 直接對應
- `baseCurrencyId` 對應 `preferences.currency`，需進行 ID 與 ISO Code 雙向轉換
- 需保持雙向同步

---

### 帳戶 Accounts

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `name`: String - Not Null
  - `iconId`: Number - Foreign Key to IconDefinitions, Not Null
  - `currencyCode`: String - Not Null, 帳戶幣別 ISO Alpha Code，例如 TWD
  - `typeId`: Number - Foreign Key to StandardAccountTypes, Not Null
  - `sortOrder`: Number - Not Null, Default 0, 使用者自訂排序位置
  - `scheduleId`: String | Null - Foreign Key to Schedules, Nullable, 標記此筆為定期交易產生
  - `disabledOn`: Number | Null, Unix Timestamp ms - Nullable, 使用者主動停用此帳戶的時間；Null 代表啟用中
  - `createdAt`: Number, Unix Timestamp ms - Not Null, 資料建立的系統時間
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable, Index

---

### 類別 Categories

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `name`: String - Not Null
  - `type`: String - Not Null, expense 或 income，決定此類別為支出或收入
  - `iconId`: Number - Foreign Key to IconDefinitions, Not Null
  - `standardCategoryId`: Number - Foreign Key to StandardCategory, Not Null, 用於報表歸類
  - `sortOrder`: Number - Not Null, Default 0, 使用者自訂排序位置
  - `disabledOn`: Number | Null, Unix Timestamp ms - Nullable, 使用者主動停用此類別的時間；Null 代表啟用中
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable, Index

---

### 收支紀錄 Transactions

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `accountId`: String - Foreign Key to Accounts, Not Null
  - `categoryId`: String - Foreign Key to Categories, Not Null
  - `amount`: Number - Not Null, 金額，以幣別最小單位儲存
  - `date`: Number, Unix Timestamp ms - Not Null, 交易發生日，使用者可編輯，用於報表與排序
  - `note`: String | Null - Nullable, 用於搜尋
  - `scheduleId`: String | Null - Foreign Key to Schedules, Nullable
  - `scheduleInstanceDate`: Number | Null, Unix Timestamp ms - Nullable
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable, Index

---

### 轉帳紀錄 Transfers

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `accountFromId`: String - Foreign Key to Accounts, Not Null
  - `accountToId`: String - Foreign Key to Accounts, Not Null
  - `amountFrom`: Number - Not Null, 轉出帳戶的金額，以該帳戶幣別計
  - `amountTo`: Number - Not Null, 轉入帳戶的金額，以該帳戶幣別計
  - `impliedRate`: Number | Null - Nullable, 匯率乘以一百萬後的整數；同步至 Firestore 時欄位名稱轉為 impliedRateScaled
  - `date`: Number, Unix Timestamp ms - Not Null, 轉帳發生日，用於報表篩選
  - `note`: String | Null - Nullable, 用於搜尋
  - `scheduleId`: String | Null - Foreign Key to Schedules, Nullable
  - `scheduleInstanceDate`: Number | Null, Unix Timestamp ms - Nullable
  - `createdAt`: Number, Unix Timestamp ms - Not Null, 資料建立的系統時間
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable, Index

---

### 貨幣匯率 CurrencyRates

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `currencyFromId`: Number - Foreign Key to Currencies, Not Null
  - `currencyToId`: Number - Foreign Key to Currencies, Not Null
  - `rate`: Number - Not Null, 匯率乘以一百萬後的整數
  - `date`: Number, Unix Timestamp ms - Not Null, 匯率生效日期，儲存該日 00:00:00 UTC
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據

---

### 貨幣顯示設定 CurrencyConfig

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `currencyId`: Number - Foreign Key to Currencies, Not Null
  - `decimalPlaces`: Number | Null - Nullable, 自訂小數位數；Null 代表使用貨幣預設
  - `useThousandsUnit`: Boolean - Not Null, 是否以千為單位顯示
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null

---

### 定期交易排程 Schedules

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `frequency`: String - Not Null, 例如 DAILY、WEEKLY、MONTHLY、YEARLY
  - `interval`: Number - Not Null, 頻率倍數，例如每兩週一次時 interval 為 2
  - `startOn`: Number, Unix Timestamp ms - Not Null, 排程開始日期，基於使用者時區的 00:00:00 轉存 UTC
  - `endOn`: Number | Null, Unix Timestamp ms - Nullable, 排程結束日期
  - `isTransfer`: Boolean - Not Null, true 代表轉帳排程，false 代表收支排程
  - `templateAmount`: Number | Null - Nullable, 收支金額
  - `templateCategoryId`: String | Null - Nullable, 收支類別 ID
  - `templateAccountId`: String | Null - Nullable, 收支帳戶 ID
  - `templateAmountFrom`: Number | Null - Nullable, 轉出金額
  - `templateAccountFromId`: String | Null - Nullable, 轉出帳戶 ID
  - `templateAmountTo`: Number | Null - Nullable, 轉入金額
  - `templateAccountToId`: String | Null - Nullable, 轉入帳戶 ID
  - `templateNote`: String | Null - Nullable
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable, Index

---

### 使用者 User

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key, 對應 Auth UID
  - `email`: String | Null - Nullable
  - `displayName`: String | Null - Nullable
  - `photoUrl`: String | Null - Nullable
  - `lastLoginAt`: Number, Unix Timestamp ms - Not Null
  - `iapEntitlementsJson`: String | Null - Nullable, JSON, IAP 服務回傳的 entitlements
  - `iapActivePurchasesJson`: String | Null - Nullable, JSON, 有效訂閱列表
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null

---

## App 標準定義資料

### 標準收支類別 StandardCategory

- **說明:**
  - 統一管理標準的收支大類，使用者自訂類別需映射到此
- **檔案:**
  - `assets/definitions/StandardCategory.json`
- **欄位:**
  - `id`: `Number`
  - `categoryType`: `Number` - 0 代表收入，1 代表支出
  - `translationKey`: `String`
  - `defaultName`: `String`

---

### 標準帳戶類型 StandardAccountType

- **說明:**
  - 定義帳戶的金融本質分類，例如支付、投資、貸款、其他
- **檔案:**
  - `assets/definitions/StandardAccountType.json`
- **欄位:**
  - `id`: `Number`
  - `name`: `String`
  - `types`: `Array<String>`
  - `tags`: `Array<String> | Null`

---

### 貨幣 Currencies

- **說明:**
  - 定義支援的貨幣及其基本資訊
- **檔案:**
  - `assets/definitions/Currency.json`
- **欄位:**
  - `id`: `Number` - ISO Numeric
  - `name`: `String`
  - `alphabeticCode`: `String` - ISO Alpha
  - `numericCode`: `Number`
  - `minorUnits`: `Number`
  - `symbol`: `String | Null`

---

## Local State

### PremiumContext Local State

- **說明:**
  - 執行期 Premium 等級狀態；IAP 原始資料快取於 User 實體的 IAP 欄位
- **欄位:**
  - `currentTier`: String - Not Null, 當前 Premium 等級；LEVEL_0 代表免費，LEVEL_1 代表訂閱用戶
    - **來源:**
      - 從 IAP 服務回傳的有效訂閱列表解析

---

## 時間格式標準

- **儲存標準:**
  - 所有時間相關欄位儲存為 UTC Unix Timestamp 毫秒，型別為 Number
