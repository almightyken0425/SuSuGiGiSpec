import csv
import os

CSV_PATH = 'no2_equity_model/product_value_allocation.csv'
OUTPUT_PATH = 'no2_equity_model/product_value_allocation.csv'

def migrate():
    rows = []
    fieldnames = []
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        old_fieldnames = reader.fieldnames
        
        # Define new fieldnames
        # Remove Frontend RD_Construction, Frontend RD_Operation
        # Add App RD_Construction, App RD_Operation, Web RD_Construction, Web RD_Operation
        
        fieldnames = [f for f in old_fieldnames if 'Frontend RD' not in f]
        
        # Find insertion point (after UI or UX)
        try:
            idx = fieldnames.index('UI_Operation') + 1
        except ValueError:
            # Fallback
            idx = 10
            
        new_cols = ['App RD_Construction', 'App RD_Operation', 'Web RD_Construction', 'Web RD_Operation']
        for col in reversed(new_cols):
            fieldnames.insert(idx, col)
            
        print(f"New columns: {new_cols}")
        
        for row in reader:
            # Get original values
            frontend_c = int(row.get('Frontend RD_Construction', '0') or '0')
            frontend_o = int(row.get('Frontend RD_Operation', '0') or '0')
            
            product = row['Product']
            
            app_c = 0
            app_o = 0
            web_c = 0
            web_o = 0
            
            # Logic: 
            # App: 記帳 App, AI Advisor
            # Web: Web Console, Macro Data
            
            if product in ['記帳 App', 'AI Advisor']:
                app_c = frontend_c
                app_o = frontend_o
            elif product in ['Web Console', 'Macro Data']:
                web_c = frontend_c
                web_o = frontend_o
            else:
                # Default to Web if unknown or split? 
                # Let's assume Web for safety or print warning.
                # Actually, Macro Data has "Macro API" which might be Backend only, but if it had Frontend points, where do they go?
                # Macro Data has "Dashboard" -> Web.
                # Let's stick to the plan.
                web_c = frontend_c
                web_o = frontend_o
                
            # Apply updates
            new_row = row.copy()
            
            # Remove old keys
            if 'Frontend RD_Construction' in new_row: del new_row['Frontend RD_Construction']
            if 'Frontend RD_Operation' in new_row: del new_row['Frontend RD_Operation']
            
            # Set new keys
            new_row['App RD_Construction'] = str(app_c)
            new_row['App RD_Operation'] = str(app_o)
            new_row['Web RD_Construction'] = str(web_c)
            new_row['Web RD_Operation'] = str(web_o)
            
            rows.append(new_row)

    with open(OUTPUT_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Migrated {len(rows)} rows to {OUTPUT_PATH}")

if __name__ == "__main__":
    migrate()
