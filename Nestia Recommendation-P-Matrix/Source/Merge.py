##Developed by Xulang Wan
import csv
import Algorithm as al
import re

device_id = re.compile('[a-zA-Z0-9]{16,16}|[a-zA-Z0-9-]{36,36}')

#merge & filter android data
name = []
rows = []
for i in range(4,14):
    if len(str(i)) == 1:
        i = '0' + str(i)
    print(i)
    with open('LogData/data-2016-11-%s.csv' % i, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            row[3] = al.TimeTransform(row[3])
            rows.append(row)
    f.close()

with open('Raw_Data.csv', mode='w', newline='', encoding = 'utf-8') as wf:
    data = rows
    writer = csv.writer(wf, delimiter=',')
    writer.writerows(data)
wf.close()