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


def get_message(question_no, user_id):
	if question_no == -2:
		message = "Hi there. You have answered {q_no} questions".format(q_no=get_latest_question_answered(user_id)+1)
	elif question_no == -3:
		message = "Check back later for more questions. Type info to know about your progress information."
	elif question_no >= len(questions):
		message = "Thank You!!! Type info to know about your progress information."
	else:
		message = None
	return message


def send_response(user_id, question_no):
	message = get_message(question_no, user_id)
	if message is not None:
		send(user_id, message)
	else:
		send_question(user_id, question_no)


def get_latest_question(user_id, collection):
	question_data = db.find(collection, {'user_id': user_id, 'question_no': {'$exists': True}})
	try:
		question_no = question_data[0]['question_no']
	except Exception:
		question_no = -1
	return question_no


def get_latest_question_answered(user_id):
	return get_latest_question(user_id, 'received')


def get_latest_question_sent(user_id):
	return get_latest_question(user_id, 'sent')


def get_next_update_id():
	docs = db.find('received', {})
	try:
		update_id = docs[0]['update_id'] + 1
	except Exception:
		update_id = None
	return update_id



def is_command(message_dict):
	return message_dict['text'].lower() == 'info'


def non_command_response(message_dict, user_id, latest_q_no_sent, latest_q_no_answered):
	if latest_q_no_sent < 0:
		send_response(user_id, 0)
	elif latest_q_no_sent > latest_q_no_answered:
		if message_dict['text'] in questions[latest_q_no_sent]['choices']:
			message_dict.update({'question_no': latest_q_no_sent})
			send_response(user_id, latest_q_no_sent+1)
	else:
		send_response(user_id, -3)
	return message_dict


def send_appropriate_response(message_dict):
	user_id = message_dict['user_id']
	if is_command(message_dict):
		send_response(user_id, -2)
	else:
		latest_q_no_sent = get_latest_question_sent(user_id)
		latest_q_no_answered = get_latest_question_answered(user_id)
		non_command_response(message_dict, user_id, latest_q_no_sent, latest_q_no_answered)
	db.insert('received', message_dict)


def process_received_messages(message_list):
	for message in message_list:
		message_dict = dict(( key, message.message.__dict__[key]) for key in ('date', 'text'))
		message_dict.update({'update_id': message.__dict__['update_id'],
								'user_id': message.message.__dict__['from_user'].id})
		send_appropriate_response(message_dict)


def callback():
	offset = get_next_update_id()
	try:
		message_list = bot.getUpdates(offset=offset)
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)
	process_received_messages(message_list)
	
		
if __name__ == '__main__':
	while True:
		callback()
		