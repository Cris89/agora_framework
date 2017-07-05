#ifndef AGORA_MARGOTMANAGER_HPP
#define AGORA_MARGOTMANAGER_HPP

#include <iostream>
#include <string>
#include <vector>

#include <margot.hpp>
#include <agora/framework.hpp>

class Agora_Margot_Manager
{
public:
	Agora_Margot_Manager();

	void init();

	void updateOPs();

	// the order of parameters and features in params_features must be lexicographic, as in the defaultConfiguration
	// the order of metrics in metrics must be lexicographic
	void sendResult( std::vector<float> params_features, std::vector<float> metrics );

	// features must be in lexicographic order
	void storeFeatures( std::vector<float> features );

	virtual ~Agora_Margot_Manager();

private:
	Framework *agora_framework;
};

#endif
