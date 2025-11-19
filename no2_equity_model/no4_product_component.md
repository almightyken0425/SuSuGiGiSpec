# 產品組件與價值分配

## 核心目標

- 本文件依據產品定義的產品個體，詳細列出每個組件的價值構成。
- 採用 **雙重價值模型**：每個模組同時包含 **施工價值** (Construction) 與 **維運價值** (Operation)。
- 針對每個 **User Story**，依據 `no2_role_definition.md` 定義的角色進行價值點數分配。
- **營運角色整合:** Marketing 與 Operations 角色整合至每個 User Story 中，其施工價值為 0，但隨著功能上線，其維運價值 (Operation Value) 將逐步累積。

---

## 1. 記帳 App + Firestore, Accounting App

**價值模型:**
- **施工價值, Construction:** 170,000 點 / 次
- **維運價值, Operation:** 3,000 點 / 月

### 1.1 交易與自動化, Transaction & Automation

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **支出管理** | PDM | 1,000 | 5 |
| (Expense CRUD) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 1,000 | 5 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **9,000** | **60** |
| **收入管理** | PDM | 1,000 | 5 |
| (Income CRUD) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 1,000 | 5 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **9,000** | **60** |
| **轉帳管理** | PDM | 1,000 | 5 |
| (Transfer CRUD) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 1,000 | 5 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **9,000** | **60** |
| **定期交易** | PDM | 2,000 | 10 |
| (Recurring) | Designer | 3,000 | 10 |
| | Frontend RD | 8,000 | 20 |
| | Backend RD | 3,000 | 10 |
| | QA | 2,000 | 10 |
| | **Marketing** | **0** | **30** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **18,000** | **100** |

### 1.2 資產管理, Asset Management

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **帳戶管理** | PDM | 1,000 | 5 |
| (Account CRUD) | Designer | 1,500 | 5 |
| | Frontend RD | 3,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **6,500** | **55** |
| **類別管理** | PDM | 1,000 | 5 |
| (Category CRUD) | Designer | 1,500 | 5 |
| | Frontend RD | 3,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **6,500** | **55** |
| **預設資料** | PDM | 500 | 2 |
| (Onboarding) | Frontend RD | 2,000 | 5 |
| | QA | 500 | 2 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **3,000** | **24** |
| **多幣別支援** | PDM | 1,500 | 5 |
| (Multi-Currency) | Designer | 1,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 2,000 | 5 |
| | QA | 1,500 | 5 |
| | **Marketing** | **0** | **30** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **10,000** | **70** |
| **解除限制** | PDM | 500 | 2 |
| (Unlimited) | Frontend RD | 1,000 | 5 |
| | Backend RD | 1,000 | 5 |
| | QA | 500 | 2 |
| | **Marketing** | **0** | **50** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **3,000** | **84** |

### 1.3 資料與同步, Data & Sync

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **離線支援** | Frontend RD | 8,000 | 20 |
| (Offline Arch) | QA | 2,000 | 10 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **10,000** | **45** |
| **雲端同步** | PDM | 2,000 | 10 |
| (Sync Engine) | Frontend RD | 8,000 | 20 |
| | Backend RD | 15,000 | 50 |
| | QA | 5,000 | 20 |
| | **Marketing** | **0** | **50** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **30,000** | **170** |
| **資料匯入** | PDM | 1,000 | 5 |
| (CSV Import) | Frontend RD | 4,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **6,000** | **35** |

### 1.4 儀表板與體驗, Dashboard & Experience

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **首頁儀表板** | PDM | 1,000 | 5 |
| (Home Dash) | Designer | 3,000 | 10 |
| | Frontend RD | 4,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **9,000** | **60** |
| **搜尋功能** | Frontend RD | 2,000 | 5 |
| (Local Search) | QA | 500 | 2 |
| | **Marketing** | **0** | **5** |
| | **Operations** | **0** | **2** |
| | **Subtotal** | **2,500** | **14** |
| **多語言** | Frontend RD | 2,000 | 5 |
| (i18n) | QA | 500 | 2 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **2,500** | **32** |

### 1.5 共用帳本, Shared Ledger

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **預設帳本** | PDM | 1,000 | 5 |
| (Default Book) | Frontend RD | 3,000 | 10 |
| | Backend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **7,000** | **45** |
| **帳本切換** | Designer | 1,000 | 5 |
| (Book Switcher) | Frontend RD | 2,000 | 5 |
| | QA | 500 | 2 |
| | **Marketing** | **0** | **5** |
| | **Operations** | **0** | **2** |
| | **Subtotal** | **3,500** | **19** |
| **成員邀請** | PDM | 1,000 | 5 |
| (Invitation) | Designer | 2,000 | 5 |
| | Frontend RD | 4,000 | 10 |
| | Backend RD | 4,000 | 10 |
| | QA | 2,000 | 5 |
| | **Marketing** | **0** | **50** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **13,000** | **105** |
| **協作權限** | PDM | 2,000 | 10 |
| (Collaboration) | Frontend RD | 5,000 | 20 |
| | Backend RD | 10,000 | 30 |
| | QA | 5,000 | 20 |
| | **Marketing** | **0** | **30** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **22,000** | **120** |

---

## 2. Web 複雜報表, Web Console

**價值模型:**
- **施工價值, Construction:** 105,000 點 / 次
- **維運價值, Operation:** 2,500 點 / 月

