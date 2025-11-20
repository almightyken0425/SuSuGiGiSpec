import pandas as pd
import os

# ==========================================
# Configuration: File Paths
# ==========================================
# Input File
INPUT_FILE = 'no6_1_product_value_allocation.csv'

# Output Files
OUTPUT_FILE_MODULE_ROLE = 'no6_2_module_role_points.csv'
OUTPUT_FILE_ROLE_SUMMARY = 'no7_1_equity_summary_by_role.csv'
OUTPUT_FILE_COMPONENT_SUMMARY = 'no7_2_equity_summary_by_component.csv'
OUTPUT_FILE_CONSISTENCY = 'no7_3_equity_consistency_analysis.csv'

# Base Directory (Current Script Directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Full Paths
input_path = os.path.join(BASE_DIR, INPUT_FILE)
output_path_module_role = os.path.join(BASE_DIR, OUTPUT_FILE_MODULE_ROLE)
output_path_role_summary = os.path.join(BASE_DIR, OUTPUT_FILE_ROLE_SUMMARY)
output_path_component_summary = os.path.join(BASE_DIR, OUTPUT_FILE_COMPONENT_SUMMARY)
output_path_consistency = os.path.join(BASE_DIR, OUTPUT_FILE_CONSISTENCY)

# ==========================================
# Main Logic
# ==========================================

def parse_int(value):
    """Helper to parse currency/number strings to int."""
    if pd.isna(value) or value == '':
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(str(value).replace(',', '').replace('$', '').replace('+', '').strip())
    except ValueError:
        return 0

