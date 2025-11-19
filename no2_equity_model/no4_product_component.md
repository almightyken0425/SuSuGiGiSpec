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
- **施工價值, Construction:** 22,960 點 / 次 (2,296 小時 = 11.5 人月)
- **維運價值, Operation:** 1,078 點 / 月 (107.8 小時/月)

### 1.1 交易與自動化, Transaction & Automation

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **支出管理** | PDM | 150 | 3 |
| (Expense CRUD) | PJM | 90 | 2 |
|  | Designer | 400 | 8 |
|  | Frontend RD | 100 | 3 |
|  | Backend RD | 100 | 3 |
|  | Data Engineer | 0 | 10 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **840** | **34** |
| **收入管理** | PDM | 150 | 3 |
| (Income CRUD) | PJM | 90 | 2 |
|  | Designer | 400 | 8 |
|  | Frontend RD | 100 | 3 |
|  | Backend RD | 100 | 3 |
|  | Data Engineer | 0 | 10 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **840** | **34** |
| **轉帳管理** | PDM | 200 | 3 |
| (Transfer CRUD) | PJM | 120 | 2 |
|  | Designer | 500 | 8 |
|  | Frontend RD | 150 | 3 |
|  | Backend RD | 130 | 3 |
|  | Data Engineer | 0 | 10 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **1,100** | **34** |
| **定期交易** | PDM | 390 | 8 |
| (Recurring) | PJM | 230 | 5 |
|  | Designer | 900 | 18 |
|  | Frontend RD | 400 | 10 |
|  | Backend RD | 250 | 8 |
|  | Data Engineer | 0 | 30 |
|  | **Marketing** | **0** | **10** |
| | **Subtotal** | **2,170** | **89** |

### 1.2 資產管理, Asset Management

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **帳戶管理** | PDM | 100 | 3 |
| (Account CRUD) | PJM | 60 | 2 |
|  | Designer | 300 | 8 |
|  | Backend RD | 100 | 3 |
|  | Data Engineer | 0 | 8 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **560** | **29** |
| **類別管理** | PDM | 110 | 3 |
| (Category CRUD) | PJM | 70 | 2 |
|  | Designer | 350 | 8 |
|  | Backend RD | 100 | 3 |
|  | Data Engineer | 0 | 8 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **630** | **29** |
| **預設資料** | PDM | 60 | 2 |
| (Onboarding) | PJM | 40 | 1 |
|  | Designer | 200 | 5 |
|  | Backend RD | 50 | 2 |
|  | Data Engineer | 0 | 5 |
|  | **Marketing** | **0** | **3** |
| | **Subtotal** | **350** | **18** |
| **多幣別支援** | PDM | 210 | 5 |
| (Multi-Currency) | PJM | 130 | 3 |
|  | Designer | 450 | 10 |
|  | Frontend RD | 250 | 8 |
|  | Backend RD | 150 | 5 |
|  | Data Engineer | 0 | 20 |
|  | **Marketing** | **0** | **10** |
| | **Subtotal** | **1,190** | **61** |
| **解除限制** | PDM | 60 | 2 |
| (Unlimited) | PJM | 40 | 1 |
|  | Designer | 100 | 5 |
|  | Frontend RD | 100 | 5 |
|  | Backend RD | 50 | 2 |
|  | Data Engineer | 0 | 30 |
|  | **Marketing** | **0** | **15** |
| | **Subtotal** | **350** | **60** |

### 1.3 資料與同步, Data & Sync

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **離線支援** | PDM | 290 | 0 |
| (Offline Arch) | PJM | 170 | 0 |
|  | Designer | 900 | 20 |
|  | Backend RD | 250 | 10 |
|  | Data Engineer | 0 | 5 |
|  | **Marketing** | **0** | **3** |
| | **Subtotal** | **1,610** | **38** |
| **雲端同步** | PDM | 820 | 10 |
| (Sync Engine) | PJM | 500 | 6 |
|  | Designer | 900 | 25 |
|  | Frontend RD | 1,800 | 50 |
|  | Backend RD | 600 | 25 |
|  | Data Engineer | 0 | 40 |
|  | **Marketing** | **0** | **20** |
| | **Subtotal** | **4,620** | **176** |
| **資料匯入** | PDM | 140 | 5 |
| (CSV Import) | PJM | 90 | 3 |
|  | Designer | 450 | 10 |
|  | Backend RD | 120 | 5 |
|  | Data Engineer | 0 | 8 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **800** | **36** |

