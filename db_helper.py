import pymongo
from pymongo import MongoClient
from config import mongo_config

class Database:
	def __init__(self, db):
		host = mongo_config['host']
		port = mongo_config['port']
		url = "mongodb://{host}:{port}".format(host=host, port=port)
		self.db = MongoClient(url)[db]


	def insert(self, collection, data):
		self.db[collection].insert(data)


	def find(self, collection, data):
		docs = self.db[collection].find(data).sort([("_id", pymongo.DESCENDING)])
		return [item for item in docs]