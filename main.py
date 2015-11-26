import requests
import time
import text_message
from config import token, base_url
import json
from db_helper import Database
import telegram
db = Database('messages')
bot = telegram.Bot(token)
	

def send(user_id, text=None, choices=None, custom_message=None):
	if custom_message is not None:
		text = eval('text_message.'+custom_message)	
	if choices is not None:
		keyboard = json.dumps({'keyboard': [[item] for item in choices]})				
	elif custom_message == 'onboarding_message':
		keyboard = json.dumps({'keyboard': [['Yup', 'Nope']]})	  	
	else:
		keyboard = json.dumps({'hide_keyboard': True})
	try:
		bot.sendMessage(user_id, text, reply_markup = keyboard)
	except Exception as e:
		print "Could not send message. error = {error}".format(error=e)

def send_question(user_id, question_no = None, remark = None):
	if remark is not None:
		question,choices = remark, ["Yup", "Nope"]
		question_no = 0
	else:
		question_data = text_message.questions[question_no]
		question = text_message.reward.format(reward=20*(get_latest_question_sent(user_id)+1))
		question = question+question_data.get('question')
		choices = question_data.get('choices')
		payload = {
				'user_id': user_id, 
				'question': question,
				'choices': choices,
				'question_no': question_no
			}
		db.insert('sent', payload)
	send(user_id, question, choices)

def send_response(user_id, response):
	if 'remark' in response:
		q_no = get_latest_question_sent(user_id)+1
		message = eval('text_message.'+response['remark']).format(q_no=q_no, reward=20*q_no)
	elif ('question_no' in response) and response['question_no'] >= len(text_message.questions):
		message = text_message.thanks
	else:
		message = None

	if message is None and 'question_no' in response:
		send_question(user_id, question_no = response['question_no'])
	elif response.values()[0] == 'declined':
		send_question(user_id, remark = message)
	else:
		send(user_id, message)

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
		send_response(user_id, {'question_no':0})
	elif latest_q_no_sent > latest_q_no_answered:
		if message_dict['text'] in text_message.questions[latest_q_no_sent]['choices']:
			message_dict.update({'question_no': latest_q_no_sent})
			send_response(user_id, {'question_no':latest_q_no_sent+1})
	else:
		send_response(user_id, {'remark':'completed'})
	return message_dict


def send_appropriate_response(message_dict):
	user_id = message_dict['user_id']
	if message_dict['text'] == '/start':
		send(user_id, custom_message='onboarding_message')
	elif (get_latest_question_sent(user_id) == -1) and \
		(message_dict['text'].lower() != 'yup'):
		send_response(user_id, {'remark':'declined'})
	elif is_command(message_dict):
		send_response(user_id, {'remark':'info'})
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
		