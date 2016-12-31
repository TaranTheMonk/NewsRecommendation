##Integrated System
##Output Module
##6th, Dec, 2016
##Developed by Xulang
##The enter of CN
from . import CosSimilarityAL as cal

##manualy import the above##

import time
import random
import json
import copy
import csv
from gensim import similarities, corpora, models
import numpy as np
import os
from datetime import datetime


def getUserByLanguage():
    enList = set()
    cnList = set()
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/EnUser.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            enList.add(row[0])
    f.close()
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/CnUser.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            cnList.add(row[0])
    f.close()
    return enList, cnList


def getActiveUserList(UserLanguageList):
    active_user = {}
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/ActiveUser.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if (not (row[0] in active_user.keys())) and (row[0] in UserLanguageList):
                active_user.update({row[0]: ''})
    f.close()
    return active_user


def merge_sort(ary, column):
    if len(ary) <= 1: return ary
    num = int(len(ary) / 2)
    left = merge_sort(ary[:num], column)
    right = merge_sort(ary[num:], column)
    return merge(left, right, column)


def merge(left, right, column):
    l, r = 0, 0
    result = []
    while l < len(left) and r < len(right):
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
        Q_Matrix[key] = list(map(lambda x: x / ToT, Q_Matrix[key]))
    return Q_Matrix


def ImportData(active_user):
    P_Prob_Path = 'Test-P-Prob.csv'
    Q_Prob_Path = 'Test-Q-Prob.csv'

    P_Matrix = {}
    Q_Matrix = {}

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/' + P_Prob_Path), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in active_user:
                P_Matrix.update({row[0]: list(map(lambda x: float(x), row[1:]))})
    f.close()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/' + Q_Prob_Path), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in active_user:
                Q_Matrix.update({row[0]: list(map(lambda x: float(x), row[1:]))})
    f.close()

    print('Data Import Finished')
    Weight = 1
    Prob_Matrix = mergeProb(P_Matrix, Q_Matrix, Weight)
    print('Probability Matrix Merged')
    return Prob_Matrix


def DefineLang(ProbMatrix, enList, cnList):
    Prob_en = {}
    Prob_cn = {}
    for key in ProbMatrix:
        if key in enList:
            Prob_en.update({key: ProbMatrix[key]})
        elif key in cnList:
            Prob_cn.update({key: ProbMatrix[key]})
    ##Add default prob
    return Prob_en, Prob_cn


#########################
## Build Category List ##
#########################

##(PDF, size, length)
##One result one time

def BuildCategory2(matrix, sum):
    output = 0
    pro = random.random() * sum
    for i in range(len(matrix)):
        pro -= matrix[i]
        if pro <= 0:
            output = i + 1
            break
    return output


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
    DictionaryPath = os.path.expanduser('~/.recsys/Data/ConfigData/')
    DictionaryName = 'NewsDictionary.csv'
    NewsDict = {}
    with open(DictionaryPath + DictionaryName, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            NewsDict.update({int(row[0]): int(row[1])})
    f.close()
    return NewsDict


##Load Configs
def ImportCosDictionary():
    index_path = os.path.expanduser("~/.recsys/Data/ConfigData/")
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


##add en&cn

#########################
## Build Document List ##
#########################

##import existing user history and update it by latest data
##still need to build two more module

def GetUserHistory1(docs_set, active_user):
    userhistory = {}
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/Test-Reading.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] in active_user:
                userhistory.update({row[0]: []})
                for item in row[1:]:
                    if (item != '0') and (item[3:] in docs_set):
                        userhistory[row[0]].append(item)
    f.close()
    return userhistory


def getText(docs_address, dictionary):
    # Import User Dataset
    # Specify dataset location
    corpus = cal.load_corpus(docs_address)
    docs = cal.corpus_docs(corpus)
    docs = cal.docs_stemmer(docs)

    ##stemmering and cleanning for reducing dimensions of vector space
    ##Use docs dictionary as the dictionary
    vecs = cal.docs_vecs(docs, dictionary)

    fileids = [x for x in corpus.fileids() if (x != '.DS_Store' and x != '.keep')]
    output = {}
    for i in range(len(vecs)):
        output.update({fileids[i]: vecs[i]})
    return output, fileids


