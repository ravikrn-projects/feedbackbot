import requests
from config import token, base_url

def send_response(user_id):
	message = "What's up?"
	url = base_url.format(token=token, method="sendMessage")
	params = {'chat_id': user_id, 'text': message}
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not send message. error = {error}".format(error=e)
	

def callback(update_id):
	url = base_url.format(token=token, method="getUpdates")
	params = {'offset': update_id}
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)
	
	message_list = response["result"]
	if len(message_list) != 0:
		for message in message_list:
			print message['update_id'], message['message']['text']
			send_response(message['message']['from']['id'])
		update_id = message_list[-1]['update_id']
	return update_id

if __name__ == '__main__':
	update_id = None
	while True:
		previous_update_id = callback(update_id)
		if previous_update_id is not None:
			update_id = previous_update_id + 1