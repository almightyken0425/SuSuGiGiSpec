# 主題設定規格: ThemeSettingsScreen

## 畫面目標

- **提供:** 瀏覽 App 內建配色主題
- **提供:** 切換並即時預覽主題效果

## UI 佈局

- **頂部導航列:**
    - **內部元件:**
        - **返回按鈕**
            - **導航:** PreferenceScreen
        - **標題**
            - **內容:** 配色主題
- **主題列表:**
    - **UI:** Grid (2 columns) 或 List
    - **資料來源:** `ThemeManager.getAvailableThemes()`
    - **內部元件 - 主題卡片 (Item):**
        - **預覽區:**
            - **UI:** 顯示主題核心配色 (Primary, Background, Surface)
        - **名稱:**
            - **UI:** 顯示主題名稱 (e.g., 海洋藍)
        - **標籤:**
            - **UI:** 顯示 "Light" 或 "Dark"
        - **選取狀態:**
            - **IF** 為當前主題:
                - **UI:** 顯示打勾圖示或高亮邊框

## 核心邏輯

- **資料載入:**
    - **觸發:** 畫面載入 (On Mount)
    - **行為:** 從 `ThemeManager` 獲取所有可用主題列表
    - **行為:** 從 `Settings` (或 Context) 獲取 `currentThemeId`
- **切換主題:**
    - **觸發:** 點擊任一 主題卡片
    - **輸入:** `themeId`
    - **行為:** 呼叫 `ThemeManager.setTheme(themeId)`
    - **行為:** 更新 Context 中的 `currentTheme`
    - **行為:** 持久化儲存 `currentThemeId` 到 `Settings` 表
    - **效果:** App UI 即時反應新主題配色

## 狀態管理

- **本地狀態:**
    - `availableThemes`
    - `currentThemeId`

## 導航

- **進入:**
    - **來源:** PreferenceScreen
- **退出:**
    - **來源:** 頂部導航列 返回按鈕
    - **導航:** PreferenceScreen
