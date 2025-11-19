import csv

CSV_PATH = 'no2_equity_model/product_value_allocation.csv'
OUTPUT_PATH = 'no2_equity_model/product_value_allocation.csv'

def move_ai_advisor():
    rows = []
    fieldnames = []
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            product = row['Product']
            
            if product == 'AI Advisor':
                # Move App RD points to Web RD
                app_c = int(row.get('App RD_Construction', '0') or '0')
                app_o = int(row.get('App RD_Operation', '0') or '0')
                
                web_c = int(row.get('Web RD_Construction', '0') or '0')
                web_o = int(row.get('Web RD_Operation', '0') or '0')
                
                # Add to Web RD
                row['Web RD_Construction'] = str(web_c + app_c)
                row['Web RD_Operation'] = str(web_o + app_o)
                
                # Clear App RD
                row['App RD_Construction'] = '0'
                row['App RD_Operation'] = '0'
                
            rows.append(row)

    with open(OUTPUT_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Moved AI Advisor points to Web RD in {OUTPUT_PATH}")

if __name__ == "__main__":
    move_ai_advisor()
