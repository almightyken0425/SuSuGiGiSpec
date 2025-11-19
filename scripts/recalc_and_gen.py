import csv
import os

CSV_PATH = 'no2_equity_model/product_value_allocation.csv'
MD_PATH = 'no2_equity_model/no4_product_component.md'

def calculate_points(row):
    # Columns to sum for Base Points
    # Designer is split into UX and UI
    # Frontend is split into App RD and Web RD
    tech_roles = [
        'UX_Construction', 'UI_Construction', 
        'App RD_Construction', 'Web RD_Construction', 'Backend RD_Construction',
        'QA_Construction', 'AI Engineer_Construction', 'Data Engineer_Construction'
    ]
    
    base_points = 0
    for role in tech_roles:
        val = row.get(role, '0')
        if val == '': val = '0'
        base_points += int(val.replace(',', ''))
    
    # Calculate PDM (25%) and PJM (15%)
    pdm_points = int(round(base_points * 0.25 / 10) * 10)
    pjm_points = int(round(base_points * 0.15 / 10) * 10)
    
    return pdm_points, pjm_points

def update_csv():
    rows = []
    fieldnames = []
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        # Ensure PJM columns exist (already handled by migration, but safe to keep)
        if 'PJM_Construction' not in fieldnames:
            # Insert after PDM
            pdm_idx = fieldnames.index('PDM_Operation')
            fieldnames.insert(pdm_idx + 1, 'PJM_Construction')
            fieldnames.insert(pdm_idx + 2, 'PJM_Operation')
            
        for row in reader:
            pdm, pjm = calculate_points(row)
            
            # Update PDM
            row['PDM_Construction'] = str(pdm)
            # PDM Operation is usually static or based on other logic, keeping existing logic or default
            # For now, we only touched Construction value logic in the plan. 
            # But wait, the plan said "Update PDM_Construction and PDM_Operation values".
            # The user only discussed Construction value (Blueprint vs Construction). 
            # I will leave Operation as is for now unless it's clearly proportional.
            # Actually, let's look at the CSV, PDM_Operation is small (3, 5, 10). 
            # I will leave PDM_Operation alone as I don't have a formula for it.
            
            # Update PJM
            row['PJM_Construction'] = str(pjm)
            # PJM Operation = PDM Operation * 0.6
            pdm_op = int(row.get('PDM_Operation', '0') or '0')
            pjm_op = int(round(pdm_op * 0.6))
            row['PJM_Operation'] = str(pjm_op)
            
            rows.append(row)
            
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    return rows