### 2.1 高密度資料瀏覽, Data Browsing

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **表格視圖** | PDM | 2,000 | 10 |
| (Data Grid) | Designer | 5,000 | 20 |
| | Frontend RD | 15,000 | 50 |
| | QA | 3,000 | 20 |
| | **Marketing** | **0** | **100** |
| | **Operations** | **0** | **50** |
| | **Subtotal** | **25,000** | **250** |
| **進階匯出** | PDM | 1,000 | 5 |
| (Adv Export) | Frontend RD | 5,000 | 20 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **30** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **7,000** | **70** |

### 2.2 進階篩選與查詢, Advanced Query

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **JQL 介面** | PDM | 3,000 | 15 |
| (JQL Interface) | Designer | 2,000 | 10 |
| | Frontend RD | 15,000 | 50 |
| | QA | 5,000 | 25 |
| | **Marketing** | **0** | **50** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **25,000** | **170** |
| **視圖儲存** | Frontend RD | 3,000 | 10 |
| (Saved Views) | QA | 1,000 | 5 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **4,000** | **30** |

### 2.3 客製化報表, Custom Reporting

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **自訂維度** | PDM | 3,000 | 15 |
| (Custom Charts) | Designer | 5,000 | 20 |
| | Frontend RD | 15,000 | 50 |
| | QA | 5,000 | 25 |
| | **Marketing** | **0** | **100** |
| | **Operations** | **0** | **50** |
| | **Subtotal** | **28,000** | **260** |
| **報表匯出** | Frontend RD | 3,000 | 10 |
| (Report Export) | QA | 1,000 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **4,000** | **45** |

---

## 3. AI 個人化建議, AI Advisor

**價值模型:**
- **施工價值, Construction:** 100,000 點 / 次
- **維運價值, Operation:** 3,500 點 / 月

### 3.1 智慧偵測, Intelligent Detection

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **異常通知** | PDM | 2,000 | 10 |
| (Anomaly Alert) | AI Engineer | 15,000 | 100 |
| | Backend RD | 5,000 | 20 |
| | Frontend RD | 2,000 | 10 |
| | QA | 2,000 | 10 |
| | **Marketing** | **0** | **100** |
| | **Operations** | **0** | **50** |
| | **Subtotal** | **26,000** | **300** |
| **重複偵測** | AI Engineer | 10,000 | 50 |
| (Duplicate) | Backend RD | 3,000 | 10 |
| | Frontend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **50** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **16,000** | **145** |

### 3.2 預測與診斷, Forecast & Diagnosis

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **現金流預測** | PDM | 2,000 | 10 |
| (Cashflow) | AI Engineer | 15,000 | 100 |
| | Backend RD | 5,000 | 20 |
| | Frontend RD | 3,000 | 10 |
| | QA | 2,000 | 10 |
| | **Marketing** | **0** | **150** |
| | **Operations** | **0** | **50** |
| | **Subtotal** | **27,000** | **350** |
| **健康評分** | AI Engineer | 10,000 | 50 |
| (Health Score) | Backend RD | 3,000 | 10 |
| | Frontend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **50** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **16,000** | **145** |
| **AI 對話** | PDM | 2,000 | 10 |
| (AI Chat) | AI Engineer | 5,000 | 50 |
| | Backend RD | 5,000 | 20 |
| | Frontend RD | 2,000 | 10 |
| | QA | 1,000 | 5 |
| | **Marketing** | **0** | **100** |
| | **Operations** | **0** | **50** |
| | **Subtotal** | **15,000** | **245** |

---

## 4. 總經分析報表與 API, Macro Data Service

**價值模型:**
- **施工價值, Construction:** 80,000 點 / 次
- **維運價值, Operation:** 5,000 點 / 月

### 4.1 B 端數據服務, B2B Data Services

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **市場儀表板** | PDM | 2,000 | 20 |
| (Dashboard) | Data Engineer | 10,000 | 100 |
| | Frontend RD | 8,000 | 50 |
| | QA | 2,000 | 20 |
| | **Marketing** | **0** | **200** |
| | **Operations** | **0** | **100** |
| | **Subtotal** | **22,000** | **490** |
| **競品分析** | PDM | 2,000 | 20 |
| (Competitor) | Data Engineer | 10,000 | 100 |
| | Frontend RD | 8,000 | 50 |
| | QA | 2,000 | 20 |
| | **Marketing** | **0** | **200** |
| | **Operations** | **0** | **100** |
| | **Subtotal** | **22,000** | **490** |
| **總經 API** | PDM | 2,000 | 20 |
| (Macro API) | Data Engineer | 10,000 | 100 |
| | Backend RD | 8,000 | 50 |
| | QA | 2,000 | 20 |
| | **Marketing** | **0** | **200** |
| | **Operations** | **0** | **100** |
| | **Subtotal** | **22,000** | **490** |
| **隱私合規** | PDM | 2,000 | 20 |
| (Privacy) | Data Engineer | 10,000 | 100 |
| | Backend RD | 2,000 | 20 |
| | QA | 2,000 | 20 |
| | **Marketing** | **0** | **50** |
| | **Operations** | **0** | **50** |
| | **Subtotal** | **16,000** | **260** |

---

## 價值彙整

| 產品組件 | 施工價值, 點 | 維運價值, 點/月 |
| :--- | :--- | :--- |
| 1. 記帳 App + Firestore | 170,000 | 3,000 |
| 2. Web 複雜報表 | 105,000 | 2,500 |
| 3. AI 個人化建議 | 100,000 | 3,500 |
| 4. 總經分析報表與 API | 80,000 | 5,000 |
| **總計** | **455,000** | **14,000** |
