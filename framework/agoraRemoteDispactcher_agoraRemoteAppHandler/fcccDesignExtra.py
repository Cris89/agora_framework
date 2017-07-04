from pyDOE import *
from configuration import configuration

class fcccDesignExtra():
    '''
    face centered central composite design (with one center point) generation
    plus
    latin-hypercube random design generation
    ''' 
    def __init__( self, paramsValues, numSamples, numOPs ):
        '''
        Constructor
        '''
        self.paramsValues = paramsValues
        self.numSamples = numSamples
        self.numOPs = numOPs

        self.fcccdConfigurations = []
        self.lhdConfigurations = []

        self.configurationsObjectsList = []
    
    def buildConfigurations( self ):
        # fcccd configurations
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
            
            self.fcccdConfigurations.append( conf )

        # lhd configurations
        lhdAgain = True

        while( lhdAgain == True ):
            self.lhdConfigurations = []

            lhd = lhs( len(self.paramsValues), samples = self.numSamples )

            for indexLHD, itemLHD in enumerate( lhd ):
                found = False

                conf = []
                
                for indexRow, itemRow in enumerate( itemLHD ):
                    parameterValues = self.paramsValues[indexRow]
                    
                    conf.append( parameterValues[ int( len(parameterValues) * itemRow - 0.5 ) ] )

                if( conf in self.fcccdConfigurations ):
                    found = True
                    break

                else:
                    self.lhdConfigurations.append( conf )

            if( found == False ):
                lhdAgain = False
        
        for conf in self.fcccdConfigurations:
            config = configuration( conf, self.numOPs )
            self.configurationsObjectsList.append( config )

        for conf in self.lhdConfigurations:
            config = configuration( conf, self.numOPs )
            self.configurationsObjectsList.append( config )

        return self.configurationsObjectsList        