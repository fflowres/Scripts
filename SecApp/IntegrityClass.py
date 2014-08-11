from SecApp.ConfigClass import AppConfig
from SecApp.IOClass import AppIO
from SecApp.IOClass import DeviceDetection

import os


class Integrity:

	def __init__(self): #if you want to add analysis database

		self.configFileName='configs/seccuConfig.ini'
		self.DBConfig = AppConfig()

		if (DeviceDetection().embeddedapp): #if embedded
			import sys
			sys.path = ['/pythonHome/Lib','/pythonHome/','/pythonHome','.','/Lib','/pythonHome/system']


	#def detectdb



	def checkReal(self):
		if(os.path.isfile(self.configFileName)):
			try:
				self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']
				pass
				#then try and read master index and compare against version in config file
	
			except ConfigParser.NoSectionError:
				AppIO('False')   
				return False
				
			if(self.dbName==None): #not empty
				AppIO('False')   
				return False
			try:
				os.path.exists(self.dbName)
				AppIO('True')
				return True
	
			except UnboundLocalError:
				AppIO('False')			
				return False
				
		else:
			AppIO('False')   
			return False

	def checkExists(self):
		if(os.path.isfile(self.configFileName)):
			try:
				self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']
				#then try and read master index and compare against version in config file
				
			except NoSectionError:
				return False
				
			if(self.dbName==None): #not empty
				return False

			try:
				os.path.exists(self.dbName)
				return True
	
			except UnboundLocalError:		  
				return False
				
		else:
			return False