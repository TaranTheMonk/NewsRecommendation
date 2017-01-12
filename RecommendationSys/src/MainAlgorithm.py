import random
import copy

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
        # Q_Matrix[key][7] += Weight * P_Matrix[key][6]
        # for i in range(len(Q_Matrix[key])):
        #     if not (i in P_id):
        #         Q_Matrix[key][i] += Weight * (P_Matrix[key][7] / (len(Q_Matrix[key]) - len(P_Matrix[key])))
        ToT = sum(Q_Matrix[key])
        Q_Matrix[key] = list(map(lambda x: x/ToT, Q_Matrix[key]))
    return Q_Matrix

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

def BuildList(Prob_Matrix, size, length):
    ##length: number of elements in one matrix
    ##size: number of matrix for one id
    List = copy.deepcopy(Prob_Matrix)
    for key in List:
        Temp = copy.deepcopy(List[key])
        List[key] = []
        for i in range(size):
            List[key].append(BuildCategory(Temp, length))
    return List

def merge_sort(ary, column):
    if len(ary) <= 1 : return ary
    num = int(len(ary)/2)
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left , right, column)

def merge(left, right, column):
    l,r = 0,0
    result = []
    while l<len(left) and r<len(right) :
        if left[l][column] > right[r][column]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result