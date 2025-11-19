# 產品組件與價值分配

## 核心目標

- 本文件依據產品定義的產品個體，詳細列出每個組件的價值構成。
- 採用 **雙重價值模型**：每個模組同時包含 **施工價值** (Construction) 與 **維運價值** (Operation)。
- 針對每個 **User Story**，依據 `no2_role_definition.md` 定義的角色進行價值點數分配。

---

## 1. 記帳 App + Firestore, Accounting App

**價值模型:**
- **施工價值, Construction:** 170,000 點 / 次
- **維運價值, Operation:** 1,000 點 / 月

### 1.1 交易與自動化, Transaction & Automation

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **支出管理** | PDM | 1,000 | 5 |
| (Expense CRUD) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 1,000 | 5 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **9,000** | **30** |
| **收入管理** | PDM | 1,000 | 5 |
| (Income CRUD) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 1,000 | 5 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **9,000** | **30** |
| **轉帳管理** | PDM | 1,000 | 5 |
| (Transfer CRUD) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 1,000 | 5 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **9,000** | **30** |
| **定期交易** | PDM | 2,000 | 10 |
| (Recurring) | Designer | 3,000 | 10 |
| | Frontend RD | 8,000 | 20 |
| | Backend RD | 3,000 | 10 |
| | QA | 2,000 | 10 |
| | **Subtotal** | **18,000** | **60** |

### 1.2 資產管理, Asset Management

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **帳戶管理** | PDM | 1,000 | 5 |
| (Account CRUD) | Designer | 1,500 | 5 |
| | Frontend RD | 3,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **6,500** | **25** |
| **類別管理** | PDM | 1,000 | 5 |
| (Category CRUD) | Designer | 1,500 | 5 |
| | Frontend RD | 3,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **6,500** | **25** |
| **預設資料** | PDM | 500 | 2 |
| (Onboarding) | Frontend RD | 2,000 | 5 |
| | QA | 500 | 2 |
| | **Subtotal** | **3,000** | **9** |
| **多幣別支援** | PDM | 1,500 | 5 |
| (Multi-Currency) | Designer | 1,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 2,000 | 5 |
| | QA | 1,500 | 5 |
| | **Subtotal** | **10,000** | **30** |
| **解除限制** | PDM | 500 | 2 |
| (Unlimited) | Frontend RD | 1,000 | 5 |
| | Backend RD | 1,000 | 5 |
| | QA | 500 | 2 |
| | **Subtotal** | **3,000** | **14** |

### 1.3 資料與同步, Data & Sync

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **離線支援** | Frontend RD | 8,000 | 20 |
| (Offline Arch) | QA | 2,000 | 10 |
| | **Subtotal** | **10,000** | **30** |
| **雲端同步** | PDM | 2,000 | 10 |
| (Sync Engine) | Frontend RD | 8,000 | 20 |
| | Backend RD | 15,000 | 50 |
| | QA | 5,000 | 20 |
| | **Subtotal** | **30,000** | **100** |
| **資料匯入** | PDM | 1,000 | 5 |
| (CSV Import) | Frontend RD | 4,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **6,000** | **20** |

### 1.4 儀表板與體驗, Dashboard & Experience

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **首頁儀表板** | PDM | 1,000 | 5 |
| (Home Dash) | Designer | 3,000 | 10 |
| | Frontend RD | 4,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **9,000** | **30** |
| **搜尋功能** | Frontend RD | 2,000 | 5 |
| (Local Search) | QA | 500 | 2 |
| | **Subtotal** | **2,500** | **7** |
| **多語言** | Frontend RD | 2,000 | 5 |
| (i18n) | QA | 500 | 2 |
| | **Subtotal** | **2,500** | **7** |

### 1.5 共用帳本, Shared Ledger

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **預設帳本** | PDM | 1,000 | 5 |
| (Default Book) | Frontend RD | 3,000 | 10 |
| | Backend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **7,000** | **30** |
| **帳本切換** | Designer | 1,000 | 5 |
| (Book Switcher) | Frontend RD | 2,000 | 5 |
| | QA | 500 | 2 |
| | **Subtotal** | **3,500** | **12** |
| **成員邀請** | PDM | 1,000 | 5 |
| (Invitation) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 4,000 | 10 |
| | QA | 2,000 | 5 |
| | **Subtotal** | **13,000** | **35** |
| **協作權限** | PDM | 2,000 | 10 |
| (Collaboration) | Frontend RD | 5,000 | 20 |
| | Backend RD | 10,000 | 30 |
| | QA | 5,000 | 20 |
| | **Subtotal** | **22,000** | **80** |

---

## 2. Web 複雜報表, Web Console

**價值模型:**
- **施工價值, Construction:** 105,000 點 / 次
- **維運價值, Operation:** 850 點 / 月

