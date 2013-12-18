# Ah, my pride and joy

# This script converts Ferranti SRTM data into the same format as the GTOPO30. This
# allows the use of updated, abet averaged, data with the new systems, greatly
# increasing their accuracy. A comparison picture can be seen here: http://i.imgur.com/22VT6x0.jpg


import os, math, time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import pylab
from height_maps.ferranti import Ferranti_Height_Map

SQUARE_SIZE = 120

class Ferranti_conversion():
	
	def __init__(self, start_coords, end_coords, start_string, end_string):
	
		self.lat = [start_coords[0], end_coords[0]]
		self.lon = [start_coords[1], end_coords[1]]
		
		# Make sure that the coords are arranged west => east and north => south to make combining the maps easier
		if self.lat[1] < self.lat[0]:
			placeholder = self.lat[0]
			self.lat[0] = self.lat[1]
			self.lat[1] = placeholder
			
		if self.lon[1] < self.lon[0]:
			placeholder = self.lon[0]
			self.lon[0] = self.lon[1]
			self.lon[1] = placeholder
		
		# Instead of holding the location of the corner, convert it into an offset from the original point
		self.lat[1] = 1#80#abs(self.lat[0] - self.lat[1])
		self.lon[1] = 1#360 #abs(self.lon[0] - self.lon[1])
		#print end_coords[0]
		
		# Calcs the jump between each data reading based off on the size of the map
		offset = 1#int(math.sqrt((self.lat[1] + 1) * (self.lon[1] + 1)) / 6)
		shortened_offset = int(SQUARE_SIZE/offset)
		
		# Variables to hold the min/max data
		boundaries = [0,0]
		
		# Empty data set sized to fit all of the info
		zero_point = 0
		t = time.time()
		
		# Loop through each column of maps
		for file_ID in range(3,4):
			new_data = np.zeros((6000,4800), "H")
			for column in range(-180 + (file_ID * 40) , -140 + (file_ID * 40) ):
				
				c_counter = -1 * (-180 + (file_ID * 40))  + column 
				# And each row
				for row_block in range(-89, -39):#self.lat[1],1):
				
					# Log time for later printing
					# File existance check. If the file doesnt exist, it just skips that chunk of array values, hence populating it with 0s earlier
					if column < 0:
						c_text = "W%s" % str(1000 - column)[1:]
					else:
						c_text = "E%s" % str(1000 + column)[1:]
						
					if row_block <= zero_point:
						r_text = "N%s" % str(100 -  row_block)[1:]
						r_counter = row_block + 89
					else:
						r_text = "S%s" % str(100 + row_block)[1:]
						r_counter = row_block + 89
					filename = "/scratch/t/tm197/Internship/data/%s/%s%s.hgt" % (c_text, r_text, c_text)
					print(filename)
					if os.path.isfile(filename):
						# Create height map using the currently loaded file
						with open(filename, "rb") as f:
							height = np.fromfile(f, np.dtype('>H'))
						height[height >= 10000] = 0
						for i in range (0,120):
							for a in range(0,120):
								av = 0
								for b in range(0,10):
									for c in range(0,10):
										av += height[(((i * 10) + b) * 1201) + (a * 10) + c]

								new_data[r_counter * 120 + i][c_counter * 120 + a] = av / 100
				
					print("Time taken so far: %f" % ((time.time() - t)/60))
			with open("W%fN90.DEM" % file_ID , "wb") as f:
					new_data.byteswap(True)
					new_data.tofile(f)
			self.full_data_set = new_data
			print("Total time: %f" %((time.time() - t) / 60))
				
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
