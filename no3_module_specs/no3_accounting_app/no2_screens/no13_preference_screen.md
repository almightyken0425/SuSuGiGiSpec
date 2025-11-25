# 偏好設定規格: PreferenceScreen

## 畫面目標

- **提供:** 設定 App 核心行為的介面
    - 基礎貨幣
    - 時區
    - 顯示語言
- **提供:** 資料管理與帳號登出的進階選項

## UI 佈局

- **頂部導航列:**
    - **內部元件:**
        - **返回按鈕**
            - **導航:** SettingsScreen
        - **標題**
            - **內容:** 偏好設定
- **設定列表:**
    - **UI:** 分組列表, SectionList
    - **內部元件 - 外觀:**
        - **配色主題:**
            - **UI:** 顯示當前主題名稱, 例如 淺色, 深色
            - **互動:** 點擊導航至 ThemeSettingsScreen
            - **邏輯:**
                - **讀取:** SettingKey = currentThemeId
    - **內部元件 - 本地化:**
        - **主要貨幣:**
            - **UI:** 顯示當前設定的基礎貨幣
            - **互動:** 點擊彈出貨幣選擇器
            - **邏輯:**
                - **儲存:** SettingKey = baseCurrencyId
                - **限制:** 僅應在新增帳戶前設定
                - **IF** 已存在非基礎貨幣帳戶:
                    - **行為:** 變為不可編輯或顯示警告
        - **時區:**
            - **UI:** 顯示當前設定的 IANA 時區 ID
            - **互動:** 點擊開啟時區選擇器列表
            - **邏輯:**
                - **儲存:** SettingKey = timeZone
                - **備註:** 變更後, App 內所有日期顯示、報表計算邊界皆應以此時區為準
        - **語系:**
            - **UI - 平台差異:**
                - **Android:**
                    - **UI:** 可點擊項目, 顯示當前 App 顯示的語言
                    - **互動:** 點擊開啟支援的語言列表
                    - **邏輯:**
                        - **儲存:** SettingKey = language
                        - **行為:** 變更後即時切換 i18n
                - **iOS:**
                    - **UI:** 不顯示此項目, 改為顯示說明文字
                    - **說明:** 如需更改語言, 請至 iOS 系統設定 > [App名稱] > 偏好語言 中調整
                    - **邏輯:** App 一律遵循 iOS 系統設定
    - **內部元件 - 資料同步:**
        - **立即同步:**
- **資料載入:**
    - **觸發:** 畫面載入
    - **來源:** 本機 DB Settings 表
    - **讀取:** baseCurrencyId, timeZone, language 的 SettingValue
    - **IF** 無設定值:
        - **行為:** 顯示 App 預設值
- **資料儲存:**
    - **觸發:** 使用者變更任一選項
    - **本地更新:**
        - **行為:** 立即更新 本機 DB Settings 表
        - **欄位:** 必須設定 `updatedOn`
    - **雲端同步:**
        - **行為:** 同步更新 Firestore `users/{uid}`
        - **邏輯:** 呼叫 User Management API 或直接寫入 `preferences` 欄位
            - **注意:** 寫入 `currency` 時，需將 `baseCurrencyId` 轉換回 ISO Code (String)
        - **錯誤處理:** 若無網路，標記 dirty flag 待下次連線更新，或依賴 Batch Sync 機制補上，但建議即時寫入以確保 User Management 資料即時性
    - **後續:**
        - **IF** 變更時區或語系:
            - **行為:** 立即觸發 App 相關設定重新載入, 確保 UI 即時更新
- **登出邏輯:**
    - **觸發:** 點擊 登出 按鈕
    - **行為:** 顯示確認對話框
    - **成功:**
        - **行為:** 呼叫 `authService.signOut()`
    - **監聽:**
        - **目標:** AuthContext 認證狀態變化
        - **行為:** AppNavigator 自動切換回 LoginScreen

---

## 狀態管理

- **本地狀態:**
    - `baseCurrencyId`
    - `timeZone`
    - `language`

---

## 導航

- **進入:**
    - **來源:** SettingsScreen
- **退出:**
    - **來源:** 頂部導航列 返回按鈕
    - **導航:** SettingsScreen