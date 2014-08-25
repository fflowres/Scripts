import time
import datetime
class DataNormalization:
    '''
    description:
    takes x (arbitrary date based) and y and normalizes the data by aligning an interpolated version to a time difference constant
    
    
    data =initDO.iffo().orderedmap().processFrameList 
    
    datakey = the question you want
    normalizationConst = some time delta object {eg: datetime.timedelta(minutes=15)}
    
    important outputs:
    
    the first date in the acceptable analysis sequence
    self.firstrefdate_dto
    self.firstrefdate
    
    the last date in the acceptable analysis sequence
    self.lastrefdate_dto
    self.lastrefdate
    
    
    self.normalizedX = [...Aligned sequence...]
    self.normalizedY = [...Aligned sequence...]
    self.normalizedY_dto = [...Aligned sequence...]
    
    - Data normalized to time constant and aligned, outputs list of tuple (x,y) pairs {dto is data time object}
    normalized
    normalized_dto
    
    '''
    
    
    
    
    def __init__(self,data,datakey,normalizationConst):
        self.data = data
        self.keysearch = datakey
        self.normalizationConst = normalizationConst #this is the time interval between points expressed as a timedelta object
        
        # List of tuples
        self.denormalized = []
        self.denormalizedX = []
        self.denormalizedY = []
        
        self.normalized_dtokey_dict = {}
        self.normalized = []
        self.normalized_dto = []
        
        self.normalizedX = []
        self.normalizedX_dto = []
        self.normalizedY = []
        
        
        self.firstregdate = self.data[0].keys()[0]
        
        self.firstrefdate_dto = self.firstregdate + datetime.timedelta(days=1) #since there isnt sufficient data the first day, go to the next to start
        self.firstrefdate = time.mktime(self.firstrefdate_dto.timetuple()) # ^ but in unix timestamp format
        
        self.firstdate = None
        self.lasttdate = None
        self.first_iterate()
        self.Ynormal_interpolation = Interpolate(self.denormalizedX , self.denormalizedY)
        
        self.normalizer()
        
        #self.lastrefdate_dto # the last acceptable key in the sequence
        self.lastrefdate = time.mktime(self.lastrefdate_dto.timetuple()) # the last acceptable key in the sequence, in unix time format
     
    def first_iterate(self):
        for i in range(len(self.data)):
            try:
                dataTime = time.mktime(self.data[i].keys()[0].timetuple())
                dataAtTime = self.data[i][self.data[i].keys()[0]][self.keysearch]
                #append tuple
                self.denormalized.append((dataTime,dataAtTime))
                self.denormalizedX.append(dataTime)
                self.denormalizedY.append(dataAtTime)
                if (self.firstdate == None): #only catch first valid
                    self.firstdate = self.data[i].keys()[0]
                    
                self.lasttdate = self.data[i].keys()[0] # will be caught and updated untill the last valid entry
                #print 'key: ' + str(self.keysearch)+' found at: ' +str(i)
                
            except KeyError:
                #print 'xxxxxxxxxxxxxxxxxxx key: ' + str(self.keysearch)+' not found at: ' +str(i)
                continue
        return self
    
        
    def normalizer(self):
        #iterate from start every
        #get times it can be divided
        try:

            curtimedelta = self.firstrefdate_dto + self.normalizationConst
            #print curtimedelta
            #print self.lasttdate

            while (curtimedelta <= self.lasttdate):

                nX = time.mktime(curtimedelta.timetuple())
                nX_dto = curtimedelta
                nY = self.Ynormal_interpolation[nX]
                
                self.normalizedX.append(nX) #time
                self.normalizedX_dto.append(nX_dto)
                
                self.normalizedY.append(nY) #value
                
                
                self.normalized.append((nX,nY))
                self.normalized_dto.append((nX_dto,nY))
                self.normalized_dtokey_dict[nX_dto] = nY
                

                self.lastrefdate_dto = curtimedelta #continue updating untill last date, checked this round
                curtimedelta = curtimedelta + self.normalizationConst # checked next round

                
        except Exception as e:
            print e
        return self
        
        


from bisect import bisect_left
class Interpolate(object):
    def __init__(self, x_list, y_list):
        if any([y - x <= 0 for x, y in zip(x_list, x_list[1:])]):
            raise ValueError("x_list must be in strictly ascending order!")
        x_list = self.x_list = map(float, x_list)
        y_list = self.y_list = map(float, y_list)
        intervals = zip(x_list, x_list[1:], y_list, y_list[1:])
        self.slopes = [(y2 - y1)/(x2 - x1) for x1, x2, y1, y2 in intervals]
    def __getitem__(self, x):
        i = bisect_left(self.x_list, x) - 1
        return self.y_list[i] + self.slopes[i] * (x - self.x_list[i])