import requests
from config import token, base_url


def callback():
	url = base_url.format(token=token, method="getUpdates")
	params = {}
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		print "Could not get updates. error = {error}".format(error=e)
	finally:
		message_list = response["result"]
		for message in message_list:
			print message['update_id'], message['message']['text']



if __name__ == '__main__':
	callback()