import pymongo
from config import mongo_config

class Database:
	def __init__(self, db):
		host = mongo_config['host']
		port = mongo_config['port']
		url = "mongodb://{host}:{port}".format(host=host, port=port)
		self.db = pymongo.MongoClient(url)[db]


	def insert(self, collection, data):
		self.db[collection].insert(data)


	def find(self, collection, data):
		docs = self.db[collection].find(data).sort([("_id", pymongo.DESCENDING)])
		return [item for item in docs]


	def update(self, collection, key, data):
		self.db[collection].update_one(key, {"$set": data})


	def delete(self, collection):
		self.db[collection].delete_many({})


	def count_docs(self, collection, data={}):
		return self.db[collection].count(data)


	def aggregate(self, collection, field, data={}):
		result = self.db[collection].aggregate([{"$match": data}, {"$group": {"_id": "$"+field, "count": {"$sum": 1}}}])
		return [item for item in result]