#include "agora/framework.hpp"

#include <string>
#include <cstring>
#include <vector>
#include <iostream>

Framework::Framework( std::string name,

						int numMetrics,

						std::vector<float> defaultConf,
						std::vector<int> features_idx,

						std::vector< std::string > info,
						
						int threadSleepTime )
{
	appStruct = new AppStruct( name,

								numMetrics,

								info,
								
								defaultConf,
								features_idx );

	topics = new Topics( appStruct->getAppName(),
							appStruct->getHostpidStr() );

	mqtt = new MQTT( IPaddress,
						brokerPort,
						*appStruct,
						*topics,
						threadSleepTime );
}

void Framework::checkOPs()
{
	changeOPs = appStruct->checkOPs();
}

AppStruct *Framework::getAppStruct()
{
	return appStruct;
}

void Framework::init()
{
	mqtt->connect();

	// topic on which the app will eventually receive the request about app info
	// es.: "agora/swaptions"
	mqtt->subscribe( topics->getCommunicationTopic() );

	// topic on which the app will receive the configurations
	// es.: "agora/swaptions/crisXPS15_1897/conf"
	mqtt->subscribe( topics->getConfTopic() );
	
	// topic on which the app will receive the model
	// es.: "agora/swaptions/crisXPS15_1897/model"
	mqtt->subscribe( topics->getModelTopic() );

	// topic es.: "agora/apps"
	// payload es.: "swaptions crisXPS15_1897"
	mqtt->publish( appStruct->getAppName_hostpid(), topics->getAppsTopic() );
}

void Framework::sendResult( std::string op )
{
	char* operatingPointP = new char[op.length() + 1];
	std::strcpy(operatingPointP, op.c_str());

	mqtt->publish( operatingPointP, topics->getOPsTopic() );
}

void Framework::storeFeatures( std::vector<float> features )
{
	appStruct->setFeatures( features );
}

void Framework::updateOPs()
{
	appStruct->updateOPs();
}