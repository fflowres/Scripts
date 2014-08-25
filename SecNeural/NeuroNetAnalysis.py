
            
from SecNeural.ClassAlignmentSubsystem import DataNormalization
import datetime
from SecApp.DBOutputClass import SecuFrame

class NeuroResolve(object):
    def __init__(self):
        NeuroResolve.rawresults = []
        
        NeuroResolve.pairedResults = {}
        
        NeuroResolve.byConditionIDs = []
        NeuroResolve.byConditionNames = []
        NeuroResolve.queryID = None # id that won the final neural query, that will be used to output respective data
        self.basicResolver()
        
       
        
    def basicResolver(self):
        self.getNeuralData()
        self.resultpairid()
        self.orderresults()
        self.assignFullConditionName()
        return self
        
    def getNeuralData(self): # get
        
        # will probably need to iterate this once we have more data
        
        #just one to start
        NeuroResolve.queryID = NeuroBasicConditions.allPointSelectionIds[0]
        tmplst=[]
        tmplst.append(NeuroResolve.queryID)
        NeuroResolve.rawresults = NeuroTrainer.mynet.getresult(tmplst,NeuroBasicConditions.allConditionIds)
        #itterate and compare datasets
        
        
        
        return self
    
    def resultpairid(self): # pair respective to id
        NeuroResolve.pairedResults = {}
        for i in range(len(NeuroResolve.rawresults)):
            NeuroResolve.pairedResults[NeuroBasicConditions.allConditionIds[i]] = NeuroResolve.rawresults[i]
        return self
    
    def orderresults(self): # order by value return Condition ID list
        #list
        NeuroResolve.byConditionIDs = sorted(NeuroResolve.pairedResults, key=NeuroResolve.pairedResults.get, reverse=True)
        return self
    
    def assignFullConditionName(self):   # ordered by value return Condition Name list
        for _id in NeuroResolve.byConditionIDs:
            NeuroResolve.byConditionNames.append(NeuroBasicConditions.idLookupCondtion[_id])
        return self

    
class NeuroOutput(object):
    def __init__(self):
        NeuroOutput.RawTrainerOutput = [] #empty start
        NeuroOutput.process_points = {}
        NeuroOutput.process_datasets = {}
        NeuroOutput.process_conditions = {}
        
    def basic_get_top(self):
        self.outputConditionID = NeuroResolve.byConditionIDs[0]  # the very first in the ordered array
        
        self.outputConditionConfiguration = NeuroBasicConditions.conditionsConfig[NeuroBasicConditions.idLookupCondtion[self.outputConditionID]]
        
        #copy configuration of single point
        NeuroOutput.process_points[NeuroBasicConditions.idLookupPointSelection[NeuroResolve.queryID]] = NeuroBasicConditions.pointSelectionConfig[NeuroBasicConditions.idLookupPointSelection[NeuroResolve.queryID]]
        
        NeuroOutput.process_datasets[NeuroBasicConditions.idLookupDataset[self.outputConditionConfiguration['analyze']]] = NeuroBasicConditions.datasetConfig[NeuroBasicConditions.idLookupDataset[self.outputConditionConfiguration['analyze']]]
        
        NeuroOutput.process_conditions[self.outputConditionConfiguration['analyze']] = [self.outputConditionConfiguration['ID']] # {datasetid:conditionid}
        
        
        
        NeuroTrainer.getResult = True # set to get appended output
        NeuroTrainer.methodBasicTrain(self) #appends and writes to NeuroOutput.RawTrainerOutput
        NeuroTrainer.getResult = False # reset to train mode
        
        
        
        
        #print (NeuroOutput.RawTrainerOutput) #x-coords unordered
        
        return self
        
        
    def basic_generate_graph(self):
        #iffo already ran on this dataobject
        NeuroTrainer.initDO.Agraph(NeuroOutput.RawTrainerOutput)
        #print NeuroTrainer.initDO.AgraphFrame

