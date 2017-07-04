#include "agora/appStruct.hpp"

#include <unistd.h>
#include <iostream>
#include <cstring>
#include <algorithm>

AppStruct::AppStruct()
{

}

AppStruct::AppStruct( std::string name,

						int numM,

						std::vector< std::string > i,

						std::vector<float> defaultConf,
						std::vector<int> feats_idx )
{
	appName = name;
	info = i;

	numMetrics = numM;
	features_indexes = feats_idx;
	defaultConfiguration = defaultConf;
	




	if( features_indexes.empty() == true )
	{
		numParams = defaultConfiguration.size();
		numFeatures = 0;

		for( int i = 0; i < numParams; i++ )
		{
			parameters_indexes.emplace_back( i );
		}
	}
	else
	{
		numFeatures = features_indexes.size();
		numParams = defaultConfiguration.size() - numFeatures;

		for( int i = 0; i < numParams + numFeatures; i++ )
		{
			if( std::find( features_indexes.begin(), features_indexes.end(), i ) != features_indexes.end() )
			{
				;
			}
			else
			{
				parameters_indexes.emplace_back( i );
			}
		}
	}





	operatingPoints = new OPs();

	configurationsList.push_back( defaultConfiguration );

	AppStruct::updateOPs();

	operatingPoints->makeOPs( configurationsList, numParams + numFeatures, numMetrics, newOPs );





	char hostname[128];
	gethostname( hostname, 128 );

	int pid = getpid();





	// hostpid
	// es.: crisXPS15_1897
	std::string hostpidStr = hostname;
	hostpidStr += "_" + std::to_string(pid);

	hostpid = new char[hostpidStr.length() + 1];
	std::strcpy( hostpid, hostpidStr.c_str() );





	// name of the application + hostname_pid for MQTT pubblication on topic /apps
	std::string appName_hostpidStr = appName + " " + hostpid;

	appName_hostpid = new char[appName_hostpidStr.length() + 1];
	std::strcpy( appName_hostpid, appName_hostpidStr.c_str() );





	setStatus( defaultStatus );
}

void AppStruct::addOp( std::vector<float> op )
{
	model.push_back(op);
}

bool AppStruct::checkOPs()
{
	if( configurationsList != currentConfigurations )
	{
		operatingPoints->makeOPs( configurationsList, numParams + numFeatures, numMetrics, newOPs);
		operatingPoints->makeOPs( currentConfigurations, numParams + numFeatures, numMetrics, notNewOPs);
		operatingPoints->makeCommonOPs();
		
		return true;
	}
	else
	{
		return false;
	}
}

void AppStruct::clearModel()
{	
	model.clear();
}

std::string AppStruct::getAppName()
{
	return appName;
}

char *AppStruct::getAppName_hostpid()
{
	return appName_hostpid;
}

std::vector<float> AppStruct::getFeatures()
{
	return features;
}

OPs *AppStruct::getOperatingPoints()
{
	return operatingPoints;
}

std::vector<float> AppStruct::getDefaultConfiguration()
{
	return defaultConfiguration;
}

char *AppStruct::getHostpid()
{
	return hostpid;
}

std::string AppStruct::getHostpidStr()
{
	std::string hostpidStr = hostpid;
	return hostpidStr;
}

std::vector< std::string > AppStruct::getInfo()
{
	return info;
}

std::vector< std::vector<float> > AppStruct::getModel()
{
	return model;
}

std::vector<float> AppStruct::orderValues( std::vector<float> values )
{
	std::vector<float> ordered_values;
	ordered_values.resize( numParams + numFeatures );

	int idx = 0;
	// put parameters values in correct place
	for( int i = 0; i < numParams; ++i, ++idx )
	{
		ordered_values[ parameters_indexes[i] ] = values[idx];
	}
	// eventually put features values in correct place
	for( int i = 0; i < numFeatures; ++i, ++idx )
	{
		ordered_values[ features_indexes[i] ] = values[idx];
	}
	// eventually put metrics values in correct place
	for( int i = numParams + numFeatures; i < values.size(); i++ )
	{
		ordered_values.emplace_back( values[i] );
	}

	return ordered_values;
}

std::vector<int> AppStruct::getParametersIndexes()
{
	return parameters_indexes;
}

std::vector<int> AppStruct::getFeaturesIndexes()
{
	return features_indexes;
}

AppStruct::appStatus AppStruct::getStatus()
{
	return status;
}

void AppStruct::setConfigurationsList( std::vector< std::vector<float> > confsList )
{
	configurationsList = confsList;
}

void AppStruct::setFeatures( std::vector<float> feats )
{
	features = feats;

	if( status == AppStruct::defaultStatus )
	{
		// update defaultConfiguration with new feature values
		std::vector<float> newDefaultConf = defaultConfiguration;

		// add params values
		for( int i = 0; i < features.size(); i++ )
		{
			newDefaultConf[ features_indexes[i] ] = features[i];
		}

		AppStruct::setConfigurationsList( { newDefaultConf } );
	}
}

void AppStruct::setStatus( appStatus s)
{
	status = s;
}

void AppStruct::updateOPs()
{	
	currentConfigurations = configurationsList;
}

AppStruct::~AppStruct()
{

}