from SecApp.FileHandlerClass import FileHandler
from SecApp.ConfigClass import AppConfig

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
class CloudHandler:
	'''




	'''




	def __init__(self):
		self.DBConfig = AppConfig()
		self.FH = FileHandler()




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



	def uploaddropbox(self,filename,email,password):
		from dbupload import DropboxConnection
		try:
			# Create the connection
			conn = DropboxConnection(email, password)
			# Upload the file
			conn.upload_file(filename,"/",filename)
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

	