class NeuroTrainer(object):
    
    def __init__(self):
        #pass mynet object
        NeuroTrainer.mynet = None
        NeuroTrainer.getResult = False
        
        
        
    def aquiredata(self):
        NeuroTrainer.initDO = SecuFrame('')
        NeuroTrainer.fromDB = NeuroTrainer.initDO.iffo().orderedmap().processFrameList
                
        return self
    
    def methodBasicTrain(self):
        if (NeuroTrainer.getResult):
            NeuroTrainer.process_points = NeuroOutput.process_points
            NeuroTrainer.process_datasets = NeuroOutput.process_datasets
            NeuroTrainer.process_conditions = NeuroOutput.process_conditions
        else: # if it is in training mode, iterate through all conditons and combinations
            NeuroTrainer.process_points = NeuroBasicConditions.pointSelectionConfig
            NeuroTrainer.process_datasets = NeuroBasicConditions.datasetConfig
            NeuroTrainer.process_conditions = NeuroBasicConditions.DatasetConditions
        
        
        
        
        for selectionPointVariable in NeuroTrainer.process_points.keys(): # iterate through point sets
            
            #Normalized points dataset(object)
            #print NeuroBasicConditions.pointSelectionConfig[selectionPointVariable]["NormConstant"]
            #print "--------------------"
            #print NeuroBasicConditions.pointSelectionConfig[selectionPointVariable]
            #print "--------------------"
            #print NeuroBasicConditions.pointSelectionConfig
            
            normalizedSelectionPointData = DataNormalization(NeuroTrainer.fromDB,NeuroBasicConditions.pointSelectionConfig[selectionPointVariable]["pointSelectSet"],NeuroBasicConditions.pointSelectionConfig[selectionPointVariable]["NormConstant"])
            normalizedSelectionPointDataID = NeuroBasicConditions.pointSelectionConfig[selectionPointVariable]["ID"]
            #computed selection points
            
            NeuroPoints.__init__(self,normalizedSelectionPointDataID,normalizedSelectionPointData.normalizedX,normalizedSelectionPointData.normalizedY)
            computedSelectionPoints = NeuroPoints.XpointsofInterest
            
            #print "computedSelectionPoints " + str(computedSelectionPoints)
            
            for analyzableDatasetVariable in NeuroTrainer.process_datasets.keys(): # iterate through datasets
                
                #Normalize dataset (object)
                normalizedAnalyzableDataset = DataNormalization(NeuroTrainer.fromDB,analyzableDatasetVariable,NeuroBasicConditions.datasetConfig[analyzableDatasetVariable]["NormConstant"])
                normalizedAnalyzableDatasetID = NeuroBasicConditions.datasetConfig[analyzableDatasetVariable]["ID"]
                #compute each condition and train neural network
                
                
                NeuroCondSearch.__init__(self, normalizedAnalyzableDataset.normalizedX, normalizedAnalyzableDataset.normalizedY)
                
                for computeConditionID in NeuroTrainer.process_conditions[normalizedAnalyzableDatasetID]: # returns ids of conditions attached to dataset
                    '''
                    {datasetID:[conditionid,conditionid]}
                    '''
                    #initialize conditional search, use id
                    NeuroCondSearch.setID(self, computeConditionID)
                    
                    #print "computeConditionID " + str(computeConditionID)
                    for xpoint in computedSelectionPoints: # iterate through each point
                        bool_result = NeuroCondSearch.runop(self,xpoint) #process point
                        
                        if (NeuroTrainer.getResult):
                            if (bool_result):
                                #append resultant to graph output variable
                                
                                NeuroOutput.RawTrainerOutput.append((datetime.datetime.fromtimestamp(NeuroCondSearch.CursorDataX[0][0]),datetime.datetime.fromtimestamp(NeuroCondSearch.CursorDataX[1][-1]))) #very first x coord

                        else: # if in training mode
                            if (bool_result):
                                #print "= TRAIN WAS OK; Xpoint:  " + str(xpoint)  + "computeConditionID: " + str(computeConditionID) + " normalizedAnalyzableDatasetID: " + str(normalizedAnalyzableDatasetID) + " normalizedSelectionPointDataID: " + str(normalizedSelectionPointDataID)
                                NeuroTrainer.mynet.trainquery(NeuroBasicConditions.allPointSelectionIds,NeuroBasicConditions.allConditionIds, computeConditionID)

                            
                            
                            
                            
