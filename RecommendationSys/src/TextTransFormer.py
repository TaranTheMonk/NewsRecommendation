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

    FixType = lambda x: '0' + x if len(x) == 1 else x
    for doc in text:
        language_path = doc[4]

        title = FixType(doc[1]) + '#' + doc[0]
        ##title = type#id
        with open('TestDocs/' + language_path + '/' + title + '.txt', 'w', encoding = 'utf-8') as t:
            t.write(doc[2])
        t.close()
    return