def getPropertyDict():
    output = {}
    ban_list = set()
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/property_dict.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ##[title, time bound, distance day, status(only 1 is ok), reveal mode(1 or 0 is ok, 2 is banned)]
            if int(row[1]) == 1:
                output.update({row[0] + '.txt': TimeScoreFunctionRelevant(float(row[2]))})
            elif int(row[1]) == 0:
                output.update({row[0] + '.txt': TimeScoreFunctionIrrelevant(float(row[2]))})
            if (int(row[3]) != 1) or (int(row[4]) == 2):
                ban_list.add(row[0])
    f.close()
    return output, ban_list


def timeMatrix(property_dict, fileids):
    output = copy.deepcopy(fileids)
    for i in range(len(output)):
        output[i] = property_dict[output[i]]
    # maxmum = max(output)
    # output = list(map(lambda x: x/maxmum, output))
    return np.array(output)


def GiveRecommendationBySimilarity(userHistory, index, fileids, timematrix, docs, tfidf, ban_list, allhistory):
    C = 100
    ##C: output size
    outputdict = {}
    output = []
    for text in userHistory:
        if text + '.txt' in docs.keys():
            score = index[tfidf[docs[text + '.txt']]]
            maxmum = max(score)
            minmum = min(score)
            score = np.array(list(map(lambda x: ((x - minmum) + (maxmum - minmum) * 0.01 / (maxmum - minmum))
                                                * ((TimeScoreFunctionRelevant(0) + TimeScoreFunctionIrrelevant(0)) / 2),
                                      score)))
            score = score * timematrix
            maxmum = max(score)
            score = np.array(list(map(lambda x: x / maxmum, score)))
            ##top k, k = c - 1
            locallist = []
            #i = 0
            while len(locallist) <= C:
                if not int(fileids[score.argmax()].split('.')[0].split('#')[1]) in allhistory:
                    locallist.append((fileids[score.argmax()], score[score.argmax()]))
                score[score.argmax()] = -1
                #i += 1
            for textPair in locallist[1:]:
                if not (textPair[0] in outputdict.keys()):
                    outputdict.update({textPair[0]: 0})
                outputdict[textPair[0]] = max(outputdict[textPair[0]], textPair[1])
    for key in outputdict:
        if not (key.replace('.txt', '') in ban_list):
            output.append([key, outputdict[key]])
    ##delete docs by criterion
    return output


##time * similarity

def putDocsInBag(docslist):
    output = []
    for i in range(28):
        output.append([['empty', 0]])
    if docslist != []:
        for textPair in docslist:
            type = int(textPair[0].split('#')[0]) - 1
            if not (int(textPair[0].split('#')[0]) in range(1, 29)):
                textPair[1] = 0
            ##type out of 1-28, score = 0
            output[type].append(textPair)
    return output


def GetDocsList(userhistory, langFlag, index, fileids, timematrix, docs, tfidf, ban_list, allhistory):
    docslist = {}
    for key in userhistory.keys():
        if userhistory[key] == []:
            docslist.update({key: []})
            docslist[key] = putDocsInBag(docslist[key])
        else:
            if key in allhistory.keys():
                docslist.update({key: GiveRecommendationBySimilarity(
                    userhistory[key], index[langFlag], fileids[langFlag], timematrix[langFlag], docs[langFlag],
                    tfidf[langFlag], ban_list, allhistory[key])})
            else:
                docslist.update({key: GiveRecommendationBySimilarity(
                    userhistory[key], index[langFlag], fileids[langFlag], timematrix[langFlag], docs[langFlag],
                    tfidf[langFlag], ban_list, {key: set()})})
            docslist[key] = putDocsInBag(docslist[key])
        for i in range(len(docslist[key])):
            if docslist[key][i][1:] != []:
                docslist[key][i][1:] = merge_sort(docslist[key][i][1:], 1)
    return docslist


##{'ID': {'0' : [1,2,3,4],
##        '1' : [2,3,4,5],...}

