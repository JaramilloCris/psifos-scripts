import csv

new_stats = []
with open('estadisticas.csv', newline='') as csvfile:
    stats = csv.reader(csvfile)
    last_date = ''
    last_unit = ''
    
    for row in stats:
        if len(row) >= 2:  # Ensure we have at least 2 columns
            if not row[0]:  # Handle empty date
                row[0] = last_date
            else:
                last_date = row[0]
            
            if not row[1]:  # Handle empty unit
                row[1] = last_unit
            else:
                last_unit = row[1]
                
            new_stats.append(row)

with open('new_stats.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_stats)
