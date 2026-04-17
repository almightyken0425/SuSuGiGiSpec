# 設定: SettingsScreen

## 畫面目標

- 提供存取所有帳戶、資料與偏好設定的中心化入口

---

## 線框圖

```text
+--------------------------------+
| < Back      Settings           |
+--------------------------------+
| Data Management                |
|  [Icon] Categories             |
|  [Icon] Accounts               |
|  [Icon] Currency Rates         |
|  [Icon] Import Data            |
|                                |
| Preferences                    |
|  [Icon] Preferences            |
|                                |
| Upgrade                        |
|  [Icon] Upgrade to Premium     |
+--------------------------------+
```

---

## 佈局

### 導覽列

- 返回按鈕
- 設定 標題

### 設定列表

- 資料管理 分組
  - 類別管理 入口
  - 帳戶管理 入口
  - 匯率管理 入口
  - 匯入資料 入口
- 偏好設定 分組
  - 偏好設定 入口
- **IF** 未訂閱付費版:
  - 升級 分組
    - 升級至付費版 入口

---

## 互動

- **點按返回按鈕:**
  - 返回上一頁

- **點按類別管理:**
  - 導航至 CategoryListScreen

- **點按帳戶管理:**
  - 導航至 AccountListScreen

- **點按匯率管理:**
  - **IF** = Tier0:
    - 導航至 PaywallScreen
  - **IF** > Tier0:
    - 導航至 CurrencyRateListScreen

- **點按匯入資料:**
  - 導航至 ImportWizardScreen

- **點按偏好設定:**
  - 導航至 PreferenceScreen

- **點按升級至付費版:**
  - 導航至 PaywallScreen
