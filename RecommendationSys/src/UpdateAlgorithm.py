import time
import re

#Compile Regular expressions
#Add more regular expressions
p1_promotion = re.compile('(/promotions$|/promotions/\d+)')
c1_promotion = re.compile('(L_Pro)+')

p1_rental = re.compile('(/rental$|/rental/\d+)')
c1_rental = re.compile('(L_Ren)+')

p1_sale = re.compile('(/sales$|/sales/\d+)')
c1_sale = re.compile('(L_Sal)+')

p1_projects = re.compile('/renovation(/projects$|/projects\d+)')
c1_projects = re.compile('(L_Prj)+')

p1_companies = re.compile('/renovation(/companies$|/companies\d+)')
c1_companies = re.compile('(L_Com)+')

p1_restaurants = re.compile('(/restaurants$|/restaurants/\d+)')
c1_restaurants = re.compile('(L_Res)+')

p1_movies = re.compile('(/movies$|/movies/\d+)')
c1_movies = re.compile('(L_Mov)+')

p1_cinemas = re.compile('(/cinemas$|/cinemas/\d+)')
c1_cinemas = re.compile('(L_Cin)+')

p1_lotteries = re.compile('/lotteries')
c1_lotteries = re.compile('(L_Lot)+')

p1_mrt = re.compile('^/v[0-9.]+/transportations/mrt_path')
c1_mrt = re.compile('(L_Mrt)+')

p1_bus = re.compile('^/v[0-9.]+/transportations/(buses|stops)')
c1_bus = re.compile('(L_Bus)+')

p1_directions = re.compile('^/v[0-9.]+/transportations/directions')
c1_directions = re.compile('(L_Dir)+')

p1_homeservices = re.compile('(/services$|/services/\d+)')
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
            if (Reg_M1[pos].search(raw_status[i][0])):
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

news_pattern = re.compile('^/api/v[0-9.]+/news/[0-9]+$')

def DetectNews(raw_input, news_dict):
    output = []
    for news_id in raw_input:
        if news_pattern.match(news_id[0]):
            output.append(news_dict[int(news_id[0][len('/api/v4.5/news/'):])] - 1)
    return output

def NewsCount(news_category, news_dict):
    output = [0] * max(set(news_dict.values()))
    for i in news_category:
        output[i] += 1
    output = list(map(lambda x: float(x), output))
    return output

def OneStep(matrix, element):
    i = len(matrix) - 1
    while i > 0:
        matrix[i] = matrix[i-1]
        i -= 1
    matrix[i] = element
    return matrix

FixType = lambda x: '0' + x if len(x) == 1 else x

def DetectNews(raw_input, news_dict, history):
    output1 = []
    output2 = history
    for news_id in raw_input:
        if news_pattern.match(news_id[0]):
            news = int(news_id[0].split('/')[-1])
            if not news in news_dict:
                continue
            output1.append(news_dict[int(news)] - 1)
            output2 = OneStep(output2, FixType(str(news_dict[int(news)])) + '#' + str(news))
    return output1, output2

def QDataTransform(raw_input, history, newsdict):
    output1 = TimeTransform(raw_input)
    output2 = merge_sort(output1)
    output3, output3_2 = DetectNews(output2, newsdict, history)
    output4 = NewsCount(output3, newsdict)
    return output4, output3_2

def DetectNewsIds(raw_input):
    output = set()
    for news_id in raw_input:
        if news_pattern.match(news_id[0]):
            news = int(news_id[0].split('/')[-1])
            output.add(news)
    return output


def PBuildProbability2(matrix):
    total = sum(matrix)
    matrix = [matrix[0], sum(matrix[1:5]), matrix[5], sum(matrix[6:7]), matrix[8], matrix[9]]
    num_category = len(matrix)
    C = 0.075
    if total == 0:
        total = num_category*C
    rest = 1 - C * num_category
    cr_s = 10
    cr_t = 20
    if sum(matrix) < cr_t and max(matrix) < cr_s:
        residual = rest * (1 - max([sum(matrix)/cr_t, max(matrix)/cr_s]))
    else:
        residual = 0
    rest = rest - residual
    output = [C + residual/num_category]* num_category
    if sum(matrix) != 0:
        for i in range(len(matrix)):
            output[i] = output[i] + rest * (matrix[i]/sum(matrix))
    else:
        for i in range(len(matrix)):
            output[i] = output[i] + rest / 6
##add basic pro X
##x/((6x + 1)*(10/7)) = basic pro
##when x = 0.1, basic pro = 0.04375
##This means, with other 0.2, at least 45% chance others will be chosen.
    total = sum(output)
    other = total*(3/7)
##no action cant mean no interest, so other will take 20% probability
    for i in range(len(output)):
        output[i] = output[i] / (total + other)
    # no need to append rest and news
    # output.append(0.2)
    # output.append(0.1)
    return output
##output = [p1, p1, ....]
##no action cant mean no interest, so other will take 10% probability
##news will take 20%

def PBuildProbability(matrix):
    total = sum(matrix)
    MergedMatrix = [matrix[0], sum(matrix[1:5]), matrix[5], sum(matrix[6:8]), matrix[8], matrix[9]]
    num_category = len(MergedMatrix)
    rest = 1
    cr_s = 10
    cr_t = 20
    if sum(MergedMatrix) < cr_t and max(MergedMatrix) < cr_s:
        residual = rest * (1 - max([sum(MergedMatrix)/cr_t, max(MergedMatrix)/cr_s]))
    else:
        residual = 0
    rest = rest - residual
    output = [residual/num_category]* num_category
    if sum(MergedMatrix) != 0:
        for i in range(len(MergedMatrix)):
            output[i] = output[i] + rest * (MergedMatrix[i]/sum(MergedMatrix))
    else:
        for i in range(len(MergedMatrix)):
            output[i] = output[i] + rest / num_category
    return output

def QBuildProbability(matrix):
    num_category = len(matrix)
    C = 0.02469
    rest = 1 - C*num_category
    cr_s = 10
    cr_t = 20
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