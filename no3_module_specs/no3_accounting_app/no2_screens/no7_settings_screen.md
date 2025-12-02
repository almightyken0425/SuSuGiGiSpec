# 設定主頁畫面: SettingsScreen

## 畫面目標

- **提供:** 存取所有帳戶、資料、偏好設定的中心化入口
- **提供:** 登出與升級至付費版的路徑

```text
+--------------------------------+
| < Back      Settings           |
+--------------------------------+
| Data Management                |
|  [Icon] Categories             |
|  [Icon] Accounts               |
|  [Icon] Currency Rates (Pro)   |
|  [Icon] Import Data (Pro)      |
|                                |
| Preferences                    |
|  [Icon] Preferences            |
|                                |
| Upgrade                        |
|  [Icon] Upgrade to Premium     |
|                                |
| Account                        |
|  [Logout]                      |
+--------------------------------+
```

---

## UI 佈局

- **頂部導航列:**
    - `返回按鈕`
        - **導航:** HomeScreen
    - `標題` 設定
- **設定列表:**
    - **資料管理:**
        - `類別管理`
            - **導航:** CategoryListScreen
        - `帳戶管理`
            - **導航:** AccountListScreen
        - `匯率管理` Premium 標籤
            - **導航:** CurrencyRateListScreen
            - **權限:** 點擊時檢查付費狀態
        - `匯入資料` Premium 標籤
            - **導航:** ImportScreen
            - **權限:** 點擊時檢查付費狀態
    - **偏好設定:**
        - `偏好設定`
            - **導航:** PreferenceScreen
    - **升級:**
        - `升級至 Premium`
            - **樣式:** 醒目項目
            - **可見性:** 僅免費版使用者顯示
            - **導航:** PaywallScreen
    - **帳號:**
        - `登出`
            - **樣式:** 紅色文字按鈕
            - **行為:** 觸發登出邏輯

---

## 核心邏輯

- **付費功能檢查:**
    - **觸發:** 畫面載入
    - **行為:** 讀取 `PremiumContext.isPremiumUser` 狀態
    - **IF 免費版:**
        - **匯率管理或匯入資料點擊:** 導航 PaywallScreen
    - **升級至 Premium 項目:**
        - **行為:** 依 `isPremiumUser` 狀態動態顯示或隱藏
- **登出邏輯:**
    - **觸發:** 點擊登出按鈕
    - **行為:** 顯示確認對話框
    - **成功:**
        - **行為:** 呼叫 `authService.signOut()`
    - **監聽:**
        - **目標:** AuthContext 認證狀態變化
        - **行為:** AppNavigator 自動切換回 LoginScreen

---

## 導航

- **進入:**
    - **來源:** HomeScreen 設定圖示點擊
- **退出:**
    - **觸發:** 頂部導航列返回按鈕點擊
    - **導航:** HomeScreen