### 1.4 儀表板與體驗, Dashboard & Experience

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **首頁儀表板** | PDM | 160 | 5 |
| (Home Dash) | PJM | 90 | 3 |
|  | Designer | 500 | 12 |
|  | Backend RD | 130 | 5 |
|  | Data Engineer | 0 | 15 |
|  | **Marketing** | **0** | **8** |
| | **Subtotal** | **880** | **48** |
| **搜尋功能** | PDM | 70 | 0 |
| (Local Search) | PJM | 40 | 0 |
|  | Designer | 220 | 5 |
|  | Backend RD | 60 | 2 |
|  | Data Engineer | 0 | 3 |
|  | **Marketing** | **0** | **2** |
| | **Subtotal** | **390** | **12** |
| **多語言** | PDM | 80 | 0 |
| (i18n) | PJM | 50 | 0 |
|  | Designer | 250 | 6 |
|  | Backend RD | 70 | 3 |
|  | Data Engineer | 0 | 12 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **450** | **26** |

### 1.5 共用帳本, Shared Ledger

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **預設帳本** | PDM | 150 | 5 |
| (Default Book) | PJM | 90 | 3 |
|  | Designer | 300 | 10 |
|  | Frontend RD | 200 | 10 |
|  | Backend RD | 100 | 5 |
|  | Data Engineer | 0 | 8 |
|  | **Marketing** | **0** | **5** |
| | **Subtotal** | **840** | **46** |
| **帳本切換** | PDM | 70 | 0 |
| (Book Switcher) | PJM | 40 | 0 |
|  | Designer | 220 | 6 |
|  | Backend RD | 60 | 3 |
|  | Data Engineer | 0 | 5 |
|  | **Marketing** | **0** | **3** |
| | **Subtotal** | **390** | **17** |
| **成員邀請** | PDM | 300 | 6 |
| (Invitation) | PJM | 180 | 4 |
|  | Designer | 450 | 12 |
|  | Frontend RD | 500 | 12 |
|  | Backend RD | 230 | 6 |
|  | Data Engineer | 0 | 60 |
|  | **Marketing** | **0** | **20** |
| | **Subtotal** | **1,660** | **120** |
| **協作權限** | PDM | 590 | 12 |
| (Collaboration) | PJM | 350 | 7 |
|  | Designer | 600 | 25 |
|  | Frontend RD | 1,200 | 35 |
|  | Backend RD | 550 | 22 |
|  | Data Engineer | 0 | 55 |
|  | **Marketing** | **0** | **15** |
| | **Subtotal** | **3,290** | **171** |

---

## 2. Web 複雜報表, Web Console

**價值模型:**
- **施工價值, Construction:** 12,060 點 / 次 (1,206 小時 = 6.0 人月)
- **維運價值, Operation:** 771 點 / 月 (77.1 小時/月)

### 2.1 高密度資料瀏覽, Data Browsing

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **表格視圖** | PDM | 550 | 12 |
| (Data Grid) | PJM | 330 | 7 |
|  | Designer | 1,800 | 55 |
|  | Backend RD | 400 | 22 |
|  | Data Engineer | 0 | 80 |
|  | **Marketing** | **0** | **40** |
| | **Subtotal** | **3,080** | **216** |
| **進階匯出** | PDM | 170 | 5 |
| (Adv Export) | PJM | 100 | 3 |
|  | Designer | 550 | 22 |
|  | Backend RD | 120 | 6 |
|  | Data Engineer | 0 | 20 |
|  | **Marketing** | **0** | **8** |
| | **Subtotal** | **940** | **64** |

### 2.2 進階篩選與查詢, Advanced Query

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **JQL 介面** | PDM | 600 | 18 |
| (JQL Interface) | PJM | 360 | 11 |
|  | Designer | 1,800 | 58 |
|  | Backend RD | 600 | 28 |
|  | Data Engineer | 0 | 45 |
|  | **Marketing** | **0** | **18** |
| | **Subtotal** | **3,360** | **178** |
| **視圖儲存** | PDM | 120 | 0 |
| (Saved Views) | PJM | 70 | 0 |
|  | Designer | 350 | 12 |
|  | Backend RD | 120 | 6 |
|  | Data Engineer | 0 | 8 |
|  | **Marketing** | **0** | **4** |
| | **Subtotal** | **660** | **30** |

### 2.3 客製化報表, Custom Reporting

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **自訂維度** | PDM | 600 | 18 |
| (Custom Charts) | PJM | 360 | 11 |
|  | Designer | 1,800 | 58 |
|  | Backend RD | 600 | 28 |
|  | Data Engineer | 0 | 85 |
|  | **Marketing** | **0** | **42** |
| | **Subtotal** | **3,360** | **242** |
| **報表匯出** | PDM | 120 | 0 |
| (Report Export) | PJM | 70 | 0 |
|  | Designer | 350 | 12 |
|  | Backend RD | 120 | 6 |
|  | Data Engineer | 0 | 15 |
|  | **Marketing** | **0** | **8** |
| | **Subtotal** | **660** | **41** |

