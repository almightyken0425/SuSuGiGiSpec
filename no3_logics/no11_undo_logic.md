# 復原邏輯: UndoLogic

## 目的

- 支援單步撤銷刪除操作，透過 Soft Delete 的可逆性讓使用者救回誤刪資料

---

## revertDelete 復原刪除

- **輸入:**
  - 待復原的紀錄類型與識別碼
- **執行:**
  - 將目標紀錄的 `deletedOn` 設為 null
  - **IF** 類型為帳戶:
    - 同時將其關聯交易的 `deletedOn` 設為 null
