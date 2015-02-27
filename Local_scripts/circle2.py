#!/usr/bin/env python
# Takes a list of username pairs, returns a circular relation graph
# Author: __brony__

from PIL import Image, ImageDraw, ImageFont
import math
import colorsys
import random

img_size = 1600
edge = 75
fontsize = 19
numspace = 1.04
cd = 8
fc = fontsize/2

pairs = [t[:-1].split('\t') for t in lines]
names = list(set([t2 for t1 in pairs for t2 in t1]))
#print(names, '\n\n', pairs, '\n\n', len(names))

num_points = len(names)
extra = img_size // 4
image = Image.new('RGB', (img_size+extra, img_size), color=0)
draw = ImageDraw.Draw(image)
center = img_size / 2
radius = center - edge
draw.ellipse((center-radius, center-radius, center+radius, center+radius), outline='blue')
angle_inc = 2*math.pi / num_points
coords = []
font = ImageFont.truetype('arial.ttf',fontsize)

color = [tuple([int(255*c) for c in t]) for t in [colorsys.hls_to_rgb(float(i)/num_points,0.7,1) for i in range(num_points)]]
random.shuffle(color)

for i in range(num_points):
	x = radius * math.cos(angle_inc * i)
	y = radius * math.sin(angle_inc * i)
	draw.ellipse((x+center-cd/2, y+center-cd/2, x+center+cd/2, y+center+cd/2), fill=color[i])
	draw.text((x*numspace+center-fc, y*numspace+center-fc), "%02d" % i,font=font)
	coords.append((x+center,y+center))

for i in range(len(names)):
	draw.text((img_size+fontsize, (fontsize+3)*i+2), "%02d: %s" % (i, names[i]),font=font)
	draw.ellipse((img_size,(fontsize+3)*i+2,img_size+fontsize,(fontsize+3)*i+2+fontsize), fill=color[i])
#print(color)
for p in pairs:
	draw.line([coords[names.index(p[i])] for i in (0,1)],fill=color[names.index(p[0])])

image.show()
image.save('circle.png')