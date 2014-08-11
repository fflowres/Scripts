class AppIO:
	'''
	AppIO class

	ensure cross platform capability; 
	if it's embedded in application, log function pupes stdout output to c++ function. tuples are then parsed and used in c++

	if not and its just being run in console, variables are passed to console. 

	Return funciton can also be used

	@@ future:
		add data type detection to output different tuple formats to c++; once javascript GUI is removed c++ will require this.

	'''



	def __init__(self,data):
		try:
			import log
			self.dataOut = str(data)
			self.useCPP()
		except ImportError:
			#print instead
			self.dataOut = str(data)
			self.useCPP()
	def useCPP(self):
		log.CaptureStdout(self.dataOut)
		return self #allows chaining

	def useConsole(self):
		print (self.dataOut)
		return self #allows chaining

class DeviceDetection:
	'''
	ex:
	from SecApp import IOClass
	IOClass.DeviceDetection().embeddedapp
	'''
	def __init__(self):
		self.embeddedapp = self.detectcpp()
	def detectcpp(self):
		try:
			import log
			return True
		except ImportError, NameError:
			return False