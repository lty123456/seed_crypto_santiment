import csv  
from datetime import datetime  
  
# input_file = 'BTCUSDT-2017-2020-1d.csv' 
# output_file = 'T_BTCUSDT-2017-2020-1d.csv' 
input_file = 'ETHUSDT-2017-2020-1d.csv' 
output_file = 'T_ETHUSDT-2017-2020-1d.csv' 
  
with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.reader(infile)  
    writer = csv.writer(outfile)  

    for row in reader:  
        if len(row) >= 6: 

            timestamp = int(float(row[0]))  
            date_time = datetime.utcfromtimestamp(timestamp)  
            formatted_date = date_time.strftime('%Y%m%dT')  
              
            new_row = [formatted_date] + row[1:6]  

            writer.writerow(new_row)