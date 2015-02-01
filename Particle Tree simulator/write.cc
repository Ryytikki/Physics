#include "./n_body.h"
#include <iostream>
#include <fstream>
#include <random>
#include <sstream>


using namespace std;
using namespace nbody;

const double Pi = 3.14159265358979323846264338328;  // Pi                   
const double third = 1.0/3.0;
const double sqrt2 = std::sqrt(2.0);
const int PNUM = 10000000;
double G_VAL = 1;

point gal_core = {0,0};
double gal_m = 100000000;

  class sampling_directions_uniform{
    std::default_random_engine&gen;
	
    mutable std::uniform_real_distribution<double> uniform;
	mutable std::uniform_real_distribution<double> uniform2;
  public:
    sampling_directions_uniform(std::default_random_engine&g) : gen(g), uniform(-1.0, 1.0), uniform2(0,1) {}
	
    point operator()(double r) const
    {	
		double theta = uniform(gen) * Pi;

		double l = 2000 * sqrt(uniform2(gen));
		double y =  l * cos(theta);
		double x = l * sin(theta);
		return {x,y};
    } 
};

int main()
{
	Particles data(PNUM);
	
	std::default_random_engine gen;
	std::uniform_real_distribution<double> R_val(1.0,1.0);
	sampling_directions_uniform sample_sphere(gen	);
	for (int i = 1; i < PNUM; i++)
	{
	    
		auto R= R_val(gen)*2*Pi;
		auto r = abs(-1 * log(R));    // convert cumulative mass to radius
		data[i].x = sample_sphere(r); 

		point dx = {data[i].x[0] - gal_core[0], data[i].x[1] - gal_core[1]};
		double dist = sqrt(dx[0] * dx[0] + dx[1] * dx[1]);
		
		double theta = atan2(dx[1], dx[0]);
		
		double vel = sqrt(G_VAL * gal_m / dist);
		
		data[i].v = {vel * sin(theta), -1 * vel * cos(theta)};
		data[i].m = 1;
	}
	
	data[0].x = gal_core;
	data[0].v = {0,0};
	data[0].m = gal_m;

	std::stringstream filename;
	filename << "D:/N_BODY/DATA/N_BODY_0";
	std::ofstream file(filename.str());
	data.write(file, 0);

}

