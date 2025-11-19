# 產品組件與價值分配

## 核心目標

- 本文件依據產品定義的產品個體，詳細列出每個組件的價值構成。
- 採用 **雙重價值模型**：每個模組同時包含 **施工價值** (Construction) 與 **維運價值** (Operation)。
- 針對每個 **User Story**，依據角色定義進行價值點數分配。
- **營運角色整合:** Marketing 與 Operations 角色整合至每個 User Story 中，其施工價值為 0，但隨著功能上線，其維運價值 (Operation Value) 將逐步累積。
- **價值單位:** 1 點 = 0.1 小時，詳見股權原則文件。

---

## 1. 記帳 App + Firestore, Accounting App

**價值模型:**
- **施工價值, Construction:** 20,250 點 / 次 (2,025 小時 = 10.1 人月)
- **維運價值, Operation:** 1,081 點 / 月 (108 小時/月)

### 1.1 交易與自動化, Transaction & Automation

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **支出管理** | PDM | 100 | 3 |
| (Expense CRUD) | Designer | 200 | 3 |
| | Frontend RD | 400 | 8 |
| | Backend RD | 100 | 3 |
| | QA | 100 | 3 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **900** | **35** |
| **收入管理** | PDM | 100 | 3 |
| (Income CRUD) | Designer | 200 | 3 |
| | Frontend RD | 400 | 8 |
| | Backend RD | 100 | 3 |
| | QA | 100 | 3 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **900** | **35** |
| **轉帳管理** | PDM | 120 | 3 |
| (Transfer CRUD) | Designer | 200 | 3 |
| | Frontend RD | 500 | 8 |
| | Backend RD | 150 | 3 |
| | QA | 130 | 3 |
| | **Marketing** | **0** | **10** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **1,100** | **35** |
| **定期交易** | PDM | 250 | 8 |
| (Recurring) | Designer | 300 | 8 |
| | Frontend RD | 900 | 18 |
| | Backend RD | 400 | 10 |
| | QA | 250 | 8 |
| | **Marketing** | **0** | **30** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **2,100** | **92** |

### 1.2 資產管理, Asset Management

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **帳戶管理** | PDM | 80 | 3 |
| (Account CRUD) | Designer | 150 | 3 |
| | Frontend RD | 300 | 8 |
| | QA | 100 | 3 |
| | **Marketing** | **0** | **8** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **630** | **30** |
| **類別管理** | PDM | 100 | 3 |
| (Category CRUD) | Designer | 150 | 3 |
| | Frontend RD | 350 | 8 |
| | QA | 100 | 3 |
| | **Marketing** | **0** | **8** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **700** | **30** |
| **預設資料** | PDM | 50 | 2 |
| (Onboarding) | Frontend RD | 200 | 5 |
| | QA | 50 | 2 |
| | **Marketing** | **0** | **5** |
| | **Operations** | **0** | **3** |
| | **Subtotal** | **300** | **17** |
| **多幣別支援** | PDM | 150 | 5 |
| (Multi-Currency) | Designer | 100 | 5 |
| | Frontend RD | 450 | 10 |
| | Backend RD | 250 | 8 |
| | QA | 150 | 5 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **10** |
| | **Subtotal** | **1,100** | **63** |
| **解除限制** | PDM | 50 | 2 |
| (Unlimited) | Frontend RD | 100 | 5 |
| | Backend RD | 100 | 5 |
| | QA | 50 | 2 |
| | **Marketing** | **0** | **30** |
| | **Operations** | **0** | **15** |
| | **Subtotal** | **300** | **59** |

### 1.3 資料與同步, Data & Sync

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **離線支援** | Frontend RD | 900 | 20 |
| (Offline Arch) | QA | 250 | 10 |
| | **Marketing** | **0** | **5** |
| | **Operations** | **0** | **3** |
| | **Subtotal** | **1,150** | **38** |
| **雲端同步** | PDM | 200 | 10 |
| (Sync Engine) | Frontend RD | 900 | 25 |
| | Backend RD | 1,800 | 50 |
| | QA | 600 | 25 |
| | **Marketing** | **0** | **40** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **3,500** | **170** |
| **資料匯入** | PDM | 100 | 5 |
| (CSV Import) | Frontend RD | 450 | 10 |
| | QA | 120 | 5 |
| | **Marketing** | **0** | **8** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **670** | **33** |

