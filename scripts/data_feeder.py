import sys
sys.path.append('./../')

from feedbackbot.db_helper import Database
from feedbackbot.text_message import questions, info_messages
db = Database('messages')

question_no = 0
for question in questions:
	question.update({'question_no': question_no})
	db.insert('questions', question)
	question_no += 1


for k, v in info_messages.iteritems():
	db.insert('info_messages', {k: v})