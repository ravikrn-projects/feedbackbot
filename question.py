
class Question:
	def __init__(self, db):
		self.db = db

	def get_question(self, question_no):
		question_data = self.db.find('questions', {'question_no': question_no})
		try:
			question_data = question_data[0]
		except Exception:
			question_data = None
		return question_data


	def get_number_of_questions(self):
		return self.db.count_docs('questions')


	def get_latest_question(self, user_id, collection):
		question_data = self.db.find(collection, {'user_id': user_id, 'question_no': {'$exists': True}})
		try:
			question_no = question_data[0]['question_no']
		except Exception:
			question_no = -1
		return question_no


	def get_latest_question_answered(self, user_id):
		return self.get_latest_question(user_id, 'received')


	def get_latest_question_sent(self, user_id):
		return self.get_latest_question(user_id, 'sent')
