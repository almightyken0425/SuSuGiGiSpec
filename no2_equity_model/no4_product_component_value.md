# 產品組件與價值分配

## 核心目標

- 本文件依據產品定義的產品個體，詳細列出每個組件的價值構成。
- 採用 **雙重價值模型**：每個模組同時包含 **施工價值** Construction 與 **維運價值** Operation。
- 針對每個 **User Story**，依據角色定義進行價值點數分配。
- **營運角色整合:** Marketing 與 Operations 角色整合至每個 User Story 中，其施工價值為 0，但隨著功能上線，其維運價值 Operation Value 將逐步累積。
- **價值單位:** 1 點 = 0.1 小時，詳見股權原則文件。

---

## 1. 記帳 App + Firestore, Accounting App

**價值模型:**
- **施工價值, Construction:** 24,060 點 / 次 (2,406 小時 = 12.0 人月)
- **維運價值, Operation:** 1,068 點 / 月 (106.8 小時/月)

### 1.1 交易與自動化, Transaction & Automation

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **支出管理** | PDM | 150 | 3 |
| Expense CRUD | PJM | 90 | 2 |
|  | UX Designer | 160 | 3 |
|  | UI Designer | 240 | 4 |
|  | App RD | 100 | 3 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 100 | 3 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 10 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **840** | **33** |
| **收入管理** | PDM | 150 | 3 |
| Income CRUD | PJM | 90 | 2 |
|  | UX Designer | 160 | 3 |
|  | UI Designer | 240 | 4 |
|  | App RD | 100 | 3 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 100 | 3 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 10 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **840** | **33** |
| **轉帳管理** | PDM | 200 | 3 |
| Transfer CRUD | PJM | 120 | 2 |
|  | UX Designer | 200 | 3 |
|  | UI Designer | 300 | 4 |
|  | App RD | 150 | 3 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 130 | 3 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 10 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,100** | **33** |
| **定期交易** | PDM | 310 | 8 |
| Recurring | PJM | 190 | 5 |
|  | UX Designer | 400 | 7 |
|  | UI Designer | 200 | 10 |
|  | App RD | 400 | 10 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 250 | 8 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 30 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 10 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,750** | **88** |

### 1.2 資產管理, Asset Management

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **帳戶管理** | PDM | 100 | 3 |
| Account CRUD | PJM | 60 | 2 |
|  | UX Designer | 120 | 3 |
|  | UI Designer | 180 | 4 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 100 | 3 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 8 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **560** | **28** |
| **類別管理** | PDM | 110 | 3 |
| Category CRUD | PJM | 70 | 2 |
|  | UX Designer | 140 | 3 |
|  | UI Designer | 210 | 4 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 100 | 3 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 8 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **630** | **28** |
| **預設資料** | PDM | 60 | 2 |
| Onboarding | PJM | 40 | 1 |
|  | UX Designer | 80 | 2 |
|  | UI Designer | 120 | 3 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 50 | 2 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 5 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 3 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **350** | **18** |
| **多幣別支援** | PDM | 210 | 5 |
| Multi-Currency | PJM | 130 | 3 |
|  | UX Designer | 180 | 4 |
|  | UI Designer | 270 | 6 |
|  | App RD | 250 | 8 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 150 | 5 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 20 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 10 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,190** | **61** |
| **解除限制** | PDM | 60 | 2 |
| Unlimited | PJM | 40 | 1 |
|  | UX Designer | 40 | 2 |
|  | UI Designer | 60 | 3 |
|  | App RD | 100 | 5 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 50 | 2 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 30 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 15 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **350** | **60** |

### 1.3 資料與同步, Data & Sync

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **離線支援** | PDM | 290 | 0 |
| Offline Arch | PJM | 170 | 0 |
|  | UX Designer | 360 | 8 |
|  | UI Designer | 540 | 12 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 250 | 10 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 5 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 3 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,610** | **38** |
| **雲端同步** | PDM | 960 | 10 |
| Sync Engine | PJM | 580 | 6 |
|  | UX Designer | 500 | 10 |
|  | UI Designer | 100 | 15 |
|  | App RD | 2,340 | 50 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 900 | 25 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 40 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 20 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **5,380** | **176** |
| **資料匯入** | PDM | 200 | 5 |
| CSV Import | PJM | 120 | 3 |
|  | UX Designer | 500 | 4 |
|  | UI Designer | 200 | 6 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 120 | 5 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 8 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,140** | **36** |