from SecApp.DBQuestionClass import SecuQ
class NeuroBasicConditions(object):
    def __init__(self,key,depVarsLst,indepVarsLst):
        self.depVarsLst = depVarsLst
        self.indepVarsLst = indepVarsLst
        self.key = key
        self.initQ = SecuQ(self.key)
        '''
        available parameters used to construct conditions
        '''
        #analytics conditions
        self.baseconditions = ["increase"]
        self.pointofinteresttype = ["localmax"]
        #more to be added
        #baseconditions = {"increase":1,"decrease":2,"MA14_increase":3,"MA14_decrease":4}
        self.phasedeltas = [2,3,4,5,6,7,14,21] #how much data in each segment 
        self.phaseshifts = [1,2,3,4,5,6,7,14,21] # how much data is shifted from phase ( x coord[date])
    
        '''
        constructed conditions (with different maps for easy access)
        '''

    
        NeuroBasicConditions.conditionsConfig = {} #analysis algo conditions
        NeuroBasicConditions.conditionLookupId = {}
        NeuroBasicConditions.idLookupCondtion = {}
        NeuroBasicConditions.allConditionIds = []
        NeuroBasicConditions.DatasetConditions = {}
        
    
    
        NeuroBasicConditions.pointSelectionConfig = {} #dependant IDs point selection algo
        NeuroBasicConditions.pointSelectionLookupId = {}
        NeuroBasicConditions.idLookupPointSelection = {}
        NeuroBasicConditions.allPointSelectionIds = []
    
    
    
    
        NeuroBasicConditions.datasetConfig = {} #independantID datasets available
        NeuroBasicConditions.datasetLookupId = {}
        NeuroBasicConditions.idLookupDataset = {}
        NeuroBasicConditions.allDatasetIds = []
        
    
        '''
        this holds starting id numbers for configurtation data 
        '''
        ###
        self.depIDcount = 300
        
        self.indepIDcount = 500
        
        self.condIDcount = 700
    
        self.buildselectionpointIDs()
        self.buildindependantIDs()
        self.buildconditions()

    
    

    
    
    def getNormConstant(self,varkey):  # for variables only
        if (varkey in self.initQ.multipoint.keys()) & (varkey in self.initQ.aggregate.keys()):
            #self.varTypes_v2t_dict[varkey] = 'mp_aggre' # multipoint with aggregate data in dailykey, "keyname"_aggregate:value
            
            #self.varTypes_id2t_dict[self.variable_v2id_dict[varkey]] = 'mp_aggre'
            raise Exception("NO MULTI-AGREGATE VARIABLES (IN ALPHA)")
            return False #breakloop
            
        if (varkey in self.initQ.aggregate.keys()):
            return datetime.timedelta(days = 1 )
        
        if (varkey in self.initQ.multipoint.keys()):
            return datetime.timedelta(minutes = 30 )
            
        if (varkey in self.initQ.active.keys()):
            return datetime.timedelta(days = 1 )
  
    
    
    def buildselectionpointIDs(self): #builddependantIDs
        for pointselectionalgo in self.pointofinteresttype:
            for var in self.depVarsLst:
                
                builtPointSelectionTmp = str(var) + "-" + str(pointselectionalgo)+ "-" + str(self.depIDcount)
                NeuroBasicConditions.pointSelectionConfig[builtPointSelectionTmp] = {}
                NeuroBasicConditions.pointSelectionConfig[builtPointSelectionTmp]["pointSelectSet"] = var
                NeuroBasicConditions.pointSelectionConfig[builtPointSelectionTmp]["selection_algo"] = pointselectionalgo
                NeuroBasicConditions.pointSelectionConfig[builtPointSelectionTmp]["ID"] = self.depIDcount
                NeuroBasicConditions.pointSelectionConfig[builtPointSelectionTmp]["NormConstant"] = self.getNormConstant(var)
              
                NeuroBasicConditions.pointSelectionLookupId[builtPointSelectionTmp] = self.depIDcount
            
                NeuroBasicConditions.idLookupPointSelection[self.depIDcount] = builtPointSelectionTmp
            
                NeuroBasicConditions.allPointSelectionIds.append(self.depIDcount)
            
                self.depIDcount+= 1
        return self
            
                
            
            
    def buildindependantIDs(self): #build analyzable (comparable dataset) ids
        for var in self.indepVarsLst:
            NeuroBasicConditions.datasetConfig[var] = {}
            NeuroBasicConditions.datasetConfig[var]["ID"] = self.indepIDcount
            NeuroBasicConditions.datasetConfig[var]["NormConstant"] = self.getNormConstant(var)
            
            NeuroBasicConditions.datasetLookupId[var] = self.indepIDcount
            
            NeuroBasicConditions.idLookupDataset[self.indepIDcount] = var
            
            NeuroBasicConditions.allDatasetIds.append(self.indepIDcount)
            
            
            self.indepIDcount+=1
        return self

    
    def buildconditions(self): # add [haseshifts]
        for var in NeuroBasicConditions.datasetConfig.keys():
            currVarID = NeuroBasicConditions.datasetConfig[var]["ID"]
            NeuroBasicConditions.DatasetConditions[currVarID] = []
            
            for condition in self.baseconditions:
                for delta in self.phasedeltas:
                    for shift in self.phaseshifts:
                        
                        
                    
                        builtconditiontmp = str(condition) + "-" + str(currVarID)+ "-" + str(delta)+ "-" + str(shift)
                    
                        
                        NeuroBasicConditions.conditionsConfig[builtconditiontmp] = {}
                        NeuroBasicConditions.conditionsConfig[builtconditiontmp]["analyze"] = currVarID
                        NeuroBasicConditions.conditionsConfig[builtconditiontmp]['condition'] = condition
                        NeuroBasicConditions.conditionsConfig[builtconditiontmp]['delta'] = delta
                        NeuroBasicConditions.conditionsConfig[builtconditiontmp]['shift'] = shift
                        NeuroBasicConditions.conditionsConfig[builtconditiontmp]['ID'] = self.condIDcount
                        
                        
                        NeuroBasicConditions.DatasetConditions[currVarID].append(self.condIDcount)
                        
                        NeuroBasicConditions.idLookupCondtion[self.condIDcount] = builtconditiontmp
                    
                        NeuroBasicConditions.conditionLookupId[builtconditiontmp] = self.condIDcount
                    
                        NeuroBasicConditions.allConditionIds.append(self.condIDcount)
                    
                        self.condIDcount+=1
        return self
    

