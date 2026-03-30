import os
import csv

with open('names.csv','r',encoding='utf-8-sig', newline="") as file:
    reader = csv.reader(file)
    with open('final_names.csv','w',newline="") as outfile:
        writer = csv.writer(outfile)

        for row in reader :
            symbol = row[0]
            writer.writerow([f"{symbol}.NS"])
print('task completed')