def generate_markdown(rows):
    # Group by Product -> Module
    structure = {}
    for row in rows:
        prod = row['Product']
        mod = row['Module']
        if prod not in structure: structure[prod] = {}
        if mod not in structure[prod]: structure[prod][mod] = []
        structure[prod][mod].append(row)
        
    lines = []
    lines.append("# 產品組件與價值分配")
    lines.append("")
    lines.append("## 核心目標")
    lines.append("")
    lines.append("- 本文件依據產品定義的產品個體，詳細列出每個組件的價值構成。")
    lines.append("- 採用 **雙重價值模型**：每個模組同時包含 **施工價值** (Construction) 與 **維運價值** (Operation)。")
    lines.append("- 針對每個 **User Story**，依據角色定義進行價值點數分配。")
    lines.append("- **營運角色整合:** Marketing 與 Operations 角色整合至每個 User Story 中，其施工價值為 0，但隨著功能上線，其維運價值 (Operation Value) 將逐步累積。")
    lines.append("- **價值單位:** 1 點 = 0.1 小時，詳見股權原則文件。")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    prod_idx = 1
    grand_total_const = 0
    grand_total_op = 0
    
    # Summary table data
    summary_data = []

    for prod, modules in structure.items():
        # Calculate Product Totals
        prod_const = 0
        prod_op = 0
        for mod, items in modules.items():
            for item in items:
                for k, v in item.items():
                    if 'Construction' in k: prod_const += int(v or 0)
                    if 'Operation' in k: prod_op += int(v or 0)
        
        # Product Header
        # Need to map Product name to the specific header format if possible, or just use the name
        # The original file has "1. 記帳 App + Firestore, Accounting App"
        # I'll try to match the existing format by hardcoding or just using the CSV name if it matches enough.
        # CSV: "記帳 App", "Web Console", "AI Advisor", "Macro Data"
        # MD: "1. 記帳 App + Firestore, Accounting App", "2. Web 複雜報表, Web Console", "3. AI 個人化建議, AI Advisor", "4. 總經分析報表與 API, Macro Data Service"
        # I will map them manually to preserve the exact titles.
        
        titles = {
            "記帳 App": "記帳 App + Firestore, Accounting App",
            "Web Console": "Web 複雜報表, Web Console",
            "AI Advisor": "AI 個人化建議, AI Advisor",
            "Macro Data": "總經分析報表與 API, Macro Data Service"
        }
        
        title = titles.get(prod, prod)
        
        lines.append(f"## {prod_idx}. {title}")
        lines.append("")
        lines.append("**價值模型:**")
        # Calculate man-months (2000 pts = 1 month)
        mm = prod_const / 2000
        lines.append(f"- **施工價值, Construction:** {prod_const:,} 點 / 次 ({prod_const/10:,.0f} 小時 = {mm:.1f} 人月)")
        lines.append(f"- **維運價值, Operation:** {prod_op:,} 點 / 月 ({prod_op/10:,.1f} 小時/月)")
        lines.append("")
        
        summary_data.append({
            "name": f"{prod_idx}. {prod}",
            "const": prod_const,
            "op": prod_op
        })

        mod_idx = 1
        for mod, items in modules.items():
            # Module Header
            # CSV: "交易與自動化"
            # MD: "1.1 交易與自動化, Transaction & Automation"
            # I need to map these too or just use the CSV value if I can't map.
            # The CSV doesn't have the English name for Module. 
            # I might lose the English names if I don't hardcode them. 
            # For now, I will try to keep it simple or extract from existing file? 
            # To be safe, I will just use the Chinese name from CSV and maybe append a placeholder or try to map common ones.
            # Actually, looking at the file content I read earlier:
            # 1.1 交易與自動化, Transaction & Automation
            # 1.2 資產管理, Asset Management
            # 1.3 資料與同步, Data & Sync
            # 1.4 儀表板與體驗, Dashboard & Experience
            # 1.5 共用帳本, Shared Ledger
            # 2.1 高密度資料瀏覽, Data Browsing
            # 2.2 進階篩選與查詢, Advanced Query
            # 2.3 客製化報表, Custom Reporting
            # 3.1 智慧偵測, Intelligent Detection
            # 3.2 預測與診斷, Forecast & Diagnosis
            # 4.1 B 端數據服務, B2B Data Services
            
            mod_en_map = {
                "交易與自動化": "Transaction & Automation",
                "資產管理": "Asset Management",
                "資料與同步": "Data & Sync",
                "儀表板與體驗": "Dashboard & Experience",
                "共用帳本": "Shared Ledger",
                "高密度資料瀏覽": "Data Browsing",
                "進階篩選與查詢": "Advanced Query",
                "客製化報表": "Custom Reporting",
                "智慧偵測": "Intelligent Detection",
                "預測與診斷": "Forecast & Diagnosis",
                "B2B 數據服務": "B2B Data Services"
            }
            
            mod_title = f"{prod_idx}.{mod_idx} {mod}"
            if mod in mod_en_map:
                mod_title += f", {mod_en_map[mod]}"
            
            lines.append(f"### {mod_title}")
            lines.append("")
            lines.append("| User Story | Role | 施工價值 (Pt) | 維運價值 (Pt/Mo) |")
            lines.append("| :--- | :--- | :--- | :--- |")
            
            for item in items:
                us_name = item['User Story (中文)']
                us_en = item['User Story (English)']
                
                # Calculate Subtotal
                sub_const = 0
                sub_op = 0
                
                # Roles to display (Updated with App/Web RD)
                roles_order = [
                    ('PDM', 'PDM'),
                    ('PJM', 'PJM'),
                    ('UX', 'UX Designer'),
                    ('UI', 'UI Designer'),
                    ('App RD', 'App RD'),
                    ('Web RD', 'Web RD'),
                    ('Backend RD', 'Backend RD'),
                    ('AI Engineer', 'AI Engineer'),
                    ('Data Engineer', 'Data Engineer'),
                    ('QA', 'QA'),
                    ('Marketing', 'Marketing'),
                    ('Operations', 'Operations')
                ]
                
                first_row = True
                
                # Collect active roles
                active_roles = []
                for role_key, role_name in roles_order:
                    c = int(item.get(f"{role_key}_Construction", 0) or 0)
                    o = int(item.get(f"{role_key}_Operation", 0) or 0)
                    if c > 0 or o > 0:
                        active_roles.append((role_name, c, o))
                        sub_const += c
                        sub_op += o
                
                # Render rows
                # First role line includes the User Story name
                if not active_roles:
                    continue
                    
                for i, (r_name, c, o) in enumerate(active_roles):
                    us_col = ""
                    if i == 0:
                        us_col = f"**{us_name}**"
                    elif i == 1:
                        us_col = f"({us_en})"
                    
                    # Bold Marketing and Operations rows as per original style
                    r_display = r_name
                    c_display = f"{c:,}"
                    o_display = f"{o:,}"
                    
                    if r_name in ['Marketing', 'Operations']:
                        r_display = f"**{r_name}**"
                        c_display = f"**{c:,}**"
                        o_display = f"**{o:,}**"
                        
                    lines.append(f"| {us_col} | {r_display} | {c_display} | {o_display} |")
                
                # If US name/en took more lines than roles (unlikely but possible if no roles), handle it.
                # But here we have roles.
                # If there are fewer than 2 roles, we still need to print the English name on the second line?
                # The original format:
                # | **支出管理** | PDM | 100 | 3 |
                # | (Expense CRUD) | Designer | 200 | 3 |
                # If only 1 role:
                # | **Name** | Role | ... |
                # | (En Name) | | | |  <-- Need to handle this
                
                if len(active_roles) < 2:
                     lines.append(f"| ({us_en}) | | | |")
                
                # Subtotal Row
                lines.append(f"| | **Subtotal** | **{sub_const:,}** | **{sub_op:,}** |")
            
            lines.append("")
            mod_idx += 1
            
        lines.append("---")
        lines.append("")
        prod_idx += 1
        grand_total_const += prod_const
        grand_total_op += prod_op

    # Summary Table
    lines.append("## 價值彙整")
    lines.append("")
    lines.append("| 產品組件 | 施工價值 (點) | 施工工時 | 維運價值 (點/月) | 年化維運 |")
    lines.append("| :--- | ---: | ---: | ---: | ---: |")
    
    for item in summary_data:
        mm = item['const'] / 2000
        annual_op = item['op'] * 12
        lines.append(f"| {item['name']} | {item['const']:,} | {mm:.1f} 人月 | {item['op']:,} | {annual_op:,} |")
        
    total_mm = grand_total_const / 2000
    total_annual = grand_total_op * 12
    lines.append(f"| **總計** | **{grand_total_const:,}** | **{total_mm:.1f} 人月** | **{grand_total_op:,}** | **{total_annual:,}** |")
    lines.append("")

    with open(MD_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    print("Updating CSV...")
    rows = update_csv()
    print("Generating Markdown...")
    generate_markdown(rows)
    print("Done.")