### 2.1 高密度資料瀏覽, Data Browsing

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **表格視圖** | PDM | 2,000 | 10 |
| (Data Grid) | Designer | 5,000 | 20 |
| | Frontend RD | 15,000 | 50 |
| | QA | 3,000 | 20 |
| | **Subtotal** | **25,000** | **100** |
| **進階匯出** | PDM | 1,000 | 5 |
| (Adv Export) | Frontend RD | 5,000 | 20 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **7,000** | **30** |

### 2.2 進階篩選與查詢, Advanced Query

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **JQL 介面** | PDM | 3,000 | 15 |
| (JQL Interface) | Designer | 2,000 | 10 |
| | Frontend RD | 15,000 | 50 |
| | QA | 5,000 | 25 |
| | **Subtotal** | **25,000** | **100** |
| **視圖儲存** | Frontend RD | 3,000 | 10 |
| (Saved Views) | QA | 1,000 | 5 |
| | **Subtotal** | **4,000** | **15** |

### 2.3 客製化報表, Custom Reporting

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **自訂維度** | PDM | 3,000 | 15 |
| (Custom Charts) | Designer | 5,000 | 20 |
| | Frontend RD | 15,000 | 50 |
| | QA | 5,000 | 25 |
| | **Subtotal** | **28,000** | **110** |
| **報表匯出** | Frontend RD | 3,000 | 10 |
| (Report Export) | QA | 1,000 | 5 |
| | **Subtotal** | **4,000** | **15** |

---

## 3. AI 個人化建議, AI Advisor

**價值模型:**
- **施工價值, Construction:** 100,000 點 / 次
- **維運價值, Operation:** 1,700 點 / 月

### 3.1 智慧偵測, Intelligent Detection

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **異常通知** | PDM | 2,000 | 10 |
| (Anomaly Alert) | AI Engineer | 15,000 | 100 |
| | Backend RD | 5,000 | 20 |
| | Frontend RD | 2,000 | 10 |
| | QA | 2,000 | 10 |
| | **Subtotal** | **26,000** | **150** |
| **重複偵測** | AI Engineer | 10,000 | 50 |
| (Duplicate) | Backend RD | 3,000 | 10 |
| | Frontend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **16,000** | **75** |

### 3.2 預測與診斷, Forecast & Diagnosis

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **現金流預測** | PDM | 2,000 | 10 |
| (Cashflow) | AI Engineer | 15,000 | 100 |
| | Backend RD | 5,000 | 20 |
| | Frontend RD | 3,000 | 10 |
| | QA | 2,000 | 10 |
| | **Subtotal** | **27,000** | **150** |
| **健康評分** | AI Engineer | 10,000 | 50 |
| (Health Score) | Backend RD | 3,000 | 10 |
| | Frontend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **16,000** | **75** |
| **AI 對話** | PDM | 2,000 | 10 |
| (AI Chat) | AI Engineer | 5,000 | 50 |
| | Backend RD | 5,000 | 20 |
| | Frontend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Subtotal** | **15,000** | **95** |

---

## 4. 總經分析報表與 API, Macro Data Service

**價值模型:**
- **施工價值, Construction:** 80,000 點 / 次
- **維運價值, Operation:** 2,500 點 / 月

### 4.1 B 端數據服務, B2B Data Services

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **市場儀表板** | PDM | 2,000 | 20 |
| (Dashboard) | Data Engineer | 10,000 | 100 |
| | Frontend RD | 8,000 | 50 |
| | QA | 2,000 | 20 |
| | **Subtotal** | **22,000** | **190** |
| **競品分析** | PDM | 2,000 | 20 |
| (Competitor) | Data Engineer | 10,000 | 100 |
| | Frontend RD | 8,000 | 50 |
| | QA | 2,000 | 20 |
| | **Subtotal** | **22,000** | **190** |
| **總經 API** | PDM | 2,000 | 20 |
| (Macro API) | Data Engineer | 10,000 | 100 |
| | Backend RD | 8,000 | 50 |
| | QA | 2,000 | 20 |
| | **Subtotal** | **22,000** | **190** |
| **隱私合規** | PDM | 2,000 | 20 |
| (Privacy) | Data Engineer | 10,000 | 100 |
| | Backend RD | 2,000 | 20 |
| | QA | 2,000 | 20 |
| | **Subtotal** | **16,000** | **160** |

---

## 價值彙整

| 產品組件 | 施工價值, 點 | 維運價值, 點/月 |
| :--- | :--- | :--- |
| 1. 記帳 App + Firestore | 170,000 | 1,000 |
| 2. Web 複雜報表 | 105,000 | 850 |
| 3. AI 個人化建議 | 100,000 | 1,700 |
| 4. 總經分析報表與 API | 80,000 | 2,500 |
| **總計** | **455,000** | **6,050** |
