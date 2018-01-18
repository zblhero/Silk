
'''
author: zblhero@gmail.com

    FLASK_APP=run.py flask run
'''


from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

import sys
sys.path.append('../')

from search import *



app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

companies = get_companies()
orders = get_orders(companies)

@app.route('/')
def home_page():
    
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_query():
    print(request.method)
    if request.method == 'POST':
        name = request.form['name']
        js = request.form['js']
        ws = request.form['ws']
        md = request.form['md']
        kz = request.form['kz']
        xjmf = request.form['xjmf']
        zz = request.form['zz']

        query = {'js': js, 'ws': ws, 'md': md, 'kz': kz, 'xjmf': xjmf, 'zz': zz, 'name': name}

        orders1, coms2 = search(companies, query)
        #orders = orders1+orders2+orders3

        coms = []
        search_orders = {}
        #orders = search1(query, companies)
        for order in orders1:
            com = companies[int(order['user_id'])]
            if com in coms:
                search_orders[int(order['user_id'])].append(order)
            else:
                coms.append(companies[int(order['user_id'])])
                search_orders[int(order['user_id'])] = [order]

        
        #coms2 = search2(query, companies)
        #print companies[int(order['user_id'])].info
        return render_template('result.html', coms=coms, orders=search_orders, coms2=coms2)
    if request.method == 'GET':
        print('get method')

        
    