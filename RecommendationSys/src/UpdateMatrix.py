##Integrated System
##Updating Module
##6th, Dec, 2016
##Developed by Xulang

from src import UpdateAlgorithm as ual
import csv
import copy
import numpy as np
import pandas as pd
import os

os.system('mkdir -p ~/.recsys/Data/ConfigData')

def GetUserHistory2():
    userhistory = {}
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/Test-Reading.csv'), 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            userhistory.update({row[0]: row[1:] })
    f.close()
    return userhistory

def WriteInUserLang(en_user, cn_user):
    en_user_list = pd.DataFrame(list(en_user))
    cn_user_list = pd.DataFrame(list(cn_user))
    en_user_list.to_csv(os.path.expanduser('~/.recsys/Data/ConfigData/EnUser.csv'), index = False, header = False)
    cn_user_list.to_csv(os.path.expanduser('~/.recsys/Data/ConfigData/CnUser.csv'), index = False, header = False)
    return

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

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/Test-P-Matrix.csv'), mode='w', newline='') as wf:
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

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/Test-P-Prob.csv'), mode='w', newline='') as wf:
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
    DictionaryPath = os.path.expanduser('~/.recsys/Data/ConfigData/')
    DictionaryName = 'NewsDictionary.csv'
    NewsDict = {}
    with open(DictionaryPath + DictionaryName, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            NewsDict.update({int(row[0]): int(row[1])})
    f.close()
    return NewsDict

def BuildQ(Dict_1, history):
    NewsDict = getDictionary()
    for key in Dict_1.keys():
        if not key in history:
            history[key] = [0]*10
        Dict_1[key], history[key] = ual.QDataTransform(Dict_1[key], history[key], NewsDict)
    print('Q-Matrix Finished')
    return Dict_1, history

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

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/Test-Q-Matrix.csv'), mode='w', newline='') as wf:
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

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/Test-Q-Prob.csv'), mode='w', newline='') as wf:
        data = output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('P-Matrix write in finished')
    return

def OutputReading(history):
    output = []
    for key in history:
        output.append([key] + history[key])
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/Test-Reading.csv'), mode='w', newline='') as wf:
        data = output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    print('History write in finished')
    return

#####################
# Q-Matrix Finished #
#####################

def main():
    ##Get User Lang
    enUser = set()
    cnUser = set()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/EnUser.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            enUser.add(row[0])
    f.close()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/CnUser.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cnUser.add(row[0])
    f.close()

    ##Give path for existing matrix
    P_PATH = os.path.expanduser('~/.recsys/Data/ConfigData/Test-P-Matrix.csv')
    Q_PATH = os.path.expanduser('~/.recsys/Data/ConfigData/Test-Q-Matrix.csv')

    ##After (ResidualValue_Period) updates, current data will have (ResidualValue)% Value
    ResidualValue = 0.5
    ResidualValue_Period = 15
    Delta = ResidualValue ** (1 / ResidualValue_Period)

    ##Probability Headers = ['Property', 'Home', 'F&B', 'Movie', 'Promotion', 'Lottery', 'Others']
    ##Raw_Headers = ['Url', 'API', 'Method', 'Time', 'ID']
    ##Read in data
    Q_Dict_Old = {}
    with open(Q_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            Q_Dict_Old.update({row[0]: list(map(lambda x: float(x), row[1:]))})
    f.close()

    P_Dict_Old = {}
    with open(P_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            P_Dict_Old.update({row[0]: list(map(lambda x: float(x), row[1:]))})
    f.close()

    # C2908B87-BE8F-41F9-A464-B904FDB1F041

    userhistory = GetUserHistory2()

    Dict_New = {}
    with open(os.path.expanduser('~/.recsys/Data/Input/input.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[4] in enUser:
                enUser.remove(row[4])
            elif row[4] in cnUser:
                cnUser.remove(row[4])
            if (row[5][:2] == 'en'):
                enUser.add(row[4])
            elif (row[5][:2] == 'zh'):
                cnUser.add(row[4])
            if not (row[4] in Dict_New.keys()):
                Dict_New.update({row[4]: []})
            Dict_New[row[4]].append([row[1], row[3]])
            ##{'ID': [API, TIME], [API, TIME], [API, TIME]]
    f.close()
    # del Dict_New['']
    print('Data Import Finished')
    WriteInUserLang(enUser, cnUser)

    active_user = pd.DataFrame(list(Dict_New.keys()))
    active_user.to_csv(os.path.expanduser('~/.recsys/Data/ConfigData/ActiveUser.csv'), index=False, header=False)

    if '' in Dict_New.keys():
        del Dict_New['']
    P_Dict_New = copy.deepcopy(Dict_New)
    Q_Dict_New = copy.deepcopy(Dict_New)
    P_Dict_New = BuildP(P_Dict_New)
    Q_Dict_New, userhistory = BuildQ(Q_Dict_New, userhistory)
    P_Dict_Old = UpdateP(P_Dict_Old, P_Dict_New, Delta)
    Q_Dict_Old = UpdateQ(Q_Dict_Old, Q_Dict_New, Delta)
    OutputP_Count(P_Dict_Old)
    OutputQ_Count(Q_Dict_Old)

    print('Updating Finished')
    print('Building Probability Matrix')

    P_Dict_Prob = ProbabilityP(P_Dict_Old)
    Q_Dict_Prob = ProbabilityQ(Q_Dict_Old)
    OutputP_Prob(P_Dict_Prob)
    OutputQ_Prob(Q_Dict_Prob)
    OutputReading(userhistory)

    print('Probability Matrix Finished')

#####################
# Updating Finished #
#####################
main()
