from mock_data import catalog
import json


def find_prod(word):
    prods = []
    for x in catalog:
        if word.lower() in x['title'].lower():
            prods.append(x)
            print('title: ' , x['title'])
            print('price: ' , x['price'])
    return prods
print(find_prod('hem'))
