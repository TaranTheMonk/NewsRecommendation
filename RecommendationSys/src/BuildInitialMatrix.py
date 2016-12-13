##Integrated System
##Building Matrix Module
##6th, Dec, 2016
##Developed by Xulang

import csv
import BuildInitialAlgorithm as bal
import copy

##Probability Headers = ['Property', 'Home', 'F&B', 'Movie', 'Promotion', 'Lottery', 'Others']
##Raw_Headers = ['Url', 'API', 'Method', 'Time', 'ID']
##Read in data
##Only Consider EN user here
Dict = {}
with open('InitialData/Test-Initial.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if (row[5][:2] == 'en'):
            if not(row[4] in Dict.keys()):
                Dict.update({row[4]: []})
            Dict[row[4]].append([row[1], row[3]])
        ##{'ID': [API, TIME], [API, TIME], [API, TIME]]
f.close()
if '' in Dict.keys():
    del Dict['']
print('Data Import Finished')

def BuildP(Dict):
    #take sample to try
    for key in Dict.keys():
        Dict[key] = bal.PDataTransform(Dict[key])
    print('Matrix Finished')

    output = []
    print('Probability finished')
    for key in Dict:
        output.append([key] + Dict[key])

    with open('ConfigData/Test-P-Matrix.csv', mode='w', newline='') as wf:
        data = output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('P-Matrix write in finished')
    return

#####################
# P-Matrix Finished #
#####################

def getNewsDictionary():
    ##Import News Dictionary
    DictionaryPath = 'ConfigData/'
    DictionaryName = 'NewsDictionary.csv'
    NewsDict = {}
    with open(DictionaryPath + DictionaryName, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            NewsDict.update({int(row[0]): int(row[1])})
    f.close()
    return NewsDict

def BuildQ(Dict):
    NewsDict = getNewsDictionary()
    Dict2 = {}
    for key in Dict.keys():
        Dict2.update({key: ''})
        Dict[key], Dict2[key] = bal.QDataTransform(Dict[key], NewsDict)
    print('Matrix Finished')

    output1 = []
    output2 = []
    print('Probability finished')
    for key in Dict:
        output1.append([key] + Dict[key])
        output2.append([key] + Dict2[key])

    with open('ConfigData/Test-Q-Matrix.csv', mode='w', newline='') as wf:
        data = output1
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    with open('ConfigData/Test-Reading.csv', mode='w', newline='') as wf:
        data = output2
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('Q-Matrix write in finished')
    return

#####################
# Q-Matrix Finished #
#####################

P_Dict = copy.deepcopy(Dict)
Q_Dict = copy.deepcopy(Dict)
BuildP(P_Dict)
BuildQ(Q_Dict)
print('Matrix Finished')

##User's reading history module

##Reading history finished
