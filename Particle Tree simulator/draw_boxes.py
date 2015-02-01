# Draws boxes around each "node" on the tree

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib import animation

fig = plt.figure()
axis = fig.add_subplot(111)

def animate(FILENUM):
	#axis.clear()
	f = open("DATA/TREE_" + str(FILENUM+1))	


	vals = []

	text = f.readlines()
	for line in text:
		vals = line.split(",")
		for i in range(0,3):
			vals[i] = float(vals[i])
		path = Path([ [vals[0], vals[1]] , [vals[0]+vals[2], vals[1]] , [vals[0]+vals[2], vals[1]-vals[2]], [vals[0], vals[1]-vals[2]], [vals[0], vals[1]] ])
		
		patch = PathPatch(path, facecolor='none')
		#axis.add_patch(patch);

	f = open("DATA/N_BODY_" + str(FILENUM+997))

	dx = []
	dy = []	
	text = f.readlines()

	for line in text:
		if len(line) > 10:
			vals = line.split(",")	
			dx.append(float(vals[1]))
			dy.append(float(vals[2]))

	axis.scatter(dx, dy, c='RED', marker='.', s=1)
	axis.scatter(dx[0], dy[0], c='RED', marker='x', s=5)
	axis.set_xlim(-100, 100)
	axis.set_ylim(-100, 100)
	
	return axis,
	
# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate,
                               frames=1)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html

mywriter = animation.FFMpegFileWriter()
#anim.save('galaxy_animation_box.mp4', fps=30, writer=mywriter, dpi=300, bitrate=-1)	


fig.savefig('Tree.png')