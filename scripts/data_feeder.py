from db_helper import Database
from questions import questions
db = Database('messages')

for question in questions:
	db.insert('questions', question)