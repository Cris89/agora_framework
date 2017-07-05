from sparkGenLinRegrTransforms import SparkGenLinRegrTransforms
from sparkGenLinRegrPolyComb2 import SparkGenLinRegrPolyComb2

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
        if( self.appStruct.getRsmKind() == "sparkGenLinRegrTransforms" ):
            rsm = SparkGenLinRegrTransforms( self.appStruct.getName(),
                                              self.appStruct.getMetrics(),
                                              self.appStruct.getSparkGenLinearRegrTransforms(),
                                              self.appStruct.getParamsValues(),
                                              self.appStruct.getOPsList(),
                                              self.appStruct.getDoEsModelString() )
            return rsm.buildModel()

        elif( self.appStruct.getRsmKind() == "sparkGenLinRegrPolyComb2" ):
            rsm = SparkGenLinRegrPolyComb2( self.appStruct.getName(),
                                            self.appStruct.getMetrics(),
                                            self.appStruct.getParamsValues(),
                                            self.appStruct.getOPsList(),
                                            self.appStruct.getDoEsModelString() )
            return rsm.buildModel()

