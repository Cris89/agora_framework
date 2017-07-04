import copy
import csv
import itertools
from libsvmFiles import libsvm
import os
import shutil
import subprocess

class sparkGenLinearRegr2nd():
    '''
    classdocs
    '''
    def __init__( self, app, metrs, transforms, paramVs, OPs, partialModel):
        '''
        Constructor
        '''
        self.tesiCris = "/home/cris/Documents/tesiCris/"
        self.sparkFolderDir = "/home/cris/spark-2.1.0-bin-hadoop2.7/"
        
        self.appName = app
        
        self.sparkFolder = self.tesiCris + self.appName + "/spark/"
        
        # the order of the metrics must be the same here and in the opsList
        # es.: [ "avg_error", "avg_throughput" ]
        self.metrics = metrs
        
        # orderedDict
        # the order of the metrics must be the same here and in the opsList
        # es.: (key, value): ( "avg_throughput", ["ln", "ln", "gaussian", "log"] )
        self.transformations = transforms
        
        self.paramsValues = paramVs

        # compute the number of terms of the polynomial expansion of parameters
        # grade 1 terms
        self.polyExpNumTerms = len( self.paramsValues )
        # cross product terms
        for i in range( len(self.paramsValues) -1 ):
            for j in range( i + 1, len(self.paramsValues) ):
                self.polyExpNumTerms += 1
        # square terms
        self.polyExpNumTerms += len( self.paramsValues )
        
        # parameters and metrics (in this order)
        # es.: [ [1.0, 1.0, 1.0], [100000.0, 100000.0, 100000.0], [5.4573, 6.0573, 5.7573], [32.584, 31.004, 33.0] ]
        self.OPsList2nd = [ [] for _ in range( self.polyExpNumTerms + len(self.metrics) ) ]       
        self.buildOPsList2nd( OPs )

        # all the possible configurations
        # (testing list values,
        # with witch spark will generate the complete model
        # that also contain
        # the relative polynomial expansion)
        # es.: [ [6, 6, 6, 6, 6, ...], [1, 1, 1, 1, 1, ...], [100000, 200000, 300000, 400000, 500000, ...] ]
        self.testing = [ [] for _ in range( self.polyExpNumTerms + 1 ) ]
        self.buildTestingValues()

        self.DoEModel = partialModel
        
        # spark folder
        self.manageSparkFolder()
        
        # popen variables
        self.comand = self.sparkFolderDir + "bin/pyspark"
        self.args = self.comand.split(" ")
    
    def buildOPsList2nd( self, OPs ):
        for string in OPs:
            string = string.replace( ":", " " )
            
            splitted = string.split(" ")

            # grade 1 terms
            for i in range( len(self.paramsValues) ):
                self.OPsList2nd[i].append( float(splitted[i]) )
            
            currentIndex = len(self.paramsValues)

            # cross product terms
            for i in range( len(self.paramsValues) - 1 ):
                for j in range( i + 1, len(self.paramsValues) ):
                    crossProduct = float( splitted[i] ) * float( splitted[j] )
                    self.OPsList2nd[currentIndex].append( crossProduct )
                    currentIndex += 1

            # square terms
            for i in range( len(self.paramsValues) ):
                square = float( splitted[i] ) * float( splitted[i] )
                self.OPsList2nd[currentIndex].append( square )
                currentIndex += 1

            # metrics terms
            for i in range( len(self.paramsValues), len(splitted) ):
                self.OPsList2nd[currentIndex].append( float( splitted[i] ) )
                currentIndex += 1
    
    def buildTestingValues( self ):
        # create all the possible configurations (testing list values,
        # with witch spark will generate the complete ops list)
        fakePrediction = 6
        
        cartesianProduct = itertools.product( *self.paramsValues )
        
        for tupla in cartesianProduct:
            self.testing[0].append( fakePrediction )
            for i in range( len(tupla) ):
                self.testing[i + 1].append( tupla[i] )

            currentIndex = len(tupla) + 1

            # cross products
            for i in range( len(tupla) - 1 ):
                for j in range( i + 1, len(tupla) ):
                    crossProduct = tupla[i] * tupla[j]
                    self.testing[currentIndex].append( crossProduct )
                    currentIndex += 1

            # square terms
            for term in tupla:
                square = term * term
                self.testing[currentIndex].append( square )
                currentIndex += 1
    
    def manageSparkFolder( self ):
        # spark folder
        if( os.path.isdir( self.sparkFolder ) == True ):
            shutil.rmtree( self.sparkFolder )
            
        # es.: /home/cris/Documents/tesiCris/swaptions/spark
        os.makedirs( self.sparkFolder )
    
    def buildModel( self ):
        # start spark subprocess
        sparkProc = subprocess.Popen( self.args, stdin = subprocess.PIPE )

        if( len( self.transformations ) > 0 ):
            # I know the transformations
            self.knownModel( sparkProc )
             
        else:
            # I don't know the transformations --> bruteforce
            self.unknownModel( sparkProc )
                                
        # wait spark subprocess to terminate        
        sparkProc.communicate()
        
        return self.finalModel()
    
