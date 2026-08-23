# 設定管理: SettingsManagementLogic

## initializeTheme 主題初始化

- App 啟動時載入並套用主題設定
- **執行:**
  - 讀取 `Settings` 表中的 `theme`
  - **IF** `theme` 不存在:
    - 採用 THEMES 清單的固定預設主題，識別碼 `theme1`
  - 從 THEMES 內建主題清單取得對應主題定義
  - 將主題定義套用至 App 的主題提供層

---

## switchTheme 切換主題

- **輸入:**
  - 目標主題識別碼
- **執行:**
  - 更新 `theme` 為目標主題識別碼
  - 從 THEMES 內建主題清單取得對應主題定義並套用至 App 的主題提供層
  - 非同步將 `theme` 寫入 `Settings` 表
  - 委派 PreferenceUploadLogic 的 uploadPreferences，帶入 theme 欄位為目標主題識別碼

---

## setLaunchMode 設定啟動模式

- **輸入:**
  - 目標啟動模式
- **執行:**
  - 更新 `Settings` 表中的 `launchMode` 為目標值
  - 委派 PreferenceUploadLogic 的 uploadPreferences，帶入 launchMode 欄位為目標值

---

## setBaseCurrency 設定主要貨幣

- **輸入:**
  - 目標主要貨幣 ID
- **執行:**
  - 更新 `Settings` 表中的 `baseCurrencyId` 為目標值
  - 為每個與新主要貨幣不同的既有帳戶幣別，呼叫 createInitialCurrencyRate 種入對新主要貨幣的佔位匯率；已有紀錄則略
  - 委派 PreferenceUploadLogic 的 uploadPreferences，帶入 baseCurrencyId 欄位為目標值

---

## setLanguage 設定語系

- **輸入:**
  - 目標語系代碼
- **執行:**
  - 更新 `Settings` 表中的 `language` 為目標值
  - 切換 App 執行期的介面語系
  - 委派 PreferenceUploadLogic 的 uploadPreferences，帶入 language 欄位為目標值

---

## setTimeZone 設定時區

- **輸入:**
  - 目標時區 IANA 名稱
- **執行:**
  - 更新 `Settings` 表中的 `timeZone` 為目標值
  - 委派 PreferenceUploadLogic 的 uploadPreferences，帶入 timeZone 欄位為目標值

---

## setWeekStart 設定週起始日

- **輸入:**
  - 目標週起始日值
- **執行:**
  - 更新 `Settings` 表中的 `weekStart` 為目標值
  - 委派 PreferenceUploadLogic 的 uploadPreferences，帶入 weekStart 欄位為目標值

---

## setAnalyticsConsent 設定分析同意

- **輸入:**
  - 目標同意狀態
- **執行:**
  - 更新 `Settings` 表中的 `analyticsConsent` 為目標值
  - 委派 PreferenceUploadLogic 的 uploadPreferences，帶入 analyticsConsent 欄位為目標值

---

## setUsageAnalyticsConsent 設定使用分析同意

- **輸入:**
  - 目標同意狀態
- **執行:**
  - 更新 `usageAnalyticsConsent`
  - 委派 configureUsageAnalytics
  - 不參與偏好上傳

---

## setCurrencyFormat 設定貨幣顯示格式

- **輸入:**
  - 目標貨幣 ID
  - 小數位數
  - 是否啟用千分位顯示
- **執行:**
  - 查找 `CurrencyConfig` 表中 `userId` 與 `currencyId` 對應的既有紀錄
  - **IF** 紀錄存在:
    - 更新該紀錄的 `decimalPlaces` 與 `useThousandsUnit`
  - **ELSE:**
    - 新增一筆紀錄至 `CurrencyConfig` 表，設定 `currencyId`、`decimalPlaces`、`useThousandsUnit`

---

## resetCurrencyFormat 重置貨幣小數位數

- **輸入:**
  - 目標貨幣 ID
- **執行:**
  - 查找 `CurrencyConfig` 表中 `userId` 與 `currencyId` 對應的既有紀錄
  - **IF** 紀錄存在:
    - 將該紀錄的 `decimalPlaces` 設為 Null，回歸該貨幣預設位數
  - **ELSE:**
    - 新增一筆紀錄至 `CurrencyConfig` 表，設定 `currencyId`、`decimalPlaces` 為 Null、`useThousandsUnit` 為 false
