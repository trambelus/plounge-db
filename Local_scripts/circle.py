#!/usr/bin/env python
# Takes a list of username pairs, returns a circular relation graph

from PIL import Image, ImageDraw, ImageFont
import math
import colorsys
import random
import sys

img_size = 1000
extra = img_size // 6
#extra = 0
edge = 75
fontsize = 12
numspace = 1.02
cd = 8
fc = fontsize/2

with open(sys.argv[1],'r') as f:
	lines = f.readlines()
pairs = [t[:-1].split('\t') for t in lines]
names = list(set([t2 for t1 in pairs for t2 in t1]))
#print(names, '\n\n', pairs, '\n\n', len(names))

num_points = len(names)
image = Image.new('RGB', (img_size+extra, img_size), color=0)
draw = ImageDraw.Draw(image)
center = img_size / 2
radius = center - edge
draw.ellipse((center-radius, center-radius, center+radius, center+radius), outline='blue')
angle_inc = 2*math.pi / num_points
coords = []
font = ImageFont.truetype('arial.ttf',fontsize)

color = [colorsys.hls_to_rgb(float(i)/num_points,0.7,1) for i in range(num_points)]
color = [tuple([int(255*c) for c in t]) for t in color]
random.shuffle(color)

# Draw 
for i in range(num_points):
	x = radius * math.cos(angle_inc * i)
	y = radius * math.sin(angle_inc * i)
	draw.ellipse((x+center-cd/2, y+center-cd/2, x+center+cd/2, y+center+cd/2), fill=color[i])
	draw.text((x*numspace+center-fc, y*numspace+center-fc), "%02d" % i,font=font)
	coords.append((x+center,y+center))

# Draw name dots
for i in range(len(names)):
	draw.text((img_size+fontsize*1.5, (fontsize+3)*i+2), "%02d: %s" % (i, names[i]),font=font)
	draw.ellipse((img_size,(fontsize+3)*i+2,img_size+fontsize,(fontsize+3)*i+2+fontsize), fill=color[i])
#print(color)
# Draw lines
for p in pairs:
	draw.line([coords[names.index(p[i])] for i in (0,1)],fill=color[names.index(p[0])])

image.show()
image.save('%s.png' % sys.argv[1][:-4])

# Pair selection:
# SELECT DISTINCT CASE WHEN c1.author > c2.author THEN c1.author ELSE c2.author END AS a1,
# CASE WHEN c1.author > c2.author THEN c2.author ELSE c1.author END AS a2, COUNT(*) AS n
# FROM comments AS c1 INNER JOIN comments AS c2 ON c1.id = c2.parent_id
# WHERE a1 != '[deleted]' AND a2 != '[deleted]' GROUP BY a1, a2 HAVING n >= 100 ORDER BY n DESC
