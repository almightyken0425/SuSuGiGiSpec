# 設定管理: SettingsManagement

## initializeTheme 主題初始化

- App 啟動時載入並套用主題設定
- **執行:**
  - 讀取 `Settings` 表中的 `theme`
  - **IF** `theme` 不存在:
    - 依系統深淺色決定初始主題，預設為 `theme_light_default`
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
  - 呼叫 updateUserPreferences，帶入 theme 欄位為目標主題識別碼

---

## updateUserPreferences 更新使用者偏好設定

- 偏好設定的 Firestore 寫入統一透過此操作執行
- **輸入:**
  - 本次需變更的偏好設定欄位，未傳入的欄位不受影響
- **執行:**
  - 以逐欄 dot notation 方式更新 preferences，避免覆寫整個 preferences 物件
  - 自動更新 updatedAt 為當前時間，無論傳入欄位數量
  - **IF** Firestore 寫入失敗:
    - 不拋出例外，錯誤僅記錄於 log

---

## setLaunchMode 設定啟動模式

- **輸入:**
  - 目標啟動模式
- **執行:**
  - 將啟動模式寫入本機快取

---

## setBaseCurrency 設定主要貨幣

- **輸入:**
  - 目標主要貨幣 ID
- **執行:**
  - 更新 `Settings` 表中的 `baseCurrencyId` 為目標值
  - 呼叫 updateUserPreferences，帶入 baseCurrencyId 欄位為目標值

---

## setLanguage 設定語系

- **輸入:**
  - 目標語系代碼
- **執行:**
  - 更新 `Settings` 表中的 `language` 為目標值
  - 切換 App 執行期的介面語系
  - 呼叫 updateUserPreferences，帶入 language 欄位為目標值

---

## setTimeZone 設定時區

- **輸入:**
  - 目標時區 IANA 名稱
- **執行:**
  - 更新 `Settings` 表中的 `timeZone` 為目標值
  - 呼叫 updateUserPreferences，帶入 timeZone 欄位為目標值

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
