import time
import re

#Compile Regular expressions
#Add more regular expressions
p1_promotion = re.compile('^/api/v[0-9.]+(/promotions|/promotions/[0-9]+)$')
c1_promotion = re.compile('(L_Pro)+')

p1_rental = re.compile('^/v[0-9.]+/properties(/rental|/rental/[0-9]+)$')
c1_rental = re.compile('(L_Ren)+')

p1_sale = re.compile('^/v[0-9.]+/properties(/sales|/sales/[0-9]+)$')
c1_sale = re.compile('(L_Sal)+')

p1_projects = re.compile('^/v[0-9.]+/renovations(/projects|/projects/[0-9]+)$')
c1_projects = re.compile('(L_Prj)+')

p1_companies = re.compile('^/v[0-9.]+/renovations(/companies|/companies/[0-9]+)$')
c1_companies = re.compile('(L_Com)+')

p1_restaurants = re.compile('^/api/v[0-9.]+(/restaurants|/restaurants/[0-9]+)$')
c1_restaurants = re.compile('(L_Res)+')

p1_movies = re.compile('^/v[0-9.]+(/movies|/movies/[0-9]+)$')
c1_movies = re.compile('(L_Mov)+')

p1_cinemas = re.compile('^/v[0-9.]+/cinemas')
c1_cinemas = re.compile('(L_Cin)+')

p1_lotteries = re.compile('^/v[0-9.]+/lotteries')
c1_lotteries = re.compile('(L_Lot)+')

p1_mrt = re.compile('^/v[0-9.]+/transportations/mrt_path')
c1_mrt = re.compile('(L_Mrt)+')

p1_bus = re.compile('^/v[0-9.]+/transportations/(buses|stops)')
c1_bus = re.compile('(L_Bus)+')

p1_transportations = re.compile('^/v[0-9.]+/transportations/(buses|stops)')

p1_directions = re.compile('^/v[0-9.]+/transportations/directions')
c1_directions = re.compile('(L_Dir)+')

p1_homeservices = re.compile('^/v[0-9.]+/homeservices/services')
c1_homeservices = re.compile('(L_Hom)+')
##Initial Status Matrix
Reg_M1 = [p1_promotion, p1_rental, p1_sale, p1_projects, p1_companies, p1_restaurants, p1_movies, p1_cinemas, p1_lotteries, p1_homeservices]

##Transformed Status Matrix
Reg_M4 = [c1_promotion, c1_rental, c1_sale, c1_projects, c1_companies, c1_restaurants, c1_movies, c1_cinemas, c1_lotteries, c1_homeservices]
StaList = ['L_Pro', 'L_Ren', 'L_Sal', 'L_Prj', 'L_Com', 'L_Res', 'L_Mov', 'L_Cin', 'L_Lot', 'L_Hom']
Title = ['Promotion', 'Rental', 'Sales', 'Projects', 'Companies', 'Restaurants', 'Movies', 'Cinemas', 'Lottery', 'Homeservices']

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
    for i in range(len(raw_time)):
        temp = (raw_time[i][1][:10] + ' ' + raw_time[i][1][11:19])
        raw_time[i][1] = time.mktime(time.strptime(temp,'%Y-%m-%d %H:%M:%S'))
    return raw_time

def StatusTransform(raw_status):
    output = []
    for i in range(len(raw_status)):
        for pos in range(len(Title)):
            if (Reg_M1[pos].match(raw_status[i][0])):
                sta = StaList[pos]
                output.append([sta, raw_status[i][1]])
                break
    return output
##input: ['api', num_time]
##output [status, num_time]

def SessionTransform(raw_session):
    threshold = 600 ##Session range is set as 600 secs here
    scale = len(raw_session)
    boundary = scale - 1
    output = []
    for i in range(scale):
        if (raw_session[i][0] != 'Delete'):
            SessionOperation = raw_session[i][0]
            time = raw_session[i][1]
            m = i + 1
            while m <= boundary:
                if raw_session[m][1] - time > threshold:
                    break
                else:
                    SessionOperation = SessionOperation + raw_session[m][0]
                    time = raw_session[m][1]
                    raw_session[m][0] = 'Delete'
                m = m + 1
            output.append(SessionOperation)
    return output
##input: raw_session = ['status','time']
##output: dict = {"ID1" : ['SESSION1','SESSION2','SESSION3',..],...}

def SessionCount(session_list):
    Matrix = [0] * len(StaList)
    for session in session_list:
        for pos in range(len(Reg_M4)):
            if Reg_M4[pos].search(session):
                Matrix[pos] = Matrix[pos] + 1
    Matrix = list(map(lambda x: float(x), Matrix))
    return Matrix
##input: dict = {"ID1" : ['session1','session2',...]}
##output: dict = {"ID" : [count1,count2,..]}

def PDataTransform(raw_input):
    output1 = TimeTransform(raw_input)
    output2 = merge_sort(output1)
    output3 = StatusTransform(output2)
    output4 = SessionTransform(output3)
    output5 = SessionCount(output4)
    return output5
##input: {'ID': [1, 2, 3, 4, 5, 6]]

news_pattern = re.compile('/api/v[0-9.]+/news/[0-9]+')

def OneStep(matrix, element):
    i = len(matrix) - 1
    while i > 0:
        matrix[i] = matrix[i-1]
        i -= 1
    matrix[i] = element
    return matrix

FixType = lambda x: '0' + x if len(x) == 1 else x

def DetectNews(raw_input, news_dict):
    output1 = []
    output2 = [0] * 10
    for news_id in raw_input:
        if news_pattern.match(news_id[0]):
            news = int(news_id[0][len('/api/v4.5/news/'):])
            if not news in news_dict:
                continue
            output1.append(news_dict[news] - 1)
            output2 = OneStep(output2, FixType(str(news_dict[int(news)])) + '#' + str(news))
    return output1, output2

def NewsCount(news_category, news_dict):
    output = [0] * max(set(news_dict.values()))
    for i in news_category:
        output[i] += 1
    output = list(map(lambda x: float(x), output))
    return output



def QDataTransform(raw_input, newsdict):
    output1 = TimeTransform(raw_input)
    output2 = merge_sort(output1)
    output3, output3_2 = DetectNews(output2, newsdict)
    output4 = NewsCount(output3, newsdict)
    return output4, output3_2

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
    return Q_Matrix