### 1.4 儀表板與體驗, Dashboard & Experience

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **首頁儀表板** | PDM | 120 | 5 |
| (Home Dash) | Designer | 350 | 10 |
| | Frontend RD | 500 | 12 |
| | QA | 130 | 5 |
| | **Marketing** | **0** | **15** |
| | **Operations** | **0** | **8** |
| | **Subtotal** | **1,100** | **55** |
| **搜尋功能** | Frontend RD | 220 | 5 |
| (Local Search) | QA | 60 | 2 |
| | **Marketing** | **0** | **3** |
| | **Operations** | **0** | **2** |
| | **Subtotal** | **280** | **12** |
| **多語言** | Frontend RD | 250 | 6 |
| (i18n) | QA | 70 | 3 |
| | **Marketing** | **0** | **12** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **320** | **26** |

### 1.5 共用帳本, Shared Ledger

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **預設帳本** | PDM | 100 | 5 |
| (Default Book) | Frontend RD | 300 | 10 |
| | Backend RD | 200 | 10 |
| | QA | 100 | 5 |
| | **Marketing** | **0** | **8** |
| | **Operations** | **0** | **5** |
| | **Subtotal** | **700** | **43** |
| **帳本切換** | Designer | 100 | 5 |
| (Book Switcher) | Frontend RD | 220 | 6 |
| | QA | 60 | 3 |
| | **Marketing** | **0** | **5** |
| | **Operations** | **0** | **3** |
| | **Subtotal** | **380** | **22** |
| **成員邀請** | PDM | 120 | 6 |
| (Invitation) | Designer | 220 | 6 |
| | Frontend RD | 450 | 12 |
| | Backend RD | 500 | 12 |
| | QA | 230 | 6 |
| | **Marketing** | **0** | **60** |
| | **Operations** | **0** | **20** |
| | **Subtotal** | **1,520** | **122** |
| **協作權限** | PDM | 250 | 12 |
| (Collaboration) | Frontend RD | 600 | 25 |
| | Backend RD | 1,200 | 35 |
| | QA | 550 | 22 |
| | **Marketing** | **0** | **55** |
| | **Operations** | **0** | **15** |
| | **Subtotal** | **2,600** | **164** |

---

## 2. Web 複雜報表, Web Console

**價值模型:**
- **施工價值, Construction:** 11,090 點 / 次 (1,109 小時 = 5.5 人月)
- **維運價值, Operation:** 795 點 / 月 (79.5 小時/月)

### 2.1 高密度資料瀏覽, Data Browsing

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **表格視圖** | PDM | 250 | 12 |
| (Data Grid) | Designer | 600 | 22 |
| | Frontend RD | 1,800 | 55 |
| | QA | 400 | 22 |
| | **Marketing** | **0** | **80** |
| | **Operations** | **0** | **40** |
| | **Subtotal** | **3,050** | **231** |
| **進階匯出** | PDM | 100 | 5 |
| (Adv Export) | Frontend RD | 550 | 22 |
| | QA | 120 | 6 |
| | **Marketing** | **0** | **20** |
| | **Operations** | **0** | **8** |
| | **Subtotal** | **770** | **61** |

### 2.2 進階篩選與查詢, Advanced Query

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **JQL 介面** | PDM | 350 | 18 |
| (JQL Interface) | Designer | 230 | 12 |
| | Frontend RD | 1,800 | 58 |
| | QA | 600 | 28 |
| | **Marketing** | **0** | **45** |
| | **Operations** | **0** | **18** |
| | **Subtotal** | **2,980** | **179** |
| **視圖儲存** | Frontend RD | 350 | 12 |
| (Saved Views) | QA | 120 | 6 |
| | **Marketing** | **0** | **8** |
| | **Operations** | **0** | **4** |
| | **Subtotal** | **470** | **30** |

### 2.3 客製化報表, Custom Reporting

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **自訂維度** | PDM | 350 | 18 |
| (Custom Charts) | Designer | 600 | 22 |
| | Frontend RD | 1,800 | 58 |
| | QA | 600 | 28 |
| | **Marketing** | **0** | **85** |
| | **Operations** | **0** | **42** |
| | **Subtotal** | **3,350** | **253** |
| **報表匯出** | Frontend RD | 350 | 12 |
| (Report Export) | QA | 120 | 6 |
| | **Marketing** | **0** | **15** |
| | **Operations** | **0** | **8** |
| | **Subtotal** | **470** | **41** |

---

## 3. AI 個人化建議, AI Advisor