def main():
    print(f"Reading input from: {input_path}")
    
    # 1. Load Data
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    # Clean up column names (strip whitespace)
    df.columns = df.columns.str.strip()

    # Identify Role Columns dynamically
    # Columns ending with _Construction or _Operation
    role_cols = [c for c in df.columns if c.endswith('_Construction') or c.endswith('_Operation')]
    
    # Extract unique role names
    roles = sorted(list(set([c.replace('_Construction', '').replace('_Operation', '') for c in role_cols])))
    
    print(f"Identified Roles: {roles}")

    # Ensure numeric columns are actually numeric
    for col in role_cols:
        df[col] = df[col].apply(parse_int)

    # Role Display Mapping
    role_display_map = {
        'UI': 'UI Designer',
        'UX': 'UX Designer',
    }

    # ==========================================
    # Task 1: Generate no6_2_module_role_points.csv
    # ==========================================
    print("Generating no6_2_module_role_points.csv...")
    
    module_role_rows = []
    
    for index, row in df.iterrows():
        product = row['Product']
        module = row['Module']
        user_story = row.get('User Story (中文)', '')
        launch_date = row.get('Launch Date', '')
        status = row.get('Status', '')
        
        for role in roles:
            const_points = row.get(f'{role}_Construction', 0)
            ops_points = row.get(f'{role}_Operation', 0)
            
            # if const_points == 0 and ops_points == 0:
            #    continue
            
            display_role = role_display_map.get(role, role)
            
            module_role_rows.append({
                'Product': product,
                'Module': module,
                'User Story': user_story,
                'Launch Date': launch_date,
                'Status': status,
                'Role': display_role,
                'Construction Points': const_points,
                'Operation Points': ops_points
            })
            
    df_module_role = pd.DataFrame(module_role_rows)
    # Reorder columns
    df_module_role = df_module_role[['Product', 'Module', 'User Story', 'Launch Date', 'Status', 'Role', 'Construction Points', 'Operation Points']]
    df_module_role.to_csv(output_path_module_role, index=False, encoding='utf-8-sig')


    # ==========================================
    # Task 2: Generate no7_1_equity_summary_by_role.csv
    # ==========================================
    print("Generating no7_1_equity_summary_by_role.csv...")
    
    role_summary_data = []
    total_construction_points = 0
    
    for role in roles:
        const_col = f'{role}_Construction'
        total_points = df[const_col].sum()
        total_construction_points += total_points
        
        display_role = role_display_map.get(role, role)
        role_summary_data.append({
            'Role': display_role,
            'Points': total_points
        })
        
    df_role_summary = pd.DataFrame(role_summary_data)
    df_role_summary = df_role_summary.sort_values('Points', ascending=False)
    
    # Calculate percentages and man-months
    # Avoid division by zero
    if total_construction_points == 0:
        total_construction_points = 1 
        
    df_role_summary['Percentage'] = (df_role_summary['Points'] / total_construction_points * 100).map('{:.1f}%'.format)
    df_role_summary['Man Months'] = (df_role_summary['Points'] / 2000).map('{:.1f} 人月'.format)
    
    # Formatting for output
    output_rows_role_summary = []
    output_rows_role_summary.append(['角色', '施工價值 (點)', '佔總價值比例', '換算工時'])
    
    for _, row in df_role_summary.iterrows():
        if row['Points'] == 0: continue
        output_rows_role_summary.append([
            f"**{row['Role']}**",
            f"{row['Points']:,}",
            row['Percentage'],
            row['Man Months']
        ])
        
    # Total Row
    total_mm = total_construction_points / 2000
    output_rows_role_summary.append([
        "**總計**",
        f"**{total_construction_points:,}**",
        "**100.0%**",
        f"**{total_mm:.1f} 人月**"
    ])
    
    pd.DataFrame(output_rows_role_summary).to_csv(output_path_role_summary, index=False, header=False, encoding='utf-8-sig')


    # ==========================================
    # Task 3: Generate no7_2_equity_summary_by_component.csv
    # ==========================================
    print("Generating no7_2_equity_summary_by_component.csv...")
    
    # Calculate total construction points per product
    # We need to sum all role construction columns for each row, then group by Product
    df['Row_Total_Construction'] = 0
    for role in roles:
        df['Row_Total_Construction'] += df[f'{role}_Construction']
        
    product_summary = df.groupby('Product')['Row_Total_Construction'].sum().reset_index()
    
    component_map = {
        '記帳 App': '記帳 App + Firestore',
        'Web Console': 'Web 複雜報表',
        'AI Advisor': 'AI 個人化建議',
        'Macro Data': '總經分析報表與 API'
    }
    
    ordered_products = ['記帳 App', 'Web Console', 'AI Advisor', 'Macro Data']
    
    output_rows_component_summary = []
    output_rows_component_summary.append(['產品組件', '施工價值 (點)', '佔總價值比例', '換算工時'])
    
    for prod in ordered_products:
        points = product_summary.loc[product_summary['Product'] == prod, 'Row_Total_Construction'].sum()
        name = component_map.get(prod, prod)
        
        percentage = (points / total_construction_points * 100)
        man_months = points / 2000
        
        output_rows_component_summary.append([
            name,
            f"{points:,}",
            f"{percentage:.1f}%",
            f"{man_months:.1f} 人月"
        ])
        
    # Total Row
    output_rows_component_summary.append([
        "**總計**",
        f"**{total_construction_points:,}**",
        "**100.0%**",
        f"**{total_mm:.1f} 人月**"
    ])
    
    pd.DataFrame(output_rows_component_summary).to_csv(output_path_component_summary, index=False, header=False, encoding='utf-8-sig')


    # ==========================================
    # Task 4: Generate no7_3_equity_consistency_analysis.csv
    # ==========================================
    print("Generating no7_3_equity_consistency_analysis.csv...")
    
    # Calculate Ops points per product
    df['Row_Total_Operation'] = 0
    for role in roles:
        df['Row_Total_Operation'] += df[f'{role}_Operation']
        
    prod_ops_summary = df.groupby('Product')['Row_Total_Operation'].sum()
    prod_const_summary = df.groupby('Product')['Row_Total_Construction'].sum()
    
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
    
    output_rows_consistency = []
    output_rows_consistency.append(['Tier', '月費', '年費', '累積施工 (點)', '年化維運 (點)', '維運/定價比'])
    
    for tier in tiers:
        const = 0
        ops_annual = 0
        
        for p in tier['products']:
            const += prod_const_summary.get(p, 0)
            if not tier.get('is_tier_0', False):
                ops_annual += prod_ops_summary.get(p, 0) * 12
                
        # Ratio
        ratio_str = "-"
        if ops_annual > 0:
            price_val = parse_int(tier['price_yr'])
            if price_val > 0:
                ratio = ops_annual / price_val
                ratio_str = f"{int(round(ratio))}:1"
                
        output_rows_consistency.append([
            tier['name'],
            tier['price_mo'],
            tier['price_yr'],
            f"{const:,}",
            f"{ops_annual:,}",
            ratio_str
        ])
        
    pd.DataFrame(output_rows_consistency).to_csv(output_path_consistency, index=False, header=False, encoding='utf-8-sig')

    print("All files generated successfully.")

if __name__ == "__main__":
    main()