#     def knownModel( self, sparkProc ):
#         # possible parameters transformations, final libsvm files
#         lib = libsvm()
        
#         sparkProc.stdin.write( "from pyspark.ml.regression import GeneralizedLinearRegression\
# \nfrom pyspark.sql import SparkSession" )  
#         sparkProc.stdin.write( "\n\nspark = SparkSession.builder.appName(\"LinearRegression\").getOrCreate()" )            
                        
#         for metric in self.transformations.items():
#             # es.: metric[0]: "avg_throughput"
#             #      metric[1]: ["ln", "ln", "gaussian", "log"]       
            
#             # es.: "gaussian"
#             family = metric[1][ len(self.paramsValues) ]
#             # es.: "log"
#             link = metric[1][ len(self.paramsValues) + 1 ]
            
#             sparkProc.stdin.write( "\n\n\n\n# " + metric[0] )
                
#             sparkProc.stdin.write( "\n\nglr_" + metric[0] + " = GeneralizedLinearRegression( family = \"" + family + "\", link = \"" + link + "\", maxIter = 10 )" )       
            
#             # training file
            
#             # training list values
#             training = []          
            
#             # add metric values to training list
#             metricV = copy.deepcopy( self.OPsList2nd[ len(self.paramsValues) + 
#                                           self.transformations.keys().index(metric[0]) ] )
#             training.append( metricV )
            
#             # add parameters values to training list
#             for feature in range( 0, len(self.paramsValues) ):
#                 featureV = copy.deepcopy( self.OPsList2nd[feature] )
#                 training.append( featureV )
                
#             lib.insertInput( training )
            
#             trainingFilename = "training_" + metric[0] + "_"
            
#             for feature in range( 0, len(self.paramsValues) ):
#                 if( metric[1][feature] == "id" ):
#                     trainingFilename += "id" + str(feature + 1)
                    
#                 elif( metric[1][feature] == "ln" ):
#                     lib.lnFeature( feature + 1 )
                     
#                     trainingFilename += "ln" + str(feature + 1)
                 
#                 elif( metric[1][feature] == "sqrt" ):
#                     lib.sqrtFeature( feature + 1 )
                     
#                     trainingFilename += "sqrt" + str(feature + 1)
                 
#                 elif( metric[1][feature] == "inv" ):
#                     lib.invFeature( feature + 1 )
                     
#                     trainingFilename += "inv" + str(feature + 1)
            
#             # training modifications in order to let the linear regression work
#             # es.: if link function == "log", metrics must not be < limit value
#             lib.correctMetrics( link )
            
#             # final training libsvm file
#             lib.libsvmfile( self.sparkFolder + trainingFilename + ".txt" )
            
#             sparkProc.stdin.write( "\n\n\n# load " + metric[0] + " training data\
# \n" + trainingFilename + " = spark.read.format(\"libsvm\").load(\"" + self.sparkFolder + trainingFilename + ".txt\")" )
                                
#             sparkProc.stdin.write( "\n\n# fit " + metric[0] + " model on training data\
# \ntry:\
# \n\tmodel_" + metric[0] + " = glr_" + metric[0] + ".fit(" + trainingFilename + ")" )
            
