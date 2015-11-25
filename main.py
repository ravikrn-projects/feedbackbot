import requests
import time
from config import token, base_url
from questions import questions
import json
from db_helper import Database
import telegram
db = Database('messages')
bot = telegram.Bot(token)
	
def send(user_id, question, choices=None):
	if choices is not None:
		keyboard = json.dumps({'keyboard': [[item] for item in choices]})					  	
	else:
		keyboard = json.dumps({'hide_keyboard': True})
	try:
		bot.sendMessage(user_id, question, reply_markup = keyboard)
	except Exception as e:
		print "Could not send message. error = {error}".format(error=e)
	
def send_question(user_id, question_no):
	if question_no < len(questions):
		question_data = questions[question_no]
		question = question_data.get('question')
		choices = question_data.get('choices')
		send(user_id, question, choices)
		
		payload = {
					'user_id': user_id, 
					'question': question,
					'choices': choices,
					'question_no': question_no
				}
		db.insert('sent', payload)
	else:
	 	send(user_id, "Thank You!!!")

def send_response(user_id, question_no):
	send_question(user_id, question_no)
	

def get_latest_question_sent(user_id):
	question_data = db.find('sent', {'user_id': user_id})
	try:
		question_no = question_data[0]['question_no']
	except Exception:
		question_no = -1
	return question_no


def get_latest_update_id():
	docs = db.find('recieved', {})
	try:
		update_id = docs[0]['update_id']
	except Exception:
		update_id = None
	return update_id


def callback():
	update_id = get_latest_update_id()
	if update_id is not None:
		offset = update_id+1
	else:
		offset = None
	try:
		message_list = bot.getUpdates(offset=offset)
		print  offset, len(message_list), message_list[-1].__dict__['update_id']
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)

	for message in message_list:
		message_dict = dict(( key, message.message.__dict__[key]) for key in \
		 ('date', 'text'))
		message_dict['user_id'] = message.message.__dict__['from_user'].id
		question_no = get_latest_question_sent(message_dict['user_id'])
		message_dict.update({'question_no': question_no, 'update_id': \
			message.__dict__['update_id']})
		db.insert('recieved', message_dict)
		send_response(message_dict['user_id'], question_no+1)
	
if __name__ == '__main__':
	while True:
		callback()
		