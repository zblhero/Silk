#!coding=utf-8
import datetime
import pymysql.cursors
from bs4 import BeautifulSoup
import re

from process import *


lines = {}
orders = []
companies = {}
zzs = []
names = []

def conn():
    connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='',
                             db='buziyuan',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection


class Company():
    def __init__(self):
        self.orders = []

def init_coms():
    for id in companies:
        com = companies[id]
        com['fit'] = ''
        com['fit_orders'] = []
        com['dis'] = 99999.0

def get_lines():
    
    with connection.cursor() as cursor:
        sql = 'select * from deep_line'
        cursor.execute(sql)
        results = cursor.fetchall()
        for i, result in enumerate(results):
            #lines[result['id']] = result
            line = Line(id=result['id'], s=result['full_name'], shazhi=result['shazhi'], name=result['name'], gz=result['guangzedu'], jianian=result['jianian'], jianianfangxiang=result['jianianfangxiang'], pailie=result['pailie'])
            lines[result['id']] = line
    return lines

def get_orders(companies, lines):
    order = {'name': 'xxx',
            'md': 1, 'js': '20D', 'ws': '50D'}
            
    with connection.cursor() as cursor:
        #sql = 'INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)'
        sql = 'select * from deep_order'
        cursor.execute(sql)
        orders = cursor.fetchall()
        #print('Total orders', len(orders))
        for i, order in enumerate(orders):
            #if not companies.has_key(int(order['user_id'])):
            if int(order['user_id']) not in companies:
                pass
            else:
                if order['zz'] not in zzs:
                    zzs.append(order['zz'])
                if order['name'] not in names:
                    names.append(order['name'])
                
                jss = order['jss'].split(',')
                order['js_line'] = [int(js) for js in jss if len(js) > 0]
                wss = order['wss'].split(',')
                order['ws_line'] = [int(ws) for ws in wss if len(ws) > 0]
                #print(i, order['js_line'], order['ws_line'])

                order['dis'] = 0.0
                order['lines'] = []
                for js in jss:
                    if len(js) > 0:
                        order['lines'].append(lines[int(js)])
                for ws in wss:
                    if len(ws) > 0:
                        order['lines'].append(lines[int(ws)])

                #print(len(order['lines']), order['jss'], order['wss'])

                companies[int(order['user_id'])]['orders'].append(order)

    return orders



def get_companies():
    with connection.cursor() as cursor:
        #sql = 'INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)'
        # id user_id name areash areasi areaqu address 
        sql = 'select * from deep_company'
        cursor.execute(sql)
        results = cursor.fetchall()
        print('com info number:', len(results))
        for i, com in enumerate(results):
            com['orders'] = []
            com['fit_orders'] = []
            com['dis'] = 99999.0
            companies[int(com['user_id'])] = com
    return companies

def full_pattern(query, content):
    for word in query:
        if content.find(word) == -1:
            return False
    return True


def parse_value(query, value='100D+100D'):
    value = value.upper()

    cpmf_pattern = re.compile(r'\d+CM$')
    cpmf_match = cpmf_pattern.match(value)
    if cpmf_match is not None:
        query['cpmf'] = cpmf_match.group()
        return

    kz_pattern = re.compile(r'\d+GSM$')
    kz_match = kz_pattern.match(value)
    if kz_match is not None:
        query['kz'] = kz_match.group()
        return

    md_pattern = re.compile(r'(\d+\*)+\d+$')
    md_match = md_pattern.match(value)
    if md_match is not None:
        query['md'] = md_match.group()
        return

    cpmd_pattern = re.compile(r'\d+T$')
    cpmd_match = cpmd_pattern.match(value)
    if cpmd_match is not None:
        query['cpmd'] = cpmd_match.group()
        return 

    cf_pattern = re.compile(r'\d+\%.*$')
    cf_match = cf_pattern.match(value)
    if cf_match is not None:
        query['cf'] = cf_match.group()
        return 

    

    silk = Silk(s=value)
    if 'js' in query and len(silk.lines) > 0:
        query['ws'] = silk
        return 
    if len(silk.lines) > 0:
        query['js'] = silk
        return
    
    if value in zzs:
        query['zz'] = value
        return

    if 'name' in query:
        query['name'] += value
    else:
        query['name'] = value

    

def parse_query(s='100D+100D'):
    query = {}
    for value in s.split(' '):
        parse_value(query, value=value)

    for key in query:
        print(key, ':', query[key])
    return query

