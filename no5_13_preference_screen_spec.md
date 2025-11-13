# 設定 - 偏好設定 (PreferenceScreen)

_(本文件定義「偏好設定」畫面的 UI、流程與邏輯)_

## 畫面目標 (Screen Objective)

- 提供一個介面，讓使用者可以設定 App 的核心行為，包括基礎貨幣、時區和顯示語言。
    
- 提供資料管理和帳號登出的進階選項。
    

## UI 佈局與元件 (UI Layout & Components)

- **頂部導航列 (Top Navigation Bar):**
    
    - **左側:** 「返回」按鈕，導航回設定主頁 (`SettingsScreen`)。
        
    - **中間:** 畫面標題，顯示「偏好設定」。
        
- **設定列表 (Settings List):**
    
    - **UI:** 一個分組列表 (`SectionList`)。
        
    - **項目:**
        
        - **本地化 (Localization)**
            
            - **主要貨幣 (Base Currency):**
                
                - **UI:** 顯示當前設定的基礎貨幣 (例如 "TWD")。
                    
                - **互動:** 點擊後彈出貨幣選擇器 (`Currency.json`)。
                    
                - **邏輯:**
                    
                    - 儲存 `SettingKey` = 'baseCurrencyId'。
                        
                    - 僅應在「新增帳戶」前設定，若已存在非基礎貨幣帳戶，此處應變為不可編輯或顯示警告。
                        
            - **時區 (Time Zone):**
                
                - **UI:** 顯示當前設定的 IANA 時區 ID (例如 "Asia/Taipei")。
                    
                - **互動:** 點擊後開啟時區選擇器列表。
                    
                - **邏輯:**
                    
                    - 儲存 `SettingKey` = 'timeZone'。
                        
                    - 變更後，App 內所有日期顯示、報表計算邊界（日/週/月）皆應以此時區為準。
                        
            - **語系 (Language):**
                
                - **UI (平台差異):**
                    
                    - **Android:** 顯示一個可點擊的項目，內容為當前 App 顯示的語言 (例如 "繁體中文")。
                        
                    - **iOS:** **不顯示此項目**。改為顯示一段不可點擊的說明文字：「如需更改語言，請至 iOS 系統『設定 > [App名稱] > 偏好語言』中調整。」
                        
                - **互動 (Android Only):**
                    
                    - 點擊後開啟支援的語言列表 (例如 "繁體中文", "English")。
                        
                - **邏輯 (Android Only):**
                    
                    - 儲存 `SettingKey` = 'language'。
                        
                    - 變更後即時切換 App 介面語言 (i18n)。
                        
                - **邏輯 (iOS):**
                    
                    - App 應**一律遵循** iOS 系統設定中的 App 偏好語言，或（若未設定）系統的整體語言。
                        
        - **資料同步 (Data Sync)**
            - **立即同步 (Sync Now):**
              - **UI:** 一個按鈕項目，文字為「**立即同步**」。
              - **_[付費功能]_**
              - **邏輯:**
                - **1. 付費牆檢查:** 點擊時，首先檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser`。若為 `false`，導航至「付費牆畫面」，**終止**流程。
                - **2. 冷卻機制檢查:** 檢查 `Now < nextSyncAllowedTime`（`nextSyncAllowedTime` 儲存於本機）。
                  - **若在冷卻期:** 顯示提示「您剛才同步過了，請 5 分鐘後再試」，**終止**流程。
                  - **若不在冷卻期:** 繼續執行。
                - **3. 執行同步:**
                  - 顯示載入指示器。
                  - **手動觸發**「批次同步規格」中定義的「同步流程」（上傳 -> 下載 -> 更新時間戳記）。
                  - 同步成功後，顯示「同步完成」提示。
                  - 同步失敗後，顯示「同步失敗」提示。
                - **說明文字:** 按鈕下方應有輔助說明：「手動觸發一次與雲端的資料同步。這是您更換手機或跨裝置作業時的標準操作。」
        - **帳號 (Account)**
            
            - **登出:**
                
                - **UI:** 一個紅色的「登出」文字按鈕。
                    
                - **邏輯:** 點擊後觸發下方的登出邏輯。
                    

## 核心邏輯

- **資料載入:**
    - 畫面載入時，從「**本機資料庫 (Local DB)**」的 `Settings` 表讀取 'baseCurrencyId', 'timeZone', 'language' 的 `SettingValue` 並顯示在 UI 上。
    - 若無設定值，應顯示 App 的預設值（例如裝置偵測到的時區）。
        
- **資料儲存:**
    - 使用者對任何選項（貨幣、時區、語系）進行變更並確認後，應立即在「**本機資料庫 (Local DB)**」中更新 `Settings` 表（**必須**設定 `updatedOn` 時間戳記）。
    - 變更**時區**或**語系**後，應立即觸發 App 相關設定（例如 i18n 實例、日期計算輔助函數）的重新載入，以確保 UI 即時更新。
        
- **登出邏輯 (Logout Logic)**
    
    - 點擊「登出」按鈕時，彈出一個確認對話框（例如：「您確定要登出嗎？」）。
        
    - 使用者確認後，呼叫 `authService.signOut()`。
        
    - `AuthContext` 應監聽認證狀態的變化。當偵測到使用者已登出時，`AppNavigator` 會自動將畫面切換回 `LoginScreen`。
        

## 狀態管理 (State Management)

- 使用 `useState` 管理從 `Settings` 讀取的各項設定值：
    
    - `baseCurrencyId: number`
        
    - `timeZone: string`
        
    - `language: string`
        

## 導航 (Navigation)

- **進入:** 從設定主頁 (`SettingsScreen`) 的「偏好設定」項目點擊進入。
    
- **退出:** 點擊頂部導航列的「返回」按鈕，返回 `SettingsScreen`。