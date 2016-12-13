##Integrated System
##Output Module
##6th, Dec, 2016
##Developed by Xulang
import random
import os, sys
import re
os.chdir('/Users/Taran/Desktop/NestiaRecommendation/RecommendationSys/src')
sys.path.append('/Users/Taran/Desktop/NestiaRecommendation/RecommendationSys/src')

import copy
import csv
import CosSimilarityAL as cal
from gensim import similarities, corpora, models
import gensim
import numpy as np

def merge_sort(ary, column):
    if len(ary) <= 1 : return ary
    num = int(len(ary)/2)
    left = merge_sort(ary[:num], column)
    right = merge_sort(ary[num:], column)
    return merge(left , right, column)

def merge(left, right, column):
    l,r = 0,0
    result = []
    while l<len(left) and r<len(right) :
        if left[l][column] < right[r][column]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result

#############################
## Merge P-Prob and Q-Prob ##
#############################

def mergeProb(P_Matrix, Q_Matrix, Weight):
## P: [promotion, property, food, movie, lottery, home, news, other]
## Q: [6, 1, 3, 4, 7, 2, 8, rest] [5,0,2,3,6,1,7]
    P_id = {0, 1, 2, 3, 5, 6, 7}
    for key in P_Matrix.keys():
        Q_Matrix[key][5] += Weight * P_Matrix[key][0]
        Q_Matrix[key][0] += Weight * P_Matrix[key][1]
        Q_Matrix[key][2] += Weight * P_Matrix[key][2]
        Q_Matrix[key][3] += Weight * P_Matrix[key][3]
        Q_Matrix[key][6] += Weight * P_Matrix[key][4]
        Q_Matrix[key][1] += Weight * P_Matrix[key][5]
        Q_Matrix[key][7] += Weight * P_Matrix[key][6]
        for i in range(len(Q_Matrix[key])):
            if not (i in P_id):
                Q_Matrix[key][i] += Weight * (P_Matrix[key][7] / (len(Q_Matrix[key]) - len(P_Matrix[key])))
        ToT = sum(Q_Matrix[key])
        Q_Matrix[key] = list(map(lambda x: x/ToT, Q_Matrix[key]))
    return Q_Matrix

def ImportData():
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
    Prob_Matrix = mergeProb(P_Matrix, Q_Matrix, Weight)
    print('Probability Matrix Merged')
    return Prob_Matrix

Prob_Matrix = ImportData()

#########################
## Build Category List ##
#########################

##(PDF, size, length)
##One result one time

def BuildCategory(matrix):
    output = 0
    ##lenthg: number of elements in one matrix
    level = [0, matrix[0]]
    for i in range(2,len(matrix)):
        level.append(sum(matrix[:i]))
    level.append(1)
    pro = random.random()
    for m in range(1, len(level)):
        if pro > level[m-1] and pro <= level[m]:
            output = m
            break
    return output

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
def ImportCosDictionary():
    index_path = "ConfigData/"
    index = similarities.SparseMatrixSimilarity.load(index_path + "enTFIDF.idx")
    tfidf = models.TfidfModel.load(index_path + "enTFIDF.mdl")
    WordDictionary = corpora.Dictionary.load(index_path + "en.dic")
    NewsDictionary = getNewsDictionary()
    return index, tfidf, WordDictionary, NewsDictionary

index, tfidf, WordDictionary, NewsDictionary = ImportCosDictionary()

#########################
## Build Document List ##
#########################

##import existing user history and update it by latest data
##still need to build two more module

