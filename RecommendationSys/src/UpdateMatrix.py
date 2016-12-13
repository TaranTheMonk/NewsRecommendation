##Integrated System
##Updating Module
##6th, Dec, 2016
##Developed by Xulang

import UpdateAlgorithm as ual
import csv
import copy
import numpy as np

##Give path for existing matrix
P_PATH = 'ConfigData/Test-P-Matrix.csv'
Q_PATH = 'ConfigData/Test-Q-Matrix.csv'

##After (ResidualValue_Period) updates, current data will have (ResidualValue)% Value
ResidualValue = 0.5
ResidualValue_Period = 15
Delta = ResidualValue ** (1 / ResidualValue_Period)

##Probability Headers = ['Property', 'Home', 'F&B', 'Movie', 'Promotion', 'Lottery', 'Others']
##Raw_Headers = ['Url', 'API', 'Method', 'Time', 'ID']
##Read in data
Q_Dict_Old = {}
with open(Q_PATH, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        Q_Dict_Old.update({row[0]: list(map(lambda x: float(x), row[1:]))})
f.close()

P_Dict_Old = {}
with open(P_PATH, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        P_Dict_Old.update({row[0]: list(map(lambda x: float(x), row[1:]))})
f.close()

Dict_New = {}
with open('Input/Test-Input.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if (row[5][:2] == 'en'):
            if not(row[4] in Dict_New.keys()):
                Dict_New.update({row[4]: []})
            Dict_New[row[4]].append([row[1], row[3]])
        ##{'ID': [API, TIME], [API, TIME], [API, TIME]]
f.close()
#del Dict_New['']
print('Data Import Finished')

def BuildP(Dict):
    #take sample to try
    for key in Dict.keys():
        Dict[key] = ual.PDataTransform(Dict[key])
    print('P-Matrix Finished')
    return Dict

def UpdateP(DictOld, DictNew, DeltaPara):
    for key in DictNew:
        if key in DictOld.keys():
            DictOld[key] = list(np.array(list(map(lambda x: x * DeltaPara, DictOld[key]))) + np.array(DictNew[key]))
        else:
            DictOld.update({key: DictNew[key]})
    print('Update P Finished')
    return DictOld

def OutputP_Count(Dict):
    output = []
    for key in Dict:
        output.append([key] + Dict[key])

    with open('ConfigData/Test-P-Matrix.csv', mode='w', newline='') as wf:
        data = output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('P-Matrix write in finished')
    return

def ProbabilityP(Dict):
    for key in Dict:
        Dict[key] = ual.PBuildProbability(Dict[key])
    return Dict

def OutputP_Prob(Dict):
    output = []
    for key in Dict:
        output.append([key] + Dict[key])

    with open('ConfigData/Test-P-Prob.csv', mode='w', newline='') as wf:
        data = output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('P-Matrix write in finished')
    return

#####################
# P-Matrix Finished #
#####################

def getDictionary():
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
    NewsDict = getDictionary()
    for key in Dict.keys():
        Dict[key] = ual.QDataTransform(Dict[key], NewsDict)
    print('Q-Matrix Finished')
    return Dict

def UpdateQ(DictOld, DictNew, DeltaPara):
    for key in DictNew:
        if key in DictOld.keys():
            DictOld[key] = list(np.array(list(map(lambda x: x * DeltaPara, DictOld[key]))) + np.array(DictNew[key]))
        else:
            DictOld.update({key: DictNew[key]})
    print('Update Q Finished')
    return DictOld

def OutputQ_Count(Dict):
    output = []
    for key in Dict:
        output.append([key] + Dict[key])

    with open('ConfigData/Test-Q-Matrix.csv', mode='w', newline='') as wf:
        data = output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('Q-Matrix write in finished')
    return

def ProbabilityQ(Dict):
    for key in Dict:
        Dict[key] = ual.QBuildProbability(Dict[key])
    return Dict

def OutputQ_Prob(Dict):
    output = []
    for key in Dict:
        output.append([key] + Dict[key])

    with open('ConfigData/Test-Q-Prob.csv', mode='w', newline='') as wf:
        data = output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('P-Matrix write in finished')
    return

#####################
# Q-Matrix Finished #
#####################

P_Dict_New = copy.deepcopy(Dict_New)
Q_Dict_New = copy.deepcopy(Dict_New)
P_Dict_New = BuildP(P_Dict_New)
Q_Dict_New = BuildQ(Q_Dict_New)
P_Dict_Old = UpdateP(P_Dict_Old, P_Dict_New, Delta)
Q_Dict_Old = UpdateQ(Q_Dict_Old, Q_Dict_New, Delta)
OutputP_Count(P_Dict_Old)
OutputQ_Count(Q_Dict_Old)

#####################
# Updating Finished #
#####################

print('Updating Finished')
print('Building Probability Matrix')

P_Dict_Prob = ProbabilityP(P_Dict_Old)
Q_Dict_Prob = ProbabilityQ(Q_Dict_Old)
OutputP_Prob(P_Dict_Prob)
OutputQ_Prob(Q_Dict_Prob)

print('Probability Matrix Finished')