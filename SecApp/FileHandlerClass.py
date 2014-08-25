from SecApp.IOClass import DeviceDetection
from SecApp.ConfigClass import AppConfig



import os
import zipfile

import datetime

import os, random, struct


import hashlib #for md5 hash
import hmac #sha256
#from Crypto.Cipher import AES
import aes # aes.py from slow aes (standalone) from googlecode
import shutil





class FileHandler:
	'''
	- performs file operations
	- gets file version info
	- verify hashes
	- encrypt 
	- decrypt


	'''


	def __init__(self):
		self.DBConfig = AppConfig()
		#self.DBConfig.mapget('section')['key']
		self.packtype = self.DBConfig.mapget('databaseinfo')['packtype']
		self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']
		self.zipname = self.dbName + ".z"
		self.encryptedzipname = self.dbName + ".z" + ".crypt"






		if (DeviceDetection().embeddedapp): # =True
			import sys
			sys.path = ['/pythonHome/Lib','/pythonHome/','/pythonHome','.','/Lib','/pythonHome/system']

		#if database detected get version info


	def keygen(self,password,salt):
		dig = hmac.new(salt, msg=password, digestmod=hashlib.sha256)
		fkey = dig.hexdigest()
		skey = fkey[0:32]
		return skey


	def encrypt_file(self,key, in_filename, out_filename):
		with open(in_filename, 'rb') as infile:
			with open(out_filename, 'wb') as outfile:
				outfile.write(aes.encryptData(key,infile.read()))

	def decrypt_file(self,key, in_filename, out_filename):
		#out_filename = os.path.splitext(in_filename)[0]
		with open(in_filename, 'rb') as infile:
			with open(out_filename, 'wb') as outfile:
				outfile.write(aes.decryptData(key,infile.read()))


	def getfilesize(self,path):
		filesize=os.path.getsize(path) #returns float
		return filesize
	
	def moddate(self,path):
		t = os.path.getmtime(path)
		return datetime.datetime.fromtimestamp(t)
	
	
	def deletefile(self,file_name): # deletes singe file
		if (os.path.isfile(file_name)):
			try:
			 	os.remove(file_name)
			#except OSError:
			except Exception as e:
				print e
				print 'a'
			 	return False
			else:
				return True
		else:
			print "b"
			return False

	def checkfile(self,path):
		return os.path.isfile(path)
		
	def deletepath(self,path): #deletes entire path and everythin inside
		import shutil
		shutil.rmtree(path)


	
	def zipit(self,path,zip): #sip entire path to file
		zipf = zipfile.ZipFile(zip, 'w', zipfile.ZIP_DEFLATED)
		self.zipdir(path, zipf)
		zipf.close()
	
	def unzipit(self,path,zip):#unzip function
		with zipfile.ZipFile(zip, "r") as z:
			z.extractall(path)	
	
	
	
	def zipdir(self,path, zip):# directoyry stepping funtion use zipit
		for root, dirs, files in os.walk(path):
			for file in files:
				zip.write(os.path.join(root, file))
	

	
	
	def eraseALL(self):
		dbName=self.DBConfig.mapget('databaseinfo')['databasename']
		self.deletepath(dbName)
		self.deletefile("configs/seccuConfig.ini")
	
	
	
	
	
	def md5_for_file(self,path, block_size=256*128, hr=True):
		'''
		Block size directly depends on the block size of your filesystem
		to avoid performances issues
		Here I have blocks of 4096 octets (Default NTFS)
		'''
		md5 = hashlib.md5()
		with open(path,'rb') as f: 
			for chunk in iter(lambda: f.read(block_size), b''): 
				 md5.update(chunk)
		if hr:
			return md5.hexdigest()
		return md5.digest()
	
	
	
	def compareVersions(self):
		return true
		#this should be a seperate module
	
	
	def localVersion(self):
		return True
	def cloudVersion(self):
		return True


	def packdbsecure(self,password):


		#zip path
		self.zipit(self.dbName, self.zipname)
		#key
		salt = self.dbName
		key32 = self.keygen(password,salt)
		#encrypt
		self.encrypt_file(key32, self.zipname,self.encryptedzipname)
		
		pass








	def packdb(self):
		#zip path
		pass

		self.zipit(self.dbName, self.zipname) # self.dbName corresponds to (currDir)./dbname/xxxxx
		return True



	def unpackdbsecure(self):

		#key
		salt = self.dbName
		key32 = self.keygen(self.key , salt)
		#encrypt
		self.encrypt_file(key32, self.encryptedzipname, self.zipname)
		#unzip path
		self.unzipit(self.zipname , self.dbName)
	def unpackdb(self):
		pass




	def parsepacktype(self):
		#if regular zip
		#return False

		#if secure
		return False



	def cleanpacked(self):
		self.deletefile(str(self.finalpackname))


	def genpack(self,password=None):
		


		#check pack type

		#pack
		


		#get file hash
		#get version info
		if (self.parsepacktype()): #if secure or not



			#if it's true (secure)
			self.packdbsecure(password)
			self.finalpackname = self.encryptedzipname
		else: #regular zip
			self.packdb()
			self.finalpackname = self.zipname

		return True


	def genunpack(self):

		#check pack type
		# get verison info
		#verify file hash

		#(decrypt)
		#unpack

		#delete garbadge

		pass








#add error handling
#if file doesnt exist, if file doesnt



# def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
#	 """ Encrypts a file using AES (CBC mode) with the
#		 given key.

#		 key:
#			 The encryption key - a string that must be
#			 either 16, 24 or 32 bytes long. Longer keys
#			 are more secure.

#		 in_filename:
#			 Name of the input file

#		 out_filename:
#			 If None, '<in_filename>.enc' will be used.

#		 chunksize:
#			 Sets the size of the chunk which the function
#			 uses to read and encrypt the file. Larger chunk
#			 sizes can be faster for some files and machines.
#			 chunksize must be divisible by 16.
#	 """
#	 if not out_filename:
#		 out_filename = in_filename + '.enc'

#	 iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
#	 encryptor = AES.new(key, AES.MODE_CBC, iv)
#	 filesize = os.path.getsize(in_filename)

#	 with open(in_filename, 'rb') as infile:
#		 with open(out_filename, 'wb') as outfile:
#			 outfile.write(struct.pack('<Q', filesize))
#			 outfile.write(iv)

#			 while True:
#				 chunk = infile.read(chunksize)
#				 if len(chunk) == 0:
#					 break
#				 elif len(chunk) % 16 != 0:
#					 chunk += ' ' * (16 - len(chunk) % 16)

#				 outfile.write(encryptor.encrypt(chunk))


# def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
#	 """ Decrypts a file using AES (CBC mode) with the
#		 given key. Parameters are similar to encrypt_file,
#		 with one difference: out_filename, if not supplied
#		 will be in_filename without its last extension
#		 (i.e. if in_filename is 'aaa.zip.enc' then
#		 out_filename will be 'aaa.zip')
#	 """
#	 if not out_filename:
#		 out_filename = os.path.splitext(in_filename)[0]

#	 with open(in_filename, 'rb') as infile:
#		 origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
#		 iv = infile.read(16)
#		 decryptor = AES.new(key, AES.MODE_CBC, iv)

#		 with open(out_filename, 'wb') as outfile:
#			 while True:
#				 chunk = infile.read(chunksize)
#				 if len(chunk) == 0:
#					 break
#				 outfile.write(decryptor.decrypt(chunk))

#			 outfile.truncate(origsize)







