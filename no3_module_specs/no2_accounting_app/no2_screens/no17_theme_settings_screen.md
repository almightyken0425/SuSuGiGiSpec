# 主題設定畫面 (Theme Settings Screen)

## 1. 畫面摘要
- **名稱**: ThemeSettingsScreen
- **路徑**: `/settings/theme`
- **功能**: 讓使用者瀏覽並切換 App 的配色主題。

## 2. UI 結構

### 2.1 Header
- **Title**: "配色主題"
- **Left**: Back Button (返回 PreferenceScreen)

### 2.2 主題列表 (Theme List)
- **Layout**: Grid (2 columns) or List
- **Item (Theme Card)**:
  - **Preview**: 顯示主題的色彩預覽 (Primary, Background, Surface)
  - **Name**: 主題名稱 (e.g., "海洋藍")
  - **Selected Indicator**: 若為當前主題，顯示打勾圖示或高亮邊框
  - **Tag**: 顯示 "Light" 或 "Dark" 標籤

## 3. 互動邏輯

### 3.1 載入主題
- **On Mount**:
  - 從 `ThemeManager` 獲取所有可用主題列表。
  - 從 `Settings` (或 Context) 獲取 `currentThemeId`。

### 3.2 切換主題
- **Action**: 使用者點擊任一主題卡片。
- **Logic**:
  1. 呼叫 `ThemeManager.setTheme(themeId)`。
  2. 更新 Context 中的 `currentTheme`。
  3. 持久化儲存 `currentThemeId` 到 `Settings` 表。
  4. App UI 應即時反應新主題配色。

## 4. 導航
- **Back**: 返回上一頁 (PreferenceScreen)。
