# 偏好設定: PreferenceScreen

## 畫面目標

- 提供設定 App 核心行為的介面

---

## 線框圖

```text
+--------------------------------+
| <           Preferences        |
+--------------------------------+
|  Launch Mode: Default >        |
+--------------------------------+
|  Base Currency: TWD >          |
|  Currency Format Settings >    |
|  Exchange Rates >              |
+--------------------------------+
|  Language: 繁體中文 >          |
|  Time Zone: Asia/Taipei >      |
|  Week Start: 跟隨語系 >        |
+--------------------------------+
|  Allow Financial Analysis [ON] |
|  Share Usage Data         [OFF]|
+--------------------------------+
```

---

## 佈局

### 導覽列

- Header 模式: A
- 返回按鈕
- 偏好設定 標題

### 設定列表

- List 模式: A
- 各分組以空白間距區隔
- 不顯示分組標題文字
- 第一組
  - 啟動模式 入口
    - 顯示當前啟動模式
- 第二組
  - 主要貨幣 入口
    - 顯示當前設定的主要貨幣代碼
  - 貨幣格式設定 入口
  - 匯率管理 入口
- 第三組
  - 語系 入口
    - 顯示當前 App 語言
  - 時區 入口
    - 顯示當前設定的時區
  - 週起始日 入口
    - 顯示當前週起始日選項
- 第四組
  - 財務分析同意 開關
    - 顯示 analyticsConsent 目前狀態
  - 使用分析同意 開關
    - 顯示 usageAnalyticsConsent 目前狀態
    - 說明不含記帳內容

---

## 互動

- **點按返回按鈕:**
  - 返回上一頁

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

- **點按週起始日:**
  - 導航至 WeekStartSettingScreen

- **切換財務分析同意開關:**
  - 呼叫 setAnalyticsConsent
  - 即時生效

- **切換使用分析同意開關:**
  - 呼叫 setUsageAnalyticsConsent
  - 即時生效