class NeuroPoints(object):
    def __init__(self,ID,datasetX,datasetY):      
        self.datasetX = datasetX
        self.datasetY = datasetY
        self.datasetID = ID
        
        ## must be initialized before hand
        self.PointTypeName = NeuroBasicConditions.idLookupPointSelection[self.datasetID]
        self.datasetParams = NeuroBasicConditions.pointSelectionConfig[self.PointTypeName]
        
        ##class variable
        NeuroPoints.XpointsofInterest = None
        
        self.runop()
        
        
    def runop(self):
        '''
        These must correspond to the methods available in NeuroBasic Conditions under key
        self.pointofinteresttype = ["localmax"]
        '''
        if (self.datasetParams["selection_algo"] == "localmax" ):
            NeuroPoints.XpointsofInterest = self.FindMaximalpos(self.datasetX,self.datasetY)
            return True
        
        
     # finds points of interest in dependant variable (phase points)
    def FindMaximalpos(self,aX,aY):
        '''
        Input aligned:
        x array
        y array
        
        Output (X):
        array[x_dto ,....]
        
        '''
        maximaposX = []
        length = len(aY)
        if length >= 2:
            if aY[0] > aY[1]:
                maximaposX.append(aX[0])
    
           
        if length > 3:
            for i in range(1, length-1):     
                if aY[i] > aY[i-1] and aY[i] > aY[i+1]:
                    maximaposX.append(aX[i])
    
    
        if aY[length-1] > aY[length-2]:
            maximaposX.append(aX[length-1])
           
        #print "maximaposX " + str(maximaposX)
        return maximaposX
    
    
