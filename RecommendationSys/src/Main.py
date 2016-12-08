##Integrated System
##Output Module
##6th, Dec, 2016
##Developed by Xulang

import MainAlgorithm as mal
import csv

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

Weight = 0.5
Prob_Matrix = mal.mergeProb(P_Matrix, Q_Matrix, Weight)