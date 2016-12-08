import csv

dict_1 = {}
dict_2 = {}
n = 0
m = 0

##C1, C2 are the target columns you want to compare
C1 = 0
C2 = 0

with open('Raw_Data_1.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        dict_1.update({row[C1]: n})
        n = n + 1

with open('Raw_Data_2.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        dict_2.update({row[C2]: m})
        m = m + 1

overlap_list = {}
for key in dict_2.keys():
    if key in dict_1.keys():
        overlap_list.update({key: [dict_1[key], dict_2[key]]})

output = []
for key in overlap_list:
    output.append([key, overlap_list[key][0], overlap_list[key][1]])

with open('output.csv', 'w', newline='') as wf:
    data = output
    writer = csv.writer(wf, delimiter=',')
    writer.writerows(data)