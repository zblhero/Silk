#!coding=utf-8
import datetime
import pymysql.cursors
from bs4 import BeautifulSoup
import re

connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='',
                             db='buziyuan',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# dismiss space between two numbers
def dismiss_space(line):
    newline = ''
    for i, s in enumerate(line):
        if s == ' ' and line[i-1].isdigit() and i+1<len(line) and line[i+1].isdigit():
            #print('dismiss space', line[i-1:i+2])
            pass
        else:
            newline += s
    return newline

def split_products(line):
    products = re.split(u'、，', line)
    return products

def get_silk_distance(silk1, silk2):
    dis = 0.0

    # todo add zz_dis
    zz_dis = 0.0
    #zz_dis = get_str_distance(silk1.zz, silk2.zz)

    line_dis = 0.0
    if len(silk1.lines) == len(silk2.lines):
        for i, line in enumerate(silk1.lines):
            try:
                number_dis = abs(silk1.lines[i]['number'] - silk2.lines[i]['number'])/100.0
                
                type_dis = get_str_distance(silk1.lines[i]['type'], silk2.lines[i]['type'])
                line_dis = number_dis + type_dis
                #print 'line dis', i, line_dis, number_dis, type_dis, silk1.lines[i], silk2.lines[i]
            except KeyError:
                line_dis = 2.0
    else:
        line_dis = 2.0

    dis = line_dis + zz_dis
    return dis

    #if len(silk1.lines) > 0 and len(silk2.lines) > 0 and  silk1.lines[0]['number'] == silk2.lines[0]['number']:
    #    print 'line dis', dis, line_dis, silk1.lines[i]['number'], silk2.lines[i]['number']
    
    #print 'get dis', dis, zz_dis, line_dis
    #for line in 

class Silk():
    def __init__(self, s):
        #self.s = [] # split by '/+ '
        self.zz = ''
        self.lines = []
        self.info = s
        if len(s) != 0:
            self.parse_info(s)
            
        

        # zz
        # lines
        #   1. parts, number, type
        #   2.
        #   3. ...

    def parse_info(self, s):
        #s = u'150DFDY+（150DDTY+40DSP）'
        s = s.strip(' ')
        re.sub(u'（', '(', s)
        re.sub(u'）', ')', s)
        #s.replace(u'）', ')')
        #print s
        if len(s) == 0:
            return

        #print s
        if s.find('(') != -1 or s.find(u'（') != -1:
            pass
        elif s.find(' ') != -1 or s.find('*')!=-1:
            pass
        else:
            # exceptions: 160D*2双纬 300D.600D.700D.900  150D、200D  50D*68D 4.5   R21S紧赛
            #print s
            silks = split_silk(s)
            #if silks.has_key('zz'):
            if 'zz' in silks:
                self.zz = silks['zz']
            self.lines = silks['lines']

def split_silk(s):
    silks = {}
    if s.find(' ') != -1:
        zzs = s.split(' ')
        #print zzs
        s = zzs[0]
        silks['zz'] = zzs[1:]

    values = s.split('+')
    silks['lines'] = [{} for i in range(len(values))]
    for i, value in enumerate(values):
        if value.find('/') != -1:
            parts = value.split('/')
            value = parts[0]
            silks['lines'][i]['parts'] = parts[1]


        number, silk_type = '', ''
        for x in value:
            if x.isdigit() or x=='.':
                number += x
            else:
                silk_type += x
        if len(number) > 0: 
            try:
                silks['lines'][i]['number'] = float(number)
            except ValueError:
                break
        if len(silk_type) > 0: silks['lines'][i]['type'] = silk_type
        
        #print s, silks['lines']
    #print s, silks
    return silks

        #split to number + material

