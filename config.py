import pymongo
import certifi

mongo_url = 'mongodb+srv://pchapl1:Lsutigers1@cluster0.g4ume.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

client = pymongo.MongoClient(mongo_url, tlsCAFile = certifi.where())

db = client.get_database('shirts-r-us')