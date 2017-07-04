#include "tesiCris_margot_manager.hpp"

tesiCris_Margot_Manager::tesiCris_Margot_Manager()
{
	
}

void tesiCris_Margot_Manager::init()
{
	////////////////////////////////////////////////////////////////////////////////////////////////////
	////////// Configuration part
	////////////////////////////////////////////////////////////////////////////////////////////////////
	std::string appName = "appName";

	int numMetrics = 2;

	// the order of parameters and features must be lexicographic
	// es. parameters: "aaa" and "ccc", features: "bbb" --> aaa = 100, bbb = 150, ccc = 360
	std::vector<float> defaultConfiguration = { 100, 150, 360 };

	// in this case, 100 is a feature value
	std::vector<int> features_indexes = { 0 };

	// metrics and parameters must follow a lexicographic order
	std::vector< std::string > info = { "metric avg_error",
										"metric avg_throughput",

										"param param1 enum 1 50 150 300 450 700 800",
										"param param2 range 10 850 70",

										"numFeats 1",
										"minNumObsFeatValues 3",

										"doe fcccdExtra",
										"lhdSamples 10",
										"numOPs 1",

										"rsm sparkGenLinRegr2nd" };

	// milliseconds
	int threadMQTTReqSleepTime = 3000;
	////////////////////////////////////////////////////////////////////////////////////////////////////
	////////// Configuration part
	////////////////////////////////////////////////////////////////////////////////////////////////////
	




	tesiCris_framework = new Framework( appName,

										numMetrics,

										defaultConfiguration,
										features_indexes,
										
										info,
											
										threadMQTTReqSleepTime );

	tesiCris_framework->init();





	operating_points_t defaultOP = tesiCris_framework->getAppStruct()->getOperatingPoints()->getNewOPs();

	margot::sleeping::manager.add_operating_points( defaultOP );

	margot::init();
}

void tesiCris_Margot_Manager::updateOPs()
{
	tesiCris_framework->checkOPs();

	if(tesiCris_framework->changeOPs == true)
	{
		operating_points_t newOPs = tesiCris_framework->getAppStruct()->getOperatingPoints()->getNewOPs();
		operating_points_t currentOPs = tesiCris_framework->getAppStruct()->getOperatingPoints()->getCurrentOPs();
		operating_points_t commonOPs = tesiCris_framework->getAppStruct()->getOperatingPoints()->getCommonOPs();

		/*printf("\t+-------newOPs---------+\n");
		for( auto newOP : newOPs)
		{
			for ( const auto c : newOP.first )
			{
				printf("\t|% 22.2f|\n", c);
			}

			for ( const auto c : newOP.second )
			{
				printf("\t|% 22.2f|\n", c);
			}

			printf("\t+----------------------+\n");
		}

		printf("\n\t+-----currentOPs-------+\n");
		for( auto currentOP : currentOPs)
		{
			for ( const auto c : currentOP.first )
			{
				printf("\t|% 22.2f|\n", c);
			}

			for ( const auto c : currentOP.second )
			{
				printf("\t|% 22.2f|\n", c);
			}

			printf("\t+----------------------+\n");
		}

		printf("\n\t+-----commonOPs--------+\n");
		for( auto commonOP : commonOPs)
		{
			for ( const auto c : commonOP.first )
			{
				printf("\t|% 22.2f|\n", c);
			}

			for ( const auto c : commonOP.second )
			{
				printf("\t|% 22.2f|\n", c);
			}

			printf("\t+----------------------+\n");
		}*/

		margot::sleeping::manager.add_operating_points(newOPs);
		margot::sleeping::manager.remove_operating_points(currentOPs);
		margot::sleeping::manager.add_operating_points(commonOPs);

		// margot::sleeping::manager.dump();

		tesiCris_framework->updateOPs();
	}
}

// the order of parameters and features in params_features must be lexicographic
// the order of metrics in metrics must be lexicographic
void tesiCris_Margot_Manager::sendResult( std::vector<float> params_features, std::vector<float> metrics )
{
	std::string operatingPoint;

	std::vector<int> fs_idx = tesiCris_framework->getAppStruct()->getFeaturesIndexes();

	std::vector<float> ps_v;
	std::vector<float> fs_v;



	const int num_params_features = params_features.size();
	for( int i = 0; i < num_params_features; ++i )
	{
		bool is_feature = false;
		
		for( const int index : fs_idx )
		{
			if( i == index )
			{
				is_feature = true;
				break;
			}
		}
		
		if( is_feature )
		{
			fs_v.emplace_back( params_features[i] );
		}
		
		else
		{
			ps_v.emplace_back( params_features[i] );
		}
	}



	const int num_params = ps_v.size();
	for( int i = 0; i < num_params; i++ )
	{
		operatingPoint += std::to_string( ps_v[i] ) + " ";
	}

	operatingPoint = operatingPoint.substr( 0, operatingPoint.size() - 1 );
	operatingPoint += ":";

	const int num_feats = fs_v.size();
	for( int i = 0; i < num_feats; i++ )
	{
		operatingPoint += std::to_string( fs_v[i] ) + " ";
	}

	operatingPoint = operatingPoint.substr( 0, operatingPoint.size() - 1 );
	operatingPoint += ":";

	const int num_metrics = metrics.size();
	for( int i = 0; i < num_metrics; i++ )
	{
		operatingPoint += std::to_string( metrics[i] ) + " ";
	}

	operatingPoint = operatingPoint.substr( 0, operatingPoint.size() - 1 );

	tesiCris_framework->sendResult( operatingPoint );
}

// features must be in lexicographic order
void tesiCris_Margot_Manager::storeFeatures( std::vector<float> features )
{
	tesiCris_framework->storeFeatures( features );
}

tesiCris_Margot_Manager::~tesiCris_Margot_Manager()
{

}