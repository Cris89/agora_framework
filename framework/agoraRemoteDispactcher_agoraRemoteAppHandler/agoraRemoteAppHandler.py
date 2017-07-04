from appStruct import appStruct
import csv
from doe import doe
import os
import paho.mqtt.client as paho
from rsm import rsm
import threading
import datetime

# ####################################################################################################
# ####################################################################################################
# ##########  DSE time
# ####################################################################################################
# ####################################################################################################
# start_dse_t = None
# end_dse_t = None
# ####################################################################################################
# ####################################################################################################
# ########## DSE time
# ####################################################################################################
# ####################################################################################################


####################################################################################################
# doeThread
####################################################################################################

class doeThread( threading.Thread ):
    def __init__( self, threadID, name, cond, struct ):
        threading.Thread.__init__( self )
        
        self.threadID = threadID
        self.name = name
        
        self.appStruct = struct
        
        self.cond = cond   
        
        self.doe = doe( struct )
        
    def run( self ):
        print( "\nstarting " + self.name + " thread" )
        
        with self.cond:
            self.cond.wait()



            # ####################################################################################################
            # ####################################################################################################
            # ########## DoE time
            # ####################################################################################################
            # ####################################################################################################
            # start_doe_t = datetime.datetime.now()
            
            configurations = self.doe.buildDoe()

            # end_doe_t = datetime.datetime.now()
            # delta_doe_t = end_doe_t - start_doe_t

            # times_f = "/home/cris/Documents/tests/" + self.appStruct.getName() + "/times.txt"
            # timesFile = open( times_f, "a" )

            # timesFile.write( "DoE: " + str( delta_doe_t.total_seconds() ) + " seconds" )
            # timesFile.write( "\n\n\n" )

            # timesFile.close()
            # ####################################################################################################
            # ####################################################################################################
            # ########## DoE time
            # ####################################################################################################
            # ####################################################################################################


            
            self.appStruct.setDoeConfs( configurations )
            self.appStruct.setDoeConfsNumber( len( self.appStruct.getDoeConfs() ) )
                    
            self.appStruct.setStatus( "dse" )



            # ####################################################################################################
            # ####################################################################################################
            # ########## start DSE time
            # ####################################################################################################
            # ####################################################################################################
            # global start_dse_t
            # start_dse_t = datetime.datetime.now()
            # ####################################################################################################
            # ####################################################################################################
            # ########## start DSE time
            # ####################################################################################################
            # ####################################################################################################


        
        self.appStruct.showStruct()
        
        print( "\nexiting " + self.name + " thread" )


####################################################################################################
# rsmThread
####################################################################################################
    
