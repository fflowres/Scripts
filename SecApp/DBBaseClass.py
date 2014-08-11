from SecApp.ConfigClass import AppConfig
from SecApp.IOClass import AppIO
from SecApp.IntegrityClass import Integrity
from SecApp.DateClass import getDayStart


import salsa20 
import marshal
from CodernityDB.hash_index import UniqueHashIndex
from CodernityDB.storage import Storage
from CodernityDB.database import Database
from CodernityDB.database import RecordNotFound

class DBSubsystem:
	'''
	import scan: scans existing self.db and rebuilds config file 
	create self.db: creates self.db file, master index, question index and table index



	'''




	def __init__(self,passkey,xtraDB=None):
		self.DATABASE_SOFTWARE_VERSION ="0.3.1a"
		self.key = passkey
		self.DBConfig = AppConfig()
		self.dbval = xtraDB
		
	def __del__(self):
		if (self.db.opened):
			self.db.close()

# ADD REBUILD OPTION

	def createDB(self):
		if (self.creationCheck()):
			self.buildDB()
			return True
		else:
			return False

	def creationCheck(self):
		if (Integrity().checkExists() == False):
			if (self.dbval != None):
				self.DBConfig.createConfig()
				self.DBConfig.putmap('databaseinfo','databasename',self.dbval)

				self.dbName = self.dbval

				return True
			else:
				return False

		else: #if integrity passed as ok existing
			return False
	





	def buildDB(self):
	
		from _dbindex import EncUniqueHashIndex
		self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']

		self.db = Database(self.dbName)
		id_ind = EncUniqueHashIndex(self.db.path, 'id')
		self.db.set_indexes([id_ind])
		self.db.create()
		self.db.id_ind.enc_key = self.key
		self.db.close()

		self.createMasterindex() #create master index passkey, only once
		self.createQindex()
		self.createTindex()
		
		#add error handling
		return True
	
		'''
		@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	
		Index Creation
	
		@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	
		'''
	
	def createMasterindex(self):
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
	#this function assumes database
		self.db.insert(dict(t='master',Qindex=None,Tindex=None,DBVersion=self.DATABASE_SOFTWARE_VERSION))
	
	
		for curr in self.db.all('id'): #since first passkey in self.db should be only one there, function only perfomed once
			if curr['t'] == 'master':
				self.masterIndex=''.join(curr['_id'])
				self.DBConfig.putmap('databaseinfo','indexkey', self.masterIndex )#masterkey=value
				break
	
				#add else statement for errors if couldnt be written for found
	
			
		self.db.close()
		return self.masterIndex
	
	
	def createQindex(self):
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
	#this function assumes database
	#insert question index
	
		self.db.insert(dict(t='Qindex'))
	#get question index passkey, form type qintex (t=xxxx)
		for curr in self.db.all('id'): #since first passkey in self.db should be only one there, function only perfomed once
			if curr['t'] == 'Qindex':
				self.Qindexkey=''.join(curr['_id'])
				break
	
				#add else statement for errors if couldnt be written for found
	
				#write Qindex passkey to master index
	
		indexRow = self.db.get('id', self.masterIndex, with_doc=True)
	
		#write question index passkey to master index
		
		indexRow['Qindex']=self.Qindexkey
		self.db.update(indexRow)
		self.db.close()
	#wrote new Qindex passkey to master index passkey
	
	
	
	def createTindex(self):
		
	
		self.dbName=self.DBConfig.mapget('databaseinfo')['databasename']
		self.masterIndex=self.DBConfig.mapget('databaseinfo')['indexkey']
	
		self.db=Database(self.dbName)
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
	#this function assumes database
	#insert question index
	
		self.db.insert(dict(t='Tindex',table=[]))
	#get question index passkey, form type qintex (t=xxxx)
		for curr in self.db.all('id'): #since first passkey in self.db should be only one there, function only perfomed once
			if curr['t'] == 'Tindex':
				self.Tindexkey =''.join(curr['_id'])
				break
	
				#add else statement for errors if couldnt be written for found
	
				#write Qindex passkey to master index
	
		indexRow = self.db.get('id', self.masterIndex, with_doc=True)
	
		#write question index passkey to master index
	
		indexRow['Tindex']=self.Tindexkey
		self.db.update(indexRow)
		self.db.close()
	#wrote new Qindex passkey to master index passkey



	'''
	@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

	Index Queries

	@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

	'''



