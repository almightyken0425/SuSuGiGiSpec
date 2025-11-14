# 開發計劃 (順序)

_(本文件定義 MVP 範圍內的建議開發階段與優先級)_ _(已根據「本地優先 + 混合付費牆」新策略更新)_

## Phase 0: 基礎建設 (Setup)

- [ ] 建立 Expo (React Native) 專案。
    
- [ ] 實作 `src/types/index.ts` (根據 `no1_data_structure.md`，**必須**包含 `updatedOn` 欄位)。
    
- [ ] 建立 `assets/definitions/` 並置入所有標準 JSON 檔案。
    
- [ ] 建立 `src/utils/` (格式化、圖標、時間輔助)。
    
- [ ] 建立 `src/constants/` (主題色)。
    
- [ ] 建立 `src/locales/` 並設定 `i18n.ts` (MVP 階段)。
    
- [ ] 設定 Firebase 專案 (僅用於 Auth)。
    

## Phase 1: 本機資料庫 (Local-First Architecture)

- [ ] **[關鍵決策]** 選擇本機資料庫方案 (例如 `SQLite`, `WatermelonDB`, 或 `AsyncStorage` + 狀態管理)。
    
- [ ] 實作本機資料庫的 `Schema` (對應 `no1_data_structure.md`)。
    
- [ ] 實作本機資料庫的 CRUD (Create, Read, Update, Delete) 服務 (例如 `localDbService.ts`)。
    
- [ ] 實作「首次啟動流程」：偵測新用戶，並在**本機資料庫**建立預設資料。
    

## Phase 2: 核心功能與 UI (Local CRUD)

- [ ] 實作 `AuthContext` / `useAuth` Hook (用於登入/登出)。
    
- [ ] 建立 `LoginScreen.tsx` (UI + Google 登入邏輯)。
    
- [ ] 建立 App 導航 (`AppNavigator.tsx`)，根據登入狀態切換 `LoginScreen` 或 `HomeScreen`。
    
- [ ] 建立 `AccountManagement/` 畫面 (CRUD 介面，**完全對接本機資料庫**，處理 3 個帳戶限制)。
    
- [ ] 建立 `IconPickerScreen.tsx`。
    
- [ ] 建立 `CategoryManagement/` 畫面 (CRUD 介面，**完全對接本機資料庫**，處理 10 個類別限制)。
    
- [ ] 建立 `src/screens/TransactionEditor/` (收支/轉帳表單 UI，**完全對接本機資料庫**)。
    
- [ ] 建立 `HomeScreen.tsx` (儀表板 UI，**完全對接本機資料庫**)。
    
- [ ] 建立 `SearchScreen.tsx` (**對接本機資料庫**)。
    
- [ ] 建立 `SettingsScreen.tsx` 及 `PreferenceScreen.tsx` (UI，包含登出、語系切換等)。
    

## Phase 3: 付費牆與功能解鎖 (Monetization)

- [ ] 建立 `PaywallScreen.tsx` (UI 介面)。
    
- [ ] 串接 **RevenueCat** (或類似服務) 處理 App Store / Google Play 訂閱。
    
- [ ] 實作 `PremiumContext` (或狀態) 來管理 `isPremiumUser` 狀態。
    
- [ ] 在所有「付費功能觸發點」加入付費牆檢查：
    
    - [ ] 建立第 4 個帳戶 / 第 11 個類別時。
        
    - [ ] 導航至「多幣別」相關功能 (`CurrencyRateScreen`)。
        
    - [ ] 導航至「定期交易」建立畫面。
        
    - [ ] 導航至「匯入資料」(`ImportScreen`)。
        
    - [ ] 點擊「立即同步」按鈕。
        

## Phase 4: 付費版功能 (Premium Features)

- [ ] **[關鍵任務]** 建立「**批次同步引擎**」 (基於 `no8_sync_logic_spec.md`):
    
    - [ ] 實作「上傳」邏輯 (`Client-to-Server`)。
        
    - [ ] 實作「下載」邏輯 (`Server-to-Client`)。
        
    - [ ] 實作「Last Write Wins」衝突解決。
        
    - [ ] 實作「每日自動觸發」邏輯。
        
- [ ] 將「**立即同步 (Sync Now)**」按鈕（含冷卻機制）接入 `PreferenceScreen`。
    
- [ ] 實作「**多幣別**」功能 (跨幣別轉帳、`CurrencyRateScreen` CRUD)。
    
- [ ] 實作「**定期交易 (`Schedules`)**」功能 (建立介面、App 啟動時的本機檢查邏輯)。
    
- [ ] 實作 `ImportScreen.tsx` (CSV 匯入邏輯)。
    

## Phase 5: 測試與打包 (Release)

- [ ] 完整測試所有功能（特別是本機 CRUD、付費流程、同步引擎、資料還原）。
    
- [ ] 準備 App Icon、啟動畫面。
    
- [ ] 準備 App Store / Google Play 上架資料（含隱私權政策、訂閱項目設定）。
    
- [S ] 打包並提交審核。