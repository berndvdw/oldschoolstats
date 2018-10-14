from google.cloud import pubsub_v1
from unidecode import unidecode
import requests
import configparser
import time

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    'osrs-xp-tracker', 'users')

config = configparser.ConfigParser()
config.read('config.ini') # adjust this to open with OS

def get_user(user,type='normal'):
	url = "https://secure.runescape.com/m={}/index_lite.ws?player={}".format(
			config.get("types","normal"),
			user.data.decode('utf-8')
		)
	data = requests.get(url).text
	print(data)
	time.sleep(1)	

def callback(message):
    get_user(message)
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)