#             sparkProc.stdin.write( "\n\nexcept Exception:\
# \n\tprint( \"" + metric[0] + ": can't fit its model\" )" )
            
#             # testing file
#             values = copy.deepcopy( self.testing ) 
#             lib.insertInput( values )
            
#             featuresTransformations = ""

#             for feature in range( 0, len(self.paramsValues) ):
#                 if( metric[1][feature] == "id" ):
#                     featuresTransformations += "id" + str(feature + 1)
                    
#                 elif( metric[1][feature] == "ln" ):
#                     lib.lnFeature( feature + 1 )
                     
#                     featuresTransformations += "ln" + str(feature + 1)
                 
#                 elif( metric[1][feature] == "sqrt" ):
#                     lib.sqrtFeature( feature + 1 )
                     
#                     featuresTransformations += "sqrt" + str(feature + 1)
                 
#                 elif( metric[1][feature] == "inv" ):
#                     lib.invFeature( feature + 1 )
                     
#                     featuresTransformations += "inv" + str(feature + 1)
            
#             testingFilename = "testing_" + metric[0] + "_" + featuresTransformations
#             # es.: "testing_avg_throughput_ln1ln2"
            
#             # final testing libsvm file
#             lib.libsvmfile( self.sparkFolder + testingFilename + ".txt" )
            
#             sparkProc.stdin.write( "\n\n# load " + metric[0] + " testing data\
# \n" + testingFilename + " = spark.read.format(\"libsvm\").load(\"" + self.sparkFolder + testingFilename + ".txt\")" )
                        
#             sparkProc.stdin.write( "\n\n# " + metric[0] + " predictions\
# \npredictions_" + metric[0] + " = model_" + metric[0] + ".transform(" + testingFilename + ")" )
            
#             sparkProc.stdin.write( "\n\nvalues_" + metric[0] + " = predictions_" + metric[0] + ".collect()" )
            
#             predictionsFilename = self.sparkFolder + "predictions_" + metric[0] + ".txt"
#             sparkProc.stdin.write( "\n\npreds_" + metric[0] + " = open(\"" + predictionsFilename + "\", \"a\")" )
            
#             sparkProc.stdin.write( "\n\npreds_" + metric[0] + ".write(\"model: " + featuresTransformations + "_" + link + "\" + \"\\n\")" )
            
#             sparkProc.stdin.write( "\n\nfor v in values_" + metric[0] + ":\
# \n\tpreds_" + metric[0] + ".write( str(v[\"prediction\"]) )\
# \n\tpreds_" + metric[0] + ".write(\"\\n\")" )
            
