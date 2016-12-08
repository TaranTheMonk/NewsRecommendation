##Build Probability Matrix based on previous behaviour
##Probability Headers = ['Property', 'Home', 'F&B', 'Movie', 'Promotion', 'Lottery', 'Others']
##Raw_Headers = ['Url', 'API', 'Method', 'Time', 'ID']

import csv
import Algorithm as al

##Read in data
##['action', 'time', 'id']
Dict = {}
data = {}
with open('Raw_Data.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not(row[4] in Dict.keys()):
            Dict.update({row[4]: []})
        Dict[row[4]].append([row[1],int(row[3][:10]),row[4]])
f.close()
Scale = len(Dict.keys())
print('data finished')

#take sample to try
i = 0
for key in Dict.keys():
    Dict[key] = al.merge_sort(Dict[key])
    Dict[key] = al.StatusTransform(Dict[key])
    Dict[key] = al.SessionTransform(Dict[key])
    i = i + 1
    print('%.4f' % (i / Scale))
print('sort finished')
print('status finished')
print('session finished')

totalSession = 0
for key in Dict:
    for session in Dict[key]:
        totalSession = totalSession + 1
    Dict[key] = al.SessionCount(Dict[key])
print('matrix finished')
print('Total number of session: %s' % totalSession)
print('Total unique users: %s ' % len(Dict.keys()))

output1 = []
for key in Dict:
    Dict[key] = al.BuildProbability(Dict[key])
    row = Dict[key]
    row = [key].append(row)
    output1.append(row)
print('Probability finished')
with open('Test-Probability.csv', mode='w', newline='') as wf:
    data = output1
    writer = csv.writer(wf, delimiter=',')
    writer.writerows(data)
wf.close()
print('output-1 write in finished')

output2 = []
for key in Dict:
    Dict[key] = al.BuildDocList(Dict[key])
    row = Dict[key]
    output2.append([key ,row])
print('Doc list finished')
with open('Test-List.csv', mode='w', newline='') as wf:
    data = output2
    writer = csv.writer(wf, delimiter=',')
    writer.writerows(data)
wf.close()
print('output-2 write in finished')