def emptyRandom(category, doc_dict, memo_empty_dict):
    docs = doc_dict[category]
    # if len(docs) != 0:
    pro = random.random() * sum(x[1] for x in docs)
    for i in range(len(docs)):
        pro -= docs[i][1]
        if pro <= 0:
            output = docs[i][0]
            position = i
            break
    if len(doc_dict[category]) == 1:
        memo_empty_dict.append([doc_dict[category][0], category])
        del doc_dict[category]
    else:
        memo_empty_dict.append([doc_dict[category][position], category])
        del doc_dict[category][position]
        # pro = random.random() * sum(x[1] for x in matrix[1:])
        # for i in range(len(matrix)):
        #     pro -= matrix[i][1]
        #     if pro <= 0:
        #         output = [matrix[i][0], matrix[i][1]]
    return output


def emptyDocPair(category, doc_dict, memo_empty_dict):
    output = [FixType(str(category)) + '#' + str(emptyRandom(category, doc_dict, memo_empty_dict)) + '.txt', 0]
    return output


##A function that will output the final result for one time
##length: the length of a given array
##size: the number of given arrays
def FixType(type):
    output = type
    if len(type) == 1:
        output = '0' + type
    return output


def ChooseDoc2(doc_list, sum):
    output = 0
    num = random.random() * sum
    for i in range(len(doc_list)):
        num -= doc_list[i][1]
        if num <= 0:
            return i
    return -1


def ChooseDoc(category, matrix, doc_dict, memo_score_dict, memo_empty_dict):
    output = 0
    pro = random.random() * sum(x[1] for x in matrix[1:])
    for i in range(len(matrix)):
        pro -= matrix[i][1]
        if pro <= 0:
            output = [matrix[i][0], matrix[i][1]]
            memo_score_dict.append((category - 1, i, matrix[i][1]))
            matrix[i][1] = 0
            for m in range(len(doc_dict[category])):
                if doc_dict[category][m][0] == int(matrix[i][0].replace('.txt', '').split('#')[-1]):
                    memo_empty_dict.append([doc_dict[category][m], category])
                    if len(doc_dict[category]) == 1:
                        del doc_dict[category]
                    else:
                        del doc_dict[category][m]
                    break
            break
    return output


def DocsGive2(doc_dict, Prob_Matrix, docslist, length, size):
    output = {}
    sum_doc_dict = {}
    for category, docs_list in doc_dict.items():
        sum_doc_dict[category] = sum(x[1] for x in docs_list)
    for key in Prob_Matrix:
        output[key] = []
        category_prob_matrix = Prob_Matrix[key]
        # if no doc on this category, set prob = 0
        for i in range(len(category_prob_matrix)):
            if not (i + 1) in doc_dict or len(doc_dict[i + 1]) == 0:
                category_prob_matrix[i] = 0
        for n in range(size):
            temp = []
            memo_category_prob_matrix = []
            sum_category_prod_matrix = sum(category_prob_matrix)
            user_docslist = docslist[key]
            sum_user_docslist = []
            memo_user_doc_list = []
            memo_doc_dict = []
            for cate_docslist in user_docslist:
                sum_user_docslist.append(sum(x[1] for x in cate_docslist))
            for m in range(length):
                category = BuildCategory2(category_prob_matrix, sum_category_prod_matrix)
                if category == 0:
                    break

                if sum_user_docslist[category - 1] > 1e-9:
                    # similar doc is available
                    docs_list = user_docslist[category - 1]
                    index = ChooseDoc2(docs_list, sum_user_docslist[category - 1])
                    if index == -1:
                        continue
                    temp.append(docs_list[index][2])
                    # Destroy this doc
                    sum_user_docslist[category - 1] -= docs_list[index][1]
                    memo_user_doc_list.append([category, index, docs_list[index][1]])
                    docs_list[index][1] = 0
                else:
                    docs_list = doc_dict[category]
                    index = ChooseDoc2(docs_list, sum_doc_dict[category])
                    # Impossible to trigger
                    if index == -1:
                        break
                    temp.append(docs_list[index][0])
                    # Destroy this doc
                    memo_doc_dict.append([category, index, docs_list[index][1]])
                    sum_doc_dict[category] -= docs_list[index][1]
                    docs_list[index][1] = 0
                    if sum_doc_dict[category] < 1e-9:
                        # destroy this category
                        memo_category_prob_matrix.append([category, category_prob_matrix[category - 1]])
                        sum_category_prod_matrix -= category_prob_matrix[category - 1]
                        category_prob_matrix[category - 1] = 0
            for row in memo_category_prob_matrix:
                category_prob_matrix[row[0] - 1] = row[1]
            for row in memo_user_doc_list:
                user_docslist[row[0] - 1][row[1]][1] = row[2]
            for row in memo_doc_dict:
                doc_dict[row[0]][row[1]][1] = row[2]
                sum_doc_dict[row[0]] += row[2]
            output[key].append(temp)

    return output


