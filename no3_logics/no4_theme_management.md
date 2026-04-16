# 主題管理規格: ThemeManagement

## initializeTheme 主題初始化

- App 啟動時載入並套用主題設定
- **執行:**
  - 讀取 `Settings` 表中的 `currentThemeId`
  - **IF** `currentThemeId` 不存在:
    - 依系統深淺色決定初始主題，預設為 `theme_light_default`
  - 依序查找 `Themes` 表、`BuiltInThemes` 表，取得對應主題定義
  - 將主題定義套用至 App 的主題提供層

## switchTheme 切換主題

- 根據使用者選擇更新當前主題並持久化
- **輸入:**
  - 目標主題識別碼
- **執行:**
  - **IF** 目標主題識別碼不存在於 `BuiltInThemes` 且不存在於 `Themes` 表:
    - RETURN，中止操作
  - **ELSE:**
    - 更新 `currentThemeId` 為目標主題識別碼
    - 取得對應主題定義並套用至 App 的主題提供層
    - 非同步將 `currentThemeId` 寫入 `Settings` 表