---

## 3. AI 個人化建議, AI Advisor

**價值模型:**
- **施工價值, Construction:** 15,130 點 / 次 (1,513 小時 = 7.6 人月)
- **維運價值, Operation:** 1,221 點 / 月 (122.1 小時/月)

### 3.1 智慧偵測, Intelligent Detection

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **異常通知** | PDM | 690 | 12 |
| (Anomaly Alert) | PJM | 420 | 7 |
|  | Designer | 230 | 12 |
|  | Frontend RD | 600 | 22 |
|  | Backend RD | 240 | 12 |
|  | Data Engineer | 0 | 95 |
|  | QA | 1,700 | 110 |
|  | **Marketing** | **0** | **45** |
| | **Subtotal** | **3,880** | **315** |
| **重複偵測** | PDM | 450 | 0 |
| (Duplicate) | PJM | 270 | 0 |
|  | Designer | 230 | 12 |
|  | Frontend RD | 350 | 12 |
|  | Backend RD | 120 | 6 |
|  | Data Engineer | 0 | 48 |
|  | QA | 1,100 | 55 |
|  | **Marketing** | **0** | **18** |
| | **Subtotal** | **2,520** | **151** |

### 3.2 預測與診斷, Forecast & Diagnosis

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **現金流預測** | PDM | 720 | 12 |
| (Cashflow) | PJM | 430 | 7 |
|  | Designer | 350 | 12 |
|  | Frontend RD | 600 | 22 |
|  | Backend RD | 240 | 12 |
|  | Data Engineer | 0 | 135 |
|  | QA | 1,700 | 110 |
|  | **Marketing** | **0** | **45** |
| | **Subtotal** | **4,040** | **355** |
| **健康評分** | PDM | 450 | 0 |
| (Health Score) | PJM | 270 | 0 |
|  | Designer | 230 | 12 |
|  | Frontend RD | 350 | 12 |
|  | Backend RD | 120 | 6 |
|  | Data Engineer | 0 | 45 |
|  | QA | 1,100 | 55 |
|  | **Marketing** | **0** | **18** |
| | **Subtotal** | **2,520** | **148** |
| **AI 對話** | PDM | 390 | 12 |
| (AI Chat) | PJM | 230 | 7 |
|  | Designer | 230 | 12 |
|  | Frontend RD | 600 | 22 |
|  | Backend RD | 120 | 6 |
|  | Data Engineer | 0 | 90 |
|  | QA | 600 | 58 |
|  | **Marketing** | **0** | **45** |
| | **Subtotal** | **2,170** | **252** |

---

## 4. 總經分析報表與 API, Macro Data Service

**價值模型:**
- **施工價值, Construction:** 12,090 點 / 次 (1,209 小時 = 6.0 人月)
- **維運價值, Operation:** 1,764 點 / 月 (176.4 小時/月)

### 4.1 B2B 數據服務, B2B Data Services

| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |
| :--- | :--- | :--- | :--- |
| **市場儀表板** | PDM | 580 | 22 |
| (Dashboard) | PJM | 350 | 13 |
|  | Designer | 950 | 58 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 180 |
|  | **Marketing** | **0** | **90** |
| | **Subtotal** | **3,270** | **495** |
| **競品分析** | PDM | 580 | 22 |
| (Competitor) | PJM | 350 | 13 |
|  | Designer | 950 | 58 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 180 |
|  | **Marketing** | **0** | **90** |
| | **Subtotal** | **3,270** | **495** |
| **總經 API** | PDM | 580 | 22 |
| (Macro API) | PJM | 350 | 13 |
|  | Frontend RD | 950 | 58 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 180 |
|  | **Marketing** | **0** | **90** |
| | **Subtotal** | **3,270** | **495** |
| **隱私合規** | PDM | 410 | 22 |
| (Privacy) | PJM | 240 | 13 |
|  | Frontend RD | 240 | 22 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 45 |
|  | **Marketing** | **0** | **45** |
| | **Subtotal** | **2,280** | **279** |

---

## 價值彙整

| 產品組件 | 施工價值 (點) | 施工工時 | 維運價值 (點/月) | 年化維運 |
| :--- | ---: | ---: | ---: | ---: |
| 1. 記帳 App | 22,960 | 11.5 人月 | 1,078 | 12,936 |
| 2. Web Console | 12,060 | 6.0 人月 | 771 | 9,252 |
| 3. AI Advisor | 15,130 | 7.6 人月 | 1,221 | 14,652 |
| 4. Macro Data | 12,090 | 6.0 人月 | 1,764 | 21,168 |
| **總計** | **62,240** | **31.1 人月** | **4,834** | **58,008** |
