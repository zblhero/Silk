#!coding=utf-8
from search import *

import re

lines = []
table_lines = []
names = [['FDY', '拉伸丝'], ['SPH'], ['SP'], ['POY', '拉伸丝'], ['CEY', '弹力复合纤维'], ['PWY'], ['SSY'], ['FTY'], ['SQH'], ['ATY'],
         ['金银丝'], ['金丝', '金'], ['银丝'], ['亮片丝', '亮片'],
         ['海岛丝'], ['海岛黑丝'],
         ['钻石丝'], ['钻丝'], ['七彩丝', '七彩'], ['钻石纱'],
         ['涤锦复合丝', '涤锦复合'], ['阳涤复合丝'], ['涤阳复合丝'], ['锦涤复合丝'], ['阳涤'],
         ['锦纶单丝'],  ['全涤天鹅绒纱'],

         ['高弹多丽丝'], ['多丽丝'], ['空变丝'],
         ['假捻丝', '假捻'], 
         ['空变'], ['紧塞纺'], ['纯天丝'], ['天丝'], ['记忆丝'], ['单丝'],
         ['双包'], 
         ['涤纶长丝'], ['涤纶'], 
         ['氨纶包覆纱'], ['圆孔'], ['碱溶丝', '碱溶'], ['锦单丝'],
         ['阳离子舞龙丝'], ['阳离子', '阳离', '阳'], ['尼龙'], ['氨纶'], ['铜氨'],
         ['来回竹节'], ['花色竹节'],
         ['舞龙丝'], ['导电复合丝'], ['导电丝'], ['幻彩丝'],
         ['涤长丝'], ['长丝'], ['竹节'], ['人丝'], ['曲丝'], ['碱溶丝'], ['碱溶丝'], ['海岛'], ['双股'], ['乐丽丝'], ['单孔丝'], ['花蕾丝'],
         ['纯天丝'], ['三角有光异形丝'], ['三叶异型丝'], ['三角异型丝', '三角异形丝'], ['大肚纱'], ['曲线'], ['空包'], ['异形丝'],
         ['紧赛纺', '紧赛'], ['并喷'],
         ['尼龙低弹'], ['低弹丝', '低弹'], ['高弹丝', '高弹'], ['弹力', '弹丝', '弹'],
         ['黑丝白丝'], ['黑红白丝'], ['黑白空变丝'], ['黑白丝'], ['黑丝', '黑'], ['灰丝'], ['白丝', '白'], ['有光丝'], ['蓝'],
         ['锦包'], 
         ['锦纶', '锦'], ['复合丝', '复合'],
         ['涤包'], ['锦包'], ['三异'], ['亚光'], ['高配'],
         ['尼'], ['DTY', '涤纶弹丝', '涤'], ['棉'], ['氨'], ['竹'], ['网'], ['SD'], ['BD']
        ]

def init():
    with connection.cursor() as cursor:
        sql = 'select * from deep_line'
        cursor.execute(sql)
        results = cursor.fetchall()
        for i, result in enumerate(results):
            line = Line(id=result['id'], s=result['full_name'], name=result['name'], shazhi=result['shazhi'],
                gz=result['guangzedu'], jianianfangxiang=result['jianianfangxiang'],
                pailie=result['pailie'])
            if not line in lines:
                lines.append(line)
                table_lines.append(line)
        print('init....:', len(lines), len(table_lines))
    

class Line:
    def __init__(self, id=0, s='', shazhi='', name='', gz='', jianian='', jianianfangxiang='', pailie='', cgbj_id=0):
        self.id = id
        self.s = s
        self.shazhi = shazhi
        self.name = name
        self.gz = gz
        self.jianian = jianian
        self.jianianfangxiang = jianianfangxiang
        self.pailie = pailie
        self.cgbj_id = cgbj_id

        if len(s)>0:
            self.parse_line(s.upper())

    def __str__(self):
        return 'id: %s, s:%s, shazhi:%s, name:%s, gz:%s, jn:%s, jnfx:%s, pailie:%s'%(self.id, self.s, self.shazhi, self.name, self.gz, self.jianian, self.jianianfangxiang, self.pailie)

    def __eq__(self, other):
        return self.shazhi == other.shazhi and self.name==other.name and self.gz==other.gz and self.jianian==other.jianian and self.jianianfangxiang==other.jianianfangxiang and self.pailie==other.pailie
    
    

    def contains(self, line):
        for key in self.__dict__:
            if key not in ['id', 'cgbj_id'] and self.__dict__[key] is not None and len(line.__dict__[key]) > 0:
                #print(key, self.__dict__[key], line.__dict__[key])
                if self.__dict__[key].find(line.__dict__[key]) == -1:
                    return False
        return True


    def get_name(self, s):
        for classes in names:
            for name in classes:
                if s.find(name) != -1:
                    self.name = classes[0]
                    return name

    def get_gz(self, s):
        guangzedus = [['大有光'], ['有光'] , ['半消光', '半光', '半消', '半'], ['全消光', '消光', '消']]
        for gzs in guangzedus:
            for gz in gzs:
                if s.find(gz) != -1:
                    self.gz = gzs[0]
                    return gz

    def get_jianian(self, s):
        jianians = ['加捻', '无捻', '捻']
        for jn in jianians:
            if s.find(jn) != -1:
                self.jianian = jn
                return jn
        
        pattern = re.compile(r'\d+T')
        match = pattern.search(s)
        if match is not None:
            #print(s, match.group())
            self.jianian = match.group()
            return match.group()

    def parse_line(self, s):
        shazhi = s[:]

        while self.get_name(shazhi) is not None:
            #print('replace', shazhi, self.get_name(shazhi))
            shazhi = shazhi.replace(self.get_name(shazhi), '')
        
        gz = self.get_gz(shazhi)
        if gz is not None:
            shazhi = shazhi.replace(gz, '')

        # TODO: to be confirmed
        jn = self.get_jianian(shazhi)
        if jn is not None:
            shazhi = shazhi.replace(jn, '')

        pattern = re.compile(r'[\d\.]+[D, S]{0,1}(\/\+\d+F){0,1}$')
        match = pattern.search(shazhi)
        if len(shazhi) == 0:
            self.shazhi = None
        elif match is not None:
            self.shazhi=match.group()

        else:
            self.shazhi = None
        

            

