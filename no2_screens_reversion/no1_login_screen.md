# 登入畫面: LoginScreen

## 畫面目標

- 提供以 Google 帳號登入應用程式的入口

---

## 線框圖

```text
+--------------------------------+
|                                |
|           App Logo             |
|                                |
|                                |
|      [ Sign in with Google ]   |
|                                |
+--------------------------------+
```

---

## 佈局

### 主區域

- App Logo
- Google 登入按鈕

---

## 互動

- **點按 Google 登入按鈕:**
  - 呼叫 handlePostAuth
  - **IF** 操作中:
    - 顯示載入狀態
  - **IF** 操作成功:
    - 導航至 HomeScreen
  - **IF** 操作失敗:
    - 顯示登入失敗提示
