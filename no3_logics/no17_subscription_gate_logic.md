# 訂閱授權邏輯規格: SubscriptionGateLogic

## 目的

- 定義各訂閱等級可執行的受限建立動作條件與總數限制
- 規則由 canUserPerformAction 取用，作為判斷唯一依據

---

## 參照來源

- 跨 Module 的 LEVEL 商業定義: `no1_product_initiation/no3_business_model.md`
- 記帳 App 視角下各 LEVEL 可用能力的白話總覽: `no2_product_planning/no2_product_map/app/payment.md` 的 LEVEL 能力清單
- triggerCloudBackup 與 triggerMultiDeviceSync 拆解依據: `no99_archive/r1_decision_matrix.md` R1 Round 5 拍板
- 本檔的規則表與上述三者對齊，任一變更時需同步更新

---

## LEVEL 規則表

- **LEVEL_0:**
  - 允許動作，受總數限制:
    - createAccount
    - createCategory
    - createTransaction
    - createTransfer
  - 禁止動作:
    - useForeignCurrency
    - createRecurringTransaction
    - triggerMultiDeviceSync
    - importData
    - manageCurrencyRate
  - 不在禁止清單動作（含 LEVEL_0 全 LEVEL 允許）:
    - triggerCloudBackup
  - 總數限制:
    - 帳戶總數上限 3 個
    - 類別總數上限 10 個
- **LEVEL_1 以上:**
  - 允許動作: 全部
  - 禁止動作: 無
  - 總數限制: 無
  - 說明:
    - LEVEL_2 為 Logic Engine 訂閱者，記帳 App 視角下能力與 LEVEL_1 相同
    - 授權判斷採用當前訂閱等級大於等於 LEVEL_1 即允許的形式

---

## canUserPerformAction 判斷使用者是否可執行動作

- **輸入:**
  - 當前使用者訂閱等級
  - 動作識別碼
- **動作識別碼:**
  - createAccount
  - createCategory
  - createTransaction
  - createTransfer
  - useForeignCurrency
  - createRecurringTransaction
  - triggerCloudBackup
  - triggerMultiDeviceSync
  - importData
  - manageCurrencyRate
- **性質:**
  - 純本地計算，可讀取當前使用者的帳戶總數與類別總數
- **執行:**
  - **IF** 動作識別碼為 createAccount:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - 讀取當前使用者的帳戶總數
      - **IF** 帳戶總數小於 3:
        - **回傳:** 允許
      - **ELSE:**
        - **回傳:** 禁止
    - **ELSE:**
      - **回傳:** 允許
  - **IF** 動作識別碼為 createCategory:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - 讀取當前使用者的類別總數
      - **IF** 類別總數小於 10:
        - **回傳:** 允許
      - **ELSE:**
        - **回傳:** 禁止
    - **ELSE:**
      - **回傳:** 允許
  - **IF** 動作識別碼為 useForeignCurrency:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - **回傳:** 禁止
    - **ELSE:**
      - **回傳:** 允許
  - **IF** 動作識別碼為 manageCurrencyRate:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - **回傳:** 禁止
    - **ELSE:**
      - **回傳:** 允許
  - **IF** 動作識別碼為 createRecurringTransaction:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - **回傳:** 禁止
    - **ELSE:**
      - **回傳:** 允許
  - **IF** 動作識別碼為 triggerCloudBackup:
    - **回傳:** 允許
  - **IF** 動作識別碼為 triggerMultiDeviceSync:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - **回傳:** 禁止
    - **ELSE:**
      - **回傳:** 允許
  - **IF** 動作識別碼為 importData:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - **回傳:** 禁止
    - **ELSE:**
      - **回傳:** 允許
  - **IF** 動作識別碼為 createTransaction 或 createTransfer:
    - **IF** 當前訂閱等級為 LEVEL_0:
      - 讀取當前使用者的帳戶總數與類別總數
      - **IF** 帳戶總數已達 3 或類別總數已達 10:
        - **回傳:** 禁止
      - **ELSE:**
        - **回傳:** 允許
    - **ELSE:**
      - **回傳:** 允許
