# 產品組件與價值分配

## 核心目標

- 本文件依據產品定義的產品個體，詳細列出每個組件的價值構成。
- 採用 **雙重價值模型**：每個模組同時包含 **施工價值**, 純施工價值 與 **維運價值**, 純營運價值。
- 針對每個產品個體，依據 User Story 切分 Role Definition 並給出價值點數。

---

## 1. 記帳 App + Firestore, Accounting App

**價值模型:**
- **施工價值, Construction:** 150,000 點, 一次性
- **維運價值, Operation:** 12,000 點 / 年

### Role Definition & Value Allocation

| User Story Group | Role | 職責描述 | 價值點數, 施工 |
| :--- | :--- | :--- | :--- |
| **交易與自動化** | **Mobile Dev** | 實作 CRUD 與定期交易邏輯 | 35,000 |
| | **UI/UX** | 設計極速記帳互動介面 | 10,000 |
| **資產管理** | **Mobile Dev** | 實作帳戶、類別、多幣別與限制邏輯 | 20,000 |
| | **Mobile Dev** | 實作首次啟動資料初始化 | 5,000 |
| **資料與同步** | **Mobile Dev** | 實作離線資料庫與 CSV 匯入 | 25,000 |
| | **Mobile Dev** | 整合雲端同步邏輯 | 10,000 |
| | **Backend Dev** | 實作 Sync Engine 與備份 | 30,000 |
| **儀表板與體驗** | **Mobile Dev** | 實作首頁儀表板、搜尋與 i18n | 10,000 |
| | **UI/UX** | 設計儀表板視覺 | 5,000 |
| **總計** | | | **150,000** |

---

## 2. Web 複雜報表, Web Console

**價值模型:**
- **施工價值, Construction:** 120,000 點, 一次性
- **維運價值, Operation:** 10,000 點 / 年

### Role Definition & Value Allocation

| User Story Group | Role | 職責描述 | 價值點數, 施工 |
| :--- | :--- | :--- | :--- |
| **高密度資料管理** | **Frontend Dev** | 實作 Data Grid 與批量操作 | 40,000 |
| | **Frontend Dev** | 實作進階匯出功能 | 10,000 |
| | **UI/UX** | 設計桌面版管理介面 | 15,000 |
| **進階篩選與查詢** | **Frontend Dev** | 實作 JQL Parser 與視圖儲存 | 30,000 |
| **客製化報表** | **Frontend Dev** | 實作自訂維度圖表與匯出 | 20,000 |
| | **UI/UX** | 設計報表設定流程 | 5,000 |
| **總計** | | | **120,000** |

---

## 3. AI 個人化建議, AI Advisor

**價值模型:**
- **施工價值, Construction:** 100,000 點, 一次性
- **維運價值, Operation:** 20,000 點 / 年

### Role Definition & Value Allocation

| User Story Group | Role | 職責描述 | 價值點數, 施工 |
| :--- | :--- | :--- | :--- |
| **智慧偵測** | **AI Engineer** | 訓練異常與重複偵測模型 | 40,000 |
| **預測與診斷** | **AI Engineer** | 建立現金流預測與評分模型 | 30,000 |
| | **Backend Dev** | 整合 LLM API 與 Prompt | 20,000 |
| | **Mobile/Web** | 呈現 AI 建議與對話介面 | 10,000 |
| **總計** | | | **100,000** |

---

## 4. 總經分析報表與 API, Macro Data Service

**價值模型:**
- **施工價值, Construction:** 80,000 點, 一次性
- **維運價值, Operation:** 30,000 點 / 年

### Role Definition & Value Allocation

| User Story Group | Role | 職責描述 | 價值點數, 施工 |
| :--- | :--- | :--- | :--- |
| **B 端數據服務** | **Data Engineer** | 建立 ETL Pipeline 與去識別化 | 40,000 |
| | **Frontend Dev** | 實作市場情資儀表板 | 20,000 |
| | **Backend Dev** | 開發總經 API Gateway | 20,000 |
| **總計** | | | **80,000** |

---

## 價值彙整

| 產品組件 | 施工價值, 點 | 維運價值, 點/年 |
| :--- | :--- | :--- |
| 1. 記帳 App + Firestore | 150,000 | 12,000 |
| 2. Web 複雜報表 | 120,000 | 10,000 |
| 3. AI 個人化建議 | 100,000 | 20,000 |
| 4. 總經分析報表與 API | 80,000 | 30,000 |
| **總計** | **450,000** | **72,000** |