class NeuroCondSearch(object):
    ''' 
    this class defines all the conditional operations available to be performed on normalized data
    
    '''

    def __init__(self,datasetX,datasetY):
        
        self.datasetX = datasetX
        self.datasetY = datasetY
        
    
    def setID(self,ID): #id is the condition you want to search
        #temporary lookup operation
        conditionName = NeuroBasicConditions.idLookupCondtion[ID]
        #assign constants
        self.CursorShift = NeuroBasicConditions.conditionsConfig[conditionName]['shift']
        self.CursorDelta = NeuroBasicConditions.conditionsConfig[conditionName]['delta']
        #assign method
        self.method = NeuroBasicConditions.conditionsConfig[conditionName]['condition']
    
    def runop(self,XSelectionPoint):
        #print "XSelectionPoint " + str(XSelectionPoint) 
        self.XSelectionPoint = XSelectionPoint
        
        if (self.method == "increase"):
            return self.Method_increase()
    

    def single_output(self): #special method for processing with graph output
        
        
        
        
        '''
        Methods for processing data, return is always boolean
    
        '''
        
    def Method_increase(self):
               
        #Phase point array
        self.error = False # if there is an error anywhere
        self.phase_shift_delta_sample_cursor()
        return self.sectionincrease()
        
        '''
        processing helpers
        '''
        
    def phase_shift_delta_sample_cursor(self):
        '''
        Only two sets are computed using this
        
        index 0 used as the phase point, then delta searches backwards in time
        self.CursorX = :
        self.CursorY =
        array[(x_dto,y)], array[(x_dto,y]
        
        '''
        #shift
        
        #self.CursorShift
        
        #delta
        #self.CursorDelta
        
        #phase
        #print self.datasetX
        #print "=================================================================="
        #print self.XSelectionPoint
        
        try:
            phaseIndex = self.datasetX.index(self.XSelectionPoint)
        except: 
            '''
            Key error pretty sure, if there is an error, 
            the selection point variable is a multipoint type variable, 
            therefore if compared to a variable with daily type, their normalization was not the same and 
            therefore will have points that dont match.
            
            to fix:
            solution 1 (harder): findout if multipoint is being compared to daily type before normalization, 
            then adjust normalization constant accordingly ( will have problems re-calling data afterwards)
            
            solution 2:
            
            
            solution 3: (bad/lazy):
            ignore it and say FALSE
            
            
            '''
            
            self.error = True
            return self #exit loop
        
        
        
        shiftIndex = phaseIndex - self.CursorShift
        
        x0 = shiftIndex
        x1 = shiftIndex - self.CursorDelta
        x2 = x1 - self.CursorDelta
        delta0X = []
        delta0Y = []
        delta1X = []
        delta1Y = []
        
        # both sets left to right, forward in time
        try:
            for i in xrange(x1,x0):
                delta0X.append(self.datasetX[i])
                delta0Y.append(self.datasetY[i])
            for i in xrange(x2,x1):
                delta1X.append(self.datasetX[i])
                delta1Y.append(self.datasetY[i])
        except:
            self.error = True
            return self #exit loop
            
        # left to right
        NeuroCondSearch.CursorDataY = delta1Y,delta0Y # output Y coords 
        NeuroCondSearch.CursorDataX = delta1X,delta0X # output Y coords
        return self
            
            
        
        
        
        
        
        
        
        
        
    
    def sectionincrease(self): #only for comparing two sets
        
        '''
        input section list[(tuple),(tuple)] 
        (tuple) = 
        
        output tuple(x_dto,boolean)
        
        self.Cursor
        
        '''
        #check error processing error level
        if (self.error): # if there's an error exit and return point as false to trainer
            return False
        
        #self.CursorData, left to right
        #using average of list
        av1 = reduce(lambda y1, y2: y1 + y2, NeuroCondSearch.CursorDataY[0]) / len(NeuroCondSearch.CursorDataY[0])
        av2 = reduce(lambda y1, y2: y1 + y2, NeuroCondSearch.CursorDataY[1]) / len(NeuroCondSearch.CursorDataY[1])
        if (av1<av2): # if left smaller than right, increased forward in time
            return True
        else:
            return False
        
        
    def allincreases(self):
        '''
        
        input:
        
        
        '''
        
        
        
        
