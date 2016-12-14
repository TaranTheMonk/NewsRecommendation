##Integrated System
##Output Module
##6th, Dec, 2016
##Developed by Xulang
##The enter of CN
import time
import random
import os, sys
import re
import numpy as np
os.chdir('/Users/Taran/Desktop/NestiaRecommendation/RecommendationSys/src')
sys.path.append('/Users/Taran/Desktop/NestiaRecommendation/RecommendationSys/src')

import copy
import csv
from gensim import similarities, corpora, models
import CosSimilarityAL as cal
import gensim
import numpy as np

active_user = {}
with open('ConfigData/ActiveUser.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not(row[0] in active_user.keys()):
            active_user.update({row[0]: ''})
f.close()

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
            if row[0] in active_user.keys():
                P_Matrix.update({row[0]: list(map(lambda x: float(x), row[1:]))})
    f.close()

    with open('ConfigData/' + Q_Prob_Path, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in active_user.keys():
                Q_Matrix.update({row[0]: list(map(lambda x: float(x), row[1:]))})
    f.close()

    print('Data Import Finished')
    Weight = 1
    Prob_Matrix = mergeProb(P_Matrix, Q_Matrix, Weight)
    print('Probability Matrix Merged')
    return Prob_Matrix

Prob_Matrix = ImportData()

def DefineLang(ProbMatrix):
    enList = set()
    cnList = set()
    with open('ConfigData/EnUser.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            enList.add(row[0])
    f.close()
    with open('ConfigData/CnUser.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cnList.add(row[0])
    f.close()

    Prob_en = {}
    Prob_cn = {}
    for key in Prob_Matrix:
        if key in enList:
            Prob_en.update({key: Prob_Matrix[key]})
        elif key in cnList:
            Prob_cn.update({key: Prob_Matrix[key]})
    return Prob_en, Prob_cn

Prob_en, Prob_cn = DefineLang(Prob_Matrix)

#########################
## Build Category List ##
#########################

##(PDF, size, length)
##One result one time

def BuildCategory(matrix):
    output = 0
    pro = random.random()
    for i in range(len(matrix)):
        pro -= matrix[i]
        if pro <= 0:
            output = i + 1
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
    index = {'en': '', 'cn': ''}
    index['en'] = similarities.SparseMatrixSimilarity.load(index_path + "enTFIDF.idx")
    index['cn'] = similarities.SparseMatrixSimilarity.load(index_path + "cnTFIDF.idx")

    tfidf = {'en': '', 'cn': ''}
    tfidf['en'] = models.TfidfModel.load(index_path + "enTFIDF.mdl")
    tfidf['cn'] = models.TfidfModel.load(index_path + "cnTFIDF.mdl")

    WordDictionary = {'en': '', 'cn': ''}
    WordDictionary['en'] = corpora.Dictionary.load(index_path + "en.dic")
    WordDictionary['cn'] = corpora.Dictionary.load(index_path + "cn.dic")

    NewsDictionary = getNewsDictionary()
    return index, tfidf, WordDictionary, NewsDictionary

index, tfidf, WordDictionary, NewsDictionary = ImportCosDictionary()

##add en&cn

#########################
## Build Document List ##
#########################

##import existing user history and update it by latest data
##still need to build two more module

en_dict = {}
en_docs_set = set()
cn_dict = {}
cn_docs_set = set()

with open('ConfigData/en_docs_dict.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not(int(row[1]) in en_dict.keys()):
            en_dict.update({int(row[1]): []})
        en_dict[int(row[1])].append(int(row[0]))
        en_docs_set.add(row[0])
f.close()

with open('ConfigData/cn_docs_dict.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if not(int(row[1]) in cn_dict.keys()):
            cn_dict.update({int(row[1]): []})
        cn_dict[int(row[1])].append(int(row[0]))
        cn_docs_set.add(row[0])
f.close()

def GetUserHistory1(docs_set):
    userhistory = {}
    with open('ConfigData/Test-Reading.csv', 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in active_user.keys():
                userhistory.update({row[0]: []})
                for item in row[1:]:
                    if (item != '0') and (item in docs_set):
                        userhistory[row[0]].append(item)
    f.close()
    return userhistory

userhistory = {'en': '' ,'cn': ''}
userhistory['en'] = GetUserHistory1(en_docs_set)
userhistory['cn'] = GetUserHistory1(cn_docs_set)
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

docs = {'en': '', 'cn': ''}
fileids = {'en': '', 'cn': ''}

address_docs_en = '../src/TestDocs/en/'
address_docs_cn = '../src/TestDocs/cn/'
docs['en'], fileids['en'] = getText(address_docs_en, WordDictionary['en'])
docs['cn'], fileids['cn'] = getText(address_docs_cn, WordDictionary['cn'])

def getTimeDict():
    output = {}
    base = 2
    with open('ConfigData/time_dict.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == 1:
                output.update({row[0] + '.txt': base ** (1/float(row[2]))})
            else:
                output.update({row[0] + '.txt': base ** (1/(float(row[2])/10))})
    f.close()
    return output

time_dict = getTimeDict()

def timeMatrix(time_dict, fileids):
    output = copy.deepcopy(fileids)
    for i in range(len(output)):
        output[i] = time_dict[output[i]]
    maxmum = max(output)
    output = list(map(lambda x: x/maxmum, output))
    return np.array(output)

timematrix = {'en': '', 'cn': ''}
timematrix['en'] = timeMatrix(time_dict, fileids['en'])
timematrix['cn'] = timeMatrix(time_dict, fileids['cn'])


def GiveRecommendationBySimilarity(userHistory, index, fileids, timematrix):
    C = 100
    ##C: output size
    outputdict = {}
    output = []
    for text in userHistory:
        if text + '.txt' in docs.keys():
            score = index[tfidf[docs[text + '.txt']]]
            maxmum = max(score)
            score = np.array(list(map(lambda x: x/ maxmum, score)))
            score = score * timematrix
        ##top k, k = c - 1
            locallist = []
            i = 0
            while i <= C:
                locallist.append((fileids[score.argmax()], score[score.argmax()]))
                score[score.argmax()] = -1
                i += 1
            for textPair in locallist[1:]:
                if not (textPair[0] in outputdict.keys()):
                    outputdict.update({textPair[0]: 0})
                outputdict[textPair[0]] = max(outputdict[textPair[0]], textPair[1])
    for key in outputdict:
        output.append([key, outputdict[key]])
    return output

##time * similarity

def putDocsInBag(docslist):
    output = []
    for i in range(28):
        output.append([['empty', 0]])
    if docslist != []:
        for textPair in docslist:
            type = int(textPair[0][:2]) - 1
            output[type].append(textPair)
    return output

def GetDocsList(userhistory, timematrix):
    docslist = {}
    for key in userhistory.keys():
        if userhistory[key] == []:
            docslist.update({key: []})
            docslist[key] = putDocsInBag(docslist[key])
        else:
            docslist.update({key: GiveRecommendationBySimilarity(userhistory[key], index, fileids, timematrix)})
            docslist[key] = putDocsInBag(docslist[key])
        for i in range(len(docslist[key])):
            if docslist[key][i][1:] != []:
                docslist[key][i][1:] = merge_sort(docslist[key][i][1:], 1)
    return docslist

docslist = {'en': '', 'cn': ''}
docslist['en'] = GetDocsList(userhistory['en'], 'en')
docslist['cn'] = GetDocsList(userhistory['cn'], 'cn')
print('Similarity list finished')

##{'ID': {'0' : [1,2,3,4],
##        '1' : [2,3,4,5],...}

def emptyRandom(category, doc_dict, memo_dict):
    docs = doc_dict[category]
    #if len(docs) != 0:
    random_number = random.randint(0, len(docs) - 1)
    output = docs[random_number]
    if len(doc_dict[category]) == 1:
        memo_dict.append([doc_dict[category][0], category])
        del doc_dict[category]
    else:
        memo_dict.append([doc_dict[category][random_number], category])
        del doc_dict[category][random_number]
    # else:
    #     del doc_dict[category]
    #     ##random change a category if the previous chosen category is empty
    #     category_new = list(doc_dict.keys())[random.randint(0, len(list(doc_dict.keys())) - 1)]
    #     output = emptyRandom(category_new, doc_dict)
    return output


def emptyDocPair(category, doc_dict, memo_dict):
    output = [str(category) + '#' + str(emptyRandom(category, doc_dict, memo_dict))+ '#rand' + '.txt', 0]
    return output


##A function that will output the final result for one time
##length: the length of a given array
##size: the number of given arrays

def ChooseDoc(category, matrix, memo_dict):
    output = 0
    pro = random.random() * sum(x[1] for x in matrix[1:])
    for i in range(len(matrix)):
        pro -= matrix[i][1]
        if pro <= 0:
            output = [matrix[i][0], matrix[i][1]]
            memo_dict.append((category - 1, i, matrix[i][1]))
            matrix[i][1] = 0
            break
    return output

def DocsGive(mega_doc_dict, Prob_Matrix, docslist, length, size):
    output = {}
    for key in Prob_Matrix:
        output.update({key: []})
        for n in range(size):
            temp = []
            #doc_dict = copy.deepcopy(mega_doc_dict)
            memo_empty_dict = []
            ##(cate,i,score)
            memo_score_dict = []
            doc_dict = mega_doc_dict
            #position = [1] * len(Prob_Matrix[key])
            for m in range(length):
                category = BuildCategory(Prob_Matrix[key])
                while not (category in doc_dict.keys()):
                    category = BuildCategory(Prob_Matrix[key])
                docc = docslist[key][category - 1]
                ##
                if sum(x[1] for x in docc) == 0:
                    temp.append(emptyDocPair(category, doc_dict, memo_empty_dict))
                    #temp.append(['empty'])
                else:
                    docPair = ChooseDoc(category, docc, memo_score_dict)
                    temp.append([docPair[0], docPair[1]])
                    #position[category - 1] += 1
                    ##[id,cate]
            for item in memo_empty_dict:
                if not(item[1] in doc_dict.keys()):
                    doc_dict.update({item[1]: []})
                doc_dict[item[1]].append(item[0])
            for item in memo_score_dict:
                docslist[key][item[0]][item[1]][1] = item[2]
            output[key].append([temp])
    return output

print(time.strftime( '%Y-%m-%d %X', time.localtime() ))

#output = {'en': '', 'cn': ''}
#output['en'] = DocsGive(en_dict, Prob_Matrix, docslist['en'], 35, 100)
#output['cn'] = DocsGive(cn_dict, Prob_Matrix, docslist['cn'], 35, 100)


output = DocsGive(en_dict, {'12d377e804a308f6': Prob_Matrix['12d377e804a308f6']}, docslist, 35, 100)
print('output finished')
print(time.strftime('%Y-%m-%d %X', time.localtime()))
##Test id: 12d377e804a308f6