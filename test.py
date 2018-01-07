#!coding=utf-8
from search import *

test_cases = [
    {'name': u'记忆布', 'js': '100D', 'ws': '120D', 'md': '', 'kz': '', 'sjmf': ''}, # search 1

    #{'js': u'170D', 'ws': u'320D', 'md': '16*12', 'kz': 200, 'sjmf':15, 'type': u'记忆布'}, # search2

    #{'js': u'104D', 'ws': u'190D'}
    
]

if __name__ == "__main__":
    companies = get_companies()
    orders = get_orders(companies)


    for i, case in enumerate(test_cases):
        orders = search(companies, case)
        for j, order in enumerate(orders[:5]):
            #print j, order['dis'], order['js'], order['ws']
            print  order['name'], order['js'], order['ws']
            
            
            '''js = Silk(case['js'])
            case['js_class'] = js

            ws = Silk(case['ws'])
            case['ws_class'] = ws
            dis = get_distance(order, case, keys=['js_class', 'ws_class'])'''
        


