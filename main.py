import requests
import time
from config import token, base_url
from questions import questions
import json
from db_helper import Database

db = Database('messages')
	
def send(user_id, message, choices=None):
	url = base_url.format(token=token, method="sendMessage")
	params = {
				'chat_id': user_id, 
				'text': message
			}
	if choices is not None:
		params.update({
			 			'reply_markup': json.dumps({'keyboard': [[item] for item in choices]})
					  	})
	else:
		params.update({
			 			'reply_markup': json.dumps({'hide_keyboard': True})
					  	})
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not send message. error = {error}".format(error=e)


def send_question(user_id, question_no):
	if question_no == -2:
		message = "Hi there. You have answered {q_no} questions".format(q_no=get_latest_question_answered(user_id)+1)
		send(user_id, message)
	elif question_no == -3:
		print 'Hi'
		send(user_id, "Check back later for more questions. Type info to know about your progress information.")
	elif question_no < len(questions):
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
		send(user_id, "Thank You!!! Type info to know about your progress information.")
	

def send_response(user_id, question_no):
	send_question(user_id, question_no)


def get_latest_question_answered(user_id):
	question_data = db.find('recieved', {'message.chat.id': user_id, 'question_no': {'$exists': True}})
	try:
		question_no = question_data[0]['question_no']
	except Exception:
		question_no = -1
	return question_no


def get_latest_question_sent(user_id):
	question_data = db.find('sent', {'user_id': user_id, 'question_no': {'$exists': True}})
	try:
		question_no = question_data[0]['question_no']
	except Exception:
		question_no = -1
	return question_no


def get_latest_update_id():
	docs = db.find('recieved', {})
	try:
		update_id = docs[0]['update_id'] + 1
	except Exception:
		update_id = None
	return update_id


def callback():
	update_id = get_latest_update_id()

	url = base_url.format(token=token, method="getUpdates")
	params = {'offset': update_id}
	
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)
	
	if response is not None:
		message_list = response["result"]
		for message in message_list:
			user_id = message['message']['from']['id']
			if message['message']['text'] == 'info':
				send_response(user_id, -2)
			else:
				question_no = get_latest_question_sent(user_id)
				answered_q_no = get_latest_question_answered(user_id)
				if question_no < 0:
					send_response(user_id, 0)
				elif question_no != answered_q_no and message['message']['text'] in questions[question_no]['choices']:
					message.update({'question_no': question_no})
					send_response(user_id, question_no+1)
				elif question_no > answered_q_no:
					pass
				else:
					send_response(user_id, -3)
			db.insert('recieved', message)

if __name__ == '__main__':
	while True:
		callback()
		