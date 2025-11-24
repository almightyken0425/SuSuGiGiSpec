# User Management Module (MVP Scope)

> **模組版本**: MVP 1.0  
> **最後更新**: 2025-11-24  
> **範圍**: 僅包含 MVP 階段必要的使用者管理功能

---

## 📋 模組目的

User Management 模組負責：
1. **使用者資料儲存** - 在 Firestore 中維護使用者個人資料
2. **首次登入流程** - 新使用者註冊時建立預設資料
3. **偏好設定管理** - 語言、貨幣、時區等使用者偏好
4. **RevenueCat 整合** - 為訂閱權限資料預留欄位結構

---

## 🚫 不在 MVP 範圍內

以下功能**不在此模組 MVP 範圍**，延後至未來迭代：
- ❌ 序號兌換系統
- ❌ 自定義會員等級邏輯（由 RevenueCat 管理）
- ❌ 訂閱狀態手動更新（由 RevenueCat 自動同步）
- ❌ 管理員後台（使用 Firebase Console）

---

## 📂 模組結構

```
no1_user_management_mvp/
├── README.md                          # 本文件
├── no1_data_models/
│   └── users_schema.md                # Firestore Users collection 定義
├── no2_logics/
│   └── first_login_flow.md            # 首次登入建立使用者邏輯
└── no3_apis/
    └── update_preferences_api.md      # 更新使用者偏好設定 API (可選)
```

---

## 🔗 相關文件

- **RevenueCat 整合**: [IAP 訂閱系統完整流程](../../no5_analysis_reports/iap_subscription_flow.md)
- **序號系統 (未來)**: 延後至 MVP 之後

---

## ✅ MVP 實作重點

### 1. Firestore Users Collection
定義清楚的 schema，包含：
- Firebase Auth 基本資料
- 使用者偏好設定
- **RevenueCat 同步欄位預留區**（自動寫入，不手動維護）

### 2. 首次登入邏輯
- App 端檢查 Firestore 中是否有使用者文件
- 若無，建立預設資料
- 簡單、可靠、冪等

### 3. 偏好設定更新
- 使用者可在 App 中修改語言、貨幣、時區
- 透過 Firestore SDK 直接更新（不一定需要 Cloud Function）

---

**文件結束**
