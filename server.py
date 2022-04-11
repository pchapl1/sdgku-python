import json
from nis import cat
from flask import Flask, request, redirect, session, abort
from flask.templating import render_template
from mock_data import catalog
from dotenv import load_dotenv
import os
from bson import ObjectId
from flask_cors import CORS
load_dotenv()

from config import db

url = str(os.getenv('mongo_url'))
app = Flask('Server')
CORS(app)

@app.route('/')
def index():
    return 'hello from flask'


@app.route('/api/catalog', methods = ['get'])
def get_catalog():
    products = []
    cur = list(db.products.find({}))

    for prod in cur:
        prod['_id'] = str(prod['_id'])
        products.append(prod)
    return json.dumps(products)


@app.route('/api/save_prod', methods = ['post'])
def save_product():
    product = request.get_json()
    db.products.insert_one(product)
    #fix_id
    product['_id'] = str(product['_id'])
    return json.dumps(product)



@app.route('/api/catalog/count', methods = ['get'])
def num_products():
    cur = list(db.products.find({}))
    return json.dumps(len(cur))


@app.route('/api/catalog/total', methods = ['get'])
def total_products():
    cur = list(db.products.find({}))
    total = 0
    for x in cur:
        total += x['price']
    return json.dumps(total)





@app.route('/api/catalog/<id>', methods = ['get'])
def get_by_id(id):
    try:
        prod = db.products.find_one({'_id' : ObjectId(id)})
        prod['_id'] = str(prod["_id"])
        return json.dumps(prod)
    except Exception as e:
        return f'id doesnt exist: {e}'




@app.route('/api/catalog/most_expensive', methods = ['get'])
def most_expensive():
    cur = list(db.products.find({}))
    max_price = 0
    prod_name = cur[0]['title']
    for x in cur:
        if x['price'] > max_price:
            max_price = x['price']
            prod_name = x['title']
    return json.dumps(prod_name)

@app.route('/api/catalog/least_expensive', methods = ['get'])
def least_expensive():
    cur = list(db.products.find({}))

    min_price = cur[0]['price']
    prod_name = cur[0]['title']
    for x in cur:
        if x['price'] < min_price:
            prod_name = x['title']
    return json.dumps(prod_name)

@app.route('/api/catalog/category', methods = ['get'])
def by_category():
    cur = list(db.products.find({}))
    cats = []
    for x in cur:
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
    cat = []
    for prod in db.products.find({'category' : category}):
        prod['_id'] = str(prod['_id'])
        cat.append(prod)
    return json.dumps(cat)


@app.route('/api/someNumbers', methods = ['get'])
def someNumbers():
    return json.dumps([x for x in range(1,51)] )

# =========================================================================
# ================================Coupons================================
# =========================================================================


allCoupons = []

@app.route('/api/save_coupon', methods = ['get', 'post'])
def save_coupon():
    if request.method == 'POST':
        coupon = request.get_json()
        if not 'code' in coupon or len(coupon['code']) < 5:
            print('code error')
            return abort(400, 'coupon code must be at least 5 characters')

        if not 'discount' in coupon or int(coupon['discount']) < 5 or int(coupon['discount']) > 50:
            print('discount error')

            return abort(400, 'discount can not be lower than 5 percent or higher than 50')
        #fix_id
        db.coupons.insert_one(coupon)
        coupon['_id'] = str(coupon['_id'])
        return json.dumps(coupon)
    else:
        cur = list()
        for prod in db.coupons.find({}): 
            prod['_id'] = str(prod['_id'])
            cur.append(prod)
        return json.dumps(cur)



@app.route('/api/coupons/<code>', methods = ['get'])
def find_by_code(code):

    coup =  db.coupons.find_one({'code' : code})
    coup['_id'] = str(coup['_id'])
    return json.dumps(coup)





# =========================================================================
# ===============================Users================================
# =========================================================================

@app.route('/api/user', methods = ['get', 'post'])
def user():
    if request.method == 'POST':
        user = request.get_json()
        if not 'username' in user or len(user['username']) < 1 :
            return abort(400, 'must have username')
        if not 'email' in user or len(user['email']) < 1 :
            return abort(400, 'must have email')
        if not 'password' in user or len(user['password'] < 1):
            return abort(400, 'must have password')
        if not 'first' in user or len(user['first']) < 1:
            return abort(400, 'must have first name')
        if not 'last' in user or len(user['last']) < 1:
            return abort(400, 'must have last name')

        db.users.insert_one(user)
        user['_id'] = str(user['_id'])
        return json.dumps(user)
    elif request.method == 'GET':
        users = list()
        for user in db.users.find({}):
            user['_id'] = str(user['_id'])
            users.append(user)
        return json.dumps(users)

@app.route('/api/user/<email>', methods = ['get'])
def get_user(email):
    user = db.users.find_one({'email':email})
    user['_id'] = str(user['_id'])
    return json.dumps(user)




@app.route('/api/login', methods = ['post'])
def validate_user_data():
    data = request.get_json()

    if not 'username' in data:
        return abort(400, 'no key user')
    if not 'password' in data:
        return abort(400, 'no key password')

    user = db.users.find_one({"username": data['username'], "password" : data['password']})
    if not user:
        return abort(401, "user not found")
    else:
        user['_id'] = str(user['_id'])
        user.pop('password')
        return json.dumps(user)
app.run(debug=True)