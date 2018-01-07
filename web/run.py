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
    if request.method == 'POST':
        name = request.form['name']
        js = request.form['js']
        ws = request.form['ws']
        md = request.form['md']
        kz = request.form['kz']
        sjmf = request.form['sjmf']

        query = {'js': js, 'ws': ws, 'md': md, 'kz': kz, 'sjmf': sjmf, 'name': name}

        print(query)

        orders = search(companies, query)[:10]

        results = []
        for j, order in enumerate(orders[:5]):
            #print(order['user_id'], companies[order['user_id']], order)
            if companies[order['user_id']] not in results:
                result = {}
                result['com'] = companies[order['user_id']]
                result['order'] = order
                results.append(result)
        return render_template('result.html', results=results)

        
    