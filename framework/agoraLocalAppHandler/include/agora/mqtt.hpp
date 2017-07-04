#ifndef AGORA_MQTT_HPP
#define AGORA_MQTT_HPP

#include "agora/appStruct.hpp"
#include "agora/topics.hpp"

#include <MQTTClient.h>

#include <pthread.h>

#include <chrono>

class MQTT 
{
public:
	MQTT( std::string IPaddress,
			std::string brokerPort,
			AppStruct &app,
			Topics &t,
			int threadSleepTime );

	void connect();

	static void publish( char *payload, const char *topicName );

	void subscribe( const char *topic );
	
	virtual ~MQTT();

private:
	static AppStruct *appStruct;

	static MQTTClient client;

	// clientID
	// es.: "swaptions_crisXPS15_1897"
	static char *clientID;

	const char *connectionAddress;

	static MQTTClient_messageArrived messageArrived;

	static int rc;

	pthread_t reqThread;
	
	static void *reqThreadFunc( void * );

	static Topics *topics;
};

#endif