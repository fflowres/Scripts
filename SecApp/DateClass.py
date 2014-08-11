import datetime as dt
class ud: 
	'''
	UberDate class 
	any date to > date time object > any date format

	call

	ud.dts( ' date time string ' ) - auto detects formats


		attribute .dto returns datetime object

	ex:
	ud.dts( ' date time string ' ).dts


	---
	to other format

	ud.dts( ' date time string ' ).udiso (parameters)

	'''
	
	def __init__(self,daterange='all'):
		pass

	def dts(self,dtString):
		self.dto=dt.datetime.strptime(dts,"%Y-%m-%d %H:%M:%S.%f")
		return self

	def conv_dts_dto(self, dts):
		dto=dt.datetime.strptime(dts,"%Y-%m-%d %H:%M:%S.%f")
		return dto



def sortDates(self,dlist):
		self.dates = dlist
		self.dates.sort(reverse=True)



def getDayStart():
	d = dt.datetime.now()
	conv = str(d.year)+"-"+ str(d.month)+"-"+ str(d.day)+" "+"00:00:00.000000" #sets time to 0, therefore starts only at 0 in the morning
	#dto=dt.datetime.strptime(str(conv),"%Y-%m-%d %H:%M:%S.%f")
	return conv   

def getTimeStamp():
	import datetime as dt
	d = dt.datetime.now()
	return str(d)
