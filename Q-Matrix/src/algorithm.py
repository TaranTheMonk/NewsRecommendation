import time
import re
import random

news_pattern = re.compile('/api/v[0-9.]+/news/[0-9]+')

##Build re for news reading

def BuildDict(list):
    Dict = {}
    for i in range(len(list)):
        if not(list[i] in Dict):
            Dict.update({list[i] : []})
    return Dict
##Output = {"ID1":[] , "ID2":[] , ...}

def merge_sort(ary):
    if len(ary) <= 1 : return ary
    num = int(len(ary)/2)
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left,right)

def merge(left,right):
    l,r = 0,0
    result = []
    while l<len(left) and r<len(right) :
        if left[l][1] < right[r][1]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result

def TimeTransform(raw_time):
    temp = (raw_time[:10] + ' ' + raw_time[11:19])
    num_time = time.mktime(time.strptime(temp,'%Y-%m-%d %H:%M:%S'))
    return num_time

def StatusTransform(raw_status):
    output = []
    for i in range(len(raw_status)):
        for pos in range(len(Title)):
            ##Check '.' to see if it's the end    and raw_status[i][2][(Reg_M1[pos].match(raw_status[i][2]).end())] == '.'
            if (Reg_M1[pos].match(raw_status[i][0])):
                sta = StaList[pos]
                output.append([sta, raw_status[i][1], raw_status[i][2]])
                break
            ##Check '.' to see if it's the end
    return output

#Build new session transform
#raw_session = ['status','time','id']
def SessionTransform(raw_session):
    threshold = 600 ##Session range is set as 600 secs here
    scale = len(raw_session)
    boundary = scale - 1
    output = []
    for i in range(scale):
        if (raw_session[i][2] != 'Delete'):
            SessionOperation = raw_session[i][0]
            time = raw_session[i][1]
            m = i + 1
            while m <= boundary:
                if raw_session[m][1] - time > threshold:
                    break
                else:
                    SessionOperation = SessionOperation + raw_session[m][0]
                    time = raw_session[m][1]
                    raw_session[m][2] = 'Delete'
                m = m + 1
            output.append(SessionOperation)
    return output
##output: dict = {"ID1" : ['SESSION1','SESSION2','SESSION3',..],...}

##input: dict = {"ID1" : ['session1','session2',...]}
def SessionCount(session_list):
    Matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for session in session_list:
        for pos in range(len(Reg_M4)):
            if Reg_M4[pos].search(session):
                Matrix[pos] = Matrix[pos] + 1
    return Matrix
##output: dict = {"ID" : [count1,count2,..]}

def BuildProbability(matrix):
    num_category = len(matrix)
    C = 0.02
    rest = 1 - C*num_category
    cr_s = 5
    cr_t = 10
##for single and total count threshold
    if sum(matrix) < cr_t and max(matrix) < cr_s:
        residual = rest * (1 - max([sum(matrix)/cr_t, max(matrix)/cr_s]))
    else:
        residual = 0
    rest = rest - residual
##C is the basic probability
##residual/num_category is setting when the number of views is less than a threshold
    output = [C + residual/num_category]* num_category
    if sum(matrix) != 0:
        for i in range(len(matrix)):
            output[i] = output[i] + rest * (matrix[i]/sum(matrix))
    else:
        for i in range(len(matrix)):
            output[i] = output[i] + rest / num_category
    for i in range(len(output)):
        output[i] = output[i]/sum(output)
    return output

## category = [promotion, property, food, movie, lottery, home, new, others]
# def BuildDocList(matrix):
#     list = ''
#     category = ['none', '1', '2', '3', '4', '5', '6', '7', '8']
#     level = [0, matrix[0], sum(matrix[:2]), sum(matrix[:3]), sum(matrix[:4]), sum(matrix[:5]), sum(matrix[:6]), sum(matrix[:7]), 1]
#     i = 0
#     while i <= 100:
#         pro = random.random()
#         for m in range(1, 9):
#             if pro > level[m-1] and pro <= level[m]:
#                 list = list + category[m]
#                 break
#         i = i + 1
#     return list
# ##list = [c1, c2, c3, ....]

def DetectNews(apilist, newsdict):
    num_category = 30
    output = [0] * num_category
    for request in apilist:
        if news_pattern.match(request):
            news_id = request[15:]
            news_id = int(news_id)
            if news_id in newsdict.keys():
                output[(newsdict[news_id]-1)] += 1
    return output
