# User Management Data Models

## 1. 使用者 Users
(待補齊，目前主要定義序號相關)

## 2. 序號系統

### 序號 RedeemCodes

- **欄位:**
    
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
        

### 兌換歷史 RedemptionHistory

- **欄位:**
    
    - `id`: String, UUID/GUID - Primary Key
        
    - `codeId`: String - Foreign Key to RedeemCodes, Not Null
        
    - `userId`: String, Auth UID - Foreign Key to Users, Not Null
        
    - `redeemedOn`: Number, Unix Timestamp ms - Not Null
        
    - `previousTier`: Number | Null - 兌換前的 Tier
        
    - `newTier`: Number - 兌換後的 Tier
        
    - `subscriptionEndDate`: Number, Unix Timestamp ms - 會員到期日
