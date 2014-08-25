from SecApp.ConfigClass import AppConfig
from SecApp.DBBaseClass import DayEntry 
from SecApp.DBBaseClass import DBIndexSystem 
from SecApp.DBQuestionClass import SecuQ
#from SecApp. import 




import salsa20 
import marshal
from CodernityDB.hash_index import UniqueHashIndex
from CodernityDB.storage import Storage
from CodernityDB.database import Database
from CodernityDB.database import RecordNotFound

class SecuFrame: #in producion, key must be specified
	def __init__(self,passkey,date_range='all'):
		self.key = passkey
		self.Qeng = SecuQ(self.key)

		self.indexdb = DBIndexSystem(self.key)
		#self.indexdb.masterIndex
		#self.indexdb.Qindex
		#self.indexdb.Tindex
		#self.indexdb.IndexedTable
		#self.indexdb.dbName

		self.dayindex = DayEntry(self.key)
		#self.dayindex.dayKey

		self.DBConfig = AppConfig()

		self.dbName = self.DBConfig.mapget('databaseinfo')['databasename']

		self.db = Database(self.dbName)


		self.dbparseable = self.db2json(daterange=date_range,clean=True)
		
	def __del__(self):
		if (self.db.opened):
			self.db.close()

		
		
	def db2json(self,daterange,clean=True):
		'''
		> daterange 
		- tuple datetime objects to specify range
		(dateObj,dateObj)
		
		
		
					
		'''
		
		dfJSON = []
		
		if(self.db.exists()):
			self.db.open()
			self.db.id_ind.enc_key = self.key
			if daterange == "all":
				if clean == True:


					for currHash in self.indexdb.IndexedTable: #get row  
						curr = self.db.get('id', currHash, with_doc=True)

						curr.pop('_id')
						curr.pop('_rev')
						dfJSON.append(curr)

					self.db.close()
					return dfJSON
			
				if clean == False:
					for currHash in self.indexdb.IndexedTable: #get row  
						curr = self.db.get('id', currHash, with_doc=True)
						dfJSON.append(curr)

					self.db.close()
					return dfJSON

			if daterange == "today":
				if clean == True:
					curr = self.db.get('id', self.dayindex.dayKey, with_doc=True)
					curr.pop('_id')
					curr.pop('_rev')
					dfJSON.append(curr)
					self.db.close()
					return dfJSON
				
		'''
		#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  

			if ((type(daterange) == tuple) & (len(daterange)<=2) & (daterange[0]<daterange[1]) &(type(daterange[0])==datetime.datetime) & (type(daterange[1])==datetime.datetime): #if it's a valid daterange
				if clean == True
					
					for curr in db.all('id'): #get row   
						currdto=dt.datetime.strptime(curr['date'],"%Y-%m-%d %H:%M:%S.%f")
						if ( daterange[0] <= currdto <= daterange[1]):







							curr.pop('_id')
							curr.pop('_rev')
							dfJSON.append(curr)
					db.close()
					return dfJSON
			
				if clean == False:
					for curr in db.all('id'): #get row		  
						dfJSON.append(curr)
					db.close()
					return dfJSON





			else: # raise some kindof exception
				return False
			
	
		#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		'''	
	
	
	
	
	
	
	
	
	
	def iffo(self, daterange = "all", obey = True):
		self.dbfiltered = []
		self.dbdatemapped = {}
		self.infoIndex = self.Qeng.valid # {'a':{'active':'True','typ':'slider','range':'0-100','aggregate':'True', 'multipoint':'True'}}
		if obey == True :
			for curr in self.dbparseable: #get row
				'''
				{'date' : xx , 'a':{'xxdate1xx':1,'xxdate2xx':2},
					'b':{'xxdate1xx':14,'xxdate2xx':14},
					'c':{'xxdate1xx':11,'xxdate2xx':11},
					'note':{'xxdate2xx':'hello','xxdate3xx':'you'}
				}
				'''

				tmp={} #holder that is constructed

				rowDate = curr["date"] #'date' : xx
				'''
				date : xx
				'''

				questionsData = curr.keys() # returns a list
				questionsData.remove('date')
				'''
				['a','b','c','note']
				'''
				#questionsData.remove('note')

				for question in questionsData: #get question from list	

					try:
						if (self.infoIndex[question]['multipoint']== "True"): # & (self.infoIndex[question]['aggregate']== "False"): #display all points
		
		
							multiP = curr[question].keys()
							'''
							in 'a'
							['xxdate1xx','xxdate2xx']
							'''
							
							for point in multiP: #points are dates
								try:
									tmp[question][point] = curr[question][point]
								except KeyError:
									tmp[question]={}
									tmp[question][point] = curr[question][point]
	
								try:
									self.dbdatemapped[point][question] = curr[question][point]
								except KeyError: #avoid overwriting
									self.dbdatemapped[point] = {}
									self.dbdatemapped[point][question] = curr[question][point]			
	
						
						if (self.infoIndex[question]['multipoint']== "True") & (self.infoIndex[question]['aggregate']== "True"): #display only one aggregate in it's own column
	
							'''
							creates unique key for aggregate
							'''
							datelist = curr[question].keys() #gets all dates within the question 
							datelist.sort()	 #ensure earliest to latest
							aggregate_key_name = str(question)+"_aggregate"
							tmp[aggregate_key_name]={}
	
	
							try: #as intigers
								tmp[aggregate_key_name][rowDate] = 0
								aggregate_sum = 0
								for point in datelist:
									aggregate_sum += curr[question][point]
							except TypeError: #process aggregate function as concatenated strings
								tmp[aggregate_key_name][rowDate] = ""
								aggregate_sum = ""
								for point in datelist:
									aggregate_sum += curr[question][point] + "\n"
								
	
	
							try:
								self.dbdatemapped[rowDate][aggregate_key_name] = aggregate_sum
							except KeyError: 
								self.dbdatemapped[rowDate] = {}
								self.dbdatemapped[rowDate][aggregate_key_name] = aggregate_sum
		
							tmp[aggregate_key_name] = {}
							tmp[aggregate_key_name][rowDate] = aggregate_sum # replaces with single 
	
	
	
						if ((self.infoIndex[question]['multipoint']== "False") & (self.infoIndex[question]['aggregate']== "False")) | (self.infoIndex[question]['typ']== "note"): #display only one
							'''
							Puts last entry under rowdate 
							'''
	
	
	
							''' 
							NOTE HANDLING
							in future this should select the most positive note based on sentiment analysis
	
							- For now it will select the last note typed in
							'''
	
	
							datelist = curr[question].keys() #gets all dates within the question
		
							pointKey = self.getLastDate(datelist) #selects most recent date from list (keys)
							try:
								tmp[question][rowDate] = curr[question][pointKey] # replaces with single, most recent, point only
							except KeyError:
								tmp[question]={}
								tmp[question][rowDate] = curr[question][pointKey] # replaces with single, most recent, point only
							try:
								self.dbdatemapped[rowDate][question]  = curr[question][pointKey]
							except KeyError:
								self.dbdatemapped[rowDate] = {}
								self.dbdatemapped[rowDate][question]  = curr[question][pointKey]
	
	
		
						if (self.infoIndex[question]['multipoint']== "False") & (self.infoIndex[question]['aggregate']== "True"): #display only one aggregate in it's own column
							datelist = curr[question].keys() #gets all dates within the question 
							datelist.sort()	 #ensure earliest to latest
		
							tmp[question]={}
							
							try: #as intigers
								tmp[question][rowDate] = 0
								aggregate_sum = 0
								for point in datelist:
									aggregate_sum += curr[question][point]
							except TypeError: #process aggregate function as concatenated strings
								tmp[question][rowDate] = ""
								aggregate_sum = ""
								for point in datelist:
									aggregate_sum += curr[question][point] + "\n"
		
							#output	
							tmp[question][rowDate] = aggregate_sum
							#remapping is additive
							try:
								self.dbdatemapped[rowDate][question]  = aggregate_sum
							except KeyError:
								self.dbdatemapped[rowDate] = {}
								self.dbdatemapped[rowDate][question]  = aggregate_sum
					except KeyError:
						continue

				self.dbfiltered.append(tmp)

		return self

	def igraph(self):
		import datetime as dt
		self.graphFrame = []

		graphpoints = self.dbdatemapped.keys()
		graphdates = []

		
		for date in graphpoints:
			try:
				graphdates.append(dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f"))
			except ValueError:
				graphdates.append(dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S"))

		sortkeydto, pointerdts = zip(*sorted(zip(graphdates, graphpoints)))

		for i in xrange(0,len(pointerdts)): # want {date: xxxISOxxx , a:x ,b:x ,note:x}

			tmpRow = {}
			tmpRow['date'] = sortkeydto[i].isoformat() + "Z"
			for question in self.dbdatemapped[pointerdts[i]]:
				tmpRow[question] = self.dbdatemapped[pointerdts[i]][question]
				
			self.graphFrame.append(tmpRow)
		return self
			 
		#map accordingly with date to iso format



	def Agraph(self,neuroOutput):
		import datetime as dt
		self.neuroOutput = neuroOutput # [(dto,dto),(dto,dto),,,,]
		self.AgraphFrame = []

		graphpoints = self.dbdatemapped.keys()
		graphdates = []

		self.last_date = None
		self.curr_date = None

		self.neuro_scan_count = 0 
		self.neuro_highlight_complete = False

		for date in graphpoints:
			try:
				graphdates.append(dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f"))
			except ValueError:
				graphdates.append(dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S"))

		sortkeydto, pointerdts = zip(*sorted(zip(graphdates, graphpoints)))

		for i in xrange(0,len(pointerdts)): # want {date: xxxISOxxx , a:x ,b:x ,note:x}
			tmpRow = {}
			# set to white /  transparent first
			self.curr_date = sortkeydto[i]

			if (self.neuro_highlight_complete == False):
				tmpScanPos = divmod(self.neuro_scan_count,2) # divisor answer, remainder
				#print "tmpScanPos: " +str(tmpScanPos) + " self.neuro_scan_count:  " + str(self.neuro_scan_count)
				tmpNeuroDate = self.neuroOutput[tmpScanPos[0]][tmpScanPos[1]]

				if ( self.last_date == None): tmpRow["lineColor"] = "#FFFFFF"
				elif (self.curr_date == tmpNeuroDate):
					if (tmpScanPos[1] == 0 ): tmpRow["lineColor"] = "#CC0000" #if start of range
					if (tmpScanPos[1] == 1 ): tmpRow["lineColor"] = "#FFFFFF" # if end of range
					self.neuro_scan_count +=1

				elif(self.last_date < tmpNeuroDate < self.curr_date):
					if (tmpScanPos[1] == 0 ): tmpRow["lineColor"] = "#CC0000" #if start of range
					if (tmpScanPos[1] == 1 ): tmpRow["lineColor"] = "#FFFFFF" # if end of range
					self.neuro_scan_count +=1

				if ((tmpScanPos[0] + tmpScanPos[0]) == len(neuroOutput)): self.neuro_highlight_complete = True #checks if this should be the last iteration

				

			
			tmpRow['date'] = sortkeydto[i].isoformat() + "Z"
			for question in self.dbdatemapped[pointerdts[i]]:
				tmpRow[question] = self.dbdatemapped[pointerdts[i]][question]
				
			self.AgraphFrame.append(tmpRow)
			self.last_date = sortkeydto[i]
			 
		#map accordingly with date to iso format


	def dayresponse(self):
		self.responseFrame = {}
		try:
			tmp = self.dbdatemapped[self.dayindex.todayDate]
		except KeyError: #means there is no information for the daykey
			return self
		# remove aggregate keyword, json handles association
		
		for question in tmp.keys():
			cleankey = question.replace('_aggregate', '')
			self.responseFrame[cleankey] = tmp[question]
		
		return self

	def orderedmap(self):
		import datetime as dt
		self.processFrameList = []
		self.processFrameDict = {}

		graphpoints = self.dbdatemapped.keys()
		graphdates = []

		
		for date in graphpoints:
			try:
				graphdates.append(dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f"))
			except ValueError:
				graphdates.append(dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S"))

		sortkeydto, pointerdts = zip(*sorted(zip(graphdates, graphpoints)))

		for i in xrange(0,len(pointerdts)): # want {date: xxxISOxxx , a:x ,b:x ,note:x}

			tmpRow = {}
			tmpRow[sortkeydto[i]] = {}
			self.processFrameDict[sortkeydto[i]] = {}

			for question in self.dbdatemapped[pointerdts[i]]:
				tmpRow[sortkeydto[i]][question] = self.dbdatemapped[pointerdts[i]][question]
				self.processFrameDict[sortkeydto[i]][question] = self.dbdatemapped[pointerdts[i]][question]
				
			self.processFrameList.append(tmpRow)
		return self


	def getLastDate(self,dates): #input a list of dates
		dates.sort(reverse=True)
		return dates[0] #output most recent date in subset



