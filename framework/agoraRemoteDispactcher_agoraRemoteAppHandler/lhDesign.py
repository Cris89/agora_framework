from pyDOE import *
from configuration import configuration

class lhDesign():
    '''
    latin-hypercube random design generation
    ''' 
    def __init__( self, paramsValues, numSamples, numOPs ):
        '''
        Constructor
        '''
        self.paramsValues = paramsValues
        self.numSamples = numSamples
        self.numOPs = numOPs
        
        self.configurations = []
    
    def buildConfigurations( self ):
        lhd = lhs( len(self.paramsValues), samples = self.numSamples )
        
        for indexLHD, itemLHD in enumerate( lhd ):
            conf = []
            
            for indexRow, itemRow in enumerate( itemLHD ):
                parameterValues = self.paramsValues[indexRow]
                
                conf.append( parameterValues[ int( len(parameterValues) * itemRow - 0.5 ) ] )
            
            config = configuration( conf, self.numOPs )
            self.configurations.append( config )
        
        return self.configurations