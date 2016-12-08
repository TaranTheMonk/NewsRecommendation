import csv
import algorithm as al
import copy

def getDictionary():
    ##Import News Dictionary
    DictionaryPath = 'Data/'
    DictionaryName = 'NewsDictionary.csv'
    NewsDict = {}
    with open(DictionaryPath + DictionaryName, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            NewsDict.update({int(row[0]): int(row[1])})
    f.close()
    return NewsDict
##output: {id-1: type-1, ...}

##Import Log Files
##[URL, API, Method, Timestamp, Device-ID]
def getLogfiles():
    LogPath = 'Data/'
    LogName = 'testlog.csv'
    userDict = {}
    with open(LogPath + LogName, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not (row[4] in userDict.keys()):
                userDict.update({row[4]: []})
            userDict[row[4]].append(row[1])
    f.close()
    return userDict
##ouput: {id-1: [request-1,request-2,request-3,...], ...}

def transform(userDict, NewsDict):
    count_Dict = {}
    for key in userDict.keys():
        userDict[key] = al.DetectNews(userDict[key], NewsDict)
        count_Dict.update({key: userDict[key]})
        userDict[key] = al.BuildProbability(userDict[key])
    return userDict, count_Dict

newsDict = getDictionary()
print('Get dictionary ready')

userDict = getLogfiles()
print('Get log files ready')

userDict, countDict = transform(userDict, newsDict)
print('Probability build ready')

data1 = []
data2 = []
for key in userDict:
    userDict[key].append(key)
    data1.append(userDict[key])

for key in countDict:
    countDict[key].append(key)
    data2.append(countDict[key])

with open('Q-Test-Prob.csv', 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(data1)
f.close()

with open('Q-Test-Count.csv', 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(data2)
f.close()