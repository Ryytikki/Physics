#include "n_body.h"
#include <iostream>
#include <cmath>
#include <fstream>

using namespace std;
using namespace nbody;

double SOFT_LEN = 0.01;

void nbody::Particles::read(std::ifstream&input)
{
	if (input.is_open()) 
	{ 
		cout << "file is open" << endl;
	}else{
		cout << "cannot open the file!" << endl; 
	}
		
	int n, all ;
	char cha;
	
	input >> n >> cha >> all;
	Particles P_list(n);

	if (all == 0) 
	{
		for ( int a = 0; a<int(n) ; a++ ) 
		{ 
			Particle P;
			//Load each particle into P
			input >> P.m >> cha >> P.x[0] >> cha >> P.x[1] >> cha >> P.v[0] >> cha >>P.v[1];
			P_list[a] = P;
		}
	}else{
	
	} // if all == 0
	input.close();
	// Assign it like this as you wont know how large data will be till you've loaded
	// the first line in the file.
	data = P_list.data;
} // void read

void nbody::Particles::write(std::ofstream&output, bool all) const
{
	if (output.is_open()) 
	{ 
		cout << "file is open" << endl;
	}else{
		cout << "cannot open the file!" << endl; 
	}
	
	output << number() << "," << all;
	
	if (all == false){
	
		for (int i = 0; i<number(); i++)
		{
			output << "\n" << data[i].m << "," << data[i].x[0] << "," << data[i].x[1] << "," << data[i].v[0] << "," << data[i].v[1];
		}
	}else{
	
	}
	
	output.close();
}

bool nbody::Quad::contains(double x, double y)
{
	// If its within the bounds of the quadrant
	if ( ( x < top_left[0]) || (x > top_left[0] + size) || ( y > top_left[1]) || (y < top_left[1] - size))
	{
		return false;
	}else{
		return true;
	}	
}

// Create new Quadrants with info based on current one

Quad nbody::Quad::NW()
{
	double s = size / 2;
	point tl = top_left;
	Quad q(s, tl);
	
	return q;
}

Quad nbody::Quad::NE()
{
	double s = size / 2;
	point tl = {top_left[0] + size / 2, top_left[1]};
	Quad q(s, tl);
	
	return q;
}

Quad nbody::Quad::SW()
{
	double s = size / 2;
	point tl = {top_left[0], top_left[1] - size / 2};
	Quad q(s, tl);
	
	return q;
}

Quad nbody::Quad::SE()
{
	double s = size / 2;
	point tl = {top_left[0] + size / 2, top_left[1] - size / 2};
	Quad q(s, tl);
	
	return q;
}
nbody::Tree::Tree()
{
	int b;
	
	Quad q_hold(0,{0,0});
	Particle a;
	a.m = 0;
	a.x = {0,0};
	quad = q_hold;
	body = a;
	gen = 0;
}

// Insert new body into tree
void nbody::Tree::insert_body(Particle&p)
{
	// If there are no objects inside the tree
	if (body.m == 0)
	{
		// generate next time a particle is added
		gen = 1;
		
		//cout << "Particle " << p.x[0] << " Assigned to new node" << endl;
		
	}else{
		
		if (gen == 1)
		{
			// Create the 4 nodes
			nodes[0] = new Tree(quad.NW());
			nodes[1] = new Tree(quad.NE());
			nodes[2] = new Tree(quad.SW());
			nodes[3] = new Tree(quad.SE()); 
			//cout << "Particle " << p.x[0] << " Creating new branches" << endl;
			
			// Add the original particle to one of the nodes
			for (int i = 0; i < 4; i++)
			{
			
				if (nodes[i]->quad.contains(body.x[0], body.x[1]))
				{
					//cout << "Particle " << p.x[0] - 1 << " moved into quadrant " << i << endl;
					nodes[i]->insert_body(body);
					break;
				}
			}
			// Nodes have been generated
			gen = 2;
		}
		
		// Add particle to relevant node
		for (int i = 0; i < 4; i++)
		{
			if (nodes[i]->quad.contains(p.x[0], p.x[1]))
			{
				// Yay! recursion!
			//	cout << "Particle " << p.x[0] << " Input into quadrant " << i << endl;
				nodes[i]->insert_body(p);
				break;
			}
		}
	}
	
	// Add body to total mass of this node
	body = body.add(body, p);	
	//cout << "COM for " << p.x[0] << " = " <<body.x[0] << " " << body.x[1] << endl;
}

void nbody::Tree::check_force(Particle&p)
{
	if (gen >= 1){
		point dx = {(p.x[0] - body.x[0]), (p.x[1] - body.x[1])};
		if (gen >= 2){
			double threshold = 1;
			double dist = sqrt(dx[0] * dx[0] + dx[1] * dx[1]);
			if ((quad.length()/dist) > threshold)
			{
				for (int i = 0; i < 4; i++)
				{
					nodes[i]->check_force(p);
				}
				return;
			}
		}
		
		// Calc grav of body on p
		double denom = 1 / ((dx[0] * dx[0]) + (dx[1] * dx[1]) + SOFT_LEN);
		
		double p_ti = sqrt(denom);	
		p_ti *= body.m;
		
		p.a[0] -= p_ti * dx[0] * denom;
		p.a[1] -= p_ti * dx[1] * denom;
	}
}

void nbody::Tree::output_info(std::ofstream&output) const
{
	point pos = quad.pos();
	output << pos[0] << "," << pos[1] << "," << quad.length() << "\n";
	if (gen > 1)
	{
		for (int i = 0; i < 4; i++)
		{
			nodes[i]->output_info(output);
		}
	}
}