class DBIndexSystem:
	'''
	QindexGet: 
		-- Get the question index key


		Allows for simple calling to database variables

		ex:

	self.indexdb = DBIndexSystem()
		#self.indexdb.masterIndex
		#self.indexdb.Qindex
		#self.indexdb.Tindex
		#self.indexdb.IndexedTable
		#self.indexdb.dbName

	'''

	def __init__(self,passkey):
		self.key=passkey



		self.DBConfig = AppConfig()
		#check for self.db stuff
		#IF IT DOESNT PASS THESE TESTS
		#warn before deletion
		self.dbName=self.DBConfig.mapget('databaseinfo')['databasename']

		self.masterIndex=self.DBConfig.mapget('databaseinfo')['indexkey']

		self.db = Database(self.dbName)

		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			try:
				self.Qindex = self.QindexGet() #question index key
				self.Tindex = self.TindexGet()  #table index key
				self.IndexedTable = self.tableGet() #regular 'table' index. list of hash pointers in order 

			except:
				print 'bad index'
				self.db.close()
				self.sanitycheck = False
				
			else:
				self.db.close()
				self.sanitycheck = True

	def __del__(self):
		if (self.db.opened):
			self.db.close()


	def QindexGet(self):
		masterRow = self.db.get('id', self.masterIndex, with_doc=True)
		Qindexkey=masterRow['Qindex']
		return Qindexkey # questions as [a,b,c,d,e,f,g,h,i]
		#add try if line not found, your self.db is totally fucked eh
	
	def TindexGet(self,tableName='Tindex'):
		masterRow = self.db.get('id', self.masterIndex, with_doc=True)
		Tindexkey = masterRow[tableName]
		return Tindexkey # questions as [a,b,c,d,e,f,g,h,i]
		#add try if line not found, your self.db is totally fucked eh


	def tableGet(self,tableName='Tindex'): #the self.key in question should be loaded from config or index self.key
		Tindexkey = self.TindexGet(tableName) #not self variable because this may be a custom table
		Tindex = self.db.get('id', Tindexkey, with_doc=True)
		return Tindex['table'] # table entries as as [######,######,######,######,######,]
	
	
	def TindexPut(self,data,tableName='Tindex'): #enter ordered hash data into table
		
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			Tindexkey = self.TindexGet(tableName)
			TindexRow = self.db.get('id', Tindexkey, with_doc=True)
			try:
				TindexRow['table'].append(data)
			except KeyError:
				TindexRow['table']=[]
				TindexRow['table'].append(data)
			self.db.update(TindexRow)
			self.db.close()
	
			#append net entry to current table array
			
			#write table array to same index key
			return True 

	def selectrow(self,idIN):
	#check if already open
		if(self.db.exists()):
			if(self.db.opened == False):
				self.db.open()
				self.db.id_ind.enc_key = self.key
				#select Qindex
				data = self.db.get('id', idIN, with_doc=True)
				self.db.close()
				return data
			else:
				data = self.db.get('id', idIN, with_doc=True)
				return data
			



	def updaterow(self,data):

		if(self.db.exists()):
			if(self.db.opened == False):
				self.db.open()
				self.db.id_ind.enc_key = self.key
				self.db.update(data) #must include _id, must be dict/json
				self.db.close()
				return True
			else:
				self.db.update(data) #must include _id, must be dict/json
				return True

	
	
	
	
	
class DayEntry: #checker class
	'''
	checks day hash or creates a new one


	once instatiated, it checks for:
		- if day key in config coincideds with todays date
		- if there isnt a date in config, it scans database for the one matching todays
		- if no date in conifig, or it's the wrong date, new row is made (only if there isnt one with matching date in the entire self.db)
	'''

	def __init__(self,passkey):
		self.todayDate = str(getDayStart())
		self.key = passkey
		
		self.DBConfig = AppConfig()

		self.dayKey = None # setup befpore checking, avoid attribute error
		self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']
		self.db = Database(self.dbName)
		
		try:
			self.dayKey = self.DBConfig.mapget('databaseinfo')['daykey']
		except KeyError: # if notthin in config, check self.db for entry
			daystatus = self.checkfordate()
			if (daystatus == False):
				self.makeDayRow()
				self.DBConfig.putmap('databaseinfo','daykey', self.dayKey)
			#if true do nothing, config file fixed
		else:

			daystatus = self.checkfordate() #if false, scans for right one, and fixes config

			oldcompare = self.dayKey 
			self.dayKey = self.DBConfig.mapget('databaseinfo')['daykey']
			if (daystatus == False) & (oldcompare == self.dayKey):
				self.makeDayRow()
				self.DBConfig.putmap('databaseinfo','daykey', self.dayKey)
			if (daystatus == True): #everything all good
				pass #nothing created just a check

		
	def __del__(self):
		if (self.db.opened):
			self.db.close()



	def makeDayRow(self):
	
		
		if (self.checkfordate()==True): #already exists no need to write
			return False
		
		dbindex = DBIndexSystem(self.key)

		dayrow = {}
		dayrow["date"] = self.todayDate
		if(self.db.exists() == True):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			self.db.insert(dayrow)
			self.db.close()#must close first , no double opens
			self.getDayRowID() # resfresh day key
			dbindex.TindexPut(self.dayKey)
			## would normally write to config file
			return True


	def getDayRowID(self): #gets row id by date
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			for curr in self.db.all('id'):
				try:
					if curr['date'] == str(self.todayDate):
						dataop = curr['_id']
						dataop = "".join(dataop)  #_id is returned as a list of charaters, must be concatenated to string
						self.db.close()
						self.dayKey = dataop
						return dataop #returns datestring
				except KeyError:
					continue
					
					#break
			#if it makes it here, entry doesnt exist
			self.db.close()
			return False #there is a probplem

	def checkfordate(self): #checks for existance of that date in self.db
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			if (self.dayKey != None):
				dayrow = self.db.get('id', self.dayKey, with_doc=True)
				#doesnt account for if there is an entry in the config that doesnt exist
				if dayrow['date'] == str(self.todayDate):
					self.db.close()
					return True
			for curr in self.db.all('id'): #try to search
				try:
					if curr['date'] == str(self.todayDate):
						self.DBConfig.putmap('databaseinfo','daykey', "".join(curr['_id'])) #fix lost entry
						self.db.close()
						return False
				except KeyError:
					continue
					
					#break
			#if it makes it here, entry doesnt exist and nothing was remapped
			self.db.close()
			return False

class Developer:
	def __init__(self,passkey,dbname=None):
		self.key=passkey
		if (dbname ==None):
			self.DBConfig = AppConfig()
			self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']
		else:
			self.dbName = dbname
		self.db = Database(self.dbName)
	def dump(self):
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			for curr in self.db.all('id'):
				print curr

			self.db.close()
