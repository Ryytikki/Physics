#include <array>
#include <iostream>
#include <iomanip>
#include <vector>
#include <math.h>

#ifndef INC_N_BODY_H
#define INC_N_BODY_H

using namespace std;

namespace nbody {
    // (x,y) vector
	typedef std::array<double, 2> point;	
	
	// Dual purpose structure for holding the individual particles as well as the 
	// information for the nodes
	struct Particle
	{
		// Mass
		double m;
		// Vel, location, accel
		point v, x, a;
		
		// Find the new mass/COM when a new particle is added to the node
		static Particle add(Particle a, Particle b)
		{
			Particle r;
			r.m = a.m + b.m;
			r.x = {(a.m * a.x[0] + b.m * b.x[0]) / r.m, 
				   (a.m * a.x[1] + b.m * b.x[1]) / r.m};
			
			return r;
		}
	};
	
	class Particles
	{
		private:
			std::vector<Particle> data;
		public:
			Particles() {}
			explicit Particles(std::size_t n)
			: data(n) {}
			Particles(const Particles&) = delete;
			Particles&operator=(const Particles&) = delete;

			/// initialises particles and their data from input
			void read(std::ifstream&input);
			/// writes particle data to file
			/// \param[all]  write m,x,v,a,p or only m,x,v
			void write(std::ofstream&output, bool all=false) const;
			
			std::size_t number() const
			{
				return data.size();
			}
			
			Particle&operator[](int i)
			{
				return data[i];
			}
			
			const Particle& operator[](int i) const
			{
				return data[i];
			}
	};
	
	// Quadrant of the map
	class Quad
	{
		private:
			// Size/Location parameters
			double size;
			point top_left;
		public:
			// Initializer
			Quad(double s, point tl): size(s), top_left(tl) {}
			Quad(){};
			// Shows size of quad
			double length() const {return size;}
			point pos() const {return top_left;}
			// Checks if particle at (x,y) is inside quad
			bool contains(double x, double y);
			
			// Create 4 new subquads
			Quad NW();
			Quad NE();
			Quad SW();
			Quad SE();
	};	
	
	// Particle tree - kinda recursive function
	class Tree
	{
		private:
			// Quadrant describing the tree
			Quad quad;
			// Particle that contains mass and COM for this node
			Particle body;
			// Subnodes for this node
			// 0 - NW. 1 - NE. 2 - SW. 3 - SE
			Tree * nodes[4];
			// Populated? 0 = no, 1 = 1 p, 2 = many p
			int gen;
		public:
		
			// Constructor and destructor
			Tree();
			
			Tree(Quad q): quad(q)		
			{
				Particle a;
				a.m = 0;
				a.x = {0,0};		
				body = a;
				gen = 0;
				
			}
			
			//~Tree(){delete nodes[1]; nodes = NULL;}
		
			// Add a new body to the tree
			void insert_body(Particle&p);
			// Check forces on the tree
			void check_force(Particle&p);
			// generic output
			void output_info(std::ofstream&output) const;
	};
	
} //namespace nbody
#endif