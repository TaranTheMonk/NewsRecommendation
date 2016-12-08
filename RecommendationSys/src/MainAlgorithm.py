import random

##Merge when computing the count of each module

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

def BuildCategoryList(matrix):
    list = []
    level = [0, matrix[0]]
    for i in range(2,28):
        level.append(sum(matrix[:i]))
    level.append(1)
    i = 0
    while i < 35:
        pro = random.random()
        for m in range(1, len(level)):
            if pro > level[m-1] and pro <= level[m]:
                list.append(m)
                break
        i = i + 1
    return list