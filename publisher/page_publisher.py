from google.cloud import pubsub_v1
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('osrs-xp-tracker', 'osrs')

base_url = "https://secure.runescape.com/m=hiscore_oldschool/overall.ws?table=0&page={}"
users = 25
page_amount = 25

for n in range(1, int(users/page_amount)+1):
	data = u'{}'.format(base_url.format(n))
	data = data.encode('utf-8')
	publisher.publish(topic_path, data=data)

print('Published {} messages'.format(n))