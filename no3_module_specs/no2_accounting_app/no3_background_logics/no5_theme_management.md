# 主題管理邏輯 (Theme Management Logic)

## 1. 邏輯摘要
- **名稱**: ThemeManagement
- **目的**: 負責 App 的主題初始化、切換、持久化以及系統主題跟隨。

## 2. 狀態管理 (State Management)

### 2.1 Context / Store
- `currentTheme`: ThemeObject (當前生效的主題物件)
- `currentThemeId`: String (當前主題 ID)
- `isSystemTheme`: Boolean (是否跟隨系統，預留未來擴充)

## 3. 初始化流程 (Initialization)

1. **App 啟動時**:
   - 讀取 `Settings` 表中的 `currentThemeId`。
   - 若無設定 (First Launch)，則預設使用 `theme_light_default` (或根據系統深淺色決定)。
   - 根據 ID 從 `BuiltInThemes` 查找對應的主題物件。
   - 將主題物件注入 App 的 Theme Provider (e.g., React Context, Styled Components ThemeProvider)。

## 4. 切換流程 (Switching)

1. **使用者選擇新主題 (themeId)**:
   - 檢查 `themeId` 是否存在於 `BuiltInThemes`。
   - 更新 App State (`currentThemeId`, `currentTheme`)，觸發 UI 重繪。
   - 非同步寫入 `Settings` 表:
     - Key: `currentThemeId`
     - Value: `themeId`
   - (Optional) 若支援 Analytics，發送主題切換事件。

## 5. 擴充性設計

- **遠端主題 (Remote Themes)**:
  - 未來可從 Server 下載 JSON 格式的主題定義。
  - 下載後儲存在本地資料庫的 `Themes` 表 (目前僅定義結構，尚未實作)。
  - 初始化時優先查找本地 `Themes` 表，再查找 `BuiltInThemes`。