def DocsGive(mega_doc_dict, Prob_Matrix, docslist, length, size):
    output = {}
    for key in Prob_Matrix:
        output.update({key: []})
        for n in range(size):
            temp = []
            # doc_dict = copy.deepcopy(mega_doc_dict)
            memo_empty_dict = []
            ##(cate,i,score)
            memo_score_dict = []
            doc_dict = mega_doc_dict
            # position = [1] * len(Prob_Matrix[key])
            for m in range(length):
                category = BuildCategory(Prob_Matrix[key])
                while (not category in doc_dict) and len(doc_dict) > 0:
                    category = BuildCategory(Prob_Matrix[key])
                if len(doc_dict) == 0:
                    break
                docc = docslist[key][category - 1]
                ##
                if sum(x[1] for x in docc) == 0:
                    temp.append(int(emptyDocPair(category, doc_dict, memo_empty_dict)[0][3:].replace('.txt', '')))
                    # temp.append(['empty'])
                else:
                    docPair = ChooseDoc(category, docc, doc_dict, memo_score_dict, memo_empty_dict)
                    # temp.append([docPair[0], docPair[1]])
                    temp.append(int(docPair[0][3:].replace('.txt', '')))
                    # position[category - 1] += 1
                    ##[id,cate]
            for item in memo_empty_dict:
                if not (item[1] in doc_dict.keys()):
                    doc_dict.update({item[1]: []})
                doc_dict[item[1]].append(item[0])
            for item in memo_score_dict:
                docslist[key][item[0]][item[1]][1] = item[2]
            output[key].append(temp)
    return output


def TimeScoreFunctionRelevant(x):
    InterSectionHours = 120
    # 5 * 24 = 120
    y = 1.01 ** - (x - InterSectionHours)
    return y


def TimeScoreFunctionIrrelevant(x):
    x_ = x // 10
    InterSectionHours = 120
    # 5 * 24 = 120
    y = 1.005 ** - (x_ - InterSectionHours)
    return y


# input = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
# output = []
# for item in input:
#     output.append([TimeScoreFunctionRelevant(item), TimeScoreFunctionIrrelevant(item)])

def TimeScore(timePair):
    score = 0
    ##timePair = [time sensitivity, time distance]
    if int(timePair[0]) == 0:
        # score = 'non relavent'
        score = TimeScoreFunctionIrrelevant(float(timePair[1]))
    elif int(timePair[0]) == 1:
        score = TimeScoreFunctionRelevant(float(timePair[1]))
        # score = 'relavent'
    return score

def getAllHistory():
    output = {}
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/UserReadingHistory.tsv'), 'r', encoding = 'utf-8') as f:
        reader = f.read()
    f.close()
    sample = reader.split('\n')
    for item in sample:
        if item != '':
            temp = item.split('\t')
            if len(temp) == 2:
                output.update({temp[0]: set(json.loads(temp[1]))})
    return output

