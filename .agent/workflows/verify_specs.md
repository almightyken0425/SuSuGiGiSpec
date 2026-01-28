---
description: Verify specification files against strict linter rules
---

// turbo-all
1. First, refer to the `spec_linter` skill (`.agent/skills/spec_linter/SKILL.md`) to understand the valid rules and exceptions (note: checks exclude code blocks).

2. Then, run the spec linter on the entire SuSuGiGiSpec repository.

```powershell
python "c:\Users\ken.chio\OneDrive - 勝和科技有限公司\文件\Repository\KnowledgeVault\.agent\skills\spec_linter\scripts\lint_spec.py" "c:\Users\ken.chio\OneDrive - 勝和科技有限公司\文件\Repository\SuSuGiGiSpec"
```
