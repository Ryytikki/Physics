# Draws the particle tree as a scatter plot and animates

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
#plt.rcParams['animation.ffmpeg_path'] = 'C:\Users\Tom\Downloads\ffmpeg\ffmpeg\bin'
import numpy as np

fig = plt.figure()
axis = fig.add_subplot(111)#, projection='3d')

# animation function.  This is called sequentially
def animate(i):
	axis.clear()
	f = open("DATA/N_BODY_" + str(i))
	dx = []
	dy = []	
	vals = []
	text = f.readlines()

	i = 0
	
	for line in text:
		if len(line) > 10:
			vals = line.split(",")	
			dx.append(float(vals[1]))
			dy.append(float(vals[2]))

	axis.set_xlim(-2000, 2000)
	axis.set_ylim(-2000, 2000)
	scatter = axis.scatter(dx, dy, c='RED', marker='.', s=1)
	scatter = axis.scatter(dx[0], dy[0], c='RED', marker='x', s=1)
	return scatter,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate,
                               frames=100, blit=True, interval = 0)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html	

mywriter = animation.FFMpegFileWriter()
anim.save('galaxy_animation.mp4', fps=120, writer=mywriter, dpi=300, bitrate=-1)

#plt.show()