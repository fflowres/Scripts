from SecApp.FileHandlerClass import FileHandler
from SecApp.ConfigClass import AppConfig
from SecApp.CloudClass import CloudHandler
from SecApp.IOClass import AppIO
import socket
#ssl seed
import string
import random


class Sync:
	'''
	import scan: scans existing self.db and rebuilds config file 
	create self.db: creates self.db file, master index, question index and table index



	'''




	def __init__(self):
		self.FH = FileHandler()
		self.DBConfig = AppConfig()
		
	def ssl_seed(self,size=24, chars=string.ascii_uppercase + string.digits):
		self.randomString = ''.join(random.choice(chars) for _ in range(size))
		return self




	def getcloudselection(self):
		try:
			
			backupLocation = self.DBConfig.mapget('cloudinfo')['location']
			validlocation = ['ftp' , 'googledrive' , 'icloud' , 'dropbox' , 'skydrive']
			if (backupLocation in validlocation):
				self.backup = backupLocation
				return True
			else:
				self.backup = "False"
				return False
		except KeyError:

			self.backup = "False"
			return False





	def parseconfigjson(self,json):
		self.uploadconfig = eval(json)
		if (self.uploadconfig['action'] == 'upload'):
			status = self.upload()

		if (self.uploadconfig['action'] == 'authenticate'):
			status = self.authenticate()

		if (self.uploadconfig['action'] == 'authenticate'):
			status = self.authorize()

		if (self.uploadconfig['action'] == 'save'):
			status = self.setbackuplocation()

		if (self.uploadconfig['action'] == 'import'):
			#status = self.importDB()
			pass
		return status

	def setbackuplocation(self): # data = {location: xxxx , username: xxxxx , password: xxxxx}
		backupconfig = self.uploadconfig.copy()
		backupconfig.pop('action')
		try:
			backupconfig.pop('dbpassword')
		except KeyError:
			pass

		for setting in backupconfig.keys():
			if (setting in ("location","ftphost","ftpuser","gmail","appleid","dropboxid","livemail")):
				self.DBConfig.putmap('cloudinfo', setting , backupconfig[setting])


		


	def getconfig(self,location=None):
		self.loc = location

		if (self.loc==None):
			self.loc = self.backup
			if (self.loc=="False"):
				print "need location"
				return False


		try:
			if (self.loc == 'ftp'):
				Host=self.DBConfig.mapget('cloudinfo')['ftphost']
				User=self.DBConfig.mapget('cloudinfo')['ftpuser']
				return str(dict(ftphost=Host,ftpuser=User))
	
			if (self.loc == 'googledrive'):

				return True
	
			if (self.loc == 'icloud'):
				Email=self.DBConfig.mapget('cloudinfo')['appleid']
				return str(dict(appleid=Email))
	
			if (self.loc == 'dropbox'):
				Email=self.DBConfig.mapget('cloudinfo')['dropboxid']
				return str(dict(dropboxid=Email))
	
			if (self.loc == 'skydrive'):
				Email=self.DBConfig.mapget('cloudinfo')['livemail']
				return str(dict(livemail=Email))

			else:
				return False
		except KeyError: 
			return False

	def authenticate(self):
		socket.RAND_add(self.ssl_seed().randomString, 75.0) # pre-seed generator
		if (self.uploadconfig['location'] == 'dropbox'):

			url = CloudHandler().authenticatedropbox()
			print "============= authenticate dropbox" + str(url)
			return url
		if (self.uploadconfig['location'] == 'googledrive'):

			url = CloudHandler().authenticategoogle()
			print "============= authenticate google" + str(url)
			if (url != True):
				return url
			else:
				return True # then upload

	def authorize(self):
		if (self.uploadconfig['location'] == 'googledrive'):
			socket.RAND_add(self.ssl_seed().randomString, 75.0) # pre-seed generator
			authcode = self.uploadconfig['authcode']
			status = CloudHandler().googleauthorize(authcode)
			if (status): # True
				return True
			else:
				return False


	def upload(self):
		
		self.key = self.uploadconfig["dbpassword"]

		socket.RAND_add(self.ssl_seed().randomString, 75.0) # pre-seed generator
		self.FH.genpack(self.key) #packadge database

		self.packname = self.FH.finalpackname #from config


		if (self.uploadconfig['location'] == 'ftp'):
			host = self.uploadconfig['ftphost']
			user = self.uploadconfig['ftpuser']
			password = self.uploadconfig['password']

			self.DBConfig.putmap('cloudinfo','location','ftp')
			self.DBConfig.putmap('cloudinfo','ftphost', host )
			self.DBConfig.putmap('cloudinfo','ftpuser', user )
			status = CloudHandler().uploadftp(self.packname, host, user, password)

		if (self.uploadconfig['location'] == 'googledrive'):
			self.DBConfig.putmap('cloudinfo','location','googledrive')
			status = CloudHandler().uploadgoogledrive(self.packname)

		if (self.uploadconfig['location'] == 'icloud'):
			email = self.uploadconfig['appleid']
			password = self.uploadconfig['password']

			self.DBConfig.putmap('cloudinfo','location','icloud')
			self.DBConfig.putmap('cloudinfo','appleid',email)
			status = uploadicloud(self.packname, email, pasword)

		if (self.uploadconfig['location'] == 'dropbox'):
			authcode = self.uploadconfig['authcode']

			self.DBConfig.putmap('cloudinfo','location','dropbox')
			# self.DBConfig.putmap('cloudinfo','dropboxid',authcode)
			status = CloudHandler().uploaddropbox(self.packname, authcode)

		if (self.uploadconfig['location'] == 'skydrive'):
			email = self.uploadconfig['livemail']
			password = self.uploadconfig['password']

			self.DBConfig.putmap('cloudinfo','location','googledrive')
			self.DBConfig.putmap('cloudinfo','livemail',email)
			status = uploadskydrive(self.packname, email, password)
		#print self.FH.deletefile(str(self.FH.finalpackname)) # clean-up
		try:
			import os
			os.remove(self.FH.finalpackname)
			#except OSError:
		except Exception as e:
			print e
			ret =  "upload success: " + str(status) + " [ERROR, Clean-up]: " + str(e)
			return ret

		else:
		  return True

	

	

	 




