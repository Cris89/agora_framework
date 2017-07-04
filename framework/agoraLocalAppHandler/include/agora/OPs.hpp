#ifndef AGORA_OPS_HPP
#define AGORA_OPS_HPP

#include <vector>
#include <deque>
#include <utility>

typedef float value_t;

typedef value_t parameter_t;
typedef value_t metric_t;

typedef std::vector< parameter_t > configuration_t;
typedef std::vector< metric_t > performance_t;

typedef std::pair< configuration_t, performance_t > operating_point_t;

typedef std::deque< operating_point_t > operating_points_t;

class OPs
{
public:
	OPs();

	operating_points_t getCommonOPs();

	operating_points_t getCurrentOPs();

	operating_points_t getNewOPs();

	void makeOPs( std::vector< std::vector<float> > ops, int numParams, int numMetrics, bool areNew);

	void makeCommonOPs();

	virtual ~OPs();

private:
	operating_points_t currentOPs;

	operating_points_t newOPs;

	operating_points_t commonOPs;
};

#endif