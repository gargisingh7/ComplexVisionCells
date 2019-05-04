import numpy as np 
import cv2
import sys
import time
import random
from PIL import Image,ImageDraw
import matplotlib.pyplot as plt

#makes 100 blocks of width 80
#1 feature
#2 conjunction
def gen(object_num,feature_kind):
	width = 160
	coord_key = {}
	coord_count = 0
	for j in range(0, 10):
		for i in range(0, 10):
			coord_key[coord_count] = (i*width, j*width)
			coord_count = coord_count + 1
	coord_list = random.sample(range(0, 100), object_num)

	im = Image.new('RGB', (width*10, width*10))
	draw = ImageDraw.Draw(im)

	if feature_kind == 1:	#feature search with different colour
		s_x = coord_key[coord_list[0]][0]
		s_y = coord_key[coord_list[0]][1]
		points = [s_x+20,s_y+20,s_x+width-20,s_y+20,s_x+width-20,s_y+width-20,s_x+20,s_y+width-20,s_x+20,s_y+20]
		draw.line(points,fill='red',width=2)
		for i in range(1,len(coord_list)):
			s_x = coord_key[coord_list[i]][0]
			s_y = coord_key[coord_list[i]][1]
			points = [s_x+20,s_y+20,s_x+width-20,s_y+20,s_x+width-20,s_y+width-20,s_x+20,s_y+width-20,s_x+20,s_y+20]
			draw.line(points,fill='blue',width=2)
	elif feature_kind == 2:	#conjunction search
		s_x = coord_key[coord_list[0]][0]
		s_y = coord_key[coord_list[0]][1]
		points = [s_x+20,s_y+20,s_x+width-20,s_y+int(width/2),s_x+20,s_y+width-20,s_x+20,s_y+20]
		draw.line(points,fill='red',width=2)
		for i in range(1,int(len(coord_list)/2)):
			s_x = coord_key[coord_list[i]][0]
			s_y = coord_key[coord_list[i]][1]
			points = [s_x+20,s_y+20,s_x+width-20,s_y+20,s_x+width-20,s_y+width-20,s_x+20,s_y+width-20,s_x+20,s_y+20]
			draw.line(points,fill='red',width=2)
		for i in range(int(len(coord_list)/2),len(coord_list)):
			s_x = coord_key[coord_list[i]][0]
			s_y = coord_key[coord_list[i]][1]
			points = [s_x+20,s_y+20,s_x+width-20,s_y+int(width/2),s_x+20,s_y+width-20,s_x+20,s_y+20]
			draw.line(points,fill='blue',width=2)
	#print(type(coord_list))
	#print(coord_list)
	coord_list = sorted(coord_list)
	#print(coord_list)
	im.save('result_big.png')
	return (feature_kind,coord_list,coord_key,width)


def build_filters():
	filters = []
	ksize = 31
	for theta in np.arange(0, np.pi, np.pi / 2):
		kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
		kern /= 1.5*kern.sum()
		filters.append(kern)
	return filters

def process(img, filters,width):
	accum = np.zeros_like(img)
	count = 0
	feature = []
	for kern in filters:
		fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
		if (count == 0):
			flag1 = 0
			flag2 = 0
			for i in range(int(width/2)-1,int(width/2)+2):
				for j in range(19,22):
					if (list(fimg[i][j]) == [255,0,0]) or (list(fimg[i][j]) == [0,0,255]):
						flag1 = flag1 + 1
					elif (list(fimg[i][j]) == [0,0,0]):
						flag2 = flag2 + 1
			if (flag1 == 9):
				feature.append(1)
			elif (flag2 == 9):
				feature.append(0)
			else:
				feature.append(-1)
		else:
			flag1 = 0
			for i in range(int(width/2)-1,int(width/2)+2):
				for j in range(19,22):
					if (list(fimg[j][i]) == [255,0,0]) or (list(fimg[j][i]) == [0,0,255]):
						flag1 = flag1 + 1
			if (flag1 == 9):
				feature.append(1)
			else:
				feature.append(0)
		count = count + 1
		np.maximum(accum,fimg,accum)
	return (accum,feature)

def m_func(feature_kind,coord_list,coord_key,width):
	img_fn = 'result_big.png'
	 
	img = cv2.imread(img_fn)
	if img is None:
		#print('Failed to load image file:', img_fn)
		sys.exit(1)
	filters = build_filters()
	start_time = time.time()
	if feature_kind == 1:
	 	for i in coord_list:
	 		s_x = coord_key[i][0]
	 		s_y = coord_key[i][1]
	 		if (list(img[s_y+20][s_x+20]) == [0,0,255]):
	 			#print("Found odd stimulus at ",int(s_x/width),int(s_y/width))
	 			break
	elif feature_kind == 2:
		for i in coord_list:
			s_x = coord_key[i][0]
			s_y = coord_key[i][1]
			if (list(img[s_y+20][s_x+20]) == [0,0,255]):
				(res,feature) = process(img[s_y:s_y+width,s_x:s_x+width], filters,width)
				if (list(feature)==[1,1]):
					continue
				elif (list(feature)==[1,0]):
					#print("Found odd stimulus at ",int(s_x/width),int(s_y/width))
					break
				else:
					#print("Garbage shape")
					sys.exit(1)

	end_time = time.time()
	#print("Start time is : ",start_time)
	#print("End time is : ",end_time)
	#print("Time is : ",end_time-start_time)
	return float(end_time - start_time)
	 #print(feature)

m1 = np.zeros(100)
m2 = np.zeros(100) 
for j in range(2,101):
	#print("object_num: ",j)
	t = np.zeros(10)
	for i in range(0,10):
		#print("1 : ",i)
		#print("object_num: ",j)
		k = gen(j,1)
		t[i] = m_func(k[0],k[1],k[2],k[3])
	#print(t)
	m1[j-1] = np.mean(t) 
	t = np.zeros(10)
	for i in range(0,10):
		#print("2 : ",i)
		#print("object_num: ",j)
		k = gen(j,2)
		t[i] = m_func(k[0],k[1],k[2],k[3])
	#print(t)
	m2[j-1] = np.mean(t) 

#print(m1)
#print(m2)
plt.plot(range(1,101),m1,'g',label = "feature search")
plt.plot(range(1,101),m2,'r',label = "conjunction search")
plt.legend(loc='upper left')
plt.show()




