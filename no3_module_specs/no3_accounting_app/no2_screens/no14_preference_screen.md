# 偏好設定畫面: PreferenceScreen

## 畫面目標

- **提供:** 設定 App 核心行為的介面
    - 基礎貨幣
    - 時區
    - 顯示語言
- **提供:** 資料管理與帳號登出的進階選項

```text
+--------------------------------+
| < Back      Preferences        |
+--------------------------------+
| Appearance                     |
|  Theme: [ Current Theme ] >    |
|                                |
| Localization                   |
|  Base Currency: [ TWD ] >      |
|  Time Zone: [ Asia/Taipei ] >  |
|  Language: [ English ] >       |
|                                |
| Sync                           |
|  [ Sync Now ]                  |
|                                |
| Account                        |
|  [ Logout ]                    |
+--------------------------------+
```

---

## UI 佈局

- **頂部導航列:**
    - `返回按鈕`
        - **導航:** SettingsScreen
    - `標題` 偏好設定
- **設定列表:**
    - **外觀:**
        - `配色主題`
            - **顯示:** 當前主題名稱，例如淺色、深色
            - **導航:** ThemeSettingsScreen
            - **邏輯:** 讀取 SettingKey = currentThemeId
    - **本地化:**
        - `主要貨幣`
            - **顯示:** 當前設定的基礎貨幣
            - **互動:** 點擊彈出貨幣選擇器
            - **儲存:** SettingKey = baseCurrencyId
            - **限制:** 僅應在新增帳戶前設定
            - **IF 已存在非基礎貨幣帳戶:**
                - **行為:** 變為不可編輯或顯示警告
        - `時區`
            - **顯示:** 當前設定的 IANA 時區 ID
            - **互動:** 點擊開啟時區選擇器列表
            - **儲存:** SettingKey = timeZone
            - **備註:** 變更後，App 內所有日期顯示、報表計算邊界皆應以此時區為準
        - `語系`
            - **平台差異:**
                - **Android:**
                    - **顯示:** 當前 App 顯示的語言
                    - **互動:** 點擊開啟支援的語言列表
                    - **儲存:** SettingKey = language
                    - **行為:** 變更後即時切換 i18n
                - **iOS:**
                    - **UI:** 不顯示此項目，改為顯示說明文字
                    - **說明:** 如需更改語言，請至 iOS 系統設定 > [App名稱] > 偏好語言中調整
                    - **邏輯:** App 一律遵循 iOS 系統設定
    - **資料同步:**
        - `立即同步按鈕`
    - **帳號:**
        - `登出按鈕`

---

## 核心邏輯

- **資料載入:**
    - **觸發:** 畫面載入
    - **來源:** 本機 DB Settings 表
    - **讀取:** baseCurrencyId, timeZone, language 的 SettingValue
    - **IF 無設定值:**
        - **顯示:** App 預設值
- **資料儲存:**
    - **觸發:** 使用者變更任一選項
    - **本地更新:**
        - **寫入:** 立即更新本機 DB Settings 表
        - **欄位:** 必須設定 `updatedOn`
    - **雲端同步:**
        - **行為:** 由 Sync Engine 自動處理
        - **邏輯:** Sync Engine 監聽本地 DB 變更，若 `isPremium` 為 True 則自動同步至 Firestore
        - **錯誤處理:** Sync Engine 內建重試與離線佇列機制
    - **IF 變更時區或語系:**
        - **觸發:** App 相關設定重新載入，確保 UI 即時更新
- **登出邏輯:**
    - **觸發:** 點擊登出按鈕
    - **行為:** 顯示確認對話框
    - **成功後:**
        - **呼叫:** `authService.signOut()`
        - **監聽:** AuthContext 認證狀態變化
        - **導航:** AppNavigator 切換至 HomeScreen 進入訪客模式

---

## 導航

- **進入:**
    - **來源:** SettingsScreen
- **退出:**
    - **觸發:** 頂部導航列返回按鈕
    - **導航:** SettingsScreen