def main():
    os.system('mkdir -p ~/.recsys/Data/Output')

    enList, cnList = getUserByLanguage()

    active_user = {'en': '', 'cn': ''}
    active_user['en'] = getActiveUserList(enList)
    active_user['cn'] = getActiveUserList(cnList)

    total_active_user_set = set(active_user['en'].keys()) | set(active_user['cn'].keys())
    Prob_Matrix = ImportData(total_active_user_set)

    def cleanActiveUser(act_usr):
        for device_id in act_usr:
            if not device_id in Prob_Matrix:
                act_usr.pop(device_id, None)

    cleanActiveUser(active_user['en'])
    cleanActiveUser(active_user['cn'])

    Prob_en, Prob_cn = DefineLang(Prob_Matrix, enList, cnList)

    index, tfidf, WordDictionary, NewsDictionary = ImportCosDictionary()

    en_dict = {}
    en_docs_set = set()
    cn_dict = {}
    cn_docs_set = set()

    property_dict, ban_list = getPropertyDict()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/en_docs_dict.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not (int(row[1]) in en_dict.keys()):
                en_dict.update({int(row[1]): []})
            if not (FixType(str(row[1])) + '#' + str(row[0]) in ban_list):
                en_dict[int(row[1])].append([int(row[0]), TimeScore([row[2], row[3]])])
            en_docs_set.add(row[0])
    f.close()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/cn_docs_dict.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not (int(row[1]) in cn_dict.keys()):
                cn_dict.update({int(row[1]): []})
            if not (FixType(str(row[1])) + '#' + str(row[0]) in ban_list):
                cn_dict[int(row[1])].append([int(row[0]), TimeScore([row[2], row[3]])])
            cn_docs_set.add(row[0])
    f.close()

    ##clean en/cn_dict: invalid key or empty docs set
    en_keys = list(en_dict.keys())
    for key in en_keys:
        if (not (key in range(1, 29))) or len(en_dict[key]) == 0:
            del en_dict[key]

    cn_keys = list(cn_dict.keys())
    for key in cn_keys:
        if (not (key in range(1, 29))) or len(cn_dict[key]) == 0:
            del cn_dict[key]

    ##Delete text in ban_list from en/cn_dict
    # '12d377e804a308f6'
    userhistory = {'en': '', 'cn': ''}
    userhistory['en'] = GetUserHistory1(en_docs_set, set(active_user['en'].keys()))
    userhistory['cn'] = GetUserHistory1(cn_docs_set, set(active_user['cn'].keys()))

    docs = {'en': '', 'cn': ''}
    fileids = {'en': '', 'cn': ''}

    address_docs_en = os.path.expanduser('~/.recsys/Data/TestDocs/en/')
    address_docs_cn = os.path.expanduser('~/.recsys/Data/TestDocs/cn/')
    docs['en'], fileids['en'] = getText(address_docs_en, WordDictionary['en'])
    docs['cn'], fileids['cn'] = getText(address_docs_cn, WordDictionary['cn'])

    timematrix = {'en': '', 'cn': ''}
    timematrix['en'] = timeMatrix(property_dict, fileids['en'])
    timematrix['cn'] = timeMatrix(property_dict, fileids['cn'])

    allhistory = getAllHistory()

    docslist = {'en': '', 'cn': ''}
    docslist['en'] = GetDocsList(userhistory['en'], 'en', index, fileids, timematrix, docs, tfidf, ban_list, allhistory)
    docslist['cn'] = GetDocsList(userhistory['cn'], 'cn', index, fileids, timematrix, docs, tfidf, ban_list, allhistory)
    print('Similarity list finished')

    print('All systems go')
    print(time.strftime('%Y-%m-%d %X', time.localtime()))

    ##ADD DEFAULT!!!!!
    Prob_cn.update({'chinese_default': list(map(lambda x: x / 28, [1] * 28))})
    Prob_en.update({'english_default': list(map(lambda x: x / 28, [1] * 28))})
    docslist['cn'].update({'chinese_default': [[['empty', 0]]] * 28})
    docslist['en'].update({'english_default': [[['empty', 0]]] * 28})

    # output = {'en': '', 'cn': ''}

    def convert_name_to_id(dict):
        for key, val in dict.items():
            for cat in val:
                for doc in cat:
                    if doc[0] != 'empty' and len(doc) == 2:
                        doc.append(int(doc[0].replace('.txt', '').split('#')[-1]))

    convert_name_to_id(docslist['en'])
    convert_name_to_id(docslist['cn'])

    output_en = DocsGive2(en_dict, Prob_en, docslist['en'], 35, 100)
    output_cn = DocsGive2(cn_dict, Prob_cn, docslist['cn'], 35, 100)

    # output_cn = DocsGive2(cn_dict, {'chinese_default': Prob_cn['chinese_default']}, docslist['cn'], 35, 100)
    # output_en = DocsGive2(en_dict, {'12d377e804a308f6': Prob_en['12d377e804a308f6']}, docslist['en'], 35, 100)
    print('output finished')
    print(time.strftime('%Y-%m-%d %X', time.localtime()))
    ##Test id en: 12d377e804a308f6
    ##Test id cn: 3A3D33EF-0C28-4430-A700-4ADFAA6327B7
    return output_en, output_cn