def GetUserHistory():
    userhistory = {}
    with open('ConfigData/Test-Reading.csv', 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            userhistory.update({row[0]: []})
            for item in row[1:]:
                if item != '0':
                    userhistory[row[0]].append(item)
    f.close()
    return userhistory

userhistory = GetUserHistory()

Vecs = {}
FixType = lambda x: '0' + x if len(x) == 1 else x
for key in NewsDictionary.keys():
    ##id: key, type: NewsDictionary[key]
    Vecs.update({FixType(str(NewsDictionary[key])) + '#' + str(key): 0})

def getText(docs_address, dictionary):
    #Import User Dataset
    #Specify dataset location
    corpus = cal.load_corpus(docs_address)
    docs = cal.corpus_docs(corpus)
    docs = cal.docs_stemmer(docs)

    ##stemmering and cleanning for reducing dimensions of vector space
    ##Use docs dictionary as the dictionary
    vecs = cal.docs_vecs(docs, dictionary)
    fileids = corpus.fileids()
    output = {}
    for i in range(len(vecs)):
        output.update({fileids[i]: vecs[i]})
    return output,fileids

address_docs = '../src/TestDocs/en/'
docs, fileids = getText(address_docs, WordDictionary)

def GiveRecommendationBySimilarity(userHistory, index, fileids):
    C = 100
    ##C: output size
    outputdict = {}
    output = []
    for text in userHistory:
        if text + '.txt' in docs.keys():
            score = index[tfidf[docs[text + '.txt']]]
        ##top k, k = c - 1
            list = []
            i = 0
            while i <= C:
                list.append((fileids[score.argmax()], score[score.argmax()]))
                score[score.argmax()] = -1
                i += 1
            for textPair in list[1:]:
                outputdict.update({textPair[0]: 0})
                outputdict[textPair[0]] = max(outputdict[textPair[0]], textPair[1])
    for key in outputdict:
        output.append([key, outputdict[key]])
    return output

def putDocsInBag(docslist):
    output = []
    for i in range(28):
        output.append(['empty'])
    if docslist != []:
        for textPair in docslist:
            type = int(textPair[0][:2]) - 1
            output[type].append(textPair)
    return output

def GetDocsList(userhistory):
    docslist = {}
    for key in userhistory.keys():
        if userhistory[key] == []:
            docslist.update({key: []})
            docslist[key] = putDocsInBag(docslist[key])
        else:
            docslist.update({key: GiveRecommendationBySimilarity(userhistory[key], index, fileids)})
            docslist[key] = putDocsInBag(docslist[key])
        for i in range(len(docslist[key])):
            if docslist[key][i][1:] != []:
                docslist[key][i][1:] = merge_sort(docslist[key][i][1:], 1)
    return docslist

docslist = GetDocsList(userhistory)

print('Similarity list finished')

##{'ID': {'0' : [1,2,3,4],
##        '1' : [2,3,4,5],...}

en_dict = {}

with open('ConfigData/en_docs_dict.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not(int(row[1]) in en_dict.keys()):
            en_dict.update({int(row[1]): []})
        en_dict[int(row[1])].append(int(row[0]))
f.close()

def emptyRandom(category, doc_dict):
    docs = doc_dict[category]
    random_number = random.randint(0,len(docs) - 1)
    output = docs[random_number]
    return output


def emptyDocPair(category):
    output = [str(category) + '#' + str(emptyRandom(category, en_dict))+ '#rand' + '.txt', 0]
    return output

##A function that will output the final result for one time
##length: the length of a given array
##size: the number of given arrays
def DocsGive(doc_dict, length, size):
    output = {}
    empty = []
    for key in Prob_Matrix:
        category = -1
        output.update({key: []})
        for n in range(size):
            for m in range(length):
                while not (category in doc_dict.keys()):
                    category = BuildCategory(Prob_Matrix[key])
                docPair = docslist[key][category - 1][len(docslist[key][category - 1]) - 1]
                if docPair == 'empty':
                    temp.append(emptyDocPair(category))
                else:
                    temp.append(docPair)
                    del (docslist[key][category - 1][len(docslist[key][category - 1]) - 1])
            output[key] = empty.append(output[key])
    return output

output = DocsGive(en_dict, 2,2)
print('output finished')

##Test id: 12d377e804a308f6