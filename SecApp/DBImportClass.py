from SecApp.ConfigClass import AppConfig
import salsa20 
import marshal
from CodernityDB.hash_index import UniqueHashIndex
from CodernityDB.storage import Storage
from CodernityDB.database import Database
from CodernityDB.database import RecordNotFound

class DBImport:
	'''
	import scan: scans existing self.db and rebuilds config file 
	create self.db: creates self.db file, master index, question index and table index



	'''




	def __init__(self,passkey,xtraDB):
		self.key = passkey
		



		
		self.dbName = xtraDB
		self.db=Database(self.dbName)
		
		self.importScan()

	def __del__(self):
		if (self.db.opened):
			self.db.close()

# ADD REBUILD OPTION



	def importScan(self):

		
		#read from config, as a check
		
		self.db=Database(self.dbName)
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
	
			for curr in self.db.all('id'): #since first passkey in self.db should be only one there, function only perfomed once
				if curr['t'] == 'master':
					masterKey=''.join(curr['_id'])
					self.DBConfig = AppConfig()
					self.DBConfig.putmap('databaseinfo','indexkey',masterKey)#masterkey=value
					self.DBConfig.putmap('databaseinfo','databasename',self.dbName)
					break
					#add else statement for errors if couldnt be written for found
			self.db.close()
		return True
