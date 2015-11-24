import requests
from config import token, base_url
from questions import questions
from db_helper import Database

db = Database('messages')
	
def send(user_id, message):
	url = base_url.format(token=token, method="sendMessage")
	params = {'chat_id': user_id, 'text': message}
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not send message. error = {error}".format(error=e)
	

def send_question(user_id, question_no):
	if question_no < len(questions):
		question_data = questions[question_no]
		message = question_data.get('question')
		choices = question_data.get('choices')
		choice_id = 'A'
		for choice in choices:
			message += "\n" + choice_id + ': ' + choice
			choice_id = chr(ord(choice_id)+1)
		send(user_id, message)
		payload = {
					'user_id': user_id, 
					'message': message,
					'question_no': question_no
				}
		db.insert('sent', payload)


def send_response(user_id, question_no):
	# print question_no
	send_question(user_id, question_no)
	return question_no+1
	

def get_latest_question_sent(user_id):
	question_data = db.find('sent', {'user_id': user_id})
	try:
		question_no = question_data[0]['question_no']
	except Exception:
		question_no = -1
	return question_no


def callback(update_id):
	url = base_url.format(token=token, method="getUpdates")
	params = {'offset': update_id}
	
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)
	
	message_list = response["result"]
	for message in message_list:
		db.insert('recieved', message)
		# print message['update_id'], message['message']['text']
		question_no = get_latest_question_sent(message['message']['from']['id']) + 1
		print question_no
		question_no = send_response(message['message']['from']['id'], question_no)
	
	if len(message_list) != 0:
		update_id = message_list[-1]['update_id']
	return update_id, question_no


if __name__ == '__main__':
	update_id = None
	
	while True:
		pre_update_id, pre_question_no = callback(update_id)
		if pre_update_id is not None:
			update_id = pre_update_id + 1
			question_no = pre_question_no
