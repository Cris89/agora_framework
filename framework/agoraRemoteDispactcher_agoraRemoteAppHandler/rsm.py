from sparkGenLinearRegr import sparkGenLinearRegr
from sparkGenLinearRegr2nd import sparkGenLinearRegr2nd

class rsm():
    '''
    classdocs
    '''
    def __init__( self, struct ):
        '''
        Constructor
        '''
        self.appStruct = struct
    
    def buildRsm( self ):
        if( self.appStruct.getRsmKind() == "sparkGenLinRegr" ):
            rsm = sparkGenLinearRegr( self.appStruct.getName(),
                                      self.appStruct.getMetrics(),
                                      self.appStruct.getSparkGenLinearRegrTransforms(),
                                      self.appStruct.getParamsValues(),
                                      self.appStruct.getOPsList(),
                                      self.appStruct.getDoEsModelString() )
            return rsm.buildModel()

        elif( self.appStruct.getRsmKind() == "sparkGenLinRegr2nd" ):
            rsm = sparkGenLinearRegr2nd( self.appStruct.getName(),
                                      self.appStruct.getMetrics(),
                                      self.appStruct.getSparkGenLinearRegrTransforms(),
                                      self.appStruct.getParamsValues(),
                                      self.appStruct.getOPsList(),
                                      self.appStruct.getDoEsModelString() )
            return rsm.buildModel()

