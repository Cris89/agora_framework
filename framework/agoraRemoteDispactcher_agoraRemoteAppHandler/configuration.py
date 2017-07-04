class configuration():
    def __init__( self, conf, num ):
        '''
        Constructor
        '''
        self.conf = conf
        self.numOPs = num
    
    
    
    

    def getConf( self ):
        return self.conf
    
    
    
    
    
    def getNumOPs( self ):
        return self.numOPs
    
    def decrementNumOPs( self ):
        self.numOPs -= 1