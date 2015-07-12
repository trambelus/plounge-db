#!/usr/bin/env python
# Draws a mystic rose or something.
# Author: __brony__

from PIL import Image, ImageDraw, ImageFont
import math
import colorsys
import random

img_size = 2560
edge = 75


num_points = 32
image = Image.new('RGB', (img_size, img_size), color=0)
draw = ImageDraw.Draw(image)
center = img_size / 2
radius = center - edge
angle_inc = 2*math.pi / num_points
coords = []

#color = [tuple([int(255*c) for c in t]) for t in [colorsys.hls_to_rgb(float(i)/num_points,0.7,1) for i in range(num_points)]]
#random.shuffle(color)

for i in range(num_points):
	x = radius * math.cos(angle_inc * i)
	y = radius * math.sin(angle_inc * i)
	coords.append((x+center,y+center))

ml = len(coords)

[draw.line((coords[i], coords[j]), width=4, fill=tuple([int(255*(ml-i)/ml)]*3)) for i in range(ml) for j in range(ml)]

image.show()
image.save('circle.png')