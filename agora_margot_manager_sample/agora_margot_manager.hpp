#ifndef TESICRIS_MARGOTMANAGER_HPP
#define TESICRIS_MARGOTMANAGER_HPP

#include <iostream>
#include <string>
#include <vector>

#include <margot.hpp>
#include <tesiCris/framework.hpp>

class tesiCris_Margot_Manager
{
public:
	tesiCris_Margot_Manager();

	void init();

	void updateOPs();

	// the order of parameters and features in params_features must be lexicographic
	// the order of metrics in metrics must be lexicographic
	void sendResult( std::vector<float> params_features, std::vector<float> metrics );

	// features must be in lexicographic order
	void storeFeatures( std::vector<float> features );

	virtual ~tesiCris_Margot_Manager();

private:
	Framework *tesiCris_framework;
};

#endif
