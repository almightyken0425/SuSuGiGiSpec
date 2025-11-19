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
        # Remove Designer_Construction, Designer_Operation
        # Add UX_Construction, UX_Operation, UI_Construction, UI_Operation
        # Insert them where Designer was
        
        fieldnames = [f for f in old_fieldnames if 'Designer' not in f]
        
        # Find insertion point (after PJM or PDM)
        try:
            idx = fieldnames.index('PJM_Operation') + 1
        except ValueError:
            idx = fieldnames.index('PDM_Operation') + 1
            
        new_cols = ['UX_Construction', 'UX_Operation', 'UI_Construction', 'UI_Operation']
        for col in reversed(new_cols):
            fieldnames.insert(idx, col)
            
        print(f"New columns: {new_cols}")
        
        for row in reader:
            # Get original values
            designer_c = int(row.get('Designer_Construction', '0') or '0')
            designer_o = int(row.get('Designer_Operation', '0') or '0')
            frontend_c = int(row.get('Frontend RD_Construction', '0') or '0')
            backend_c = int(row.get('Backend RD_Construction', '0') or '0')
            
            # Default Split (40% UX, 60% UI)
            ux_c = int(designer_c * 0.4)
            ui_c = int(designer_c * 0.6)
            ux_o = int(designer_o * 0.4)
            ui_o = int(designer_o * 0.6)
            
            # Specific Re-estimation Logic
            module = row['Module']
            story = row['User Story (English)']
            
            # 1. Home Screen (High UI, High Frontend)
            if story == 'Home Dash':
                ux_c = 200
                ui_c = 600 # High visual polish
                frontend_c = int(frontend_c * 1.5) # Animation complexity
                
            # 2. Import Wizard (High UX, High Frontend)
            elif story == 'CSV Import':
                ux_c = 500 # Complex mapping flow
                ui_c = 200
                frontend_c = int(frontend_c * 1.3) # Wizard state management
                
            # 3. Sync Engine (High UX, Very High Backend, High Frontend)
            elif story == 'Sync Engine':
                ux_c = 500 # Conflict resolution flows
                ui_c = 100 # Minimal UI
                backend_c = int(backend_c * 1.5) # Offline-first complexity
                frontend_c = int(frontend_c * 1.3) # Local DB sync
                
            # 4. Recurring (High UX)
            elif story == 'Recurring':
                ux_c = 400 # Logic heavy
                ui_c = 200
                
            # 5. Data Grid / Charts (High UI, High Frontend)
            elif story in ['Data Grid', 'Custom Charts', 'Dashboard', 'Competitor']:
                ux_c = 300
                ui_c = 800 # Complex visualization
                frontend_c = int(frontend_c * 1.3)
            
            # 6. JQL / Advanced Query (High UX)
            elif story == 'JQL Interface':
                ux_c = 500 # Query builder UX
                ui_c = 300
                
            # Apply updates
            new_row = row.copy()
            
            # Remove old keys
            if 'Designer_Construction' in new_row: del new_row['Designer_Construction']
            if 'Designer_Operation' in new_row: del new_row['Designer_Operation']
            
            # Set new keys
            new_row['UX_Construction'] = str(ux_c)
            new_row['UX_Operation'] = str(ux_o)
            new_row['UI_Construction'] = str(ui_c)
            new_row['UI_Operation'] = str(ui_o)
            new_row['Frontend RD_Construction'] = str(frontend_c)
            new_row['Backend RD_Construction'] = str(backend_c)
            
            # Reset PDM/PJM to 0 for now, let the recalc script handle them based on new totals
            # Or we can just leave them and let recalc script overwrite.
            # Recalc script overwrites, so we don't need to worry.
            
            rows.append(new_row)

    with open(OUTPUT_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Migrated {len(rows)} rows to {OUTPUT_PATH}")

if __name__ == "__main__":
    migrate()
