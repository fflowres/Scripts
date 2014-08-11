from SecApp.DBBaseClass import DBIndexSystem

import salsa20 
import marshal
from CodernityDB.hash_index import UniqueHashIndex
from CodernityDB.storage import Storage
from CodernityDB.database import Database
from CodernityDB.database import RecordNotFound

class SecuQ:
	'''
	Abstract:
	Handles all Questions, input and output input into the database





	def questionGet(self):

		- reloads all question database attributes



	def questionInsert(self,data,descriptor='inclusive'):
		-> data = input question dict
				ex: 

				'a':{'active':'True','typ':'slider','range':'0-100','aggregate':True, 'multipoint':True}, ,,,,.................

		- inclusive = Updates entried (overwrites) (safe)
		- exclusive = deletes all entried not in input (dangerous)

	def questionsValidate(self,data):
		-> data = input list of questions [(keys)]

		each question verified, if not initiated, will be initiated after


	'''
	def __init__(self,passkey):
		self.key = passkey
		self.indexdb = DBIndexSystem(self.key)
		#self.indexdb.masterIndex
		#self.indexdb.Qindex
		#self.indexdb.Tindex
		#self.indexdb.IndexedTable
		#self.indexdb.dbName
		

		self.db = Database(self.indexdb.dbName)
		

		#init variables blank, avoid key errors
		self.all = {}
		self.valid = {}
		self.active = {}
		self.notactive = {}
		self.unInit = {}
		self.typ = {}
		self.aggregate = {}
		self.multipoint = {}

		self.questionGet() #populate variables



	#query: all , valid, true,unInit, false, inline
	def questionGet(self): #the passkey in question should be loaded from config or index passkey


		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key

			#select Qindex
			Qindex = self.db.get('id', self.indexdb.Qindex, with_doc=True)
	
	
			oQ = Qindex.copy()
			# delete unnessesary to modify
			# if u use del <key> it deletes all instances in all variables using same reference to dict
			oQ.pop('_rev', None)
			oQ.pop('_id', None)
			oQ.pop('t', None)
			#oQ.pop('questions', None)
			#returns list in string for of all keys aka the question and metadata
	
			#step through and assign

			questionsSet = oQ.keys()

			for question in questionsSet:

				
				self.all[question] = oQ[question]

				if oQ[question]['active'] == 'True':
					self.active[question] = oQ[question]



				
				if oQ[question]['active'] == 'unInit':
					self.unInit[question] = oQ[question]

				
				if (oQ[question]['active'] == 'unInit') | (oQ[question]['active'] == 'True'):
					self.valid[question] = oQ[question]


				
				if oQ[question]['active'] == 'False':
					self.notactive[question] = oQ[question]



				
				if oQ[question]['typ'] == 'note':
					self.typ[question] = oQ[question]


				try:
					if oQ[question]['aggregate'] == 'True':
						self.aggregate[question] = oQ[question]
				except KeyError:
					pass
	
				try:
					
					if oQ[question]['multipoint'] == 'True':
						self.multipoint[question] = oQ[question]
				except KeyError:
					pass

			self.db.close()

	
			return True 

			'''
			Qinfo=
			{
			'a':{'active':'True','typ':'slider','range':'0-100','aggregate':True, 'multipoint':True},
			
			'b':{'active':'True','typ':'slider','range':'0-100','aggregate':True, 'multipoint':False},
			
			'c':{'active':'True','typ':'slider','range':'0-100','aggregate':False, 'multipoint':True},
			
			'd':{'active':'True','typ':'slider','range':'0-100','aggregate':False, 'multipoint':False},
			
			'note':{'active':'True','typ':'note', 'multipoint':"False"}
			}
			'''


	def questionInsert(self,data,descriptor='inclusive'):# this will be a class later for ... infinite data

	
	
	
		
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			#select Qindex
			Qindex = self.db.get('id', self.indexdb.Qindex, with_doc=True)
	
			#must copy in this way for dictionaries or else all references are affected
			oQ= Qindex.copy()
			# delete unnessesary to modify
			# if u use del <key> it deletes all instances in all variables using same reference to dict
			oQ.pop('_rev', None)
			oQ.pop('_id', None)
			oQ.pop('t', None)
			oQ.pop('questions', None)
	
			# if (type(data) is str):
			nQL=eval(str(data))
	
	

	
			if (descriptor == "exclusive"):
			 #exclusive, new data always overwrites old data, deletes any data that is not new
			 # remmove old keys from row
				for key in oQ.keys(): #removes keys not in entry and overwrites everything
					if key not in nQL.keys():
						Qindex.pop(key,None)

	
			if (descriptor == "inclusive"): 
				#only overwrites data, keeps old data that is unnaffected
				pass
	
	
			#oQ.update(nQL) # update existing keys to be written
	
			
			Qindex.update(nQL) #updates existing keys in row
	
			self.db.update(Qindex) #updates NoSQL
			self.db.close()
			self.questionGet()
			return True
		else:
			print ('CANNOT LOAD self.db')
			return False
	
	
	
	def questionsValidate(self,data): #turns all uesd questions true, insert list of questions

		for question in data:
			if question in self.unInit.keys():
				updated = {}
				updated[question] = self.unInit[question]
				updated[question]['active'] = "True"
				self.questionInsert(str(updated),"inclusive")

		#update class variables
		self.questionGet()
	
		return True
	

	

		



