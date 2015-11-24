import requests
from config import token, base_url
from questions import questions
import json
from db_helper import Database
import telegram
db = Database('messages')
bot = telegram.Bot(token)
	
def send(user_id, message):
	message = message.split('\n')
	keyboard_message = json.dumps({'keyboard': [[item] for item in message[1:]]})
	try:
		bot.sendMessage(user_id, message[0], reply_markup = keyboard_message)
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
		payload = {
					'user_id': user_id, 
					'message': message,
					'question_no': question_no
				}
		db.insert('sent', payload)

def send_response(user_id, question_no):
	send_question(user_id, question_no)
	return question_no+1
	
def callback(update_id, question_no):
	try:
		message_list = bot.getUpdates(offset=update_id)
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)
	if len(message_list) != 0:
		for message in message_list:
			message_dict = dict(( key, message.message.__dict__[key]) for key in \
			 ('date', 'text'))
			message_dict['user_id'] = message.message.__dict__['from_user'].id
			db.insert('recieved', message_dict)
			question_no = send_response(message_dict['user_id'], question_no)
		update_id = message_list[-1].update_id
	return update_id, question_no


if __name__ == '__main__':
	update_id = None
	question_no = 0

	while True:
		pre_update_id, pre_question_no = callback(update_id, question_no)
		if pre_update_id is not None:
			update_id = pre_update_id + 1
			question_no = pre_question_no