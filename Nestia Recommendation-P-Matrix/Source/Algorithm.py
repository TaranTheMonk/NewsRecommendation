import time
import re
import random

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

p1_directions = re.compile('^/v[0-9.]+/transportations/directions')
c1_directions = re.compile('(L_Dir)+')

p1_homeservices = re.compile('^/v[0-9.]+/homeservices/services')
c1_homeservices = re.compile('(L_Hom)+')
##Initial Status Matrix
Reg_M1 = [p1_promotion, p1_rental, p1_sale, p1_projects, p1_companies, p1_restaurants, p1_movies, p1_cinemas, p1_lotteries, p1_homeservices]

##Transformed Status Matrix
Reg_M4 = [c1_promotion, c1_rental, c1_sale, c1_projects, c1_companies, c1_restaurants, c1_movies, c1_cinemas, c1_lotteries, c1_homeservices]
StaList = ['L_Pro', 'L_Ren', 'L_Sal', 'L_Prj', 'L_Com', 'L_Res', 'L_Mov', 'L_Lot', 'L_Hom']
StaDetail = ['D_Pro', 'D_Ren', 'D_Sal', 'D_Prj', 'D_Com', 'D_Res', 'D_Mov', 'D_Cin']
Title = ['Promotion', 'Rental', 'Sales', 'Projects', 'Companies', 'Restaurants', 'Movies', 'Lottery', 'Homeservices']

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
    total = sum(matrix)
    matrix = [matrix[0], sum(matrix[1:5]), matrix[5], matrix[6], matrix[7], matrix[8]]
    num_category = len(matrix)
    C = 0.075
    if total == 0:
        total = num_category*C
    rest = 1 - C * num_category
    cr_s = 5
    cr_t = 10
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
        output[i] = output[i]/(total + other)
    output.append(0.2)
    output.append(0.1)
    return output
##output = [p1, p1, ....]
##no action cant mean no interest, so other will take 10% probability
##news will take 20%


## category = [promotion, property, food, movie, lottery, home, new, others]
def BuildDocList(matrix):
    list = ''
    category = ['none', '1', '2', '3', '4', '5', '6', '7', '8']
    level = [0, matrix[0], sum(matrix[:2]), sum(matrix[:3]), sum(matrix[:4]), sum(matrix[:5]), sum(matrix[:6]), sum(matrix[:7]), 1]
    i = 0
    while i <= 100:
        pro = random.random()
        for m in range(1, 9):
            if pro > level[m-1] and pro <= level[m]:
                list = list + category[m]
                break
        i = i + 1
    return list
##list = [c1, c2, c3, ....]

