
'''
author: zblhero@gmail.com

    FLASK_APP=run.py flask run
'''


from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import time, datetime
import json
from pagination import Pagination

import sys
sys.path.append('../')

#from search import *
from full_search import *

PER_PAGE = 20



app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
app.config['DEBUG'] = True
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#companies = get_companies()
#orders = get_orders(companies)
max_com_id = 0
companies = get_companies()
lines = get_lines()
orders = get_orders(companies, lines)


connection = conn()

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #print(username, password)

        with connection.cursor() as cursor:
            sql = "select * from deep_user where username='%s' and password='%s'"%(username, password)
            cursor.execute(sql)
            users = cursor.fetchall()
            if len(users) > 0:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/company/<int:id>', methods=['GET'])
def company_page(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    
    if 'query' in session:
        query = session['query']
        #print('session query', query)
        app.logger.info("com:"+str(id))
        app.logger.info('query:'+query)
        session.pop('query', None)

    company = companies[id]
    
    return render_template('company.html', com=company, username=username)

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')

@app.route('/full-search', methods=['POST', 'GET'])
def full_search_query():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    
    if request.method == "POST":
        coms = []
        s = request.form['query']
        session['query'] = s
        query = parse_query(s)
        

        com_ids = []
        print('search query0:', query, len(com_ids))
        init_coms()
        search1(query, com_ids)
        search2(query, com_ids)

        print('search query:', query, len(com_ids))

        for id in com_ids:
            coms.append(companies[id])
        #print(len(coms))
        return render_template('result.html', username=username, query=query, coms=coms, s=s, orders=[])


@app.route('/search', methods=['GET', 'POST'])
def search_query():
    #print(request.method)
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

@app.route('/orders/', defaults={'page': 1})
@app.route('/orders/page/<int:page>')
def show_orders(page):
    count = get_order_counts()
    orders = get_order_for_page(page, PER_PAGE, count)
    print(count, orders[0])
    if not orders and page != 1:
        abort(404)

    pagination = Pagination(page, PER_PAGE, count)
    return render_template('orders.html',
        pagination=pagination,
        orders=orders
    )

@app.route('/companies/', defaults={'page': 1})
@app.route('/companies/page/<int:page>')
def show_companies(page):
    count = get_company_counts()
    companies = get_company_for_page(page, PER_PAGE, count)
    print(count, companies[0])
    if not companies and page != 1:
        abort(404)

    pagination = Pagination(page, PER_PAGE, count)
    return render_template('companies.html',
        pagination=pagination,
        companies=companies
    )




@app.route('/new-order', methods=['GET', 'POST'])
def new_order():
    username = session['username']
    suc = request.args.get('suc')
    suc = suc if suc is not None else -1
    if request.method == 'POST':
        
        added = False
        if len(request.form['name'])>0 and len(request.form['comname'])>0:
            added = add_order(request.form)
        print('new order', request.form, added)
        if added:
            return redirect('/orders')
        else:
            return redirect('/new-order?suc=0')
    elif request.method == 'GET':
        return render_template('new-order.html', username=username, suc=suc)

@app.route('/new-com', methods=['GET', 'POST'])
def new_com():
    suc = request.args.get('suc') 
    suc = suc if suc is not None else -1
    username = session['username']
    if request.method == 'POST':
        added = add_com(request.form)
        print('new com', added)
        if added:
            return redirect('/companies')
        else:
            return redirect('/new-com?suc=0')

    elif request.method == 'GET':
        
        return render_template('new-com.html', username=username, suc=suc)

@app.route('/search-com', methods=['GET'])
def search_com():
    s = request.args.get('s')
    sql = "select name from deep_company where name like '%"+s+"%'"
    print(sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        coms = cursor.fetchmany(10)
        print(len(coms))
        return json.dumps(coms)


if __name__ == '__main__':
    app.run(debug=True)

        
    