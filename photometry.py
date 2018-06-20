#! /usr/bin/env python
import math, sys
import numpy as np
from PIL import Image, ImageTk



#---------- Distance Function ------------#
def dist(x, c):
	return math.sqrt((x[0]-c[0])**2 + (x[1]-c[1])**2)
#-----------------------------------------#


#--------- Barycentric Triangle ----------#
def sign(p1, p2, p3):
	return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
	
def inTriangle(pt, v1, v2, v3):
	b1 = sign(pt, v1, v2) < 0
	b2 = sign(pt, v2, v3) < 0
	b3 = sign(pt, v3, v1) < 0
	
	return ((b1 == b2) and (b2 == b3))
#-----------------------------------------#


#------------ Solid Circle ---------------#
def SolidCircle(img, radius_val):
		
	neg = raw_input("Negative color? (y/n) ")
	if(neg == "y"):
		neg = True
	else:
		neg = False

	new_data = []
	
	width, height = img.size
	center = (width/2, height/2)
	
	circle_radius = int(center[0] * radius_val)

	
	matrix = list(img.getdata())
	matrix = [matrix[offset:offset+width] for offset in range(0, width*height, width)]

	#print "height range: ", center[1] - circle_radius, " to ", center[1] + circle_radius
	#print "width range: ", center[0] - circle_radius, " to ", center[0] + circle_radius
	
	for j in range(center[1] - circle_radius, center[1] + 1):
		for i in range(center[0] - circle_radius, center[0] + circle_radius):
			x = (i,j)
			d = dist(x, center)
			
			if(j == center[1] and i < center[0]):
				if neg:
					x1 = 255 - matrix[j][i][0]
					y1 = 255 - matrix[j][i][1]
					z1 = 255 - matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = 255 - matrix[j][width-i][0]
					y2 = 255 - matrix[j][width-i][1]
					z2 = 255 - matrix[j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[j][width-i] = temp_tup1
				else:
					x1 = matrix[j][i][0]
					y1 = matrix[j][i][1]
					z1 = matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = matrix[j][width-i][0]
					y2 = matrix[j][width-i][1]
					z2 = matrix[j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[j][width-i] = temp_tup1
				
			if (d <= circle_radius and j < center[1]):
				if neg:
					x1 = 255 - matrix[j][i][0]
					y1 = 255 - matrix[j][i][1]
					z1 = 255 - matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = 255 - matrix[height-j][width-i][0]
					y2 = 255 - matrix[height-j][width-i][1]
					z2 = 255 - matrix[height-j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[height-j][width-i] = temp_tup1
				else:
					x1 = matrix[j][i][0]
					y1 = matrix[j][i][1]
					z1 = matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = matrix[height-j][width-i][0]
					y2 = matrix[height-j][width-i][1]
					z2 = matrix[height-j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[height-j][width-i] = temp_tup1
					
	for j in range(0, len(matrix)):
		for i in range(0, len(matrix[0])):
			new_data.append(matrix[j][i])
	
	#new_data = list(matrix)

	#img_out = Image.new(img.mode, (radius*2, radius*2))
	img_out = Image.new(img.mode, img.size)
	img_out.putdata(new_data)
	
	#img_out.show()

	#offset = ((width - radius*2)/2, (height - radius*2)/2)
	#img.paste(img_out, offset)
	#img.show()
	#img_out.save("hi.jpg")
	#img_out.show()
	return img_out
#-----------------------------------------#


#------------ Hollow Circle ---------------#
def HollowCircle(img, radius_val, radius_width):
	

	new_data = []
	width, height = img.size
	center = (width/2, height/2)
	radius = int(width * radius_val)
	bad_zone = radius - radius_width
	
	matrix = list(img.getdata())
	matrix = [matrix[offset:offset+width] for offset in range(0, width*height, width)]


	
	for j in range(center[1] - radius, center[1] + radius):
		for i in range(center[0] - radius, center[0] + radius):
			x = (i,j)
			d = dist(x, center)
			if(d <= radius and d >= bad_zone):
					x = 255 - matrix[j][i][0]
					y = 255 - matrix[j][i][1]
					z = 255 - matrix[j][i][2]
					temp_tup = (x, y, z)
			else:
				temp_tup = matrix[j][i]
				
			new_data.append(temp_tup)


	img_out = Image.new(img.mode, (radius*2, radius*2))
	img_out.putdata(new_data)
	
	offset = ((width - radius*2)/2, (height - radius*2)/2)
	img.paste(img_out, offset)

	return img
#-----------------------------------------#

#------------ Hollow Inverted Circle ---------------#
def HollowInvCircle(img, radius_val, radius_width):
	
	# ---- extra input ---- #
	neg = raw_input("Negative color? (y/n) ")
	if neg == "y":
		neg = True
	else:
		neg = False
	# --------------------- #

	new_data = []
	
	width, height = img.size
	center = (width/2, height/2)
	
	circle_radius = int(center[0] * radius_val)
	
	bad_zone = circle_radius - radius_width
	
	matrix = list(img.getdata())
	matrix = [matrix[offset:offset+width] for offset in range(0, width*height, width)]

	for j in range(center[1] - circle_radius, center[1] + 1):
		for i in range(center[0] - circle_radius, center[0] + circle_radius):
			x = (i,j)
			d = dist(x, center)
			
			if(j == center[1] and i < center[0] and d >= bad_zone):
				if neg:
					x1 = 255 - matrix[j][i][0]
					y1 = 255 - matrix[j][i][1]
					z1 = 255 - matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = 255 - matrix[j][width-i][0]
					y2 = 255 - matrix[j][width-i][1]
					z2 = 255 - matrix[j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[j][width-i] = temp_tup1
				else:
					x1 = matrix[j][i][0]
					y1 = matrix[j][i][1]
					z1 = matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = matrix[j][width-i][0]
					y2 = matrix[j][width-i][1]
					z2 = matrix[j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[j][width-i] = temp_tup1

			if(d <= circle_radius and d >= bad_zone and j < center[1]):
				if neg:
					x1 = 255 - matrix[j][i][0]
					y1 = 255 - matrix[j][i][1]
					z1 = 255 - matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = 255 - matrix[height-j][width-i][0]
					y2 = 255 - matrix[height-j][width-i][1]
					z2 = 255 - matrix[height-j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[height-j][width-i] = temp_tup1
				else:
					x1 = matrix[j][i][0]
					y1 = matrix[j][i][1]
					z1 = matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)
					
					x2 = matrix[height-j][width-i][0]
					y2 = matrix[height-j][width-i][1]
					z2 = matrix[height-j][width-i][2]
					temp_tup2 = (x2, y2, z2)
					matrix[j][i] = temp_tup2
					matrix[height-j][width-i] = temp_tup1
					
	for j in range(0, len(matrix)):
		for i in range(0, len(matrix[0])):
			new_data.append(matrix[j][i])
	
	#new_data = list(matrix)

	#img_out = Image.new(img.mode, (radius*2, radius*2))
	img_out = Image.new(img.mode, img.size)
	img_out.putdata(new_data)
	img_out.save(str(count) + ".jpg")
	#img_out.show()

	#offset = ((width - radius*2)/2, (height - radius*2)/2)
	#img.paste(img_out, offset)
	#img.show()
	#img_out.save("hi.jpg")
	#img_out.show()
	return img_out
#-----------------------------------------#


#------------ Triangle ---------------#
def Triangle(img, radius_val, radius_width):
	
	# ---- extra input ---- #
	neg = raw_input("Negative color? (y/n) ")
	if neg == "y":
		neg = True
	else:
		neg = False
	# --------------------- #

	new_data = []
	
	width, height = img.size
	center = (width/2, height/2)
	
	tri_radius = int(center[0] * radius_val)
	ign_radius = tri_radius - radius_width
	
	seg = math.sqrt(tri_radius*tri_radius - (0.5*tri_radius)*(0.5*tri_radius))
	ign_seg = math.sqrt(ign_radius*ign_radius - (0.5*ign_radius)*(0.5*ign_radius))
	
	v1 = (center[0], center[1] - tri_radius)
	v2 = (center[0] - seg, center[1] + 0.5*tri_radius)
	v3 = (center[0] + seg, center[1] + 0.5*tri_radius)
	
	w1 = (center[0], center[1] - ign_radius)
	w2 = (center[0] - ign_seg, center[1] + 0.5*ign_radius)
	w3 = (center[0] + ign_seg, center[1] + 0.5*ign_radius)


	
	matrix = list(img.getdata())
	matrix = [matrix[offset:offset+width] for offset in range(0, width*height, width)]



	for j in range(center[1] - tri_radius, center[1] + tri_radius):
		for i in range(center[0] - tri_radius, center[0] + tri_radius):
			x = (i,j)

			if(inTriangle(x, v1, v2, v3) and not inTriangle(x, w1, w2, w3)):
				if neg:
					x1 = 255 - matrix[j][i][0]
					y1 = 255 - matrix[j][i][1]
					z1 = 255 - matrix[j][i][2]
					temp_tup1 = (x1, y1, z1)

					matrix[j][i] = temp_tup1
				
	for j in range(0, len(matrix)):
		for i in range(0, len(matrix[0])):
			new_data.append(matrix[j][i])

	img_out = Image.new(img.mode, img.size)
	img_out.putdata(new_data)
	img_out.save(str(count) + ".jpg")


	return img_out
#-----------------------------------------#



#------------ Transparency Circle ---------------#
def TransparencyCircle(img, radius_val, radius_width, neg):
	

	new_data = []
	width, height = img.size
	center = (width/2, height/2)
	radius = int(width * radius_val)
	bad_zone = radius - radius_width
	
	matrix = list(img.getdata())
	matrix = [matrix[offset:offset+width] for offset in range(0, width*height, width)]

	#moose = Image.open("moose.jpg")

	
	for j in range(center[1] - radius, center[1] + radius):
		for i in range(center[0] - radius, center[0] + radius):
			x = (i,j)
			d = dist(x, center)
			x, y, z = 0, 0, 0
			if(d <= radius and d >= bad_zone):
				if neg:
					x = 255 - matrix[j][i][0]
					y = 255 - matrix[j][i][1]
					z = 255 - matrix[j][i][2]
				else:
					x = matrix[j][i][0]
					y = matrix[j][i][1]
					z = matrix[j][i][2]
				temp_tup = (x, y, z)
			else:
				temp_tup = (255, 255, 255, 0)
				
			new_data.append(temp_tup)


	#img_out = Image.new('RGBA', (radius*2, radius*2))
	img_out = Image.new('RGBA', img.size)
	#img_out = Image.new(img.mode, (radius*2, radius*2))
	img_out.putdata(new_data)
	
	#img_out.show()
	#moose = moose.convert('RGBA')
	#img2 = img.copy()
	#img3 = img.copy()


	#offset = ((width - radius*2)/2, (height - radius*2)/2)
	#img.paste(img_out, offset, img_out)
	#img.save("1.jpg")
	
	#im2 = img_out.copy()
	#im2 = im2.resize((radius*2 + 50, radius*2 + 50), Image.ANTIALIAS)
	#img2.paste(im2, offset, im2)
	#img2.save("2.jpg")
	
	#im3 = img_out.copy()
	#im3 = im3.resize((radius*2 + 100, radius*2 + 100), Image.ANTIALIAS)
	#img3.paste(im3, offset, im3)
	#img3.save("3.jpg")
	#
	
	return img_out
#-----------------------------------------#



#------------------- MAIN ----------------------#
filename = raw_input("Which photo would you like to open? ")
original = Image.open(filename)


choice = 3
count = 1

img = original.copy()

while(1):
	choice = int(raw_input("1. Inverted Solid Circle \n2. Negative Ring \n3. Inverted Ring \n4. Triangle \n"))
	
	if choice == 1:
		radius_val = float(raw_input("Enter the circle radius as a ratio of your image width, between 0 and 1: "))
		img = SolidCircle(img, radius_val)
		img.show()
	
	if choice == 2:
		radius_val = float(raw_input("Enter the ring radius as a ratio of your image width, between 0 and 1: "))
		radius_width = float(raw_input("Enter the width of your ring: "))
		img = HollowCircle(img, radius_val, radius_width)
		img.show()
		
	if choice == 3:
		radius_val = float(raw_input("Enter the ring radius as a ratio of your image width, between 0 and 1: "))
		radius_width = float(raw_input("Enter the width of your ring: "))
		img = HollowInvCircle(img, radius_val, radius_width)
		img.show()
		
	if choice == 4:
		radius_val = float(raw_input("Enter the triangle radius as a ratio of your image width, between 0 and 1: "))
		radius_width = float(raw_input("Enter the width of your triangle: "))
		img = Triangle(img, radius_val, radius_width)
		img.show()
		
	
	count += 1
	inp = raw_input("Would you like to keep stacking? (y/n) [or 'r' to restart] ")
	
	if inp == "r":
		count = 1
		img = original.copy()
	
	if inp == "n":
		break
		
	



#######################