def search1(query, results=[]):
    for id in companies:
        com = companies[id]
        for order in com['orders']:
            find = True
            for key in query:
                if key == 'js' or key == 'ws':
                    if order[key] != query[key].s:
                        find = False
                else:
                    if order[key] != query[key]:
                        find = False
            if find:
                com['fit_orders'].append(order)
        if id not in results and len(com['fit_orders']) > 0:
            results.append(id)
    print('search1', len(results), results)
    '''for id in results:
        com = companies[id]
        print(id, com['fit_orders'][0])'''
    return results
                


def search2(query, results=[]):
    for id in companies:
        com = companies[id]

        find = {}
        # init and search if in company info 
        for key in query:
            if key not in ['js', 'ws']:
                find[key] = False
                if com['info'] is not None :
                    if com['info'].find(query[key]) != -1:
                        find[key] = True
                        com['fit'] = com['info']
            else:
                for i, line in enumerate(query[key].lines):
                    find[key+'-'+str(i)] = False
        
        # search if in each order
        for order in com['orders']:
            find_order = False
            for key in query:
                if key == 'js' or key == 'ws':
                    #find[key] = True
                    for i, line in enumerate(query[key].lines):
                        find_line = False
                        for l in order['lines']:
                            #print(l.s, line.s, l.contains(line))
                            if l.contains(line):
                                find[key+'-'+str(i)] = True
                                find_order = True
                elif key == 'cpmf':  # 400cm
                    try:
                        order['dis'] += abs(order[key]-int(query[key][:-2]))/200
                        find[key] = True
                    except TypeError:
                        order['dis'] += 1.0
                elif key == 'kz':  # 118GSM
                    try:
                        order['dis'] += abs(order[key]-int(query[key][:-3]))/300
                        find[key] = True
                    except TypeError:
                        order['dis'] += 1.0
                else:
                    #if order[key] is not None and order[key] == query[key]:
                    if order[key] is not None and full_pattern(query[key], order[key]):
                        find[key] = True
                        find_order = True
                
                '''elif key == 'kz':  # 118GSM
                    pass
                elif key == 'md':   # 19*2*25
                    pass
                elif key == 'cpmd':  # 430T
                    pass'''
                if key == 'name':
                    for l in order['lines']:
                        #print(query[key], l.s, order[key], find[key])
                        if full_pattern(query[key], l.s):
                            find[key] = True
                            find_order = True
            if find_order: # when only one key is True
                if order['dis'] < com['dis']:
                    com['dis'] = order['dis']
                com['fit_orders'].append(order)


        find_fit = True    
        for key in find:
            if not find[key]:
                find_fit = False
        if find_fit and id not in results:
            results.append(id)
            #print('fits:', com['fit'])
            #print()
    print('search2:', len(results), results)
    '''for id in results:
        com = companies[id]
        print(id)
        for order in com['fit_orders']:
            print(order['name'])'''
    return results   



def add_com(query):
    print('add com', query)
    with connection.cursor() as cursor:
        sql = "insert into deep_company (user_id, name, address, linkname, linktel, info) values (0, '%s', '%s', '%s', '%s', '%s')"%(query['name'], query['address'], query['link'], query['tel'], query['info'])
        print('sql is ', sql)
        cursor.execute(sql)
        return True
    return False

def add_order(query):
    with connection.cursor() as cursor:
        sql1 = "select user_id from deep_company where name='%s'"%(query['comname'])
        cursor.execute(sql1)
        results = cursor.fetchall()
        if len(results) > 0:
            for key in ['cpmf', 'xjmf', 'sjmf', 'kz', 'cpkz', 'jg']:
                if query[key] == '':
                    query[key] = 0
            sql2 = "insert into deep_order \
                (user_id, name, cf, zz, js, ws, md, cpmd, cpmf, xjmf, sjmf, kz, cpkz, type, zjtype, jg) \
                values (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, %d, '%s', '%s', %f)"\
                %(results[0], query['name'], query['cf'], query['zz'], query['js'], query['ws'], query['md'],query['cpmd'], int(query['cpmf']),int(query['xjmf']),int(query['sjmf']),int(query['kz']),int(query['cpkz']),query['type'],query['zjtype'], float(query['jg']))
            print(sql2)
            cursor.execute(sql2)
        else:
            return False


        #sql = "insert into deep_order (name, address, link, tel, intro) values ('%s', '%s', '%s', '%s', '%s')"%(query['name'], query['address'], query['link'], query['tel'], query['intro'])
        #print(sql)
        #cursor.execute(sql)
        pass

if __name__ == "__main__":
    companies = get_companies()
    lines = get_lines()
    orders = get_orders(companies, lines)

    #query = parse_query('消光横条四面弹 40CM 100D')
    #print('query:', query)
    #search2(query)
    query = {'name': '测试工厂', 'address': '', 'link':'', 'tel':'', 'info':''}
    add_com(query)
    