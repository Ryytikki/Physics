import struct, string, array, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab

class Ferranti_Height_Map(object):
	# Parse the data and save the heights to .height
	def __init__(self, filename):
		
		with open(filename, "rb") as f:
			self.height = np.fromfile(f, np.dtype('>H'))
		
		# Create empty map for all the data
		self.data_map = np.zeros((1201,1201))
		highest = 0
		
		# Calculate the lat/long values of the file
		self.lat_offset = 0
		self.lon_offset = 0
	
	
	def fully_parse(self):
		# Loop through rows/columns
		for r in range(0,1201):
			for c in range(0,1201):
				# Retrieve height value from the stored map
				point = self.height[(1201 * r) + c]
				# Check for null values
				if point >= 10000:
					point = 0
				
				self.data_map[r][c] = point
				
		
	def draw(self, filename):
		# Complete data parsing (wasnt completed earlier to allow multi map integration)
		self.fully_parse()
		# Convert data map into an image
		image_map = np.log1p(self.data_map)
		 # Plot the image
		plt.imshow(image_map, interpolation = 'bilinear', cmap = cm.spectral, alpha = 1.0)
		 
		# Graph settings
		plt.grid(False)
		plt.axis('off')
		fig = matplotlib.pyplot.gcf()
		fig.set_size_inches(12, 12)
		# Save to file
		plt.savefig(filename, bbox_inches = 'tight', dpi = 100)	  