### 1.4 儀表板與體驗, Dashboard & Experience

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **首頁儀表板** | PDM | 230 | 5 |
| Home Dash | PJM | 140 | 3 |
|  | UX Designer | 200 | 4 |
|  | UI Designer | 600 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 130 | 5 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 15 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 8 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,300** | **47** |
| **搜尋功能** | PDM | 70 | 0 |
| Local Search | PJM | 40 | 0 |
|  | UX Designer | 88 | 2 |
|  | UI Designer | 132 | 3 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 60 | 2 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 3 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 2 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **390** | **12** |
| **多語言** | PDM | 80 | 0 |
| i18n | PJM | 50 | 0 |
|  | UX Designer | 100 | 2 |
|  | UI Designer | 150 | 3 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 70 | 3 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 12 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **450** | **25** |

### 1.5 共用帳本, Shared Ledger

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **預設帳本** | PDM | 150 | 5 |
| Default Book | PJM | 90 | 3 |
|  | UX Designer | 120 | 4 |
|  | UI Designer | 180 | 6 |
|  | App RD | 200 | 10 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 100 | 5 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 8 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 5 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **840** | **46** |
| **帳本切換** | PDM | 70 | 0 |
| Book Switcher | PJM | 40 | 0 |
|  | UX Designer | 88 | 2 |
|  | UI Designer | 132 | 3 |
|  | App RD | 0 | 0 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 60 | 3 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 5 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 3 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **390** | **16** |
| **成員邀請** | PDM | 300 | 6 |
| Invitation | PJM | 180 | 4 |
|  | UX Designer | 180 | 4 |
|  | UI Designer | 270 | 7 |
|  | App RD | 500 | 12 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 230 | 6 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 60 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 20 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,660** | **119** |
| **協作權限** | PDM | 590 | 12 |
| Collaboration | PJM | 350 | 7 |
|  | UX Designer | 240 | 10 |
|  | UI Designer | 360 | 15 |
|  | App RD | 1,200 | 35 |
|  | Web RD | 0 | 0 |
|  | Backend RD | 550 | 22 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 55 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 15 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **3,290** | **171** |

---

## 2. Web 複雜報表, Web Console

**價值模型:**
- **施工價值, Construction:** 12,340 點 / 次 (1,234 小時 = 6.2 人月)
- **維運價值, Operation:** 866 點 / 月 (86.6 小時/月)

### 2.1 高密度資料瀏覽, Data Browsing

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **表格視圖** | PDM | 580 | 12 |
| Data Grid | PJM | 340 | 7 |
|  | UX Designer | 300 | 22 |
|  | UI Designer | 800 | 33 |
|  | App RD | 0 | 0 |
|  | Web RD | 800 | 30 |
|  | Backend RD | 400 | 22 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 80 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 40 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **3,220** | **246** |
| **進階匯出** | PDM | 220 | 5 |
| Adv Export | PJM | 130 | 3 |
|  | UX Designer | 220 | 8 |
|  | UI Designer | 330 | 13 |
|  | App RD | 0 | 0 |
|  | Web RD | 200 | 10 |
|  | Backend RD | 120 | 6 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 20 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 8 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **1,220** | **73** |

### 2.2 進階篩選與查詢, Advanced Query

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **JQL 介面** | PDM | 480 | 18 |
| JQL Interface | PJM | 280 | 11 |
|  | UX Designer | 500 | 23 |
|  | UI Designer | 300 | 34 |
|  | App RD | 0 | 0 |
|  | Web RD | 500 | 20 |
|  | Backend RD | 600 | 28 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 45 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 18 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **2,660** | **197** |
| **視圖儲存** | PDM | 160 | 0 |
| Saved Views | PJM | 90 | 0 |
|  | UX Designer | 140 | 4 |
|  | UI Designer | 210 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 150 | 5 |
|  | Backend RD | 120 | 6 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 8 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 4 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **870** | **34** |

### 2.3 客製化報表, Custom Reporting

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **自訂維度** | PDM | 620 | 18 |
| Custom Charts | PJM | 380 | 11 |
|  | UX Designer | 300 | 23 |
|  | UI Designer | 800 | 34 |
|  | App RD | 0 | 0 |
|  | Web RD | 800 | 30 |
|  | Backend RD | 600 | 28 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 85 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 42 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **3,500** | **271** |
| **報表匯出** | PDM | 160 | 0 |
| Report Export | PJM | 90 | 0 |
|  | UX Designer | 140 | 4 |
|  | UI Designer | 210 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 150 | 5 |
|  | Backend RD | 120 | 6 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 15 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 8 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **870** | **45** |

---

## 3. AI 個人化建議, AI Advisor

**價值模型:**
- **施工價值, Construction:** 15,130 點 / 次 (1,513 小時 = 7.6 人月)
- **維運價值, Operation:** 1,216 點 / 月 (121.6 小時/月)

