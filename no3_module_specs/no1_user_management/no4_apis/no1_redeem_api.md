# 序號兌換 API (Redeem API)

## 1. API 摘要
- **Endpoint**: `POST /api/v1/redeem`
- **Auth Required**: Yes (User Token)
- **Rate Limit**: 5 requests / minute / user

## 2. Request

### 2.1 Headers
- `Authorization`: `Bearer <token>`
- `Content-Type`: `application/json`

### 2.2 Body
```json
{
  "code": "ABCD-1234-EFGH",
  "userId": "user_12345"
}
```
- `code`: String, 必填, 12碼序號
- `userId`: String, 必填, 需與 Token 中的 UID 一致

## 3. Response

### 3.1 Success (200 OK)
```json
{
  "success": true,
  "message": "兌換成功",
  "data": {
    "redeemedCode": "ABCD-1234-EFGH",
    "codeType": "tier_upgrade",
    "newTier": 1,
    "subscriptionEndDate": 1735689600000
  }
}
```

### 3.2 Errors

| Status | Error Code | Message |
|--------|------------|---------|
| 400 | `INVALID_FORMAT` | 序號格式錯誤 |
| 404 | `CODE_NOT_FOUND` | 序號不存在 |
| 400 | `CODE_INACTIVE` | 序號未啟用 |
| 400 | `CODE_EXPIRED` | 序號已過期 |
| 400 | `CODE_DEPLETED` | 序號已被兌換完畢 |
| 409 | `ALREADY_REDEEMED` | 您已兌換過此序號 |
| 429 | `RATE_LIMIT_EXCEEDED` | 請求過於頻繁 |
| 500 | `INTERNAL_ERROR` | 系統錯誤 |