class rsmThread( threading.Thread ):
    def __init__( self, threadID, name, cond, struct ):
        threading.Thread.__init__( self )
        
        self.threadID = threadID
        self.name = name
        
        self.cond = cond
        
        self.appStruct = struct
        
        self.rsm = rsm( struct )
        
    def run( self ):
        print( "\nstarting " + self.name + " thread" )
        
        with self.cond:
            self.cond.wait()



            # ####################################################################################################
            # ####################################################################################################
            # ########## DSE time
            # ####################################################################################################
            # ####################################################################################################
            # global end_dse_t
            # end_dse_t = datetime.datetime.now()

            # delta_dse_t = end_dse_t - start_dse_t

            # times_f = "/home/cris/Documents/tests/" + self.appStruct.getName() + "/times.txt"
            # timesFile = open( times_f, "a" )

            # timesFile.write( "DSE: " + str( delta_dse_t.total_seconds() ) + " seconds" )
            # timesFile.write( "\n\n\n" )

            # timesFile.close()
            # ####################################################################################################
            # ####################################################################################################
            # ########## DSE time
            # ####################################################################################################
            # ####################################################################################################



            # ####################################################################################################
            # ####################################################################################################
            # ########## execution info
            # ####################################################################################################
            # ####################################################################################################
            # info_f = "/home/cris/Documents/tests/" + self.appStruct.getName() + "/info.txt"
            # infoFile = open( info_f, "a" )

            # infoFile.write( "DoE: " + self.appStruct.getDoeKind() + "\n")
            
            # if( self.appStruct.getDoeKind() == "lhd" ):
            #     infoFile.write( "numSamples: " + str( self.appStruct.getLhdSamples() ) + "\n")

            # infoFile.write( "numOPs: " + str( self.appStruct.getNumOPs() ) + "\n")

            # infoFile.write( "numHostpids: " + str( len( self.appStruct.getHostpids() ) ) )

            # infoFile.write( "\n\n\n" )

            # infoFile.close()
            # ####################################################################################################
            # ####################################################################################################
            # ########## execution info
            # ####################################################################################################
            # ####################################################################################################


            
            self.appStruct.setStatus( "buildingTheModel" )
            


            # ####################################################################################################
            # ####################################################################################################
            # ########## predicted model time
            # ####################################################################################################
            # ####################################################################################################
            # start_model_t = datetime.datetime.now()

            if( self.appStruct.getDoeKind() == "fullFact" or self.appStruct.getRsmKind() == "noRSM" ):
                # first case: I already have the complete model since I have explored all the possible configurations
                # second case: Rsm is not required --> the partial model is used
                model = self.appStruct.getDoEsModelString()

            else:
                self.appStruct.featuresBecomeParams()

                self.appStruct.showStruct()

                model = self.rsm.buildRsm()

            # end_model_t = datetime.datetime.now()

            # delta_model_t = end_model_t - start_model_t

            # times_f = "/home/cris/Documents/tests/" + self.appStruct.getName() + "/times.txt"
            # timesFile = open( times_f, "a" )

            # timesFile.write( "model_prediction: " + str( delta_model_t.total_seconds() ) + " seconds" )
            # timesFile.write( "\n\n\n" )

            # timesFile.close()
            # ####################################################################################################
            # ####################################################################################################
            # ########## predicted model time
            # ####################################################################################################
            # ####################################################################################################



            self.appStruct.setModel( model )



            # ####################################################################################################
            # ####################################################################################################
            # ########## predicted model
            # ####################################################################################################
            # ####################################################################################################
            # predicted_model_f = "/home/cris/Documents/tests/" + self.appStruct.getName() + "/predicted_model.txt"
            # modelFile = open( predicted_model_f, "a" )

            # infoRow = ""

            # for param in self.appStruct.getParams():
            #     infoRow += param + " "

            # for metric in self.appStruct.getMetrics():
            #     infoRow += metric + " "

            # modelFile.write(infoRow + "\n")

            
            # for op in model:
            #     op = op.replace( ":", " " )

            #     modelFile.write(op + "\n")

            # modelFile.close()
            # ####################################################################################################
            # ####################################################################################################
            # ########## predicted model
            # ####################################################################################################
            # ####################################################################################################


            
            self.appStruct.setStatus( "autotuning" )
            
            self.appStruct.showStruct()
        
        print( "\nexiting " + self.name + " thread" )


####################################################################################################
# AgoraRemoteAppHandler
####################################################################################################