**價值模型:**
- **施工價值, Construction:** 11,500 點 / 次 (1,150 小時 = 5.8 人月)
- **維運價值, Operation:** 1,200 點 / 月 (120 小時/月)

### 3.1 智慧偵測, Intelligent Detection

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **異常通知** | PDM | 230 | 12 |
| (Anomaly Alert) | AI Engineer | 1,700 | 110 |
| | Backend RD | 600 | 22 |
| | Frontend RD | 230 | 12 |
| | QA | 240 | 12 |
| | **Marketing** | **0** | **95** |
| | **Operations** | **0** | **45** |
| | **Subtotal** | **3,000** | **308** |
| **重複偵測** | AI Engineer | 1,100 | 55 |
| (Duplicate) | Backend RD | 350 | 12 |
| | Frontend RD | 230 | 12 |
| | QA | 120 | 6 |
| | **Marketing** | **0** | **48** |
| | **Operations** | **0** | **18** |
| | **Subtotal** | **1,800** | **151** |

### 3.2 預測與診斷, Forecast & Diagnosis

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **現金流預測** | PDM | 230 | 12 |
| (Cashflow) | AI Engineer | 1,700 | 110 |
| | Backend RD | 600 | 22 |
| | Frontend RD | 350 | 12 |
| | QA | 240 | 12 |
| | **Marketing** | **0** | **135** |
| | **Operations** | **0** | **45** |
| | **Subtotal** | **3,120** | **348** |
| **健康評分** | AI Engineer | 1,100 | 55 |
| (Health Score) | Backend RD | 350 | 12 |
| | Frontend RD | 230 | 12 |
| | QA | 120 | 6 |
| | **Marketing** | **0** | **45** |
| | **Operations** | **0** | **18** |
| | **Subtotal** | **1,800** | **148** |
| **AI 對話** | PDM | 230 | 12 |
| (AI Chat) | AI Engineer | 600 | 58 |
| | Backend RD | 600 | 22 |
| | Frontend RD | 230 | 12 |
| | QA | 120 | 6 |
| | **Marketing** | **0** | **90** |
| | **Operations** | **0** | **45** |
| | **Subtotal** | **1,780** | **245** |

---

## 4. 總經分析報表與 API, Macro Data Service

**價值模型:**
- **施工價值, Construction:** 9,570 點 / 次 (957 小時 = 4.8 人月)
- **維運價值, Operation:** 1,712 點 / 月 (171.2 小時/月)

### 4.1 B 端數據服務, B2B Data Services

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **市場儀表板** | PDM | 230 | 22 |
| (Dashboard) | Data Engineer | 1,150 | 110 |
| | Frontend RD | 950 | 58 |
| | QA | 240 | 22 |
| | **Marketing** | **0** | **180** |
| | **Operations** | **0** | **90** |
| | **Subtotal** | **2,570** | **482** |
| **競品分析** | PDM | 230 | 22 |
| (Competitor) | Data Engineer | 1,150 | 110 |
| | Frontend RD | 950 | 58 |
| | QA | 240 | 22 |
| | **Marketing** | **0** | **180** |
| | **Operations** | **0** | **90** |
| | **Subtotal** | **2,570** | **482** |
| **總經 API** | PDM | 230 | 22 |
| (Macro API) | Data Engineer | 1,150 | 110 |
| | Backend RD | 950 | 58 |
| | QA | 240 | 22 |
| | **Marketing** | **0** | **180** |
| | **Operations** | **0** | **90** |
| | **Subtotal** | **2,570** | **482** |
| **隱私合規** | PDM | 230 | 22 |
| (Privacy) | Data Engineer | 1,150 | 110 |
| | Backend RD | 240 | 22 |
| | QA | 240 | 22 |
| | **Marketing** | **0** | **45** |
| | **Operations** | **0** | **45** |
| | **Subtotal** | **1,860** | **266** |

---

## 價值彙整

| 產品組件 | 施工價值 (點) | 施工工時 | 維運價值 (點/月) | 年化維運 |
| :--- | ---: | ---: | ---: | ---: |
| 1. 記帳 App + Firestore | 20,250 | 10.1 人月 | 1,081 | 12,972 |
| 2. Web 複雜報表 | 11,090 | 5.5 人月 | 795 | 9,540 |
| 3. AI 個人化建議 | 11,500 | 5.8 人月 | 1,200 | 14,400 |
| 4. 總經分析報表與 API | 9,570 | 4.8 人月 | 1,712 | 20,544 |
| **總計** | **52,410** | **26.2 人月** | **4,788** | **57,456** |
