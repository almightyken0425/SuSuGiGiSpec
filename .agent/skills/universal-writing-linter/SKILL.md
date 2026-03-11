---
name: universal-writing-linter
description: 專門用於檢查與校正任何 Markdown 規格文件與各式程式碼或程式碼註解，確保嚴格遵循通用寫作禁令、命名規範與排版原則。
---

# Universal Writing Linter & Formatter Skill

## Policy 參考

- `universal_writing_policy.md` 底層絕對禁令，跨所有文字類型
- `spec_writing_policy.md` 規格書通用結構語言
- `screen_spec_policy.md` 畫面規格書專屬規範

---

## 觸發機制

- **自動檢查:** 在讀取或修改規格文件前，先掃描是否違反禁令
- **主動校正:** 在完成寫作或編輯後，執行格式化修正
- **腳本驗證:** 必須執行驗證腳本並確保檢核通過

---

## 執行步驟

- 對照 `universal_writing_policy.md` 掃描違禁品
- 對照 `spec_writing_policy.md` 校正結構與關鍵字格式
- 若為畫面規格書，額外對照 `screen_spec_policy.md`
- 執行 lint 腳本，根據錯誤訊息修正直到通過

```powershell
python ".agent\skills\spec_linter\scripts\lint_spec.py" <檔案路徑>
```

---

## 防呆守則：IDE 災情廣播系統回饋

- **強制要求:** 每次修改檔案準備回覆使用者前，必須注意 IDE 攔截到的語法或 Lint 錯誤回饋
- **觸發:** 檔案名稱因語法錯誤或型別錯誤變成紅色，或程式碼底部出現紅色波浪底線
- **動作:** 收到 Error Severity 或編譯錯誤時：
    - 必須把修復紅字型別與語法錯誤視為當前最高優先級任務
    - 必須主動呼叫工具修正錯誤，直到紅字消失為止
    - 嚴禁假裝沒看到錯誤就直接回覆使用者完成
