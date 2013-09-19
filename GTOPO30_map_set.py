# Works the same as ferranti_map_set just designed for the 30 arcsecond resolution GTOPO30 map data

import os, math, time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import pylab
from height_maps.ferranti import Ferranti_Height_Map

SQUARE_SIZE = 4800

class GTOPO30_Map_Set():
	
	def __init__(self, start_coords, end_coords, start_string, end_string):
		self.lat = [start_coords[0], end_coords[0]]
		self.lon = [start_coords[1], end_coords[1]]
		
		# Instead of holding the location of the corner, convert it into an offset from the original point
		self.lat[1] = 180#abs(self.lat[0] - self.lat[1])
		self.lon[1] = 360 #abs(self.lon[0] - self.lon[1])
		#print end_coords[0]
		
		# Calcs the jump between each data reading based off on the size of the map
		offset = 1# int(math.sqrt((self.lat[1] + 1) * (self.lon[1] + 1)))
		shortened_offset = int(SQUARE_SIZE)
		# Empty data set sized to fit all of the info
		self.full_data_set = np.zeros((180,360))
		zero_point = 0
		
		t = time.time()
		
		# Loop through each column of maps
		for column in range(-180,181,40):
			
			c_counter = (self.lon[1] / 2) + column
			# And each row
			for row_block in range(-90, 90,50):
			
				if column < 0:
					c_text = "W%s" % str(1000 - column)[1:]
				else:
					c_text = "E%s" % str(1000 + column)[1:]
					
				if row_block <= zero_point:
					r_text = "N%s" % str(100 +  zero_point -  row_block)[1:]
					r_counter = row_block + 90
				else:
					r_text = "S%s" % str(100 + row_block - zero_point)[1:]
					r_counter = row_block + 90
					
				# Log time for later printing
				# File existance check. If the file doesnt exist, it just skips that chunk of array values, hence populating it with 0s earlier
				filename = "/scratch/t/tm197/Internship/GTOPO30/%s%s.DEM" % ( c_text, r_text)
				print(filename)
				if os.path.isfile(filename):
					# Create height map using the currently loaded file
					with open(filename, "rb") as f:
						height = np.fromfile(f, np.dtype('>H'))
					height[height >= 10000] = 0 
					
					for x in range (0, 40):
						for y in range(0, 50):
							array = np.zeros((120,120))
							for a in range(0, 120):
								for b in range(0,120):
									array[a][b] = height[((a + 120 * y) * 4800) + b + 120 * x]
							
							self.full_data_set[r_counter + y][c_counter + x] = np.std(array)
			
		print("Total time: %f" %((time.time() - t) / 60))
		
	def draw(self, filename, boundary):	
		# Convert data map into an image1
		image_map = np.log1p(self.full_data_set)
		boundary = np.log1p(boundary)
		 # Plot the image
		img = plt.imshow(image_map, interpolation = 'bilinear', cmap = cm.spectral, vmin =boundary[0], vmax = boundary[1], alpha = 1.0)
		 
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
