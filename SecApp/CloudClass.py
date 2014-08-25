from SecApp.FileHandlerClass import FileHandler
from SecApp.ConfigClass import AppConfig

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import pickle
import base64

import string
import random
class CloudHandler:
	'''




	'''




	def __init__(self):
		self.DBConfig = AppConfig()
		self.FH = FileHandler()
		self.googleConfig = 'configs/gdrive.yaml'

	def ssl_seed(self,size=24, chars=string.ascii_uppercase + string.digits):
		self.randomString = ''.join(random.choice(chars) for _ in range(size))
		return self


	def authenticategoogle(self):
		self.ga = GoogleAuth(self.googleConfig)
		try:
			self.ga.LoadClientConfig()
			self.ga.LoadCredentials()
			self.ga.Authorize()
		except:
			return self.ga.GetAuthUrl()
			#code = raw_input("code: ").strip()
		else:
			return True
			#auth loaded ok

	def googleauthorize(self,authCode):
		code = authCode.strip()
		self.ga.Auth(code)
		self.ga.SaveCredentials()
		return True

	def googleupload(self,filename):
		packageName = filename
		self.ga = GoogleAuth(self.googleConfig)
		self.ga.LoadClientConfig()
		self.ga.LoadCredentials()
		self.ga.Authorize()
		drive = GoogleDrive(self.ga)
		#flist = drive.ListFile({'q': "title contains '.crypt' and trashed = false"})
		folderlistquery = drive.ListFile({'q': "title = 'SeccuDB' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"})
		

		cloudfolder = folderlistquery.GetList()
		if (len(cloudfolder) == 0):
			#create folder 
			folder = drive.CreateFile()
			folder['title'] = "SeccuDB"
			folder['mimeType'] = "application/vnd.google-apps.folder"
			folder['parents'] = "root"
			folder.Upload()
			cloudfolder = folderlistquery.GetList()
			if (len(cloudfolder) == 0):
				print "error"
				raise error('GooglePermissionsError')


		cloudfolderid = cloudfolder[0]['id']
		print cloudfolderid

		databaseListquery = drive.ListFile({'q': "'%s' in parents and trashed = false" % (cloudfolderid)})
		databaseList = databaseListquery.GetList()


		database_file = drive.CreateFile()
		database_file['title'] = packageName
		database_file['parents']=[{"kind": "drive#fileLink" ,'id': str(cloudfolderid) }]
		#check if already exists, if so, get id and update
		databasenamelist = []
		for databaseAvaliable in databaseList:
			databasenamelist.append(databaseAvaliable['title'])
		if packageName in databasenamelist:
			cloudPackageQuery = drive.ListFile({'q': "title = '%s' and trashed = false" % (packageName)})
			cloudPackage = cloudPackageQuery.GetList()

			if(len(cloudPackage) > 1): # if theres more than one, go for the most recent
				packdates = []
				for everypack in cloudPackage:
					packdates.append((everypack['modifiedByMeDate'],everypack['id']))
				database_file['id'] = sorted(packdates,reverse=True)[0][1]

			else:
				database_file['id'] = cloudPackage[0]['id']

		database_file.Upload()
		return True


	def getgooglefileid(self,title):

		print os.getcwd()
		self.ga = GoogleAuth(self.DBConfig.googleyaml)
		self.ga.LocalWebserverAuth()
		drive = GoogleDrive(self.ga)
		flist = drive.ListFile({'q': "title = '%s' and trashed = false"%title})
		files = flist.GetList() 
		if len(files)==0:
			return False
		else:
			return files[0]['id']


	def simpleUploadGoogle(self,filename): #test_01_Files_Insert
		drive = GoogleDrive(self.ga)
		#f = drive.CreateFile({'fluidSecurity': parent_id})
		file1 = drive.CreateFile()
		file1.SetContentFile(filename) # Read local file
		file1.Upload() # Upload it
		
	

		return True
	##save file ID to config
	
	
	def simpleUpdateGoogle(self,filename,dbID):
		drive = GoogleDrive(self.ga)
	
		file1=drive.CreateFile({'id': dbID}) #overwrite by ID
		file1['title'] = filename
		file1.FetchContent()
		file1.SetContentFile(filename)
		file1.Upload() 
		return True
		
	
	def simpleDownloadGoogle(self,filename):
		DeleteOldFile(self.filename) #delete local version, not that safe
	
		drive = GoogleDrive(self.ga)
		file1 = drive.CreateFile()
		file1['title'] = filename
		file1.FetchContent()  # Force download and double check content
		return True
	
	
#	
#	
#	def ftpDown(filename,host,user,ftpass):
#		import ftplib
#		session = ftplib.FTP(host,user,ftpass)
#		file = open(filename, 'wb')  
#		session.retrbinary('RETR %s' % filename, file.write)
#		file.close()
#		session.quit()
#	


	


	def uploadftp(self,filename,host,user,password):	  

		# upload logic
		import ftplib
		session = ftplib.FTP(host,user,password)
		file = open(filename,'rb')				  # file to send
		session.storbinary('STOR ' +filename, file)	 # send the file
		file.close()									# close file and FTP
		session.quit()

		return True

	def authenticatedropbox(self):
		import dropbox

		# Get your app key and secret from the Dropbox developer website
		app_key = 'p2iu4n7f9yegl3u'
		app_secret = '0903whnau7p2zde'

		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

		authorize_url = flow.start()
		print "============= authenticate dropbox" + str(authorize_url)

		pickled  = pickle.dumps(flow)
		encodedPickle = base64.b64encode(pickled)
		self.DBConfig.putmap('cloudinfo','dropboxobject', str(encodedPickle) )

		return authorize_url



	def uploaddropbox(self,filename,authcode):
		import socket
		socket.RAND_add(self.ssl_seed().randomString, 75.0)
		import dropbox

		try:
			# Get your app key and secret from the Dropbox developer website
			# encodedPickle =self.DBConfig.mapget('cloudinfo')['dropboxobject']
			# decodedPickle = base64.b64decode(encodedPickle)
			# flow = pickle.loads(decodedPickle)

			app_key = 'p2iu4n7f9yegl3u'
			app_secret = '0903whnau7p2zde'

			flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

			authorize_url = flow.start()
			print "============= authenticate dropbox" + str(authorize_url)


			print "loaded ok"
			print "------ authcode: " + str(authcode)
			access_token, user_id = flow.finish(authcode)

			print "finidhed oko"
			client = dropbox.client.DropboxClient(access_token)
			print "finidhed client"
			print 'linked account: ', client.account_info()

			#Uploading files
			f = open(filename, 'rb')
			response = client.put_file('/'+str(filename), f)
			print "uploaded:", response

		except Exception as e:
			print("Upload failed: " + str(e))
			return False
		return True

	def uploadgoogledrive(self,filename):
		googlefileid = self.getgooglefileid(filename)
		if googlefileid == False:
			self.simpleUploadGoogle(filename)
		else:
			self.simpleUpdateGoogle(filename,googlefileid)
		return True

	def uploadicloud(self,filename,email,password):

		return True

	def uploadskydrive(self,filename,email,password):	

		return True

	



