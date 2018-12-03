import requests
import configparser
import os
from collections import namedtuple
from unidecode import unidecode
from bs4 import BeautifulSoup

class Hiscores:

	def __init__(self):
		config_file = os.path.join(os.path.dirname(__file__),'config.ini')
		print(config_file)
		self.config = configparser.ConfigParser()
		self.config.read(config_file) # adjust this to open with OS
		
		self.base_url = self.config.get('api', 'base_url')
		self.skills = self.config.get('data_format','skills').split(',')
		self.metrics = self.config.get('data_format','hierachy_skills').split(',')
	
	def getHiscorePage(self, user_type='normal', offset=0):
		url = "{}{}/overall.ws?table=0&page={}".format(
				self.base_url,
				self.config.get('types', user_type),
				offset
			)
		
		player = namedtuple('User', ['rank','displayname','level','xp'])
		players = []
		raw = requests.get(url).text
		soup = BeautifulSoup(raw, 'html.parser')
		for row in soup.find_all('tr',{'class':'personal-hiscores__row'}):
			cols = [unidecode(x.text.strip()) for x in row.find_all('td')]
			cols = [x.replace(',','') for x in cols]
			cols = [int(col) if cols.index(col) in [0,2,3] else col for col in cols]
			players.append(player(*cols))
		return players

	def getUser(self,displayname,user_type='normal'):
		url = "{}{}/{}?player={}".format(
			self.base_url,
			self.config.get('types', user_type),
			self.config.get('api','endpoint'),
			displayname
			)
		data = requests.get(url.format(displayname)).text.split('\n')
		
		obj = {}
		for i,skill in enumerate(self.skills):
			obj[skill] = {}
			skill_data = data[i].split(",")
			for c, part in enumerate(self.metrics):
				obj[skill][part] = int(skill_data[c])
		return {displayname: obj}

test = Hiscores()