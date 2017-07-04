#ifndef AGORA_TOPICS_HPP
#define AGORA_TOPICS_HPP

#include <string>

class Topics
{
public:
	Topics();
	Topics( std::string appName, std::string hostpid );
	
	const char *getAppsTopic();
	
	const char *getCommunicationTopic();
	
	const char *getConfTopic();
	
	const char *getLastWillTopic();
	
	const char *getModelTopic();
	
	const char *getOPsTopic();
	
	const char *getReqTopic();
	
	const char *getSendInfoTopic();
	
	virtual ~Topics();

private:
	// topic on which the app will notify its existence
	// es.: "agora/apps"
	const char *appsTopic;

	// topic on which the app will eventually receive the request about app info
	// es.: "agora/swaptions"
	const char *communicationTopic;

	// topic on which the app will receive the configurations
	// es.: "agora/swaptions/crisXPS15_1897/conf"
	const char *confTopic;

	// last will and testament topic
	// es.: "agora/swaptions/disconnection"
	const char *lastWillTopic;

	// topic on which the app will publish the operating points during the dse
	// es.: "agora/swaptions/OPs"
	const char *OPsTopic;

	// topic on which the app will receive the model
	// es.: "agora/swaptions/crisXPS15_1897/model"
	const char *modelTopic;

	// topic on which the app will do a request
	// es.: "agora/swaptions/req"
	const char *reqTopic;

	// topic on which the app will eventually publish app info
	// es.: "agora/swaptions/info"
	const char *sendInfoTopic;
};

#endif