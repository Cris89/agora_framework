from configuration import configuration
import itertools

class fullFactDesign():
    '''
    full factorial design generation
    ''' 
    def __init__( self, paramsValues, numOPs ):
        '''
        Constructor
        '''
        self.paramsValues = paramsValues
        self.numOPs = numOPs
        
        self.configurations = []
    
    def buildConfigurations( self ):
        cartesianProduct = itertools.product( *self.paramsValues )

        for tupla in cartesianProduct:
            conf = []

            for value in tupla:
                conf.append( value )

            config = configuration( conf, self.numOPs )
            self.configurations.append( config )
        
        return self.configurations