class Company():
    def __init__(self):
        self.id = 0
        self.lines = []
        self.products = []
        self.machines = []

        self.fit_lines = []
        self.fit_machines = []
        
        # order: class, subclass, name_num, name,      cf, zz,   js,   ws,   md,   cpmd,    xjmf,     cpkz,    kz,  type, zjtype,  jg,  cpy, kcl, cpmf,     sjmf,      report,     gm, isjb, zjxl, ylpp, ssl, pz, kjl
        #        系列                        品名           组织   经纱  纬纱   密度  成品密度   下机门幅   成平克重  克重  类型   在机类型  价格       库存 成品门幅    上机门幅                挂码
        #        pb_class                   提花麂皮绒                                                                                               在机   喷水                                  
        self.orders = []
        #self.search_orders = []

    def has_line(self, line): # line: type, number
        #print 'has', line
        for l in self.lines:
            find = True
            for key in ['number', 'type', 'parts']:
                if key in l and key not in line:
                    find = False
                if key in line and key not in l:
                    find = False
                if key in line and key in l and l[key] != line[key]:
                    find = False
            if find:
                return l
        return False

    #def search_lines(self, lines):


    def has_lines(self, lines, addfit=False):
        
        find = True
        for line in lines:
            l = self.has_line(line)
            if not l:
                find = False
            else:
                if addfit:
                    #print(l)
                    self.fit_lines.append(l)
        #print(silk.lines, find)
        return find

    def has_machine(self, machine, addfit=False):
        for m in self.machines:
            if m == machine:
                if addfit:
                    self.fit_machines.append(machine)
                return True
        return False

    def parse_info(self, info):
        self.info = info
        soup = BeautifulSoup(info, 'lxml')
        ps = soup.find_all('p')
        for p in ps:
            if p.string is not None and len(p.string.strip())>0:
                items = re.split('\t\n   ', p.string)
                for item in items:
                    # dismiss space between phone numbers
                    item = dismiss_space(item)
                    #print '\t item:', item
                    values = item.split(u'：')

                    for j, value in enumerate(values):
                        if j == 0:
                            if value.find(u'产品') > -1:
                                #print '\t\tkey 产品:', value, len(values), item
                                if len(values) > 1:
                                    self.products = split_products(values[1])
                            if value.find(u'月产量') > -1:
                                #print '\t\tkey 产量:', value, len(values), item
                                pass


def get_orders(companies):
    order = {'name': 'xxx',
            'md': 1, 'js': '20D', 'ws': '50D'}
    with connection.cursor() as cursor:
        #sql = 'INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)'
        sql = 'select * from fs_pibu_cgbj'
        cursor.execute(sql)
        orders = cursor.fetchall()
        #print('Total orders', len(orders))
        for i, order in enumerate(orders):
            #if not companies.has_key(int(order['user_id'])):
            if int(order['user_id']) not in companies:
                #print i, order['user_id']
                pass
            else:
                js = Silk(order['js'])
                order['js_class'] = js

                ws = Silk(order['ws'])
                order['ws_class'] = ws

                # add machines
                if len(order['zz'])>0 and not order['zz']  in companies[int(order['user_id'])].machines:
                    companies[int(order['user_id'])].machines.append(order['zz'])

                
                # add lines
                for line in js.lines:
                    #print line
                    if not companies[int(order['user_id'])].has_line(line):
                        line['order'] = order
                        #print(len(companies[int(order['user_id'])].lines), line)
                        companies[int(order['user_id'])].lines.append(line)
                for line in ws.lines:
                    if not companies[int(order['user_id'])].has_line(line):
                        line['order'] = order
                        companies[int(order['user_id'])].lines.append(line)

                companies[int(order['user_id'])].id = int(order['user_id'])
                companies[int(order['user_id'])].orders.append(order)
                #print int(order['user_id']), js.lines, ws.lines#, companies[int(order['user_id'])].lines
            #if i < 3:
            #    print i, order['user_id'], companies[int(order['user_id'])]
    return orders
            

        
        #cursor.execute(sql, ('Robin', 'Zhyea', tomorrow, 'M', date(1989, 6, 14)));
    #connection.commit()
    

def get_companies():
    companies = {}
    with connection.cursor() as cursor:
        #sql = 'INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)'
        # id user_id name areash areasi areaqu address 
        sql = 'select * from fs_member_cominfo'
        cursor.execute(sql)
        company_infos = cursor.fetchall()
        print('com info number:', len(company_infos))
        for i, com in enumerate(company_infos):
            company = Company()
            company.values = com
            #print('company infor', company.info, com)
            if com['info'] is not None and len(com['info'])>0:
                company.parse_info(com['info'])
            companies[int(com['user_id'])] = company
    return companies


def sort(fit_orders, key, desc=True):
    sort_orders = []
    for i, fit_order in enumerate(fit_orders):
        for j in range(i, len(fit_orders)):
            # bubble sort
            swap = False
            if desc:
                if fit_orders[i][key] < fit_orders[j][key]:
                    swap = True
            else:
                if fit_orders[i][key] > fit_orders[j][key]:
                    swap = True
            if swap:
                temp = fit_orders[i]
                fit_orders[i] = fit_orders[j] 
                fit_orders[j] = temp
    return fit_orders

