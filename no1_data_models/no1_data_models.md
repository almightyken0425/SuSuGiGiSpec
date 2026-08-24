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
  - `launchMode`: String - Not Null, Default `home`, 啟動模式，可為 `home`、`expense`、`income`、`transfer`
  - `weekStart`: String - Not Null, Default `auto`, 週起始日偏好，可為 `auto`、`sunday`、`monday`；`auto` 代表依使用者語系慣例決定
  - `analyticsConsent`: Boolean - Not Null, Default `false`, 財務分析相容欄位，目前停用
  - `usageAnalyticsConsent`: Boolean - Not Null, Default `false`, 使用行為分析同意開關
  - `usageAnalyticsConsentDecided`: Boolean - Not Null, Default `false`, 使用分析同意是否已選擇
  - `homeTimeGranularity`: String | Null - Nullable, 首頁時間粒度顯示狀態，可為 `day`、`week`、`month`、`year`、`all`；Null 或集外值載入時視為 `day`
  - `homeGroupMode`: String | Null - Nullable, 首頁列表分組模式顯示狀態，可為 `category`、`date`；Null 或集外值載入時視為 `category`
  - `homeSelectedAccountIds`: String | Null - Nullable, 首頁已選帳戶清單，JSON 字串陣列序列化；Null 或無法解析視為無既有清單
  - `lastSyncedAt`: Number | Null, Unix Timestamp ms - Nullable, 上次完成交易備份上傳的時間，作為 Delta 篩選基準；Null 代表尚未上傳過，偏好上傳不更新此欄位
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據

**與 User Management 的關係**: 本機此表為偏好設定唯一真相；`users/{uid}/preferences` 為單向上傳鏡像，僅供資料分析維度，永不下載套用。
- 整份 `users/{uid}` 雲端文件含 `provider`、文件根層 `updatedAt` 等頂層欄位的形狀權威屬 User Management module 的 Users 資料模型，本 module 不重複承載定義
- `language`、`timeZone`、`theme`、`launchMode`、`weekStart`、`analyticsConsent` 直接對應上傳
- `usageAnalyticsConsent` 僅存本機
- `usageAnalyticsConsentDecided` 僅存本機
- `baseCurrencyId` 上傳時轉 ISO Code 寫入 `preferences.currency`，單向轉換不反向
- `homeTimeGranularity`、`homeGroupMode`、`homeSelectedAccountIds` 為首頁顯示狀態，僅存本機，不參與上傳
- 偏好設定屬裝置層級設定，不隨帳號跨裝置下載
- 多裝置各自上傳，接受最後寫入覆寫

---

### 帳戶 Accounts

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `name`: String - Not Null, 長度上限 60 字元；寫入時去除前後空白，全為空白視為空
  - `iconId`: Number - Foreign Key to IconDefinitions, Not Null, 須為 tags 含 account 的圖示
  - `currencyCode`: String - Not Null, 帳戶幣別 ISO Alpha Code，例如 TWD
  - `sortOrder`: Number - Not Null, Default 0, 使用者自訂排序位置
  - `scheduleId`: String | Null - Nullable, 棄用殘欄；任何路徑不寫入、恆為 Null，帳戶不由排程產生
  - `disabledOn`: Number | Null, Unix Timestamp ms - Nullable, 使用者主動停用此帳戶的時間；Null 代表啟用中
  - `createdAt`: Number, Unix Timestamp ms - Not Null, 資料建立的系統時間
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable

---

### 類別 Categories

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `name`: String - Not Null, 長度上限 60 字元；寫入時去除前後空白，全為空白視為空
  - `type`: String - Not Null, expense 或 income，決定此類別為支出或收入
  - `iconId`: Number - Foreign Key to IconDefinitions, Not Null, 須為 tags 含 category 的圖示
  - `sortOrder`: Number - Not Null, Default 0, 使用者自訂排序位置
  - `disabledOn`: Number | Null, Unix Timestamp ms - Nullable, 使用者主動停用此類別的時間；Null 代表啟用中
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable

---

### 收支紀錄 Transactions

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `accountId`: String - Foreign Key to Accounts, Not Null, Index
  - `categoryId`: String - Foreign Key to Categories, Not Null, Index
  - `amount`: Number - Not Null, 金額，以固定倍率縮放的整數，與幣別無關
  - `date`: Number, Unix Timestamp ms - Not Null, Index, 交易發生日，使用者可編輯，用於報表與排序
  - `note`: String | Null - Nullable, 長度上限 200 字元；寫入時去除前後空白，用於搜尋
  - `scheduleId`: String | Null - Foreign Key to Schedules, Nullable
  - `scheduleInstanceDate`: Number | Null, Unix Timestamp ms - Nullable
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable

---

### 轉帳紀錄 Transfers

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `accountFromId`: String - Foreign Key to Accounts, Not Null, Index
  - `accountToId`: String - Foreign Key to Accounts, Not Null, Index
  - `amountFrom`: Number - Not Null, 轉出金額，以固定倍率縮放的整數，與幣別無關
  - `amountTo`: Number - Not Null, 轉入金額，以固定倍率縮放的整數，與幣別無關
  - `impliedRate`: Number | Null - Nullable, 主單位對主單位匯率；同步至 Firestore 時欄位名稱轉為 impliedRateScaled
  - `date`: Number, Unix Timestamp ms - Not Null, Index, 轉帳發生日，用於報表篩選
  - `note`: String | Null - Nullable, 長度上限 200 字元；寫入時去除前後空白，用於搜尋
  - `scheduleId`: String | Null - Foreign Key to Schedules, Nullable
  - `scheduleInstanceDate`: Number | Null, Unix Timestamp ms - Nullable
  - `createdAt`: Number, Unix Timestamp ms - Not Null, 資料建立的系統時間
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable

