##Integrated System
##Output Module
##6th, Dec, 2016
##Developed by Xulang

import MainAlgorithm as mal
import csv
import copy
from gensim import similarities, corpora, models

#############################
## Merge P-Prob and Q-Prob ##
#############################

P_Prob_Path = 'Test-P-Prob.csv'
Q_Prob_Path = 'Test-Q-Prob.csv'

P_Matrix = {}
Q_Matrix = {}

with open('ConfigData/' + P_Prob_Path, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        P_Matrix.update({row[0]: list(map(lambda x: float(x), row[1:]))})
f.close()

with open('ConfigData/' + Q_Prob_Path, 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        Q_Matrix.update({row[0]: list(map(lambda x: float(x), row[1:]))})
f.close()

print('Data Import Finished')
Weight = 1
Prob_Matrix = mal.mergeProb(P_Matrix, Q_Matrix, Weight)
print('Probability Matrix Merged')

#########################
## Build Category List ##
#########################

List = mal.BuildList(Prob_Matrix)

#######################
## Load Config Files ##
#######################

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

##Load Configs
index_path = "ConfigData/"
index = similarities.SparseMatrixSimilarity.load(index_path + "allTFIDF.idx")
tfidf = models.TfidfModel.load(index_path + "allTFIDF.mdl")
WordDictionary = corpora.Dictionary.load(index_path + "all.dic")
NewsDictionary = getNewsDictionary()

#########################
## Build Document List ##
#########################

Vecs = {}
for key in NewsDictionary.keys():
    ##id: key, type: NewsDictionary[key]
    Vecs.update({NewsDictionary[key] + '#' + key: 0})