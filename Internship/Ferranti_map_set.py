# Allows the creation of larger maps formed from multiple 1 degree files.
# Was initially designed to allow for input of starting coordinates but 
# in the end i removed that feature as the primary focus was to draw large
# maps of the entire earth.

import os, math, time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import pylab
from height_maps.ferranti import Ferranti_Height_Map

SQUARE_SIZE = 1201

class Ferranti_Map_Set():
	
	def __init__(self, start_coords, end_coords, start_string, end_string):

		
		# Instead of holding the location of the corner, convert it into an offset from the original point
		self.lat[1] = 1
		self.lon[1] = 1
		#print end_coords[0]
		
		# Calcs the jump between each data reading based off on the size of the map
		offset = 1#int(math.sqrt((self.lat[1] + 1) * (self.lon[1] + 1)) / 6)
		shortened_offset = int(SQUARE_SIZE/offset)
		
		# Variables to hold the min/max data
		boundaries = [0,0]
		
		# Empty data set sized to fit all of the info
		self.full_data_set = np.zeros(((SQUARE_SIZE * (self.lat[1])) / offset, (SQUARE_SIZE * (self.lon[1]) / offset)))
		zero_point = 90
		a = time.time()
		i = 1
		# Loop through each column of maps
		for column in range(60,61):#-180, 181,1):
			
			c_counter = 0#(self.lon[1] / 2) + column 
			# And each row
			for row_block in range(40, 41):#self.lat[1],1):
			
				# Log time for later printing
				# File existance check. If the file doesnt exist, it just skips that chunk of array values, hence populating it with 0s earlier
				if column < 0:
					c_text = "W%s" % str(1000 - column)[1:]
				else:
					c_text = "E%s" % str(1000 + column)[1:]
					
				if row_block <= zero_point:
					r_text = "N%s" % str(100 +  zero_point -  row_block)[1:]
					r_counter = row_block - 40
				else:
					r_text = "S%s" % str(100 + row_block - zero_point)[1:]
					r_counter = row_block
				filename = "/scratch/t/tm197/Internship/data/%s/%s%s.hgt" % (c_text, r_text, c_text)
				print(filename)
				if os.path.isfile(filename):
					# Create height map using the currently loaded file
					with open(filename, "rb") as f:
						height = np.fromfile(f, np.dtype('d'))
					
					# Export points from the height map
					for r in range(0, SQUARE_SIZE, offset):
						for c in range(0,SQUARE_SIZE, offset):
							self.full_data_set[(r_counter * shortened_offset) + (r / offset)][(c_counter * shortened_offset) + (c / offset)] = height[(SQUARE_SIZE * r) + c]	
				print("Time taken so far: %f" % ((time.time() - a)/60))
		self.full_data_set[self.full_data_set >= 10000] = 0
		print("Total time: %f" %((time.time() - a) / 60))
		
		boundary = [np.amin(self.full_data_set), np.amax(self.full_data_set)]
		
	def draw(self, filename, boundary):	
		# Convert data map into an image
		image_map = np.log1p(self.full_data_set)
		boundary = np.log1p(boundary)
		 # Plot the image
		img = plt.imshow(image_map, interpolation = 'bilinear', cmap = cm.spectral, vmin = boundary[0], vmax = boundary[1],  alpha = 1.0)
		 
		# Graph settings
		plt.grid(False)
		plt.axis('off')
		fig = matplotlib.pyplot.gcf()
		#ax = plt.subplot(111)
		#axcolor = fig.add_axes([0.25,0.28,0.5,0.01], title = "URF") 
		#bar = pylab.colorbar(img, axcolor, cmap =  cm.spectral, orientation = 'horisontal', boundaries = None, values = None)
		#bar.set_ticks((0,8.83))
		#bar.set_ticklabels(("Drowning", "Practically space"))	
		fig.set_size_inches(20, 20)
		
		# Save to file
		plt.savefig(filename, bbox_inches = 'tight', dpi = 72)	