---

### 貨幣匯率 CurrencyRates

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `currencyFromId`: Number - Foreign Key to Currencies, Not Null
  - `currencyToId`: Number - Foreign Key to Currencies, Not Null
  - `rate`: Number - Not Null, 主單位對主單位匯率
  - `date`: Number, Unix Timestamp ms - Not Null, Index, 匯率生效時點，含日期與時刻，換算取值的新舊比較基準
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null, 資料最後更新時間，同步依據
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable

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

**與 Firestore 的關係**: 此表不同步至雲端，僅存於本地。
- 幣別顯示偏好屬裝置層級設定，不隨帳號跨裝置同步

---

### 定期交易排程 Schedules

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null, Index, 資料擁有者
  - `frequency`: String - Not Null, 例如 DAILY、WEEKLY、MONTHLY、YEARLY
  - `interval`: Number - Not Null, 頻率倍數，例如每兩週一次時 interval 為 2；數值上限 999
  - `startOn`: Number, Unix Timestamp ms - Not Null, 排程開始時點，含日期與時刻，補產實例的起點與時刻基準
  - `endOn`: Number | Null, Unix Timestamp ms - Nullable, 排程結束日期
  - `isTransfer`: Boolean - Not Null, true 代表轉帳排程，false 代表收支排程
  - `templateAmount`: Number | Null - Nullable, 收支金額
  - `templateCategoryId`: String | Null - Nullable, 收支類別 ID
  - `templateAccountId`: String | Null - Nullable, 收支帳戶 ID
  - `templateAmountFrom`: Number | Null - Nullable, 轉出金額
  - `templateAccountFromId`: String | Null - Nullable, 轉出帳戶 ID
  - `templateAmountTo`: Number | Null - Nullable, 轉入金額
  - `templateAccountToId`: String | Null - Nullable, 轉入帳戶 ID
  - `templateNote`: String | Null - Nullable, 長度上限 200 字元；寫入時去除前後空白
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable

---

### 使用者 User

- **欄位:**
  - `id`: String, UUID/GUID - Primary Key, 對應 Auth UID
  - `email`: String | Null - Nullable
  - `displayName`: String | Null - Nullable
  - `photoUrl`: String | Null - Nullable
  - `lastLoginAt`: Number, Unix Timestamp ms - Not Null
  - `iapEntitlementsJson`: String | Null - Nullable, 棄用殘欄；任何路徑不寫入、恆為 Null，不承載授權
  - `iapActivePurchasesJson`: String | Null - Nullable, 棄用殘欄；任何路徑不寫入、恆為 Null，不承載授權
  - `createdAt`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null

---

## App 標準定義資料

### 圖示定義 IconDefinitions

- **說明:**
  - 定義 App 支援的所有圖示及其所屬圖示庫
- **檔案:**
  - `assets/definitions/IconDefinition.json`
- **欄位:**
  - `id`: `Number`
  - `uniqueName`: `String` - 唯一識別名稱，格式如 ph-wallet、ph-bread
  - `library`: `String` - 圖示庫名稱，目前統一為 svg，採用 Phosphor SVG 圖示庫
  - `glyph`: `String` - 圖示庫內的字型名稱
  - `tags`: `Array<String>` - 用途標籤，界定圖示適用域；account 供帳戶使用，category 供類別使用

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
  - 執行期 Premium 等級狀態；授權真相在 StoreKit，由當前有效購買推定，離線由 StoreKit 系統快取承載
  - User 實體的 IAP 欄位為棄用殘欄、不承載授權
  - 各 LEVEL 在記帳 App 視角下的可用能力白話總覽，見 `no2_product_planning/no2_product_map/app/payment.md` 的 LEVEL 能力清單
  - 動作識別碼與授權判斷邏輯，見 `no3_product_specs/no2_accounting_app/no3_logics/no17_subscription_gate_logic.md`
- **欄位:**
  - `currentTier`: Number - Not Null, 當前 Premium 等級，值域對應 LEVEL_0..LEVEL_B，僅涵蓋 IAP 可解析的範圍
    - `LEVEL_0`
    - `LEVEL_1`
    - `LEVEL_2`
    - LEVEL_3、LEVEL_B 非 IAP 解析持有的 runtime tier，故不列入
    - **來源:**
      - 由 StoreKit 當前有效購買推定，見 `no3_logics/no6_premium_logic.md`
  - `isPremiumLoaded`: Boolean - Not Null, 訂閱狀態是否已就緒；首次解析完成前為 false，期間不以佔位的 LEVEL_0 判定授權
    - 初值 false，首次更新前 currentTier 為佔位 LEVEL_0、不可信
    - StoreKit 首次解析完成或逾時保底後設為 true
    - 身分未就緒時歸 false，身分就緒後重新解析

---

## 金額數值標準

- **儲存標準:**
  - 所有金額相關欄位以固定倍率縮放為整數存放，型別為 Number，與幣別無關
  - 涵蓋 Transactions 的 `amount`、Transfers 的 `amountFrom` 與 `amountTo`、Schedules 的 `templateAmount`、`templateAmountFrom` 與 `templateAmountTo`
  - 最大可存的縮放整數落在系統安全整數上界，約 9.007×10^15
- **輸入約束:**
  - 使用者輸入受位數上限約束，確保縮放後不超過系統安全整數上界
- **正負與零值政策:**
  - 交易金額不得為 0
  - 轉帳的轉出金額、轉入金額皆須大於 0

---

## 時間格式標準

- **儲存標準:**
  - 所有時間相關欄位儲存為 UTC Unix Timestamp 毫秒，型別為 Number
