# 偏好設定: PreferenceScreen

## 畫面目標

- 提供設定 App 核心行為的介面

---

## 線框圖

```text
+--------------------------------+
| < Back      Preferences        |
+--------------------------------+
| Appearance                     |
|  Theme: Current Theme >        |
|  Launch Mode: Default >        |
|                                |
| Currency & Finance             |
|  Base Currency: TWD >          |
|  Currency Format Settings >    |
|  Exchange Rates >              |
|                                |
| Region & Language              |
|  Language: 繁體中文 >          |
|  Time Zone: Asia/Taipei >      |
|                                |
| Account                        |
|  Login / Logout                |
+--------------------------------+
```

---

## 佈局

### 導覽列

- 返回按鈕
- 偏好設定 標題

### 設定列表

- 外觀 分組
  - 配色主題 入口
    - 顯示當前主題名稱
  - 啟動模式 入口
    - 顯示當前啟動模式
- 貨幣與財務 分組
  - 主要貨幣 入口
    - 顯示當前設定的基礎貨幣代碼
  - 貨幣格式設定 入口
  - 匯率管理 入口
- 地區與語言 分組
  - 語系 入口
    - 顯示當前 App 語言
  - 時區 入口
    - 顯示當前設定的時區
- 帳號 分組
  - **IF** 已登入:
    - 登出 按鈕
  - **IF** 未登入:
    - 登入 按鈕

---

## 互動

- **點按返回按鈕:**
  - 返回上一頁

- **點按配色主題:**
  - 導航至 ThemeSettingsScreen

- **點按啟動模式:**
  - 導航至 LaunchModeSettingScreen

- **點按主要貨幣:**
  - 導航至 BaseCurrencySettingScreen

- **點按貨幣格式設定:**
  - 導航至 CurrencyListScreen

- **點按匯率管理:**
  - 導航至 CurrencyRateListScreen

- **點按語系:**
  - 導航至 LanguageSettingScreen

- **點按時區:**
  - 導航至 TimeZoneSettingScreen

- **點按登出:**
  - 顯示登出確認對話框
  - **IF** 確認登出:
    - 呼叫 signOut
    - **IF** 操作成功:
      - 導航至 LoginScreen
    - **IF** 操作失敗:
      - 顯示錯誤提示

- **點按登入:**
  - 導航至 LoginScreen
