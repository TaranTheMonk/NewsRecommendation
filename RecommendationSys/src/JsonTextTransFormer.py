import csv
import time
from datetime import datetime
import json
import os

current = datetime.now()
def AddZero(rawString):
    if len(rawString) == 1:
        output = '00' + rawString
    elif len(rawString) == 2:
        output = '0' + rawString
    else:
        output = rawString
    return output

def FixTime(rawtime):
    date_format = "%Y-%m-%d"
    date = datetime.strptime(rawtime, date_format)
    delta = current - date
    output = str(delta.days)
    return AddZero(output)

def WashRawText(Raw_Path):
    with open(Raw_Path, 'r', encoding = 'utf-8') as f:
        reader = f.read()
    f.close()

    text = json.loads(reader)

    for i in range(len(text)):
        if text[i]['language_id'] == 1:
            text[i]['language_id'] = 'en'
        elif text[i]['language_id'] == 2:
            text[i]['language_id'] = 'cn'
        elif text[i]['language_id'] == -1:
            text[i]['language_id'] = 'en&cn'

    all_news_dict = {}
    time_dict = {}
    en_docs_dict = {}
    cn_docs_dict = {}
    FixType = lambda x: '0' + x if len(x) == 1 else x
    for doc in text:
        language_path = doc['language_id']
        title = FixType(str(doc['type'])) + '#' + str(doc['id'])
        time_dict.update({title: [1, FixTime(doc['published_at'][:10])]})
        ##1 is doc['time_senstitivity']
        ##title = type#id

        all_news_dict.update({doc['id']: doc['type']})

        if language_path == 'en':
            en_docs_dict.update({doc['id']: doc['type']})
            with open(os.path.expanduser('~/.recsys/Data/TestDocs/' + language_path + '/' + title + '.txt'), 'w', encoding='utf-8') as t:
                t.write(doc['title'] + '.'+ doc['content'])
            t.close()

        elif language_path == 'cn':
            cn_docs_dict.update({doc['id']: doc['type']})
            with open(os.path.expanduser('~/.recsys/Data/TestDocs/' + language_path + '/' + title + '.txt'), 'w', encoding='utf-8') as t:
                t.write(doc['title'] + '.' + doc['content'])
            t.close()

        elif language_path == 'en&cn':
            en_docs_dict.update({doc['id']: doc['type']})
            cn_docs_dict.update({doc['id']: doc['type']})
            with open(os.path.expanduser('~/.recsys/Data/TestDocs/' + 'en' + '/' + title + '.txt'), 'w', encoding='utf-8') as t:
                t.write(doc['title'] + '.' + doc['content'])
            t.close()
            with open(os.path.expanduser('~/.recsys/Data/TestDocs/' + 'cn' + '/' + title + '.txt'), 'w', encoding='utf-8') as t:
                t.write(doc['title'] + '.' + doc['content'])
            t.close()

    all_news_output = []
    for key in all_news_dict:
        all_news_output.append([key, all_news_dict[key]])

    en_dict_output = []
    for key in en_docs_dict:
        en_dict_output.append([key, en_docs_dict[key]])

    cn_dict_output = []
    for key in cn_docs_dict:
        cn_dict_output.append([key, cn_docs_dict[key]])

    time_dict_output = []
    for key in time_dict:
        time_dict_output.append([key, time_dict[key][0], time_dict[key][1]])

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/NewsDictionary.csv'), mode='w', newline='') as wf:
        data = all_news_output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/en_docs_dict.csv'), mode='w', newline='') as wf:
        data = en_dict_output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/cn_docs_dict.csv'), mode='w', newline='') as wf:
        data = cn_dict_output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()

    with open(os.path.expanduser('~/.recsys/Data/ConfigData/time_dict.csv'), mode='w', newline='') as wf:
        data = time_dict_output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    return
