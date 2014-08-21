import ConfigParser
import os
from SecApp import IOClass


class AppConfig:
	'''
	# createConfig()
	
	# checkReal():
	 -notes: [old name 'checkValidSettings' ]
		 checks for existence of log and if a database exists (returns bool)
	
	# mapget('section')['key'] = returns value
	
	 -notes: [old name 'ConfigSectionMap' ]
		 section and key must be lowercase [fix this]
	
	
	# putmap(section,option,value)
	
	 -notes: [old name 'writeConfigSectionMap' ]
		 section and key must be lowercase [fix this]
	
	'''


	def __init__(self):

		
		if IOClass.DeviceDetection().embeddedapp: #if embedded
			import sys
			sys.path = ['/pythonHome/Lib','/pythonHome/','/pythonHome','.','/Lib','/pythonHome/system']



		self.configFileName='configs/seccuConfig.ini'
		self.googleyaml = 'configs/gdrive.yaml'

	def mapget(self,section):
		Config = ConfigParser.ConfigParser()
		Config.read(self.configFileName)
		dict1 = {}
		options = Config.options(section)
		for option in options:
			try:
				dict1[option] = Config.get(section, option)
				if dict1[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
		return dict1
	
	
	
	def createConfig(self):
		if not os.path.exists('configs'):
			os.makedirs('configs')
		cfgfile = open(self.configFileName,'w')
	
		Config = ConfigParser.ConfigParser()
	
	
		Config.add_section('localinfo')
		Config.set('localinfo','databasehashcheck','NULL')
		Config.set('localinfo','databaselastdate','NULL')
		Config.set('localinfo','databaselastsize','NULL')
		Config.set('localinfo','databaseversion','NULL')
		Config.set('localinfo','keyfile','NULL')
	
		Config.add_section('cloudinfo')
		Config.set('cloudinfo','location','NULL')
		Config.set('cloudinfo','databaseversion','NULL')
		Config.set('cloudinfo','databasehashcheck','NULL')
	
		Config.add_section('databaseinfo')
		Config.set('databaseinfo','databasename','NULL')
		Config.set('databaseinfo','databasehashcheck','NULL')
		Config.set('databaseinfo','packtype','secure')
	
	
		Config.write(cfgfile)
		cfgfile.close()
	

	
	
	def putmap(self,section,option,value):
		# try:
		try:
			Config = ConfigParser.ConfigParser()
			cfgfile = open(self.configFileName,'r')
			Config.read(self.configFileName)
			cfgfile.close()
		except IOError:
	
			self.createConfig() #create blank slate needs functions to re import database if config is lost
	
			
			Config = ConfigParser.ConfigParser()
			cfgfile = open(self.configFileName,'r')
			Config.read(self.configFileName)
			cfgfile.close()
	
	
		
	
		cfgfile = open(self.configFileName,'w')
		
		Config.set(section, option, value)
		
		Config.write(cfgfile)
		cfgfile.close()
		return True 