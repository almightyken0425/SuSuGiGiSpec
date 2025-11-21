# 序號生成邏輯 (Redeem Code Generation Logic)

## 1. 邏輯摘要
- **名稱**: RedeemCodeGeneration
- **目的**: 負責產生唯一、安全且易於輸入的兌換序號。

## 2. 序號格式定義

### 2.1 格式結構
- **Pattern**: `XXXX-XXXX-XXXX` (12 字元，分為 3 組)
- **字元集**: 大寫英數字，排除易混淆字元
  - **Allowed**: `23456789ABCDEFGHJKLMNPQRSTUVWXYZ`
  - **Excluded**: `0`, `1`, `I`, `O`
- **長度**: 12 字元 (不含分隔符號)
- **熵值 (Entropy)**: 32^12 ≈ 1.15 x 10^18 組合，足夠防止暴力猜測。

## 3. 生成演算法

1. **輸入參數**:
   - `count`: 生成數量
   - `prefix`: (Optional) 特定前綴，如 `VIP-`

2. **生成步驟**:
   - **Step 1**: 使用加密安全的隨機數生成器 (CSPRNG) 產生隨機字串。
   - **Step 2**: 檢查字串是否符合格式與字元集規範。
   - **Step 3**: (Optional) 加入校驗碼 (Check Digit) 以便前端快速驗證。
   - **Step 4**: 檢查資料庫中是否已存在相同序號 (Collision Check)。
     - 若存在，重新生成。
   - **Step 5**: 寫入 `RedeemCodes` 表。

## 4. 批次生成流程

1. **管理員觸發**: 透過 Cloud Function 或 Admin Script。
2. **執行**:
   - 迴圈執行生成步驟。
   - 收集所有生成的序號物件。
   - 使用 Firestore Batch Write 一次性寫入 (注意 500 筆限制，需分批)。
3. **輸出**: 回傳生成的序號列表 (JSON/CSV)。
