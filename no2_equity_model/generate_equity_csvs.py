import csv
import os

INPUT_FILE = '/Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no2_equity_model/no6_1_product_value_allocation.csv'
OUTPUT_DIR = '/Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no2_equity_model'

def parse_int(value):
    if not value or value.strip() == '':
        return 0
    try:
        return int(value.replace(',', ''))
    except ValueError:
        return 0

def main():
    data = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    # Roles defined in the CSV header (Construction and Operation columns)
    # Extract roles dynamically or hardcode based on known structure
    # Based on file content: PDM, PJM, UX, UI, App RD, Web RD, Backend RD, QA, AI Engineer, Data Engineer, Marketing, Operations
    roles = [
        'PDM', 'UI', 'QA', 'App RD', 'Web RD', 'UX', 'PJM', 
        'AI Engineer', 'Backend RD', 'Data Engineer', 'Marketing', 'Operations'
    ]
    
    # Mapping for Role Names if needed (e.g. UI -> UI Designer)
    role_display_map = {
        'UI': 'UI Designer',
        'UX': 'UX Designer',
        # Others seem to match or are close enough
    }

    # --- 1. Summary by Role (L15-L30) ---
    role_stats = {}
    total_construction_points = 0

    for role in roles:
        const_key = f'{role}_Construction'
        role_total = 0
        for row in data:
            role_total += parse_int(row.get(const_key, '0'))
        
        display_name = role_display_map.get(role, role)
        role_stats[display_name] = role_total
        total_construction_points += role_total

    # Sort by points descending
    sorted_roles = sorted(role_stats.items(), key=lambda x: x[1], reverse=True)

    with open(os.path.join(OUTPUT_DIR, 'no7_1_equity_summary_by_role.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['角色', '施工價值 (點)', '佔總價值比例', '換算工時'])
        
        for role, points in sorted_roles:
            if points == 0: continue # Skip roles with 0 points if any
            percentage = (points / total_construction_points) * 100
            man_months = points / 2000
            writer.writerow([
                f"**{role}**", 
                f"{points:,}", 
                f"{percentage:.1f}%", 
                f"{man_months:.1f} 人月"
            ])
        
        # Total row
        total_mm = total_construction_points / 2000
        writer.writerow([
            "**總計**", 
            f"**{total_construction_points:,}**", 
            "**100.0%**", 
            f"**{total_mm:.1f} 人月**"
        ])

    print(f"Generated no7_1_equity_summary_by_role.csv")

    # --- 2. Summary by Product Component (L31-L39) ---
    # Mapping Product to Component Name
    # "記帳 App" -> "記帳 App + Firestore"
    # "Web Console" -> "Web 複雜報表" (Wait, need to check if this mapping is correct or if it's by row groups)
    # Looking at the markdown:
    # 記帳 App + Firestore: 25,975
    # Web 複雜報表: 13,440
    # AI 個人化建議: 9,830
    # 總經分析報表與 API: 17,640
    
    # Let's calculate points per Product in CSV
    product_points = {}
    
    for row in data:
        product = row['Product']
        # Sum all construction points for this row
        row_points = 0
        for role in roles:
            row_points += parse_int(row.get(f'{role}_Construction', '0'))
        
        if product not in product_points:
            product_points[product] = 0
        product_points[product] += row_points

    # Map CSV Product names to Output Component names
    # CSV Products: '記帳 App', 'Web Console', 'AI Advisor', 'Macro Data'
    component_map = {
        '記帳 App': '記帳 App + Firestore',
        'Web Console': 'Web 複雜報表',
        'AI Advisor': 'AI 個人化建議',
        'Macro Data': '總經分析報表與 API'
    }

    with open(os.path.join(OUTPUT_DIR, 'no7_2_equity_summary_by_component.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['產品組件', '施工價值 (點)', '佔總價值比例', '換算工時'])
        
        # We want specific order? Or just iterate. The markdown has a specific order.
        ordered_products = ['記帳 App', 'Web Console', 'AI Advisor', 'Macro Data']
        
        for prod in ordered_products:
            points = product_points.get(prod, 0)
            name = component_map.get(prod, prod)
            percentage = (points / total_construction_points) * 100
            man_months = points / 2000
            writer.writerow([
                name, 
                f"{points:,}", 
                f"{percentage:.1f}%", 
                f"{man_months:.1f} 人月"
            ])
            
        # Total row
        writer.writerow([
            "**總計**", 
            f"**{total_construction_points:,}**", 
            "**100.0%**", 
            f"**{total_mm:.1f} 人月**"
        ])

    print(f"Generated no7_2_equity_summary_by_component.csv")

    # --- 3. Value/Pricing Consistency Analysis (L75-L83) ---
    # Tiers definition
    # Tier 0: Local (Just App Construction, 0 Ops)
    # Tier 1: Cloud (App Construction, App Ops * 12)
    # Tier 2: Management (+ Web Console Construction, + Web Ops * 12)
    # Tier 3: Intelligence (+ AI Advisor Construction, + AI Ops * 12)
    # Tier B: Enterprise (+ Macro Data Construction, + Macro Ops * 12)
    
    # Calculate Total Construction and Monthly Ops per Product
    prod_stats = {} # {prod: {'const': 0, 'ops': 0}}
    for row in data:
        prod = row['Product']
        if prod not in prod_stats:
            prod_stats[prod] = {'const': 0, 'ops': 0}
        
        for role in roles:
            prod_stats[prod]['const'] += parse_int(row.get(f'{role}_Construction', '0'))
            prod_stats[prod]['ops'] += parse_int(row.get(f'{role}_Operation', '0'))

    def get_tier_stats(included_products, is_tier_0=False):
        const = 0
        ops_annual = 0
        for p in included_products:
            const += prod_stats[p]['const']
            if not is_tier_0:
                ops_annual += prod_stats[p]['ops'] * 12
        return const, ops_annual

    tiers = [
        {
            'name': 'Tier 0 (Local)', 'price_mo': '$0', 'price_yr': '$0',
            'products': ['記帳 App'], 'is_tier_0': True
        },
        {
            'name': 'Tier 1 (Cloud)', 'price_mo': '$30', 'price_yr': '$360',
            'products': ['記帳 App'], 'is_tier_0': False
        },
        {
            'name': 'Tier 2 (Management)', 'price_mo': '$90', 'price_yr': '$900',
            'products': ['記帳 App', 'Web Console'], 'is_tier_0': False
        },
        {
            'name': 'Tier 3 (Intelligence)', 'price_mo': '$140', 'price_yr': '$1,400',
            'products': ['記帳 App', 'Web Console', 'AI Advisor'], 'is_tier_0': False
        },
        {
            'name': 'Tier B (Enterprise)', 'price_mo': '$500+', 'price_yr': '$6,000+',
            'products': ['記帳 App', 'Web Console', 'AI Advisor', 'Macro Data'], 'is_tier_0': False
        }
    ]

    with open(os.path.join(OUTPUT_DIR, 'no7_3_equity_consistency_analysis.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tier', '月費', '年費', '累積施工 (點)', '年化維運 (點)', '維運/定價比'])
        
        for tier in tiers:
            const, ops = get_tier_stats(tier['products'], tier.get('is_tier_0', False))
            
            # Ratio
            ratio_str = "-"
            if ops > 0:
                # Try to parse price to int for calculation if needed, but here we just need the ratio
                # The user example has "28:1", "23:1". 
                # It seems to be Price / (Ops cost)? No, wait.
                # Tier 1: Price $360. Ops 9948. Ratio 28:1. 
                # 9948 / 360 = 27.63 -> 28. So it is Ops Points / Price ($).
                
                price_val = 0
                try:
                    price_clean = tier['price_yr'].replace('$', '').replace(',', '').replace('+', '')
                    price_val = int(price_clean)
                except:
                    price_val = 0
                
                if price_val > 0:
                    ratio = ops / price_val
                    ratio_str = f"{int(round(ratio))}:1"
            
            writer.writerow([
                tier['name'],
                tier['price_mo'],
                tier['price_yr'],
                f"{const:,}",
                f"{ops:,}",
                ratio_str
            ])

    print(f"Generated no7_3_equity_consistency_analysis.csv")

    # --- 4. Module/Role Construction & Operation Points (Detailed) ---
    # "每個 module 底下不同角色會擁有的Construction 與 Operation 點數會是多少"
    # Columns: Product, Module, Role, Construction Points, Operation Points
    
    with open(os.path.join(OUTPUT_DIR, 'no6_2_module_role_points.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Product', 'Module', 'Role', 'Construction Points', 'Operation Points'])
        
        # We need to aggregate by Module. The CSV has multiple rows per module (different User Stories).
        # Or does the user want per Module (as in the 'Module' column)? Yes.
        
        # Structure: { (Product, Module): { Role: {const: 0, ops: 0} } }
        module_stats = {}
        
        for row in data:
            key = (row['Product'], row['Module'])
            if key not in module_stats:
                module_stats[key] = {}
            
            for role in roles:
                if role not in module_stats[key]:
                    module_stats[key][role] = {'const': 0, 'ops': 0}
                
                module_stats[key][role]['const'] += parse_int(row.get(f'{role}_Construction', '0'))
                module_stats[key][role]['ops'] += parse_int(row.get(f'{role}_Operation', '0'))
        
        # Write out
        # Sort by Product then Module
        sorted_keys = sorted(module_stats.keys())
        
        for prod, mod in sorted_keys:
            for role in roles:
                stats = module_stats[(prod, mod)][role]
                if stats['const'] == 0 and stats['ops'] == 0:
                    continue # Skip empty roles for clarity? Or keep them? 
                             # User asked for "what points they will have", implies non-zero.
                
                display_role = role_display_map.get(role, role)
                writer.writerow([
                    prod,
                    mod,
                    display_role,
                    stats['const'],
                    stats['ops']
                ])

    print(f"Generated no6_2_module_role_points.csv")

if __name__ == '__main__':
    main()
