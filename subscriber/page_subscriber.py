from google.cloud import pubsub_v1
from unidecode import unidecode
from bs4 import BeautifulSoup
import requests
import configparser
import time

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('osrs-xp-tracker', 'users')

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    'osrs-xp-tracker', 'test')

def get_content(url):
	url = url.data.decode('utf-8')
	raw = requests.get(url).text
	soup = BeautifulSoup(raw, 'html.parser')
	for row in soup.find_all('tr',{'class':'personal-hiscores__row'}):
		cols = [unidecode(x.text.strip()) for x in row.find_all('td')]
		cols = [x.replace(',','') for x in cols]	
		
		data = u'{}'.format(cols[1])
		data = data.encode('utf-8')	
		publisher.publish(topic_path, data=data)
		print('Published message.')	
	time.sleep(5)	

def callback(message):
    get_content(message)
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)