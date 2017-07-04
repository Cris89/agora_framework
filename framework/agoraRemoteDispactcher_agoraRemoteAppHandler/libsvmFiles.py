import math

class libsvm():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.listValues = []
    
    def insertInput( self, values ):
        self.listValues = values
    
    def lnFeature( self, numFeature ):
        for i in range( len(self.listValues[numFeature]) ):
            self.listValues[numFeature][i] = math.log( float(self.listValues[numFeature][i]) )
    
    def invFeature( self, numFeature ):
        for i in range( len(self.listValues[numFeature]) ):
            self.listValues[numFeature][i] = 1 / float(self.listValues[numFeature][i])
            
    def sqrtFeature( self, numFeature ):
        for i in range( len(self.listValues[numFeature]) ):
            self.listValues[numFeature][i] = math.sqrt( float(self.listValues[numFeature][i]) )

    def correctMetrics( self, linkFunction ):
        if linkFunction == "log":
            # delete values < limit
            limit = 0.003
            
            elementsToRemove = []
            
            for i in range( len(self.listValues[0]) ):
                if float( self.listValues[0][i] ) < limit:
                    elementsToRemove.append(i)
            
            elementsToRemove.reverse()
                    
            for element in elementsToRemove:
                for sequence in self.listValues:
                    del sequence[element]
    
    def libsvmfile( self, filename ):
        f = open( filename, "a" )
        
        for j in range( len(self.listValues[0]) ):
            for i in range( len(self.listValues) ):
                if( i < len(self.listValues) - 1 ):
                    f.write( str(self.listValues[i][j]) + " " + str(i + 1) + ":" )
                    
                else:
                    f.write( str(self.listValues[i][j]) + "\n" )
                    
        f.close()