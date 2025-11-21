# 序號兌換系統規格補齊待辦清單

## 現況說明

產品定義 ([no2_product_definition.md](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no1_product_initiation/no2_product_definition.md)) 包含三個相關 User Stories：

1. **序號驗證系統 (Redeem System)**: 作為開發團隊，我想要建立序號生成與驗證的後端系統，以便支援多種兌換方案與會員 Tier。
2. **序號兌換介面 (Redeem UI)**: 作為使用者，我想要在設定中輸入序號，以便兌換會員資格並解鎖進階功能。
3. **序號管理工具 (Redeem Management)**: 作為營運團隊，我想要能夠生成和管理序號，以便用於行銷活動或合作夥伴方案。

**問題**: `no3_module_specs/no1_accounting_app` 中完全沒有對應的規格文件。

---

## 待補充規格清單

### 優先級 1: 資料模型

#### [ ] 1.1 序號資料模型
**檔案路徑**: `no3_module_specs/no1_accounting_app/no4_data_models/no1_data_models.md` (擴充)

**應新增 RedeemCodes 表**:
- **欄位**:
  - `id`: String, UUID/GUID - Primary Key
  - `code`: String - Not Null, Unique, Index, 序號字串 (例如: ABCD-1234-EFGH)
  - `codeType`: String - Not Null, 序號類型 (例如: 'tier_upgrade', 'trial_extension', 'feature_unlock')
  - `targetTier`: Number | Null - 目標 Tier (1, 2, 3) or null
  - `durationDays`: Number | Null - 有效期天數 (例如: 30, 90, 365)
  - `maxRedemptions`: Number - Not Null, Default 1, 最大兌換次數
  - `currentRedemptions`: Number - Not Null, Default 0, 已兌換次數
  - `isActive`: Boolean - Not Null, Default true, 序號是否啟用
  - `expiresOn`: Number | Null, Unix Timestamp ms - Nullable, 序號過期日期
  - `createdBy`: String - Not Null, 建立者 (營運人員 ID)
  - `createdOn`: Number, Unix Timestamp ms - Not Null
  - `updatedOn`: Number, Unix Timestamp ms - Not Null
  - `deletedOn`: Number | Null, Unix Timestamp ms - Nullable

**應新增 RedemptionHistory 表**:
- **欄位**:
  - `id`: String, UUID/GUID - Primary Key
  - `codeId`: String - Foreign Key to RedeemCodes, Not Null
  - `userId`: String, Auth UID - Foreign Key to Users, Not Null
  - `redeemedOn`: Number, Unix Timestamp ms - Not Null
  - `previousTier`: Number | Null - 兌換前的 Tier
  - `newTier`: Number - 兌換後的 Tier
  - `subscriptionEndDate`: Number, Unix Timestamp ms - 會員到期日

---

### 優先級 2: 使用者端 UI 規格

#### [ ] 2.1 序號兌換畫面
**檔案路徑**: `no3_module_specs/no1_accounting_app/no2_screens/no17_redeem_code_screen.md`

**應包含內容**:
- **UI 佈局**:
  - 序號輸入欄位 (TextField)
  - 格式提示 (例如: XXXX-XXXX-XXXX)
  - 兌換按鈕
  - 兌換歷史記錄區域 (可選)
- **互動邏輯**:
  - 序號格式驗證 (客戶端)
  - 兌換按鈕點擊後送出驗證請求
  - Loading 狀態顯示
  - 成功/失敗 Dialog
- **錯誤處理**:
  - 序號格式錯誤
  - 序號無效或已過期
  - 序號已被兌換
  - 網路錯誤
- **導航**:
  - 從 PreferenceScreen 或 SettingsScreen 進入
  - 成功兌換後的後續流程 (例如: 顯示升級成功訊息)

#### [ ] 2.2 偏好設定畫面更新
**檔案路徑**: `no3_module_specs/no1_accounting_app/no2_screens/no13_preference_screen.md` (修改)

**應新增**:
- 新增「兌換序號」選項
- 點擊後導航至 RedeemCodeScreen

---

### 優先級 3: 背景邏輯

#### [ ] 3.1 序號驗證邏輯
**檔案路徑**: `no3_module_specs/no1_accounting_app/no3_background_logics/no7_redeem_code_validation.md`

**應包含內容**:
- **驗證流程**:
  1. 客戶端格式檢查
  2. 送出序號至後端 API
  3. 後端驗證邏輯:
     - 序號是否存在
     - 序號是否啟用 (`isActive == true`)
     - 序號是否過期 (`expiresOn` 檢查)
     - 序號兌換次數是否已達上限
     - 使用者是否已兌換過此序號
  4. 成功後執行:
     - 更新 Users 表的 `currentTier`
     - 更新 `subscriptionEndDate`
     - 增加 `currentRedemptions` 計數
     - 新增 RedemptionHistory 記錄
     - 觸發 App 內狀態更新
  5. 回傳結果給客戶端

- **錯誤代碼定義**:
  - `INVALID_FORMAT`: 序號格式錯誤
  - `CODE_NOT_FOUND`: 序號不存在
  - `CODE_EXPIRED`: 序號已過期
  - `CODE_DEPLETED`: 序號兌換次數已用完
  - `ALREADY_REDEEMED`: 使用者已兌換過此序號
  - `CODE_INACTIVE`: 序號未啟用

