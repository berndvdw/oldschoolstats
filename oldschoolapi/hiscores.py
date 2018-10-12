import requests
import configparser
from unidecode import unidecode
from bs4 import BeautifulSoup

class Hiscores:

	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('config.ini') # adjust this to open with OS
		self.base_url = self.config.get('api', 'base_url')
	
	def getHiscorePage(self, url):
		url = "{}{}/overall.ws?table=0&page={}".format(
				self.base_url,
				self.config.get('types', 'normal'),
				offset
			)
		
		raw = requests.get(url).text
		soup = BeautifulSoup(raw, 'html.parser')
		for row in soup.find_all('tr',{'class':'personal-hiscores__row'}):
			cols = [unidecode(x.text.strip()) for x in row.find_all('td')]
			cols = [x.replace(',','') for x in cols]
			print(cols)

	def getUser(self,name,type='normal'):
		pass