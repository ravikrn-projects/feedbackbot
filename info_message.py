
class InfoMessage:
	def __init__(self, db):
		self.db = db

	def get_info_message(self, key):
		docs = self.db.find('info_messages', {key: {'$exists': True}})
		try:
			message = docs[0][key]
		except:
			message = None
		return message
