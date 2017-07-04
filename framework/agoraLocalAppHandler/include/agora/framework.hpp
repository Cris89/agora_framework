#ifndef AGORA_FRAMEWORK_HPP
#define AGORA_FRAMEWORK_HPP

#include "agora/appStruct.hpp"
#include "agora/mqtt.hpp"
#include "agora/topics.hpp"

#include <vector>
#include <string>

class Framework
{
public:
	Framework( std::string name,

				int numMetrics,

				std::vector<float> defaultConf,
				std::vector<int> features_idx,

				std::vector< std::string > info,
				
				int threadSleepTime );

	bool changeOPs;

	void checkOPs();
	
	AppStruct *getAppStruct();
	
	void init();
	
	void sendResult( std::string op );

	void storeFeatures( std::vector<float> features );
	
	void updateOPs();

private:
	std::string IPaddress = "127.0.0.1";
	std::string brokerPort = "8883";

	AppStruct *appStruct;
	
	MQTT *mqtt;
	
	Topics *topics;
};

#endif
