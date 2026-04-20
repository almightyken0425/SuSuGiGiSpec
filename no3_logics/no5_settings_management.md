# 設定管理: SettingsManagement

## initializeTheme 主題初始化

- App 啟動時載入並套用主題設定
- **執行:**
  - 讀取 `Settings` 表中的 `currentThemeId`
  - **IF** `currentThemeId` 不存在:
    - 依系統深淺色決定初始主題，預設為 `theme_light_default`
  - 依序查找 `Themes` 表、`BuiltInThemes` 表，取得對應主題定義
  - 將主題定義套用至 App 的主題提供層

---

## switchTheme 切換主題

- 根據使用者選擇更新當前主題，Premium 有效時同步至雲端
- **輸入:**
  - 目標主題識別碼
- **執行:**
  - **IF** 目標主題識別碼不存在於 `BuiltInThemes` 且不存在於 `Themes` 表:
    - RETURN
  - **ELSE:**
    - 更新 `currentThemeId` 為目標主題識別碼
    - 取得對應主題定義並套用至 App 的主題提供層
    - 非同步將 `currentThemeId` 寫入 `Settings` 表
    - **IF** Premium 有效:
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