#### [ ] 3.2 序號生成邏輯
**檔案路徑**: `no3_module_specs/no1_accounting_app/no3_background_logics/no8_redeem_code_generation.md`

**應包含內容**:
- **生成演算法**:
  - 序號格式定義 (例如: XXXX-XXXX-XXXX)
  - 字元集 (避免混淆字元如 0/O, 1/I)
  - 校驗碼生成 (可選)
- **批次生成**:
  - 單次生成多個序號
  - 確保唯一性
  - 批次匯出功能

---

### 優先級 4: 營運端管理方案 (MVP: Firebase Console)

#### [ ] 4.1 Firebase Console 操作手冊
**檔案路徑**: `no3_module_specs/no1_accounting_app/no6_admin_tools/no1_firebase_console_guide.md`

**應包含內容**:
- **前置準備**:
  - 存取權限設定 (IAM roles)
  - 專案環境切換 (Dev/Prod)
- **手動生成序號步驟**:
  1. 登入 Firebase Console
  2. 進入 Firestore Database
  3. 找到 `RedeemCodes` 集合
  4. 新增文件 (Document)
     - ID: 選擇 "Auto-ID"
     - 填寫欄位:
       - `code`: 輸入唯一序號 (如: VIP-2024-001)
       - `codeType`: 選擇類型 (如: tier_upgrade)
       - `targetTier`: 輸入目標 Tier (如: 1)
       - `durationDays`: 輸入天數 (如: 30)
       - `maxRedemptions`: 設定次數 (如: 1)
       - `isActive`: boolean true
       - `createdBy`: 輸入操作者 Email
       - `createdOn`: 輸入當前 Timestamp
- **查詢與管理**:
  - 如何篩選特定序號
  - 如何停用序號 (`isActive` 改為 false)
  - 如何查看兌換狀況 (`currentRedemptions`)

#### [ ] 4.2 營運操作標準流程 (SOP)
**檔案路徑**: `no3_module_specs/no1_accounting_app/no6_admin_tools/no2_operation_sop.md`

**應包含內容**:
- **序號發放流程**:
  - 需求申請 (誰可以申請序號)
  - 核決權限
  - 生成執行 (誰負責操作 Console)
  - 發放記錄 (記錄在外部表格或是通知信件)
- **異常處理流程**:
  - 用戶回報序號無效的處理步驟
  - 序號外洩的緊急停用程序

---

### 優先級 5: API 規格

#### [ ] 5.1 序號兌換 API
**檔案路徑**: `no3_module_specs/no1_accounting_app/no7_api_specs/no1_redeem_api.md`

**應包含內容**:
- **POST /api/v1/redeem**
  - Request Body:
    ```json
    {
      "code": "ABCD-1234-EFGH",
      "userId": "user123"
    }
    ```
  - Response Success (200):
    ```json
    {
      "success": true,
      "message": "兌換成功",
      "newTier": 1,
      "subscriptionEndDate": 1735689600000
    }
    ```
  - Response Error (400):
    ```json
    {
      "success": false,
      "errorCode": "CODE_EXPIRED",
      "message": "序號已過期"
    }
    ```

#### [ ] 5.2 序號驗證 API (僅檢查，不兌換)
**檔案路徑**: `no3_module_specs/no1_accounting_app/no7_api_specs/no2_validate_code_api.md`

**應包含內容**:
- **GET /api/v1/redeem/validate?code=XXXX**
  - Response: 序號是否有效、類型、預期效果等資訊

---

## 規格撰寫順序建議

1. **資料模型定義** → 更新 `no1_data_models.md`
2. **序號生成邏輯** → 撰寫 `no8_redeem_code_generation.md`
3. **營運端管理方案** → 撰寫 `no1_firebase_console_guide.md` 與 `no2_operation_sop.md`
4. **API 規格** → 撰寫 `no1_redeem_api.md` 與 `no2_validate_code_api.md`
5. **使用者端 UI** → 撰寫 `no17_redeem_code_screen.md`
6. **序號驗證邏輯** → 撰寫 `no7_redeem_code_validation.md`

---

## 安全性考量

> [!CAUTION]
> 序號系統涉及會員權益，需特別注意安全性：

- **防止暴力破解**:
  - API 限流 (Rate Limiting)
  - 錯誤嘗試次數限制
  - CAPTCHA (可選)

- **序號加密**:
  - 序號在資料庫中應加密儲存
  - 傳輸時使用 HTTPS

- **權限控制**:
  - 序號管理後台僅管理員可存取
  - 序號生成記錄需保留審計日誌

---

## 驗收標準

- [ ] 所有清單中的規格文件已建立
- [ ] 資料模型包含完整的欄位定義
- [ ] 邏輯規格文件清楚描述了生成與驗證流程
- [ ] UI 規格文件包含完整的互動邏輯與錯誤處理
- [ ] API 規格文件定義了完整的 Request/Response 結構
- [ ] 操作手冊與 SOP 步驟清晰可執行