#             sparkProc.stdin.write( "\n\npreds_" + metric[0] + ".close()" )
    
    def unknownModel( self, sparkProc ):
        # possible parameters transformations, final libsvm files
        lib = libsvm()
        
        sparkProc.stdin.write( "from pyspark.ml.regression import GeneralizedLinearRegression\
\nfrom pyspark.sql import SparkSession" )
 
        sparkProc.stdin.write( "\n\nspark = SparkSession.builder.appName(\"LinearRegression2ndBruteForce\").getOrCreate()" )
        
        sparkProc.stdin.write( "\n\nglr_identity = GeneralizedLinearRegression( family = \"gaussian\", link = \"identity\" )" )
        sparkProc.stdin.write( "\nglr_log = GeneralizedLinearRegression( family = \"gaussian\", link = \"log\" )" )
        sparkProc.stdin.write( "\nglr_inverse = GeneralizedLinearRegression( family = \"gaussian\", link = \"inverse\" )" )
            
        for metric in self.metrics:
            # es.: "avg_throughput"
            
            sparkFolderMetricDir = self.sparkFolder + metric
            # es.: "/home/cris/Documents/tesiCris/swaptions/spark/avg_throughput"
            
            os.mkdir( sparkFolderMetricDir )
            
            # training list values
            training = []
            
            # add metric values to training list
            training.append( self.OPsList2nd[ self.polyExpNumTerms + 
                                          self.metrics.index(metric) ] )
            
            # add parameters values to training list
            for feature in range( self.polyExpNumTerms ):
                training.append( self.OPsList2nd[feature] )
        
            sparkProc.stdin.write( "\n\nmodels_AIC_meanCoeffStandErrs_index_Dict = {}" )
            sparkProc.stdin.write( "\nmodels = []" )
            sparkProc.stdin.write( "\ni = 0" )
        
            linkFunctions = ["identity", "log", "inverse" ]
             
            # transformations = ["id", "ln", "inv", "sqrt"]
            transformations = ["id"]
            cartesianProduct = itertools.product( transformations, repeat = self.polyExpNumTerms )
            # es.: 2 parameters --> 5 terms --> ("id", "id", "id", "id", "id"), ("id", "id", "id", "id", "ln"), ...

            for tupla in cartesianProduct:
                # es.: ("id", "id", "id", "id", "ln")
                
                # testing file
                values = copy.deepcopy( self.testing ) 
                lib.insertInput( values )
                 
                featuresTransformations = ""
                 
                for index, item in enumerate( tupla ):
                    if( item == "id" ):
                        featuresTransformations += item + str(index + 1)
                     
                    elif( item == "ln" ):
                        lib.lnFeature( index + 1 )
                        featuresTransformations += item + str(index + 1)
                         
                    elif( item == "inv" ):
                        lib.invFeature( index + 1 )
                        featuresTransformations += item + str(index + 1)
                     
                    elif( item == "sqrt" ):
                        lib.sqrtFeature( index + 1 )
                        featuresTransformations += item + str(index + 1)
                 
                testingFilename = "testing_" + featuresTransformations
                # es.: "testing_id1id2id3id4ln5"
                
                # final testing libsvm file
                lib.libsvmfile( sparkFolderMetricDir + "/" + testingFilename + ".txt" )
                
                for link in linkFunctions:
                    # es.: "log"
                    
                    # training file
                    values = copy.deepcopy( training )
                    lib.insertInput( values )
                     
                    featuresTransformations = ""
                     
                    for index, item in enumerate( tupla ):
                        if( item == "id" ):
                            featuresTransformations += item + str(index + 1)
                         
                        elif( item == "ln" ):
                            lib.lnFeature( index + 1 )
                            featuresTransformations += item + str(index + 1)
                             
                        elif( item == "inv" ):
                            lib.invFeature( index + 1 )
                            featuresTransformations += item + str(index + 1)
                         
                        elif( item == "sqrt" ):
                            lib.sqrtFeature( index + 1 )
                            featuresTransformations += item + str(index + 1)
                    
                    # training modifications in order to let the linear regression work
                    # es.: if link function == "log", metrics must not be < limit value
                    lib.correctMetrics( link )
                     
                    trainingFilename = "training_" + featuresTransformations + "_" + link
                    # es.: "training_id1id2id3id4ln5_log"
                    
                    # final training libsvm file
                    lib.libsvmfile( sparkFolderMetricDir + "/" + trainingFilename + ".txt" )
                    
                    sparkProc.stdin.write( "\n\n\n# Load training data\
\n" + trainingFilename + " = spark.read.format(\"libsvm\").load(\"" + sparkFolderMetricDir + "/" + trainingFilename + ".txt\")" )
                     
                    sparkProc.stdin.write( "\n\n# Fit the model on training data\
\nprint( \"" + metric + " - " + featuresTransformations + "_" + link + "\" )\
\n\ntry:\
\n\tmodel_" + featuresTransformations + "_" + link + " = glr_" + link + ".fit(" + trainingFilename + ")\
\n\n\t# Summarize the model over the training set\
\n\tsummary = model_" + featuresTransformations + "_" + link + ".summary\
\n\n\t# compute the mean of the coefficient standard errors\
\n\tsum = 0\
\n\tfor coefficient in summary.coefficientStandardErrors:\
\n\t\tsum += coefficient\
\n\tmeanCoefStandErrs = sum / len(summary.coefficientStandardErrors)" )
                     
                    sparkProc.stdin.write( "\n\nexcept Exception:\
\n\tprint( \"" + metric + " - " + featuresTransformations + "_" + link + ": can't fit this model\" )" )
                     
                    sparkProc.stdin.write( "\n\nelse:\
\n\tmodels.append(model_" + featuresTransformations + "_" + link + ")" )
                     
                    sparkProc.stdin.write( "\n\n\tmodels_AIC_meanCoeffStandErrs_index_Dict[\"" + featuresTransformations + "_" + link + "\"] = [ summary.aic, meanCoefStandErrs, i ]" )
                     
                    sparkProc.stdin.write( "\n\n\ti += 1" )
            
            sparkProc.stdin.write( "\n\n\nAICs_meansCoeffStandErrs_indexes = models_AIC_meanCoeffStandErrs_index_Dict.values()\
\nminAIC_meanCoeffStandErrs = min(AICs_meansCoeffStandErrs_indexes)" )
             
            sparkProc.stdin.write( "\n\nbestConfigurations = []\
\nfor configuration, aic_meanCoeffStandErrs_index in models_AIC_meanCoeffStandErrs_index_Dict.iteritems():\
\n\tif( aic_meanCoeffStandErrs_index[0] == minAIC_meanCoeffStandErrs[0] and aic_meanCoeffStandErrs_index[1] == minAIC_meanCoeffStandErrs[1] ):\
\n\t\tbestConfigurations.append(configuration)" )
             
            sparkProc.stdin.write( "\n\nconfName = bestConfigurations[0]\
\nsplitted = confName.split(\"_\")\
\ntestingName = splitted[0]" )
             
            sparkProc.stdin.write( "\n\n# Load testing data\
\ntesting = spark.read.format(\"libsvm\").load(\"" + sparkFolderMetricDir + "/testing_\" + testingName + \".txt\")" )
             
            sparkProc.stdin.write( "\n\n# Predictions on testing data of the best model\
\nindex = models_AIC_meanCoeffStandErrs_index_Dict[confName][2]\
\npred = models[index].transform(testing)" )
             
            sparkProc.stdin.write( "\n\nvalues = pred.collect()" )
             
            sparkProc.stdin.write( "\n\npredictions = open(\"" + self.sparkFolder + "predictions_" + metric + ".txt\", \"a\")" )
            
            sparkProc.stdin.write( "\n\npredictions.write(\"bruteforce - best model: \" + confName + \"\\n\")" )
             
            sparkProc.stdin.write( "\n\nfor v in values:\
\n\tpredictions.write( str(v[\"prediction\"]) )\
\n\tpredictions.write(\"\\n\")" )
             
            sparkProc.stdin.write( "\n\npredictions.close()\n" )

    def finalModel( self ):
        modelExists = True

        for metric in self.metrics:
            if( os.path.exists( self.sparkFolder + "predictions_" + metric + ".txt" ) == False ):
                modelExists = False

            break

        if( modelExists == True ):
            # collect all the predictions (list of metric predictions lists)
            predictions = []
             
            for metric in self.metrics:
                predictionsMetric = []
                with open( self.sparkFolder + "predictions_" + metric + ".txt", 'r' ) as csvfile:
                    tracereader = csv.reader( csvfile )
                    for row in tracereader:
                        for element in row:
                            predictionsMetric.append( element )
                
                # delete the first row with model info
                predictionsMetric.pop(0)
                
                predictions.append( predictionsMetric )        
            
            # create the complete ops list (strings with parameters and metrics values)
            model = []
            modelFile = open( self.tesiCris + self.appName + "/model.txt", "a" )
            
            for j in range( len( self.testing[0] ) ):
                op = ""
                
                for i in range( 1, len( self.paramsValues ) + 1 ):
                    if( i < len( self.paramsValues ) ):
                        op += str( self.testing[i][j] ) + " "
                    
                    else:
                        op += str( self.testing[i][j] ) + ":"
                
                for i in range( len(predictions) ):
                    if( i < len( predictions ) - 1 ):
                        op += str( predictions[i][j] ) + " "
                    
                    else:
                        op += str( predictions[i][j] )
                
                model.append( op )
                modelFile.write( op + "\n" )
            
            modelFile.close()

            return model

        else:
            modelFile = open( self.tesiCris + self.appName + "/model.txt", "a" )
            
            for op in self.DoEModel:
                modelFile.write( op + "\n" )
                
            return self.DoEModel