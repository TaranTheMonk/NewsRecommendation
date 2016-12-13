import csv

def WashRawText(Raw_Path):
    text = []
    with open(Raw_Path, 'r', encoding = 'utf-8') as f:
        reader = csv.reader(f, delimiter = "\t")
        #headers = reader.next()
        for row in reader:
        ##[id, title. text]
            text.append([row[0], row[9], row[1].replace("/" ,"_") + '. ' + row[6], row[13]])
    f.close()

    for i in range(len(text)):
        if text[i][3] == '1':
            text[i].append('en')
        else:
            text[i].append('cn')

    en_docs_dict = {}
    cn_docs_dict = {}
    FixType = lambda x: '0' + x if len(x) == 1 else x
    for doc in text:
        language_path = doc[4]
        title = FixType(doc[1]) + '#' + doc[0]
        ##title = type#id
        if language_path == 'en':
            en_docs_dict.update({doc[0]: doc[1]})
        else:
            cn_docs_dict.update({doc[0]: doc[1]})
        with open('TestDocs/' + language_path + '/' + title + '.txt', 'w', encoding = 'utf-8') as t:
            t.write(doc[2])
        t.close()

    en_dict_output = []
    for key in en_docs_dict:
        en_dict_output.append([key, en_docs_dict[key]])

    cn_dict_output = []
    for key in cn_docs_dict:
        cn_dict_output.append([key, cn_docs_dict[key]])

    with open('ConfigData/en_docs_dict.csv', mode='w', newline='') as wf:
        data = en_dict_output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()

    with open('ConfigData/cn_docs_dict.csv', mode='w', newline='') as wf:
        data = cn_dict_output
        writer = csv.writer(wf, delimiter=',')
        writer.writerows(data)
    wf.close()
    return