### 3.1 智慧偵測, Intelligent Detection

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **異常通知** | PDM | 690 | 12 |
| Anomaly Alert | PJM | 420 | 7 |
|  | UX Designer | 92 | 4 |
|  | UI Designer | 138 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 600 | 22 |
|  | Backend RD | 240 | 12 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 95 |
|  | QA | 1,700 | 110 |
|  | Marketing | 0 | 45 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **3,880** | **314** |
| **重複偵測** | PDM | 450 | 0 |
| Duplicate | PJM | 270 | 0 |
|  | UX Designer | 92 | 4 |
|  | UI Designer | 138 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 350 | 12 |
|  | Backend RD | 120 | 6 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 48 |
|  | QA | 1,100 | 55 |
|  | Marketing | 0 | 18 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **2,520** | **150** |

### 3.2 預測與診斷, Forecast & Diagnosis

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **現金流預測** | PDM | 720 | 12 |
| Cashflow | PJM | 430 | 7 |
|  | UX Designer | 140 | 4 |
|  | UI Designer | 210 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 600 | 22 |
|  | Backend RD | 240 | 12 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 135 |
|  | QA | 1,700 | 110 |
|  | Marketing | 0 | 45 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **4,040** | **354** |
| **健康評分** | PDM | 450 | 0 |
| Health Score | PJM | 270 | 0 |
|  | UX Designer | 92 | 4 |
|  | UI Designer | 138 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 350 | 12 |
|  | Backend RD | 120 | 6 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 45 |
|  | QA | 1,100 | 55 |
|  | Marketing | 0 | 18 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **2,520** | **147** |
| **AI 對話** | PDM | 390 | 12 |
| AI Chat | PJM | 230 | 7 |
|  | UX Designer | 92 | 4 |
|  | UI Designer | 138 | 7 |
|  | App RD | 0 | 0 |
|  | Web RD | 600 | 22 |
|  | Backend RD | 120 | 6 |
|  | AI Engineer | 0 | 0 |
|  | Data Engineer | 0 | 90 |
|  | QA | 600 | 58 |
|  | Marketing | 0 | 45 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **2,170** | **251** |

---

## 4. 總經分析報表與 API, Macro Data Service

**價值模型:**
- **施工價值, Construction:** 14,190 點 / 次 (1,419 小時 = 7.1 人月)
- **維運價值, Operation:** 1,802 點 / 月 (180.2 小時/月)

### 4.1 B2B 數據服務, B2B Data Services

| User Story | Role | 施工價值 Pt | 維運價值 Pt/Mo |
| :--- | :--- | :--- | :--- |
| **市場儀表板** | PDM | 770 | 22 |
| Dashboard | PJM | 460 | 13 |
|  | UX Designer | 300 | 23 |
|  | UI Designer | 800 | 34 |
|  | App RD | 0 | 0 |
|  | Web RD | 600 | 20 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 180 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 90 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **4,320** | **514** |
| **競品分析** | PDM | 770 | 22 |
| Competitor | PJM | 460 | 13 |
|  | UX Designer | 300 | 23 |
|  | UI Designer | 800 | 34 |
|  | App RD | 0 | 0 |
|  | Web RD | 600 | 20 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 180 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 90 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **4,320** | **514** |
| **總經 API** | PDM | 580 | 22 |
| Macro API | PJM | 350 | 13 |
|  | UX Designer | 0 | 0 |
|  | UI Designer | 0 | 0 |
|  | App RD | 0 | 0 |
|  | Web RD | 950 | 58 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 180 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 90 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **3,270** | **495** |
| **隱私合規** | PDM | 410 | 22 |
| Privacy | PJM | 240 | 13 |
|  | UX Designer | 0 | 0 |
|  | UI Designer | 0 | 0 |
|  | App RD | 0 | 0 |
|  | Web RD | 240 | 22 |
|  | Backend RD | 240 | 22 |
|  | AI Engineer | 1,150 | 110 |
|  | Data Engineer | 0 | 45 |
|  | QA | 0 | 0 |
|  | Marketing | 0 | 45 |
|  | Operations | 0 | 0 |
| | **Subtotal** | **2,280** | **279** |

---

## 價值彙整

| 產品組件 | 施工價值 點 | 施工工時 | 維運價值 點/月 | 年化維運 |
| :--- | ---: | ---: | ---: | ---: |
| 1. 記帳 App | 24,060 | 12.0 人月 | 1,068 | 12,816 |
| 2. Web Console | 12,340 | 6.2 人月 | 866 | 10,392 |
| 3. AI Advisor | 15,130 | 7.6 人月 | 1,216 | 14,592 |
| 4. Macro Data | 14,190 | 7.1 人月 | 1,802 | 21,624 |
| **總計** | **65,720** | **32.9 人月** | **4,952** | **59,424** |
