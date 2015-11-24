from pymongo import MongoClient


class Database:
	def __init__(self, db):
		self.db = MongoClient()[db]


	def insert(self, collection, data):
		self.db[collection].insert(data)


	def find(self, collection, data):
		return [item for item in self.db[collection].find(data)]