class Silk():
    def __init__(self, s):
        #self.s = [] # split by '/+ '
        self.lines = []
        self.s = s
        if len(s) != 0:
            self.parse_info(s)

    def __str__(self):
        return '\n\t'.join([str(line) for line in self.lines])
        

    def parse_info(self, s):
        local_lines = []
        # 复合丝 20+26 15+15 50+50  specialities
        specalities = ['63D*24F', '50D*48F', '40D*40D', '75D*75D*150D', '75D*75D*150D',
            '20*26涤涤复合丝', '30S+30D尼龙*2', '20*26涤涤复合丝', '20+150*2', 
            '300D.600D.700D.900', '50D弹丝、50D长丝', '50D、75D、100D', '75D、150D', 
            '(50+20)D', '(30+20)D', '(70+40)D', '(40+20)D', '(75+40)D', '(20+50)D', '(40+40)D']

        if s in ['20+26', '15+15', '50+50'] or s in specalities:
            #self.lines = [{'number': s}]
            return

        s = s.strip(' ').strip('\n').strip('\t')
        s = re.sub('（', '(', s)
        s = re.sub('、', '+', s)
        s = re.sub('）', ')', s)
        s = re.sub('＋', '+', s)
        s = re.sub(',', '+', s)
        s = re.sub('×', '+', s)

        s = s.replace('(', '')
        s = s.replace(')', '')
        #s = s.replace('\'', '')
        #s = s.replace('\"', '')
        
        if len(s) == 0:
            return
            
        if s.find('/')!=-1:
            
            pattern = re.compile(r'\d+[D, S]{0,1}(\/\+\d+F){0,1}$')
            match = pattern.search(s)
            if match is not None:
                #print(s, match.group())
                pass
            pass
        #elif s.find('(') != -1 or s.find(u'（') != -1:
        #    print(s)
        else:
            if s.find(' ') != -1:
                s = s.replace(' ', '')

            if s.find('*')!=-1:
                values = s.split('*')
                s = values[0]
                #print(s)
            
            #pattern = re.compile(r'\d+[A-Z]{0,1}(\+\d+[A-Z]{0,1})*$')
            values = s.split('+')
            for value in values:
                line = Line(s=value)
                if line.shazhi is not None:
                    find = False
                    for l in lines:
                        if l == line:
                            self.lines.append(str(l.id))
                            find = True
                    if not find:
                        self.lines.append(line)


class Company():
    def __init__(self, com):
        self.id = 0
        self.com = com
        self.products = []
        self.machines = []


def process_companies():
    companies = get_companies()
    for id in companies:
        com = companies[id]
        if com.info is not None:
            print(com.info)

def process_silks():
    with connection.cursor() as cursor:
        #sql = 'INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)'
        sql = 'select * from deep_order'
        cursor.execute(sql)
        orders = cursor.fetchall()
        print('Total orders', len(orders))
        for i, order in enumerate(orders):
            #if not companies.has_key(int(order['user_id'])):
            if int(order['user_id']) not in companies:
                print(i, order['user_id'])
                pass
            else:
                if order['zz'] not in zzs:
                    zzs.append(order['zz'])
                #jss = Silk(order['js']).lines
                #wss = Silk(order['ws']).lines
                
                #sql = "update deep_order set jss='%s', wss='%s' where id=%d"%(','.join(jss), ','.join(wss), order['id'])
                #print(i, jss, wss, sql)
                #cursor.execute(sql)


def get_order_counts():
    with connection.cursor() as cursor:
        sql = 'select count(*) from deep_order'
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0]['count(*)']

def get_order_for_page(page, PER_PAGE, count):
    with connection.cursor() as cursor:
        sql = 'select * from deep_order order by id desc limit %d, %d'%((page-1)*PER_PAGE, PER_PAGE)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

def get_company_counts():
    with connection.cursor() as cursor:
        sql = 'select count(*) from deep_company'
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0]['count(*)']

def get_company_for_page(page, PER_PAGE, count):
    with connection.cursor() as cursor:
        sql = 'select * from deep_company order by id desc limit %d, %d'%((page-1)*PER_PAGE, PER_PAGE)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results


if __name__ == "__main__":
    #init()
    #companies = get_companies()
    #process_silks()
    #print(zzs)
    
    line = Line(s='20D400T')
    line1 = Line(s='20D')
    print(line.contains(line1), line, line1)
    #process_companies()