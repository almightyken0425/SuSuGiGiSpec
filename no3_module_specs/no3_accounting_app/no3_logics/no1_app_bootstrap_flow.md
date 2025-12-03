# App 啟動流程

## 觸發時機

- **觸發:** 使用者開啟 App

## 啟動畫面

- **顯示:** Splash 啟動畫面
- **實作策略:** Seamless Launch 無縫啟動
- **技術細節:**
    - **Native 層:** 使用原生 Launch Screen iOS/Android 顯示 Logo 與背景色
    - **React Native 層:** App Root View 初始渲染完全相同的 Logo 與背景色 View
    - **JS 載入完成:** RN View 蓋過 Native View 使用者無感
    - **資料讀取完畢:** 執行 Fade Out 動畫移除 RN Splash View，顯示 HomeScreen
- **目的:** 消除白畫面 White Screen 並掩蓋資料載入時間，創造「秒開」體驗

## 認證狀態檢查

- **檢查:** 本機儲存的 Auth State 認證狀態
- **IF 認證狀態為 Valid 已登入:**
    - **導航:** HomeScreen
- **IF 認證狀態為 null 未登入或訪客:**
    - **導航:** HomeScreen
    - **行為:** 進入訪客模式，使用本地資料庫
    - **立即執行:** 從本機 DB 讀取資料並顯示 UI

## 付費者背景任務

- **檢查條件:** `PremiumLogic.checkPremiumStatus()` 為 True
- **目的:** 依序執行所有必要的付費者背景啟動任務
- **非同步執行:**
    - **定期交易檢查:**
        - **檢查:** `currentDateInUserTZ > lastRecurringCheckDate`
        - **IF True:**
            - **執行:** 補產生邏輯
            - **更新:** `lastRecurringCheckDate`
    - **批次同步自動觸發:**
        - **檢查:** `currentDateInUserTZ > lastSyncCheckDate`  
        - **IF True:**
            - **執行:** 批次同步流程
            - **更新:** `lastSyncCheckDate`