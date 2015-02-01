#include "./n_body.h"
#include <iostream>
#include <fstream>
#include <random>
#include <sstream>

using namespace std;
using namespace nbody;

int ti = 0;
const double dt = 0.01;
double G_VAL = 1;

const int PNUM = 500000;

void kick(Particles&p)
{
	for (int i = 0; i < PNUM; i++)
	{
		p[i].v ={p[i].v[0] + 0.5 * dt * p[i].a[0] * G_VAL, 
				 p[i].v[1] + 0.5 * dt * p[i].a[1] * G_VAL};
	}
}

void build_tree(Particles&p)
{
	Quad q(1000.0,{-500.0,500.0});
	Tree t(q);

	kick(p);
	
	for (int i = 0; i < PNUM; i++)
	{
		p[i].x ={p[i].x[0] + dt * p[i].v[0], 
				 p[i].x[1] + dt * p[i].v[1]};
	}
	
	for (int i = 0; i < PNUM; i++)
	{
		t.insert_body(p[i]);	
	}
	
	for (int i = 0; i < PNUM; i++)
	{	
		p[i].a = {0,0};
		t.check_force(p[i]);		
	}
	
	kick(p);

	
	/*std::stringstream filename;
	filename << "D:/N_BODY/DATA/TREE_" << ti;
	std::ofstream file2(filename.str());
	t.output_info(file2);
	file2.close();*/
}

double read_data(Particles&P)
{
	std::string file_name;
	std::string file_ID;

	cout << "Enter file number: ";
	cin >> file_ID;
	
	// Chosen format for filename, each reading will be saved as "N_BODY_<I>"
	// where <I> is the time from t=0
	file_name = "D:/N_BODY/DATA/DATA/N_BODY_" + file_ID;
	
	cout << "Reading file... \n";
	std::ifstream file(file_name);
	P.read(file);

	cout << "File read \n";
	cout << "Number of particles: " << P.number() << "\n";
	
	return atof(file_ID.c_str());
	
}

int main()
{
	Particles data(PNUM);
	int ID = read_data(data);
	
	for (ti= 1; ti < 8002; ti ++)
	{
		build_tree(data);

		std::stringstream filename;
		filename << "D:/N_BODY/DATA/N_BODY_" << (ti+ID);
		std::ofstream file(filename.str());
		data.write(file, 0);
	}
}