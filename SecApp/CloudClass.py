from SecApp.FileHandlerClass import FileHandler
from SecApp.ConfigClass import AppConfig


class CloudHandler:
	'''




	'''




	def __init__(self):
		self.DBConfig = AppConfig()
		self.FH = FileHandler()







#	def simpleUploadGoogle(filename): #test_01_Files_Insert
#		drive = GoogleDrive(ga)
#		#f = drive.CreateFile({'fluidSecurity': parent_id})
#		file1 = drive.CreateFile()
#		file1.SetContentFile(filename) # Read local file
#		file1.Upload() # Upload it
#		
#	
#		writeConfigSectionMap('cloudinfo','databasecloudid',file1['id'])
#		return True
#	##save file ID to config
#	
#	
#	def simpleUpdateGoogle(filename):
#		dbID=ConfigSectionMap('cloudinfo')['databasecloudid']
#		
#		drive = GoogleDrive(ga)
#	
#		file1=drive.CreateFile({'id': dbID}) #overwrite by ID
#		file1['title'] = filename
#		file1.FetchContent()
#		file1.SetContentFile(filename)
#		file1.Upload() 
#		return True
#		
#	  
#	
#	def simpleDownloadGoogle(filename):
#		DeleteOldFile(self.filename) #delete local version, not that safe
#	
#		drive = GoogleDrive(self.ga)
#		file1 = drive.CreateFile()
#		file1['title'] = filename
#		file1.FetchContent()  # Force download and double check content
#		return True
#	
#	
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
#
#	
#	
#	def readFTPConfig():
#		try:
#			host=ConfigSectionMap('cloudinfo')['ftphost']
#			user=ConfigSectionMap('cloudinfo')['ftpuser']
#			ftpSettings=dict(host=host,user=user)
#		except KeyError: 
#			return False
#		else:	
#			return str(ftpSettings)







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

	def uploadgoogledrive(self,filename,email,password):
		
		return True

	def uploadicloud(self,filename,email,password):

		return True

	def uploadskydrive(self,filename,email,password):	

		return True

	



