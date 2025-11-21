# 序號驗證 API (Validate Code API)

## 1. API 摘要
- **Endpoint**: `GET /api/v1/redeem/validate`
- **Auth Required**: Yes (User Token)
- **Rate Limit**: 10 requests / minute / user
- **說明**: 僅檢查序號是否有效，不執行兌換。用於 UI 即時回饋。

## 2. Request

### 2.1 Headers
- `Authorization`: `Bearer <token>`

### 2.2 Query Parameters
- `code`: String, 必填, 序號字串

## 3. Response

### 3.1 Success (200 OK)
```json
{
  "success": true,
  "isValid": true,
  "data": {
    "codeType": "tier_upgrade",
    "targetTier": 1,
    "durationDays": 30,
    "description": "升級至 Tier 1 會員 (30天)"
  }
}
```

### 3.2 Invalid Code (200 OK)
注意：即使序號無效，HTTP Status 仍為 200，透過 `isValid` 判斷。

```json
{
  "success": true,
  "isValid": false,
  "errorCode": "CODE_EXPIRED",
  "message": "序號已過期"
}
```

### 3.3 Errors

| Status | Error Code | Message |
|--------|------------|---------|
| 400 | `MISSING_PARAM` | 缺少 code 參數 |
| 429 | `RATE_LIMIT_EXCEEDED` | 請求過於頻繁 |
| 500 | `INTERNAL_ERROR` | 系統錯誤 |
