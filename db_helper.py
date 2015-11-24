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
		return [item for item in self.db[collection].find(data)]