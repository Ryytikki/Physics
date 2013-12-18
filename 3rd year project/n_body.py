import math, random
from time import time
import matplotlib.pyplot as plt
import numpy as np

G_CONST = 6.67e-11

# Planet info stuff
M_VEN = 4.87e24
V_VEN = 35140.9
R_VEN = 107.48e9

M_EARTH = 5.972e24
V_EARTH = 29786.1 
R_EARTH =  149.94e9

M_MARS = 0.64e24
V_MARS = 23076.8
R_MARS = 249.23e9

M_JUP = 1898e24
V_JUP = 12748.7
R_JUP = 816.62e9

M_SAT = 568.36e24
V_SAT = 9930.10
R_SAT = 1346e9

M_SUN = 1.989e30
R_SUN = 0#-149.94e6
V_SUN = 0#0.25
Rad_SUN = 695500000

AU = 149.94e9	

# Time step - 1 week
TIME_DELAY = 604800

# Duration of the loop
DURATION = 1000000 * 52

# Calculates distance between 2 vectors
def vector_dist(item1, item2):
	return math.sqrt((item2[0] - item1[0]) ** 2 + (item2[1]- item1[1]) ** 2)

# Calculates vector grav force between 2 bodies
def calc_f(body, item):
	distance = vector_dist(body.x, item.x)
	if distance < 1000:
		return [0,0]
	force = G_CONST * item.mass / (distance) ** 2
	unit_vector = [body.sub(item)[0] / distance, body.sub(item)[1] / distance]
	return [unit_vector[0]* force, unit_vector[1] * force]

# Calculate total gravitational force on a body	
def calc_gravity(body, planets, delay):
	force = [0,0]
	
	body.x = [body.x[0] + 0.5 * delay * body.v[0], body.x[1] + 0.5 * delay * body.v[1]]
	
	for item in planets:
		body_force = calc_f(body, item)
		force = [force[0] - body_force[0], force[1] - body_force[1]]
	
	body.v = [body.v[0] + delay * force[0], body.v[1] + delay * force[1]]
	body.x = [body.x[0] + 0.5 * delay * body.v[0], body.x[1] + 0.5 * delay * body.v[1]]
	body.f = force

# Planetary body - easier to use a class than declare the info seperately
class Planet():
	def __init__(self, mass, velocity, location, name):
		force = [0,0]
		angle = random.random() * 0.5 * 3.1415
		
		self.x = [location[0] * math.sin(angle), location[0] * math.cos(angle)]
		self.v = [-1 * velocity[1] * math.sin((0.5 * 3.1415) - angle), velocity[1] * math.cos((0.5 * 3.1415) - angle)]
		self.mass = mass
		self.f = [0,0]
		
		self.orbit_var = 9e50
		self.var_type = "min"
		
		self.path = [[],[]]
		self.counter = 0
		self.av = 0

		self.orig_location = 0#vector_dist(location, [0, 0]) + 0.00000001
		
		self.name = name

	#initial force calculator
	def update_v(self, delay, planets):
		force = [0,0]
		for item in planets:
			body_force = calc_f(self, item)
			force = [force[0] - body_force[0], force[1] - body_force[1]]
		
		self.v = [self.v[0] + 0.5 * delay * force[0], self.v[1] + 0.5 * delay * force[1]]
		self.f = force
	
	# subtraction function, used when calcing grav
	def sub(self, item):
		return([self.x[0] - item.x[0], self.x[1] - item.x[1]])
		
if __name__ == '__main__':
	
	# Bodies
	venus = Planet(M_VEN, [0, V_VEN], [R_VEN, 0], "Venus")
	earth = Planet(M_EARTH, [0, V_EARTH], [R_EARTH, 0], "Earth")
	mars = Planet(M_MARS, [0, V_MARS], [R_MARS, 0], "Mars")
	jupiter = Planet(M_JUP, [0, V_JUP], [R_JUP, 0], "Jupiter")
	saturn = Planet(M_SAT, [0, V_SAT], [R_SAT, 0], "Saturn")
	sun = Planet(M_SUN, [0.0,V_SUN], [R_SUN,0.0], "Sun")
	bodies = [sun, earth, mars, jupiter, saturn]
	planets = [sun, earth, mars, jupiter, saturn]
	
	# Plot type: 1 = apoapsis vs time, 2 = apoapsis trace, 3 = orbital trace
	plot_type = 1
	
	
	# update the original f value and sets the first point for the traces
	for planet in planets:
		planet.update_v(TIME_DELAY, bodies)
		if plot_type == 3:
			planet.path[0].append(planet.x[0] / AU)	
			planet.path[1].append(planet.x[1] / AU)
		elif plot_type == 1:
			planet.path[0].append(1)
			planet.path[1].append(1)
	
	# graph stuff
	fig=plt.figure()
	axis = fig.add_subplot(111)

	# just a few vars
	i = 1
	counter = 1
	t = time()
	
	# Run the script
	while i < DURATION:
		# Drop the solar mass
		sun.mass -= (M_SUN  * 0.3) * (1e-6 / 52) 
		# calculate gravitational force for each planet
		for planet in planets:
			calc_gravity(planet, bodies, TIME_DELAY)
			# Draw graph based on type
	
			dist = math.sqrt((planet.x[0] - sun.x[0]) ** 2 + (planet.x[1] - sun.x[1]) ** 2)
			
			if planet.var_type == "min":
				if dist > planet.orbit_var:
					planet.var_type = "max"
				planet.orbit_var = dist
			else:
				if dist < planet.orbit_var:
					planet.var_type = "min"
					if planet.orig_location == 0 and planet.orbit_var != 9e50:
						planet.orig_location = planet.orbit_var
					if plot_type == 1:
						planet.path[1].append((planet.orbit_var / planet.orig_location))# / AU)
						planet.path[0].append(i / 52)
					elif plot_type == 2:
						planet.path[0].append((planet.x[0] - sun.x[0])/ AU)	
						planet.path[1].append((planet.x[1] - sun.x[1]) / AU)
				planet.orbit_var = dist
			
			# Draw points at location in space	
			if plot_type == 3:
				planet.path[0].append((planet.x[0] - sun.x[0])/ AU )	
				planet.path[1].append((planet.x[1] - sun.x[1])/ AU	 )
			 #elif plot_type == 2 and planet.name == "Sun":
				# planet.path[0].append((planet.x[0])/ AU)	
				# planet.path[1].append((planet.x[1]) / AU)
		
		i += 1
		
		
	print "total time taken: " + str(time() - t)
	
	# Plot graph of planets
	for planet in bodies:
		if planet.name != "Sun":
			#lobf = np.polyfit(planet.path[0],planet.path[1], 1)
			#yp = np.polyval(lobf,planet.path[0])
			axis.plot(planet.path[0],planet.path[1], marker = 'None', label = planet.name)
		#	axis.plot(planet.path[0],yp, marker = ' ', label = planet.name)
	
	# Set up labels etc
	if plot_type == 1:
		axis.set_xlabel("Time (years)")
		axis.set_ylabel("Absolute change in Aphelion (AU)")
	#	axis.set_title("Planetary nebula")
		legend = axis.legend(loc='upper center', shadow=True)
	elif plot_type != 1:
		circle = plt.Circle((sun.x[0], sun.x[1]), radius=R_SUN / AU, color='y')
		axis.add_patch(circle)
	# Draw figure
	fig.savefig("Averaged-orbit-%-loss.png")
	#fig.set_size_inches(6,6)
	#plt.axis([0, i / 52, 0, 0.01])
	plt.show()