def sort_coms(fit_coms, desc=True):
    for i, com in enumerate(fit_coms):
        for j in range(i, len(fit_coms)):
            # bubble sort
            swap = False
            if desc:
                if fit_coms[i].dis < fit_coms[j].dis:
                    swap = True
            else:
                if fit_coms[i].dis > fit_coms[j].dis:
                    swap = True
            if swap:
                temp = fit_coms[i]
                fit_coms[i] = fit_coms[j]
                fit_coms[j] = temp
    return fit_coms

# totally compatible
def search1(query, companies):
    # TODO: (0) search cabin first

    fits = []
    for com_id in companies:
        company = companies[com_id]
        for i, order in enumerate(company.orders):
            # check if company's order fits
            fit = True
            for key in query:
                if key in ['name', 'md', 'xjmf', 'kz', 'js', 'ws']:
                    #print(key, order[key], query[key], str)
                    if len(query[key]) > 0 and order[key] is not None:
                        try:
                            if str(order[key]) != str(query[key]):
                                fit = False
                        except UnicodeEncodeError:
                            fit = False
            if fit: # when every item fits
                order['com_id'] = com_id
                fits.append(order)
                #print(i, order, company)
                #break

    print('search 1 ', len(fits))
    fits = sort(fits, 'jg', desc=False)
    return fits

# js, ws compatible, (mf, kz, md) not compatible
def search2(query, companies):
    fit_coms, fit_ids = [], []
    for com_id in companies:
        company = companies[com_id] 
        fit = True

        if 'zz' in query and len(query['zz']) > 0:
        # if query.has_key('zz') and len(query['zz']) > 0:
            if not company.has_machine(query['zz'], addfit=True):
                fit = False
                continue
        #if query.has_key('js_class'):
        if 'js_class' in query:
            if not company.has_lines(query['js_class'].lines, addfit=True):
                fit = False
                continue
        #if query.has_key('ws_class'):
        if 'ws_class' in query:
            if not company.has_lines(query['ws_class'].lines, addfit=True):
                fit = False
                continue
        if fit:
            fit_coms.append(company)
    
    
    # TODO sort the coms
    for i, com in enumerate(fit_coms):
        min_dis = 9999
        for j, line in enumerate(com.fit_lines):
            dis = get_distance(line['order'], query, keys=['xjmf', 'kz', 'md'])
            if dis < min_dis:
                min_dis = dis
                com.dis = dis
            #order['dis'] = dis

    #for i, com in enumerate(fit_coms):
    #    print('sort fit', i, com.dis)
    fits = sort_coms(fit_coms, desc=False)

    return fits
        #company.has

'''def search2(query, companies):
    fit_orders, fit_coms, fit_ids = [], [], []
    for com_id in companies:
        company = companies[com_id]
        for i, order in enumerate(company.orders):
            if order['js'].find(query['js']) !=-1 and order['ws'].find(query['ws']) != -1:
                if order['js'] == query['js'] and order['ws'] == query['ws']:
                    order['dis'] = 0.0
                elif order['js'] == query['js'] and order['ws'] != query['ws']:
                    order['dis'] = 0.1
                elif order['js'] != query['js'] and order['ws'] == query['ws']:
                    order['dis'] = 0.1
                else:
                    order['dis'] = 0.2
                order['com_id'] = com_id
                fit_orders.append(order)
                #fit_coms.append(company)
                #fit_ids.append(com_id)
                break
    
    # TODO sort in closest mf kz md
    for i, order in enumerate(fit_orders):
        dis = get_distance(order, query, keys=['xjmf', 'kz', 'md'])
        order['dis'] += dis
    
    fits = sort(fit_orders, 'dis', desc=False)
        

    print('search 2 ', len(fits))
    # TODO （later）get closest machines
    return fits'''

