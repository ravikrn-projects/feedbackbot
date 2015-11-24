import requests
from config import token, base_url
from questions import questions
import json


def send(user_id, message):
	url = base_url.format(token=token, method="sendMessage")
	message = message.split('\n')
	keyboard_message = json.dumps({'keyboard': [[item] for item in message[1:]]})
	params = {'chat_id': user_id, 'text': message[0], 
	'reply_markup': keyboard_message}
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not send message. error = {error}".format(error=e)
	

def send_question(user_id, question_no):

	if question_no < len(questions):
		question_data = questions[question_no]
		message = question_data.get('question')
		choices = question_data.get('choices')
		for choice in choices:
			message += "\n" + choice
		send(user_id, message)


def send_response(user_id, question_no):
	print question_no
	send_question(user_id, question_no)
	return question_no+1
	

def callback(update_id, question_no):
	url = base_url.format(token=token, method="getUpdates")
	params = {'offset': update_id}
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)
	
	message_list = response["result"]
	if len(message_list) != 0:
		for message in message_list:
			# print message['update_id'], message['message']['text']
			question_no = send_response(message['message']['from']['id'], question_no)
		update_id = message_list[-1]['update_id']
	return update_id, question_no


if __name__ == '__main__':
	update_id = None
	question_no = 0
	while True:
		pre_update_id, pre_question_no = callback(update_id, question_no)
		if pre_update_id is not None:
			update_id = pre_update_id + 1
			question_no = pre_question_no