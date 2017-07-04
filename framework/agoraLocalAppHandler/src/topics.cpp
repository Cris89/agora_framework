#include "agora/topics.hpp"

#include <cstring>

#define ROOT	"agora/"

Topics::Topics()
{

}

Topics::Topics( std::string appName, std::string hostpid )
{
	// topic on which the app will notify its existence
	// es.: "agora/apps"
	std::string appsTopicStr = ROOT;
	appsTopicStr += "apps";

	char *appsTopicP = new char[appsTopicStr.length() + 1];
	std::strcpy( appsTopicP, appsTopicStr.c_str() );

	appsTopic = appsTopicP;





	// topic on which the app will eventually receive the request about app info
	// es.: "agora/swaptions"
	std::string communicationTopicStr = ROOT + appName;

	char *communicationTopicP = new char[communicationTopicStr.length() + 1];
	std::strcpy( communicationTopicP, communicationTopicStr.c_str() );

	communicationTopic = communicationTopicP;





	// topic on which the app will eventually publish app info
	// es.: "agora/swaptions/info"
	std::string sendInfoTopicStr = ROOT + appName + "/info/" + hostpid;

	char *sendInfoTopicP = new char[sendInfoTopicStr.length() + 1];
	std::strcpy( sendInfoTopicP, sendInfoTopicStr.c_str() );

	sendInfoTopic = sendInfoTopicP;





	// topic on which the app will do a request
	// es.: "agora/swaptions/req"
	std::string reqTopicStr = ROOT + appName + "/req";

	char *reqTopicP = new char[reqTopicStr.length() + 1];
	std::strcpy( reqTopicP, reqTopicStr.c_str() );

	reqTopic = reqTopicP;





	// topic on which the app will receive the configurations
	// es.: "agora/swaptions/crisXPS15_1897/conf"
	std::string confTopicStr = ROOT + appName + "/" + hostpid + "/conf";

	char *confTopicP = new char[confTopicStr.length() + 1];
	std::strcpy( confTopicP, confTopicStr.c_str() );

	confTopic = confTopicP;





	// topic on which the app will publish the operating points during the dse
	// es.: "agora/swaptions/OPs"
	std::string OPsTopicStr = ROOT + appName + "/OPs";

	char *OPsTopicP = new char[OPsTopicStr.length() + 1];
	std::strcpy( OPsTopicP, OPsTopicStr.c_str() );

	OPsTopic = OPsTopicP;





	// topic on which the app will receive the model
	// es.: "agora/swaptions/crisXPS15_1897/model"
	std::string modelTopicStr = ROOT + appName + "/" + hostpid + "/model";

	char *modelTopicP = new char[modelTopicStr.length() + 1];
	std::strcpy( modelTopicP, modelTopicStr.c_str() );

	modelTopic = modelTopicP;





	// topic on which the app will notify its disconnection through last will and testament mqtt feature
	// es.: "agora/swaptions/disconnection"
	std::string lastWillTopicStr = ROOT + appName + "/disconnection";

	char *lastWillTopicP = new char[lastWillTopicStr.length() + 1];
	std::strcpy( lastWillTopicP, lastWillTopicStr.c_str() );

	lastWillTopic = lastWillTopicP;
}

const char *Topics::getAppsTopic()
{
	return appsTopic;
}

const char *Topics::getCommunicationTopic()
{
	return communicationTopic;
}

const char *Topics::getConfTopic()
{
	return confTopic;
}

const char *Topics::getLastWillTopic()
{
	return lastWillTopic;
}

const char *Topics::getModelTopic()
{
	return modelTopic;
}

const char *Topics::getOPsTopic()
{
	return OPsTopic;
}

const char *Topics::getReqTopic()
{
	return reqTopic;
}

const char *Topics::getSendInfoTopic()
{
	return sendInfoTopic;
}

Topics::~Topics()
{

}