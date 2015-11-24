import requests
import time
from config import token, base_url
from questions import questions
import json
from db_helper import Database

db = Database('messages')
	
def send(user_id, message, choices):
	url = base_url.format(token=token, method="sendMessage")
	params = {
				'chat_id': user_id, 
				'text': message, 
				'reply_markup': json.dumps({'keyboard': [[item] for item in choices]})
			}
	try:
		response = requests.get(url, params=params).json()
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
			db.insert('recieved', message)
			question_no = get_latest_question_sent(message['message']['from']['id']) + 1
			send_response(message['message']['from']['id'], question_no)
	

if __name__ == '__main__':
	while True:
		callback()
		