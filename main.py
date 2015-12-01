import config
import db_helper
import telegram
import logger
import question
import info_message

logger = logger.Logger(config.log_file, config.logging_level)
db = db_helper.Database('messages')
bot = telegram.Bot(config.token)

q_obj = question.Question(db)
info_mgs_obj = info_message.InfoMessage(db)
	

def get_reply_keyboard(choices, custom_message):
	if choices is not None:
		keyboard = telegram.ReplyKeyboardMarkup([[item] for item in choices])				
	elif custom_message == 'onboarding_message':
		keyboard = telegram.ReplyKeyboardMarkup([['Yup', 'Nope']])	  	
	else:
		keyboard = telegram.ReplyKeyboardHide()
	return keyboard


def get_text_to_send(custom_message, first_name):
	text = None
	if custom_message is not None:
		text = info_mgs_obj.get_info_message(custom_message)
		if custom_message == 'onboarding_message':
			text = text.format(name=first_name)	
	return text


def send(user_id, text=None, choices=None, custom_message=None, first_name=None):
	if text is None:
		text = get_text_to_send(custom_message, first_name)
	keyboard = get_reply_keyboard(choices, custom_message)
	try:
		bot.sendMessage(chat_id=user_id, text=text, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as e:
		logger.error("Could not send message. error = {error}".format(error=e))


def send_question(user_id, question_no = None, remark = None):
	if remark is not None:
		question, choices = remark, ["Yup", "Nope"]
		question_no = 0
	else:
		question_data = q_obj.get_question(question_no)
		question = info_mgs_obj.get_info_message('reward').format(reward=20*(q_obj.get_latest_question_sent(user_id)+1))
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


def decide_message(response, user_id):
	message = None
	if 'remark' in response:
		q_no = q_obj.get_latest_question_sent(user_id)+1
		message = info_mgs_obj.get_info_message(response['remark']).format(q_no=q_no, reward=20*q_no)
	elif ('question_no' in response) and response['question_no'] >= q_obj.get_number_of_questions():
		message = info_mgs_obj.get_info_message('thanks')
	return message


def send_coupon(response, user_id):
	if ('question_no' in response) and response['question_no'] >= q_obj.get_number_of_questions():
		bot.sendPhoto(chat_id=user_id, photo=open(config.coupon_image))


def send_response(user_id, response):
	message = decide_message(response, user_id)
	if message is None and 'question_no' in response:
		send_question(user_id, question_no = response['question_no'])
	elif response.values()[0] == 'declined':
		send_question(user_id, remark = message)
	else:
		send(user_id, message)
	send_coupon(response, user_id)


def get_next_update_id():
	docs = db.find('received', {})
	try:
		update_id = docs[0]['update_id'] + 1
	except Exception:
		update_id = None
	return update_id


def is_command(text):
	return text.lower() in config.commands


def accept_valid_choice(message_dict, latest_q_no_sent, user_id):
	if message_dict['text'] in q_obj.get_question(latest_q_no_sent)['choices']:
		message_dict.update({'question_no': latest_q_no_sent})
	return message_dict


def onboarding_message_declined(latest_q_no_sent, text):
	return (latest_q_no_sent == -1) and (text.lower() != config.ACCEPTED)


def onboarding_message_accepted(latest_q_no_sent):
	return latest_q_no_sent < 0


def chat_in_progress(latest_q_no_sent, latest_q_no_answered):
	return latest_q_no_sent > latest_q_no_answered


def non_command_response(message_dict, latest_q_no_sent, latest_q_no_answered):
	user_id = message_dict['user_id']
	if onboarding_message_declined(latest_q_no_sent, message_dict['text']):
		send_response(user_id, {'remark':'declined'})

	elif onboarding_message_accepted(latest_q_no_sent):
		send_response(user_id, {'question_no':0})
	
	elif chat_in_progress(latest_q_no_sent, latest_q_no_answered):
		message_dict = accept_valid_choice(message_dict, latest_q_no_sent, user_id)
		send_response(user_id, {'question_no':latest_q_no_sent+1})

	else:
		send_response(user_id, {'remark':'completed'})
	
	return message_dict


def command_response(message_dict):
	user_id = message_dict['user_id']
	if message_dict['text'] in config.start_commands:
		send(user_id, custom_message='onboarding_message', first_name=message_dict['first_name'])
	elif message_dict['text'] == info_command:
		send_response(user_id, {'remark':'info'})


def send_appropriate_response(message_dict):
	user_id = message_dict['user_id']
	if is_command(message_dict['text']):
		command_response(message_dict)
	else:
		latest_q_no_sent = q_obj.get_latest_question_sent(user_id)
		latest_q_no_answered = q_obj.get_latest_question_answered(user_id)
		message_dict = non_command_response(message_dict, latest_q_no_sent, latest_q_no_answered)
	db.insert('received', message_dict)
	

def process_received_messages(message_list):
	for message in message_list:
		message_dict ={
				 		'date': str(message.message['date']),
					 	'text': message.message['text'],
					 	'update_id': message['update_id'],
					 	'user_id': message.message['from_user'].id,
					 	'first_name': message.message.from_user.first_name
					}
		send_appropriate_response(message_dict)


def callback():
	offset = get_next_update_id()
	try:
		message_list = bot.getUpdates(offset=offset)
		process_received_messages(message_list)	
	except Exception as e:
		logger.error("Could not get updates. error = {error}".format(error=e))


if __name__ == '__main__':
	while True:
		callback()
		