# js, ws not compatible
'''
    x: 线的粗细度
    D: 化纤  S：人棉   T：成品密度    F：一根线内部股数
    20+26： 20， 26两根线拧成一股丝
    20D+26S：20的化纤和26的人棉拧成一股丝
'''
def search3(query, companies):
    # 1. get closest js, ws
    js = Silk(query['js'])
    query['js_class'] = js

    ws = Silk(query['ws'])
    query['ws_class'] = ws

    fit_orders = []
    for com_id in companies:
        company = companies[com_id]
        for i, order in enumerate(company.orders):
            dis = get_distance(order, query, keys=['js_class', 'ws_class'])
            order['dis'] = dis
            if dis != None and dis<0.3:
                fit_orders.append(order)
            #print dis, query['js'], query['ws'], order['js'], order['ws']
    fits = sort(fit_orders, 'dis', desc=False)

    print('search 3 ', len(fits), len(fit_orders))

    # 2. analyze material and machines

    return fits


def get_str_distance(str1, str2):
    min_dis = 999.0

    if str1 == str2:
        return 0.0

    if str1.find(str2) != -1 or str2.find(str1) != -1:
        return 0.1

    for i in range(len(str1)):
        ldis = 0.0
        for j in range(len(str2)):
            if i+j >= len(str1) or (i+j)>=len(str2):
                ldis += 1.0
            else:
                try:
                    ldis += abs(ord(str1[i+j])-ord(str2[i+j]))/128.0
                except TypeError:
                    # str1[i+j], str2[i+j]
                    pass
        try:
            ldis /= len(str2)
        except ZeroDivisionError:
            ldis = 1.0
        if ldis < min_dis:
            min_dis = ldis
    #print 'str distance', min_dis, str1, str2
    return min_dis

def get_distance(order, query, keys=['xjmf', 'kz', 'md']):
    dis = 0.0
    max_value = 500.0
    for key in keys:
        
        value = order[key]
        
        if key in query and len(query[key]) >0:
            # return max distance when search is null
            
            if not key in order: 
                dis += 1.0
            else:
                #print(key, query[key], order[key])
                if key in ['kz']:
                    try:
                        dis += abs(int(query[key])-int(order[key]))/500.0
                    except:
                        pass
                if key == 'xjmf':
                    try:
                        if float(order[key]) < float(query[key]):
                            dis += 1.0
                        else:
                            dis += 0.0
                    except ValueError:
                        print(order[key], query[key])
                        dis += 1.0
                if key in ['md']:
                    #print 'get distance', key, query[key], order[key]
                    if order[key].find(query[key]) != -1:
                        dis += 0.0
                    else:
                        ldis = 0.0
                        qmds = query[key].split('*')
                        omds = order[key].split('*')
                        if len(qmds) == 2 and len(omds) == 2:
                            #if qmds[0].isdigit() and qmds[1].isdigit() and omds[0].isdigit() and omds[1].isdigit():
                            try:
                                dis += (abs(int(qmds[0])-int(omds[0]))/100.0 + abs(int(qmds[1])-int(omds[1]))/100.0)/2
                            except ValueError:
                                dis+=1.0
                            #else:
                            #    dis += 1.0
                            #print 'get distance', qmds, omds, dis, order['kz']
                        else:
                            dis += 1.0
                if key in ['js', 'ws']:
                    # compare zz and lines
                    dis += get_str_distance(query[key], order[key])
                if key in ['js_class', 'ws_class']:
                    dis += get_silk_distance(query[key], order[key])
                    
    return dis

def search(companies, query = {'name': u'1234', 'js': u'170D', 'ws': u'320D', 'md': 16*12, 'type': u'记忆布'}):
    # fs_pibu_type
    # 品名 经纱 纬纱 坯布密度 工厂名称 类型

    #if query.has_key('js'):
    if 'js' in query:
        js = Silk(query['js'])
        query['js_class'] = js
    #if query.has_key('ws'):
    if 'ws' in query:
        ws = Silk(query['ws'])
        query['ws_class'] = ws
    
   

    orders1 = search1(query, companies)
    coms = search2(query, companies)

    #print(query, query['js_class'].lines, len(orders1), len(coms))
    #orders3 = search3(query, companies)
    #return orders1, coms, orders3
    return orders1, coms

if __name__ == "__main__":
    companies = get_companies()
    orders = get_orders(companies)

    #for key in companies:
    #    print key, companies[key].machines
    #   print key, companies[key].has_line()
    
    #for key in companies:
    #    print key, companies[key].machines, len(companies[key].orders), companies[key].products
    #query = {'name': u'有光贡缎'}
    query = {'js': '100D', 'ws': '300D', 'md':'40*32'}

    orders1, coms = search(companies, query)
    #for com in coms:
    #    print(com.fit_machines, com.fit_lines)
    print(len(coms))
