from db_helper import Database

class DataInsights:
	def __init__(self):
		self.db = Database('messages')

	def no_of_responses(self, question_no):
		return self.db.count_docs('received', {'question_no': question_no})

	def choice_distribution(self, question_no):
		dist = {}
		aggs = self.db.aggregate('received', 'text', {'question_no': question_no})
		for item in aggs:
			dist[item['_id']] = item['count']
		return dist




di = DataInsights()

questions = di.db.find('questions', {})

for question_data in questions:
	print question_data['question']
	print "No of responses:", di.no_of_responses(1)
	dist = di.choice_distribution(question_data['question_no'])
	for choice in question_data['choices']:
		print choice, dist.get(choice, 0)
	print ''
	