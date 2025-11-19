import csv

CSV_PATH = 'no2_equity_model/product_value_allocation.csv'
OUTPUT_PATH = 'no2_equity_model/product_value_allocation.csv'

def fix_values():
    rows = []
    fieldnames = []
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            story = row['User Story (English)']
            web_c = int(row.get('Web RD_Construction', '0') or '0')
            
            # Fix missing Web RD values
            if web_c == 0:
                if story == 'Data Grid':
                    row['Web RD_Construction'] = '800'
                    row['Web RD_Operation'] = '30'
                elif story == 'Adv Export':
                    row['Web RD_Construction'] = '200'
                    row['Web RD_Operation'] = '10'
                elif story == 'JQL Interface':
                    row['Web RD_Construction'] = '500'
                    row['Web RD_Operation'] = '20'
                elif story == 'Saved Views':
                    row['Web RD_Construction'] = '150'
                    row['Web RD_Operation'] = '5'
                elif story == 'Custom Charts':
                    row['Web RD_Construction'] = '800'
                    row['Web RD_Operation'] = '30'
                elif story == 'Report Export':
                    row['Web RD_Construction'] = '150'
                    row['Web RD_Operation'] = '5'
                elif story == 'Dashboard': # B2B
                    row['Web RD_Construction'] = '600'
                    row['Web RD_Operation'] = '20'
                elif story == 'Competitor': # B2B
                    row['Web RD_Construction'] = '600'
                    row['Web RD_Operation'] = '20'
            
            rows.append(row)

    with open(OUTPUT_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Fixed Web RD values in {OUTPUT_PATH}")

if __name__ == "__main__":
    fix_values()