import datetime
from SecNeural import nn
from SecNeural.ClassAlignmentSubsystem import DataNormalization
from SecApp.DBOutputClass import SecuFrame


class NeuroBasicAlgo(NeuroBasicConditions,NeuroTrainer,NeuroPoints,NeuroCondSearch,NeuroResolve,NeuroOutput):
    '''
    ex:
    algoConfig = {"algo_id" = "SOME HEX" , "algoName":"Basic", "algoMode":"Basic" "independantVars":["some var","some var"]  , "dependantVars":["some var","some var"]}
    '''
    def __init__(self,key,algoConfig):
        self.key = key
        self.algoConfig = algoConfig
        self.GraphOutput = None
        self.runalgo()


    def runalgo(self):
        self.parseconfig()
        
        
        #creates conditional id subsystem
        NeuroBasicConditions.__init__(self,self.key,self.dependantVars,self.independantVars) ## FINISH initialization
        
        NeuroTrainer.__init__(self) #init
        self.build_neural_net() # pass neural database object to neural trainer
        self.train_neural_net()
        self.resolve_neural_net()

        #print self.GraphOutput
        return True

    def parseconfig(self):
        self.neuroStore = str(self.algoConfig["algo_id"]) + "_Basic.db"
        self.dependantVars = sorted(self.algoConfig["dependantVars"], key=str.lower)
        #independant variables always sorted alphabetically to ensure ID replication
        self.independantVars = sorted(self.algoConfig["independantVars"], key=str.lower)
        return self
        
    def build_neural_net(self):
        NeuroTrainer.mynet = nn.searchnet() # nn.searchnet(self.neuroStore) deprecated using ':memory:'
        NeuroTrainer.mynet.maketables()
        ####
        '''
        self.mynet.generatehiddennode( [   all condition ids for each analyzable dataset   ] , [  all point of interest ids   ] )
        
        self.mynet.generatehiddennode([dataids['dependant_data'],dataids['independant_data']],allconditionids(phasedeltas))
        '''
        
        NeuroTrainer.mynet.generatehiddennode(NeuroBasicConditions.allPointSelectionIds,NeuroBasicConditions.allConditionIds)
        return self
           
    def train_neural_net(self):
        #aquire data
        NeuroTrainer.aquiredata(self)
        NeuroTrainer.methodBasicTrain(self)
        return self    
    
    def resolve_neural_net(self):
        NeuroResolve.__init__(self)
        
        
        #print NeuroResolve.byConditionIDs
        
        
        #print NeuroResolve.byConditionNames
            
        #print NeuroResolve.pairedResults
        
        NeuroOutput.__init__(self)
        NeuroOutput.basic_get_top(self)
        NeuroOutput.basic_generate_graph(self)
        self.GraphOutput = NeuroTrainer.initDO.AgraphFrame
        return self
        