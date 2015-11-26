import sys
sys.path.append('./../')

from feedbackbot.db_helper import Database
from feedbackbot.text_message import questions
db = Database('messages')

question_no = 0
for question in questions:
	question.update({'question_no': question_no})
	db.insert('questions', question)
	question_no += 1