def SaveOutput():
    en_result, cn_result = main()
    # for key in cn_result:
    #     output.append([key, cn_result[key]])
    # for key in en_result:
    #     output.append([key, en_result[key]])

    with open(os.path.expanduser('~/.recsys/Data/Output/device_result.tsv'), mode='w') as wf:
        for res in en_result:
            wf.write(res + "\t" + json.dumps(en_result[res], separators=(',', ':')) + '\n')
        for res in cn_result:
            wf.write(res + "\t" + json.dumps(cn_result[res], separators=(',', ':')) + '\n')
    wf.close()


def main2():
    os.system('mkdir -p ~/.recsys/Data/Output')

    enList, cnList = getUserByLanguage()

    active_user = {'en': '', 'cn': ''}
    active_user['en'] = getActiveUserList(enList)
    active_user['cn'] = getActiveUserList(cnList)

    total_active_user_set = set(active_user['en'].keys()) | set(active_user['cn'].keys())
    Prob_Matrix = ImportData(total_active_user_set)

    def cleanActiveUser(act_usr):
        for device_id in list(act_usr):
            if not device_id in Prob_Matrix:
                act_usr.pop(device_id, None)

    cleanActiveUser(active_user['en'])
    cleanActiveUser(active_user['cn'])

    Prob_en, Prob_cn = DefineLang(Prob_Matrix, enList, cnList)

    index, tfidf, WordDictionary, NewsDictionary = ImportCosDictionary()

    en_dict = {}
    en_docs_set = set()
    cn_dict = {}
    cn_docs_set = set()

    property_dict, ban_list = getPropertyDict()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/en_docs_dict.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not (int(row[1]) in en_dict.keys()):
                en_dict.update({int(row[1]): []})
            if not (FixType(str(row[1])) + '#' + str(row[0]) in ban_list):
                en_dict[int(row[1])].append([int(row[0]), TimeScore([row[2], row[3]])])
            en_docs_set.add(row[0])
    f.close()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/cn_docs_dict.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not (int(row[1]) in cn_dict.keys()):
                cn_dict.update({int(row[1]): []})
            if not (FixType(str(row[1])) + '#' + str(row[0]) in ban_list):
                cn_dict[int(row[1])].append([int(row[0]), TimeScore([row[2], row[3]])])
            cn_docs_set.add(row[0])
    f.close()

    print('[%s]-Starting clear empty key in doc' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))
    ##clean en/cn_dict: invalid key or empty docs set
    en_keys = list(en_dict.keys())
    for key in en_keys:
        if (not (key in range(1, 29))) or len(en_dict[key]) == 0:
            del en_dict[key]

    cn_keys = list(cn_dict.keys())
    for key in cn_keys:
        if (not (key in range(1, 29))) or len(cn_dict[key]) == 0:
            del cn_dict[key]

    print('[%s]-Starting delete text in ban_list' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))
    ##Delete text in ban_list from en/cn_dict
    # '12d377e804a308f6'
    print('[%s]-Starting reading user reading history. ' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))
    userhistory = {'en': '', 'cn': ''}
    userhistory['en'] = GetUserHistory1(en_docs_set, set(active_user['en'].keys()))
    userhistory['cn'] = GetUserHistory1(cn_docs_set, set(active_user['cn'].keys()))
    print('[%s]- Finished reading user reading history. ' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))

    print('[%s]- Starting getting text. ' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))

    docs = {'en': '', 'cn': ''}
    fileids = {'en': '', 'cn': ''}

    address_docs_en = os.path.expanduser('~/.recsys/Data/TestDocs/en/')
    address_docs_cn = os.path.expanduser('~/.recsys/Data/TestDocs/cn/')
    docs['en'], fileids['en'] = getText(address_docs_en, WordDictionary['en'])
    docs['cn'], fileids['cn'] = getText(address_docs_cn, WordDictionary['cn'])
    print('[%s]- Finished getting text. ' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))
    print('[%s]- Starting timeMatrix. ' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))

    timematrix = {'en': '', 'cn': ''}
    timematrix['en'] = timeMatrix(property_dict, fileids['en'])
    timematrix['cn'] = timeMatrix(property_dict, fileids['cn'])
    print('[%s]- Finished timeMatrix. ' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))

    allhistory = getAllHistory()

    print('[%s]-Starting generating similarity list' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))
    docslist = {'en': '', 'cn': ''}
    docslist['en'] = GetDocsList(userhistory['en'], 'en', index, fileids, timematrix, docs, tfidf, ban_list, allhistory)
    docslist['cn'] = GetDocsList(userhistory['cn'], 'cn', index, fileids, timematrix, docs, tfidf, ban_list, allhistory)
    print('[%s]-Similarity list finished' % (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))

    print('All systems go')
    print(time.strftime('%Y-%m-%d %X', time.localtime()))

    ##ADD DEFAULT!!!!!
    Prob_cn.update({'chinese_default': list(map(lambda x: x / 28, [1] * 28))})
    Prob_en.update({'english_default': list(map(lambda x: x / 28, [1] * 28))})
    docslist['cn'].update({'chinese_default': [[['empty', 0]]] * 28})
    docslist['en'].update({'english_default': [[['empty', 0]]] * 28})

    # output = {'en': '', 'cn': ''}

    def convert_name_to_id(dict):
        for key, val in dict.items():
            for cat in val:
                for doc in cat:
                    if doc[0] != 'empty' and len(doc) == 2:
                        doc.append(int(doc[0].replace('.txt', '').split('#')[-1]))

    convert_name_to_id(docslist['en'])
    convert_name_to_id(docslist['cn'])

    SaveCSamplerOutput(en_dict, Prob_en, docslist['en'])
    yield 1
    SaveCSamplerOutput(cn_dict, Prob_cn, docslist['cn'])
    yield 2

    # output_cn = DocsGive2(cn_dict, Prob_cn, docslist['cn'], 35, 100)

    # output_cn = DocsGive2(cn_dict, {'chinese_default': Prob_cn['chinese_default']}, docslist['cn'], 35, 100)
    # output_en = DocsGive2(en_dict, {'12d377e804a308f6': Prob_en['12d377e804a308f6']}, docslist['en'], 35, 100)
    print('output finished')
    print(time.strftime('%Y-%m-%d %X', time.localtime()))


##Test id en: 12d377e804a308f6
##Test id cn: 3A3D33EF-0C28-4430-A700-4ADFAA6327B7
# return output_en, output_cn

def SaveCSamplerOutput(doc_dict, Prob, docslist):
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/all_docs_c.tsv'), 'w') as f:
        for cate in doc_dict:
            for doc in doc_dict[cate]:
                f.write('\t'.join([str(doc[0]), str(cate), str(doc[1])]))
                f.write('\n')
    f.close()
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/all_user_data_c.tsv'), 'w') as f:
        for deviceId in Prob:
            if deviceId in docslist:
                f.write(deviceId + ',')
                f.write(','.join(str(x) for x in Prob[deviceId]))
                doc_num = 0
                for cate in range(len(docslist[deviceId])):
                    for doc in docslist[deviceId][cate]:
                        if doc[0] != 'empty':
                            doc_num += 1
                f.write(',' + str(doc_num))
                for cate in range(len(docslist[deviceId])):
                    for doc in docslist[deviceId][cate]:
                        if doc[0] != 'empty':
                            f.write(',' + ','.join([str(doc[2]), str(cate+1), str(doc[1])]))
                f.write('\n')
    f.close()
