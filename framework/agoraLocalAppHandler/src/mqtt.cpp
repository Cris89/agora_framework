#include "agora/mqtt.hpp"

#include <cstring>

#include <sstream>

#include <thread>
#include <chrono>

#include <iostream>

#define TIMEOUT				10000L
#define QOS					0

AppStruct *MQTT::appStruct;

MQTTClient MQTT::client;

char *MQTT::clientID;

int MQTT::rc;

Topics *MQTT::topics;

MQTT::MQTT( std::string IPaddress,
			std::string brokerPort,
			AppStruct &app,
			Topics &t,
			int threadSleepTime )
{
	appStruct = &app;
	topics = &t;

	std::string connectionAddressStr = IPaddress + ":" + brokerPort;
	
	char *connectionAddressP = new char[connectionAddressStr.length() + 1];
	std::strcpy( connectionAddressP, connectionAddressStr.c_str() );

	connectionAddress = connectionAddressP;





	// clientID for MQTT connection
	// es.: swaptions_crisXPS15_1897
	std::string clientIDStr = appStruct->getAppName() + "_" + appStruct->getHostpidStr();

	clientID = new char[clientIDStr.length() + 1];
	std::strcpy( clientID, clientIDStr.c_str() );




	
	rc = MQTTClient_create( &client, connectionAddress, clientID, MQTTCLIENT_PERSISTENCE_NONE, NULL );
	rc = MQTTClient_setCallbacks( client, NULL, NULL, messageArrived, NULL );

	pthread_create( &reqThread, NULL, MQTT::reqThreadFunc, (void *)threadSleepTime );
}

void MQTT::connect()
{
	MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
	MQTTClient_willOptions will_opts = MQTTClient_willOptions_initializer;

	conn_opts.keepAliveInterval = 10;
	conn_opts.cleansession = 1;
	conn_opts.will = &will_opts;

	will_opts.topicName = topics->getLastWillTopic();
	will_opts.message = appStruct->getHostpid();
	
	rc = MQTTClient_connect(client, &conn_opts);
	
	printf( "\nclientID: %s connected at %s", clientID, connectionAddress );
}

int MQTT::messageArrived( void *context, char *topicName, int topicLen, MQTTClient_message *message )
{
	printf( "\n\nmessage arrived\n" );
	printf( "topic: %s\n", topicName );
	printf( "message: %.*s", message->payloadlen, (char *)message->payload );

	std::string topic = topicName;
	std::string payload( (char *)message->payload, message->payloadlen );

	if( topic == topics->getCommunicationTopic() )
	{
		if( payload == "info" )
		{
			for( int i = 0; i < appStruct->getInfo().size(); i++ ) 
			{
	    		char* message = new char[ appStruct->getInfo()[i].length() + 1 ];
				std::strcpy( message, appStruct->getInfo()[i].c_str() );

				MQTT::publish( message, topics->getSendInfoTopic() );
			}

			char done[] = "done";
			char* doneP = done;
			
			MQTT::publish( doneP, topics->getSendInfoTopic() );
		}

		else if( payload == "disconnection" )
		{
			if( appStruct->getStatus() != AppStruct::doeModel && appStruct->getStatus() != AppStruct::autotuning )
			{
				std::vector< std::vector<float> > defaultConf;
				defaultConf.push_back( appStruct->getDefaultConfiguration() );

				appStruct->setConfigurationsList( defaultConf );
				appStruct->setStatus( AppStruct::defaultStatus );
			}
		}
	}

	else if( topic == topics->getConfTopic() )
	{
		std::stringstream ss( payload );
		std::string token;

		std::vector< std::vector<float> > confsList;
		std::vector<float> conf;

		while( ss >> token )
		{
			const char* numberptr = token.c_str();
		    float number = atof( numberptr );
		    conf.push_back( number );
		}

		std::vector<float> features = appStruct->getFeatures();

		// add features values to configuration
		for( int i = 0; i < features.size(); i++ )
		{
			conf.push_back( features[i] );
		}

		std::vector<float> orderedConf = appStruct->orderValues( conf );

		confsList.push_back( orderedConf );
		appStruct->setConfigurationsList( confsList );

		if( appStruct->getStatus() != AppStruct::dse )
		{
			appStruct->setStatus( AppStruct::dse );
		}
	}

	else if( topic == topics->getModelTopic() )
	{
		if( payload == "DoEModelDone")
		{
			appStruct->setConfigurationsList( appStruct->getModel() );
			appStruct->clearModel();
			appStruct->setStatus( AppStruct::doeModel );
		}

		else if( payload == "modelDone" )
		{
			appStruct->setConfigurationsList( appStruct->getModel() );
			appStruct->clearModel();
			appStruct->setStatus( AppStruct::autotuning );
		}

		else
		{
			std::stringstream ss( payload );
			std::string token;

			std::vector<float> op;

			while( ss >> token )
			{
				const char* numberptr = token.c_str();	    
			    float number = atof( numberptr );

			    op.push_back( number );
			}

			std::vector<float> orderedOP = appStruct->orderValues( op );

			appStruct->addOp( orderedOP );
		}
	}

	MQTTClient_freeMessage( &message );
	MQTTClient_free( topicName );

	return 1;
}

void MQTT::publish( char *payload, const char *topicName )
{
	MQTTClient_message msg = MQTTClient_message_initializer;
	
	msg.payload = payload;
	msg.payloadlen = strlen( payload );

	msg.qos = QOS;

	msg.retained = 0;
	
	MQTTClient_deliveryToken dt;

	rc = MQTTClient_publishMessage( client, topicName, &msg, &dt );
	rc = MQTTClient_waitForCompletion( client, dt, TIMEOUT );

	printf( "\n\n%s publication\ntopic: %s\npayload: %s\n", clientID, topicName, payload );
}

void *MQTT::reqThreadFunc( void *sleepTime )
{
	while( appStruct->getStatus() != AppStruct::autotuning )
	{
		MQTT::publish( appStruct->getHostpid(), topics->getReqTopic() );

		std::this_thread::sleep_for( std::chrono::milliseconds( (long)sleepTime ) );
	}
}

void MQTT::subscribe( const char *topic )
{
	int qos = QOS;

	rc = MQTTClient_subscribe( client, topic, qos );
	
	printf( "\n\n%s subscribed to %s", clientID, topic );
}

MQTT::~MQTT()
{

}