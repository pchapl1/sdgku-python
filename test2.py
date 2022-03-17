
def test_dict():
    me = {
        'first': 'Phil',
        'last': 'Chaplin',
        'age': 36,
        'hobbies' : [],
        'address' : {
            'street': 'Polk',
            'city': 'La Paz'
        }
    }

    print(f"{me['first']} {me['last']}")
print('------ Dictionary Test -------')
test_dict()