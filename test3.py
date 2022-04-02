from mock_data import catalog
import json

def lower_than(price):

    count = 0

    for x in catalog:
        if x['price'] < price:
            count +=1
    return count

def greater_than(price):

    count = 0

    for x in catalog:
        if x['price'] > price:
            count +=1
    return count

# print(lower_than(17))
# print(greater_than(5))

def find_prod(word):
    # return len(x['title'] for x in catalog if word.lower() in x['title'].lower())
    count = 0
    for x in catalog:
        if word.lower() in x['title'].lower():
            count +=1
    return count
print(find_prod('hem'))
