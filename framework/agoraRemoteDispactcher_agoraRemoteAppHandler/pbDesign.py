from pyDOE import *
from configuration import configuration

class pbDesign():
    '''
    Plackett-Burman design generation
    ''' 
    def __init__( self, paramsValues, numOPs ):
        '''
        Constructor
        '''
        self.paramsValues = paramsValues
        self.numOPs = numOPs
        
        self.configurations = []
    
    def buildConfigurations( self ):
        pbd = pbdesign( len(self.paramsValues) )
         
        for indexPBD, itemPBD in enumerate( pbd ):
            conf = []
            
            for indexRow, itemRow in enumerate( itemPBD ):
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