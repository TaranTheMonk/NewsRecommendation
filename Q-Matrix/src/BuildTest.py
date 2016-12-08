import csv
import random
test = []

prefix = '/api/v4.5/news/'

for i in range(10000):
    user_id = random.randint(0, 100)
    api_request = prefix + str(random.randint(39, 1132))
    test.append(['url', api_request, 'method', 'time', user_id])

with open('testlog.csv', 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f, delimiter = ',')
    writer.writerows(test)
f.close()
