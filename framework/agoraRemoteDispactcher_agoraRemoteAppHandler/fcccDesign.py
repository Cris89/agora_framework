from pyDOE import *
from configuration import configuration

class fcccDesign():
    '''
    face centered central composite design (with one center point) generation
    ''' 
    def __init__( self, paramsValues, numOPs ):
        '''
        Constructor
        '''
        self.paramsValues = paramsValues
        self.numOPs = numOPs
        
        self.configurations = []
    
    def buildConfigurations( self ):
        ccd = ccdesign( len(self.paramsValues), center = (1, 0), face = "ccf" )
         
        for indexCCD, itemCCD in enumerate( ccd ):
            conf = []
            
            for indexRow, itemRow in enumerate( itemCCD ):
                parameterValues = self.paramsValues[indexRow]
                
                # value == 1 --> MAXValue of the corresponding parameter
                if itemRow == 1:
                    conf.append( parameterValues[-1] )
                    
                # value == -1 --> minValue of the corresponding parameter
                elif itemRow == -1:
                    conf.append( parameterValues[0] )
                    
                # value == 0 --> medianValue of the corresponding parameter
                elif itemRow == 0:
                    conf.append( parameterValues[ int( (len(parameterValues) / float(2)) - 0.5 ) ] )
            
            config = configuration( conf, self.numOPs )
            self.configurations.append( config )
        
        return self.configurations