class AgoraRemoteAppHandler():

    def __init__( self ):
        '''
        constructor
        '''
        self.IPaddress = "127.0.0.1"
        self.brokerPort = "8883"

        self.clientID = "AgoraRemoteAppHandler"
        self.qos = 0
        
        self.root = "/home/cris/Documents/"
        self.agora = "agora/"
        
        self.newHostpidTopic = None
        self.agoraLocalAppHandlerReqTopic = None
        self.communicationTopic = None
        self.receiveInfoTopic = None
        self.receiveInfoTopic_NoMultiLevel = None
        self.OPsTopic = None
        self.disconnectionTopic = None
        
        self.struct = None
        self.doe = None
        
        self.client = None
        
        self.thread_doe = None
        self.thread_rsm = None
        
        self.doeCond = None
        self.rsmCond = None

        self.DoEModelSent = []
    
    

    ####################################################################################################
    # MQTT
    ####################################################################################################
    
    def on_connect( self, IPaddress, brokerPort ):
        print( "\nclient ID: " + self.client._client_id + " connected at " + IPaddress + ":" + brokerPort )
    
    def on_subscribe( self, topic ):
            print( "\nsubscription" )
            print( "topic: " + topic )
     
    def on_message( self, client, userdata, msg ):
        print( "\nreceived message" )
        print( "topic: " + msg.topic )
        print( "payload: " + msg.payload )
        
        if( msg.topic == self.newHostpidTopic ):
            # new AgoraLocalAppHandler (hostpid) arrived
            self.manageNewHostpid( msg.payload )
        
        elif( msg.topic == self.agoraLocalAppHandlerReqTopic ):
            # an AgoraLocalAppHandler (hostpid) made a request
            if( self.struct.getStatus() == "unknown" ):
                # se non conosco nulla dell'applicazione
                self.requestAppInfo()        
            
            elif( self.struct.getStatus() == "dse" ):
                # se ci sono configurazioni da eseguire    
                self.sendConfiguration( msg.payload )

            elif( self.struct.getStatus() == "buildingTheModel" ):
                # se il modello non e' ancora pronto    
                self.sendDoEsModel( msg.payload )
            
            elif( self.struct.getStatus() == "autotuning" ):
                # se esiste il modello completo
                self.sendModel( msg.payload )

        elif( msg.topic == self.disconnectionTopic ):
            # an AgoraLocalAppHandler (hostpid) has disconnected
            self.struct.removeHostpid( msg.payload )

            if( self.struct.getStatus() == "receivingInfo" and self.struct.getInfoHostpid() == msg.payload ):
                self.struct.refreshStruct()

                self.requestAppInfo()

        elif( self.receiveInfoTopic_NoMultiLevel in msg.topic ):
            # received app info

            #topic es.: "agora/swaptions/info/crisXPS15_1897"
            splittedTopic = msg.topic.split("/")
            senderHostpid = splittedTopic[-1]
            
            if( self.struct.getStatus() == "unknown" ):
                self.struct.setStatus( "receivingInfo" )
                self.struct.setInfoHostpid( senderHostpid )

            if( senderHostpid == self.struct.getInfoHostpid() ):
                with self.doeCond:
                    splitted = msg.payload.split(" ")
                    
                    if( splitted[0] == "metric" ):
                        self.struct.addMetric( splitted[1] )
                        
                    elif( splitted[0] == "param" ):
                        self.struct.addParam( splitted[1] )
                        
                        values = []
                        
                        if( splitted[2] == "range" ):
                            value = float( splitted[3] )
                            MAXvalue = float( splitted[4] )
                            step = float( splitted[5] )
                         
                            while( value <= MAXvalue ):
                                values.append( value )
                                value += step
                            
                            self.struct.addParamValues( values )
                        
                        elif( splitted[2] == "enum" ):
                            for i in range(3, len(splitted) ):
                                values.append( float(splitted[i]) )
                            
                            self.struct.addParamValues( values )

                    elif( splitted[0] == "numFeats" ):
                        self.struct.setNumFeatures( int( splitted[1] ) )

                    elif( splitted[0] == "minNumObsFeatValues" ):
                        self.struct.setMinNumObsFeatValues( int( splitted[1] ) )
                            
                    elif( splitted[0] == "numReps" ):
                        self.struct.setNumOPs( int( splitted[1] ) )
                             
                    elif( splitted[0] == "DoE" ):
                        self.struct.setDoeKind( splitted[1] )

                    elif( splitted[0] == "lhdSamples" ):
                        self.struct.setLhdSamples( int(splitted[1]) )
                        
                    elif( splitted[0] == "RSM" ):
                        self.struct.setRsmKind( splitted[1] )
                    
                    elif( splitted[0] == "paramsTransforms" ):
                        self.struct.addMetricToSparkGenLinearRegrTransforms( splitted[1] )
                        
                        self.struct.addMetricInfoToSparkGenLinearRegrTransforms( splitted[1], splitted[2] )
                        self.struct.addMetricInfoToSparkGenLinearRegrTransforms( splitted[1], splitted[3] )
                        self.struct.addMetricInfoToSparkGenLinearRegrTransforms( splitted[1], splitted[4] )
                        self.struct.addMetricInfoToSparkGenLinearRegrTransforms( splitted[1], splitted[5] )
                    
                    elif( splitted[0] == "done" ):
                        self.struct.createFeaturesDict()
                        
                        self.struct.setStatus( "buildingDoe" )
                        
                        # notify the thread that computes the doeThread configurations
                        self.doeCond.notifyAll()
        
        elif( msg.topic == self.OPsTopic ):
            # msg.payload es.: "1 100000:5.3454867 0.2343545" (params:metrics)
            # OR
            # msg.payload es.: "1 100000:500 600:5.3454867 0.2343545" (params:features:metrics)
            splitted = msg.payload.split(":")

            configuration = []
            
            splittedConf = splitted[0].split(" ")
            for value in splittedConf:
                configuration.append( float(value) )
            
            newOP = False
            
            for conf in self.struct.getDoeConfs():
                if( conf.getConf() == configuration ):
                    # if the configuration is not a done configuration
                    newOP = True
                    
                    self.struct.addOP( msg.payload )

                    self.manageConfForDoEsModel( splitted )
                    
                    conf.decrementNumOPs()



                    if( len(splitted) == 3 ):
                        # manage features in order to keep track features values and the relative number of observations during DSE
                        splittedFeatures = splitted[1].split( " " )

                        for index, item in enumerate( splittedFeatures ):
                            featureFloat = float(item)

                            if( self.struct.hasFeatureValue( index, featureFloat ) == True ):
                                self.struct.incrementFeatureCounter( index, featureFloat )

                            else:
                                self.struct.addFeatureValue( index, featureFloat )


                    
                    if( conf.getNumOPs() == 0 ):
                        # if I have the right number of ops for this configuration
                        self.struct.addConfToDoneConfs( conf )
                                                
                        self.struct.removeConfToDoeConfs( conf )
                        
                        self.struct.showStruct()
                        
                        self.checkStartRsm()

                    break
            
            if( newOP == False ):
                self.struct.addOtherOP( msg.payload )
                
    def connect( self, IPaddress, brokerPort ):
        self.client.will_set(self.communicationTopic, payload = "disconnection", qos = self.qos, retain = False)
        
        self.client.connect( IPaddress, port = brokerPort )
        self.client.on_connect = self.on_connect( IPaddress, brokerPort )
        
    def subscribe( self, topic ):
        self.client.subscribe( topic, qos = self.qos )
        self.client.on_subscribe = self.on_subscribe( topic )
        self.client.on_message = self.on_message
    
    def on_publish( self, topic, message ):
        print( "\npublication" )
        print( "topic: " + topic )
        print( "message: " + message )
        
    def publish( self, topic, message ):
        self.client.on_publish = self.on_publish( topic, message )
        self.client.publish( topic, message, qos = self.qos )
    
    ####################################################################################################
    ####################################################################################################
    
        
    def start( self, appName, hostpid ):
        self.struct = appStruct( appName )

        self.manageNewHostpid( hostpid )

        self.buildTopics()

        self.client = paho.Client( client_id = self.clientID + "_" + self.struct.getName() )
        self.connect( self.IPaddress, self.brokerPort )

        self.firstSubscriptions()

        if( os.path.exists( self.root + self.agora + self.struct.getName() + "/model.txt" ) == True ):
            self.loadModel()
            
            self.struct.setStatus( "autotuning" )

        else:
            self.secondSubscriptions()
            
            self.threadsCreation()
        
        self.client.loop_start()

        while( True ):
            pass

        self.client.loop_stop()
    
    def manageNewHostpid( self, hostpid ):
        self.struct.addHostpid( hostpid )

    def buildTopics( self ):
        self.newHostpidTopic = self.agora + self.struct.getName() + "/newHostpid"
        self.agoraLocalAppHandlerReqTopic = self.agora + self.struct.getName() + "/req"
        self.disconnectionTopic = self.agora + self.struct.getName() + "/disconnection"
        self.receiveInfoTopic_NoMultiLevel = self.agora + self.struct.getName() + "/info"
        self.receiveInfoTopic = self.receiveInfoTopic_NoMultiLevel + "/#"
        self.OPsTopic = self.agora + self.struct.getName() + "/OPs"
        self.communicationTopic = self.agora + self.struct.getName()

    def firstSubscriptions( self ):
        self.subscribe( self.newHostpidTopic )
        
        self.subscribe( self.agoraLocalAppHandlerReqTopic )
        
        self.subscribe( self.disconnectionTopic )
        
    def secondSubscriptions( self ):
        self.subscribe( self.receiveInfoTopic )
        
        self.subscribe( self.OPsTopic )
        
    def threadsCreation( self ):
        self.doeCond = threading.Condition()
        self.rsmCond = threading.Condition()
         
        self.thread_doe = doeThread( 1, self.struct.getName() + "_doe", self.doeCond, self.struct )
        self.thread_rsm = rsmThread( 2, self.struct.getName() + "_rsm", self.rsmCond, self.struct )
         
        # Start new Threads
        self.thread_doe.start()
        self.thread_rsm.start()
        
    def requestAppInfo( self ):
        self.publish( self.communicationTopic, "info" )
    
    def sendConfiguration( self, hostpid ):
        if len( self.struct.getDoeConfs() ) > 0:
            #self.struct.restoreConfs(hostpid, False)
            
            configuration = self.struct.getDoeConfs().pop(0)
            self.struct.addDoeConf( configuration )
            
            confStr = ""
            for value in configuration.getConf():
                confStr += str(value) + " "
         
            # elimino ultimo carattere (spazio vuoto)
            confStr = confStr[:-1]
            # configurationStr finale es.: "4.0 500000.0"

            # invio la configurazione
            # topic es.: agora/swaptions/crisXPS15_1897/configuration
            # payload es.: "1 400000"
            self.publish( self.agora + self.struct.getName() + "/" + hostpid + "/conf", confStr )
        
    def checkStartRsm( self ):
        with self.rsmCond:
            if( len( self.struct.getDoneConfs() ) == self.struct.getDoeConfsNumber() ):
                self.struct.DoEsModelMeans()

                # notify the thread that computes the model
                self.rsmCond.notifyAll()
    
    def sendModel( self, hostpid ):
        for op in self.struct.getModel():
            op = op.replace( ":", " " )
            
            self.publish( self.agora + self.struct.getName() + "/" + hostpid + "/model", op )
        
        self.publish( self.agora + self.struct.getName() + "/" + hostpid + "/model", "modelDone" )
    
    def loadModel( self ):
        model = []
        
        with open( self.root + self.agora + self.struct.getName() + "/model.txt", 'r' ) as csvfile:
            tracereader = csv.reader( csvfile )
            for row in tracereader:
                for op in row:
                    model.append( str(op) )
        
        self.struct.setModel( model )

    def manageConfForDoEsModel( self, splittedOP ):
        # splittedOP is a list of strings
        # splittedOP[0]: parameters, es.: "1 100000"
        # splittedOP[1]: metrics, es.: "5.2341 126.2"
        # OR
        # splittedOP[0]: parameters, es.: "1 100000"
        # splittedOP[1]: features, es.: "500 600"
        # splittedOP[2]: metrics, es.: "5.2341 126.2"

        if( len(splittedOP) == 2 ):
            splittedOPMetrics = splittedOP[1].split(" ")

            key = splittedOP[0]

        else:
            splittedOPMetrics = splittedOP[2].split(" ")

            key = splittedOP[0] + ":" + splittedOP[1]

        metricsValues = []

        for metr in splittedOPMetrics:
            metricsValues.append( float(metr) )

        if( self.struct.HasDoEsModelKey( key ) == True ):
            values = self.struct.getDoEsModelKeyValues( key )

            for i in range( len(values[0]) ):
                values[0][i] += metricsValues[i]

            values[1] += 1

            self.struct.setDoEsModelKeyValues( key, values )

        else:
            values = [ metricsValues, 1]
            
            self.struct.setDoEsModelKeyValues( key, values )

    def sendDoEsModel( self, hostpid ):
        if( hostpid not in self.DoEModelSent ):
            for op in self.struct.getDoEsModelString():
                op = op.replace( ":", " " )
                
                self.publish( self.agora + self.struct.getName() + "/" + hostpid + "/model", op )
            
            self.publish( self.agora + self.struct.getName() + "/" + hostpid + "/model", "DoEModelDone" )

            self.DoEModelSent.append( hostpid )