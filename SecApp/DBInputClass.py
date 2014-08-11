from SecApp.DBBaseClass import DayEntry
from SecApp.DateClass import getTimeStamp
from SecApp.ConfigClass import AppConfig
from SecApp.DBQuestionClass import SecuQ


import salsa20 
import marshal
from CodernityDB.hash_index import UniqueHashIndex
from CodernityDB.storage import Storage
from CodernityDB.database import Database
from CodernityDB.database import RecordNotFound


class SecuIn:
	'''
	Handles all data input into the database

	'''
	def __init__(self,passkey):
		self.key = passkey


		self.initQuestions = SecuQ(self.key)

		self.DBConfig = AppConfig()
		self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']

		self.db = Database(self.dbName)


		initDay = DayEntry(self.key) # checks day hash or creates a new one
		self.dayKey = initDay.dayKey



	def questionDataIN(self,data):
	
		'''
		Data IN:
		{'a' : 2, 'b': 14 , 'c': 11, 'd': 43, 'note' : 'hello'}
	
		or
	
		{ 'b': 14 , 'c': 11, 'd': 43, 'note' : 'hello'} 
		 some entries may be missing
	
	
		Data OUT: (NEVER DELETE ANYTIHNG :) )
	
		{'date' : xx , _id: ###date2### , 'a':{'xxdate3xx':2},
						'b':{'xxdate3xx':14},
						'c':{'xxdate3xx':11},
						'note':{'xxdate3xx':'you'}}
	
	
		{'date' : xx , _id: ###date1### , 'a':{'xxdate1xx':1,'xxdate2xx':2},
						'b':{'xxdate1xx':14,'xxdate2xx':14},
						'c':{'xxdate1xx':11,'xxdate2xx':11},
						'note':{'xxdate2xx':'hello','xxdate3xx':'you'}
	
	
		'''


		timeIN = getTimeStamp() #get now time
		#initialize new questions
		
	
		# get data, as doc {'date':'xx/xx/xxTxx:xx:xxxx','question1':'x','question2':'x'}, same as dic format

		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			dayrow = self.db.get('id', self.dayKey, with_doc=True)
	
			#this function assumes database already opened
			# this is gonna be a tuple that is inserted directly

	
			#convert data from javasript to python dict/json
			# if (type(data) is str):
			dataIN=eval(data) #{ 'b': 14 , 'c': 11, 'd': 43, 'note' : 'hello'}
			datachanged = dataIN.keys()





			for question in datachanged:
				try:
					dayrow[question][timeIN] = dataIN[question]
				except KeyError: #first write to key, initiate
					dayrow[question] = {}
					dayrow[question][timeIN] = dataIN[question]

			

			self.db.update(dayrow) 
			self.db.close()
			self.initQuestions.questionsValidate(datachanged) #insert questions whos data had changed

			#if all ok!
			return True



