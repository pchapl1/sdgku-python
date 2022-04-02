
import json
from nis import cat
import random
from flask import Flask, request, redirect, session, abort
from flask.templating import render_template
from mock_data import catalog
from random import randint
from dotenv import load_dotenv
import os


app = Flask('Server')


@app.route('/')
def index():
    return 'hello from flask'

# @app.route('/me')
# def about_me():
#     return 'Phil Chaplin'

@app.route('/api/catalog', methods = ['get'])
def get_catalog():
    return json.dumps(catalog)


@app.route('/api/save_prod', methods = ['post'])
def save_product():
    product = request.get_json()
    product['_id'] = random_with_N_digits(8)
    print(product)
    catalog.append(product)
    return json.dumps(product)



@app.route('/api/catalog/count', methods = ['get'])
def num_products():
    return json.dumps(len(catalog))


@app.route('/api/catalog/total', methods = ['get'])
def total_products():
    total = 0
    for x in catalog:
        total += x['price']
    return json.dumps(total)


@app.route('/api/about', methods = ['get'])
def about_me():
    about_message = 'this is the about page'
    return json.dumps(about_message)

@app.route('/api/catalog/<id>', methods = ['get'])
def get_by_id(id):
    try:
        return json.dumps([x for x in catalog if x['_id'] == id][0])
    except Exception as e:
        return 'id doesnt exist'

@app.route('/api/catalog/most_expensive', methods = ['get'])
def most_expensive():
    max_price = 0
    prod_name = catalog[0]['title']
    for x in catalog:
        if x['price'] > max_price:
            max_price = x['price']
            prod_name = x['title']
    return json.dumps(prod_name)

@app.route('/api/catalog/least_expensive', methods = ['get'])
def least_expensive():
    min_price = catalog[0]['price']
    prod_name = catalog[0]['title']
    for x in catalog:
        if x['price'] < min_price:
            prod_name = x['title']
    return json.dumps(prod_name)

@app.route('/api/catalog/category', methods = ['get'])
def by_category():
    cats = []
    for x in catalog:
        if x['category'] not in cats:
            cats.append(x['category'])
    return json.dumps(cats)


# @app.route('/api/catalog/add_prod', methods = ['post'])
# def add_prod():
#     id = input('choose an id: ')
#     title = input('choose an title: ')
#     price = input('choose an price: ')
#     stock = input('choose an stock: ')
#     category = input('choose an category: ')
#     image = input('enter image path: ')
#     product = {"_id": id, 'title': title, 'price' : price, 'stock': stock, 'category': category, 'image': image}
#     catalog.append(product)
#     return json.dumps(catalog)


@app.route('/api/catalog/category/<category>', methods = ['get'])
def find_by_cat(category):
    return json.dumps([x['title'] for x in catalog if x['category'] == category] )


@app.route('/api/someNumbers', methods = ['get'])
def someNumbers():
    return json.dumps([x for x in range(1,51)] )





allCoupons = []

@app.route('/api/save_coupon', methods = ['get', 'post'])
def save_coupon():
    if request.method == 'POST':
        coup = request.get_json()
        coup['_id'] = random_with_N_digits(8)
        allCoupons.append(coup)
        return json.dumps(coup)
    else:
        return json.dumps(allCoupons)

# sets _id for coupons and prods
ids = []
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    new_id = randint(range_start, range_end)
    if new_id not in ids:
        ids.append(new_id)
        return new_id
    else:
        random_with_N_digits(8)

print(random_with_N_digits(8))
app.run(debug=True)