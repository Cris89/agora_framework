from pyDOE import *
from configuration import configuration

class ff2lDesign():
    '''
    2-level full-factorial design generation
    ''' 
    def __init__( self, paramsValues, numOPs ):
        '''
        Constructor
        '''
        self.paramsValues = paramsValues
        self.numOPs = numOPs
        
        self.configurations = []
    
    def buildConfigurations( self ):
        ff2l = ff2n( len(self.paramsValues) )
         
        for indexFF2L, itemFF2L in enumerate( ff2l ):
            conf = []
            
            for indexRow, itemRow in enumerate( itemFF2L ):
                parameterValues = self.paramsValues[indexRow]
                
                # value == 1 --> MAXValue of the corresponding parameter
                if itemRow == 1:
                    conf.append( parameterValues[-1] )
                    
                # value == -1 --> minValue of the corresponding parameter
                elif itemRow == -1:
                    conf.append( parameterValues[0] )
            
            config = configuration( conf, self.numOPs )
            self.configurations.append( config )
        
        return self.configurations