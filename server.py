
import json
from nis import cat
from flask import Flask, request, redirect, session, abort
from flask.templating import render_template
from mock_data import catalog




app = Flask('Server')


@app.route('/')
def index():
    return 'hello from flask'

@app.route('/me')
def about_me():
    return 'Phil Chaplin'

@app.route('/api/catalog', methods = ['get'])
def get_catalog():
    return json.dumps(catalog)

@app.route('/api/catalog', methods = ['post'])
def save_product():
    pass

@app.route('/api/catalog/count', methods = ['get'])
def num_products():
    return json.dumps(len(catalog))


@app.route('/api/catalog/total', methods = ['get'])
def total_products():
    total = 0
    for x in catalog:
        total += x['price']
    return json.dumps(total)


@app.route('/api/about')
def about_me():
    about_message = 'this is the about page'
    return json.dumps(about_message)

@app.route('/api/catalog/<id>')
def get_by_id(id):
    try:
        return json.dumps([x for x in catalog if x['_id'] == id][0])
    except Exception as e:
        return 'id doesnt exist'

@app.route('/api/catalog/most_expensive')
def most_expensive():
    max_price = 0
    prod_name = ''
    for x in catalog:
        if x['price'] > max_price:
            max_price = x['price']
            prod_name = x['title']
    return json.dumps(prod_name)


app.run(debug=True)