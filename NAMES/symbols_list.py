import os
import csv

names_dir = os.path.dirname(os.path.abspath(__file__))
count = 0

for filename in os.listdir(names_dir):
    if filename.startswith('MW-') and filename.endswith('.csv'):
        input_path = os.path.join(names_dir, filename)
        output_filename = filename.replace('MW-', '', 1)
        output_path = os.path.join(names_dir, output_filename)
        
        with open(input_path, 'r', encoding='utf-8-sig', newline="") as infile:
            reader = csv.reader(infile)
            with open(output_path, 'w', newline="") as outfile:
                writer = csv.writer(outfile)
                
                for row in reader:
                    if not row:
                        continue
                    symbol = row[0].strip()
                    # Skip the header row
                    if symbol == "SYMBOL":
                        continue
                    
                    writer.writerow([f"{symbol}.NS"])
        count += 1

print(f'Task completed: Processed {count} files.')