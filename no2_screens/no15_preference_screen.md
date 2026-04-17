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
|  [ Login / Logout ]            |
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
- 本地化 分組
  - 主要貨幣 入口
    - 顯示當前設定的基礎貨幣代碼
  - 時區 入口
    - 顯示當前設定的時區
  - 語系 入口
    - 顯示當前 App 語言
- 資料同步 分組
  - 立即同步 按鈕
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

- **點按主要貨幣:**
  - 展開貨幣選擇器
  - 支援輸入幣別代碼或名稱篩選

- **選擇主要貨幣:**
  - 呼叫 updateBaseCurrency
  - 收合貨幣選擇器

- **點按時區:**
  - 展開時區選擇器

- **選擇時區:**
  - 呼叫 updateTimeZone
  - 收合時區選擇器

- **點按語系:**
  - 展開語系選擇器

- **選擇語系:**
  - 呼叫 updateLanguage
  - 收合語系選擇器
  - 即時切換 App 顯示語言

- **點按立即同步:**
  - 呼叫 syncNow

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
