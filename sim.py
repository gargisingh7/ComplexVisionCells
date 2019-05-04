import numpy as np 
import cv2
import sys
from gen_big import *
import time

def build_filters():
	filters = []
	ksize = 31
	for theta in np.arange(0, np.pi, np.pi / 2):
		kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
		kern /= 1.5*kern.sum()
		filters.append(kern)
	return filters

def process(img, filters):
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

if __name__ == '__main__':
	img_fn = 'result_big.png'
	 
	img = cv2.imread(img_fn)
	if img is None:
		print('Failed to load image file:', img_fn)
		sys.exit(1)
	filters = build_filters()
	start_time = time.time()
	if feature_kind == 1:
	 	for i in coord_list:
	 		s_x = coord_key[i][0]
	 		s_y = coord_key[i][1]
	 		imgg = img.copy()
	 		for i in range(int(width/2)-7,int(width/2)+8):
	 			for j in range(int(width/2)-7,int(width/2)+8):
	 				imgg[s_y+i][s_x+j][0]=255
	 				imgg[s_y+i][s_x+j][1]=255
	 				imgg[s_y+i][s_x+j][2]=255
	 		cv2.imshow('result', imgg)
	 		cv2.waitKey(2000)
	 		if (list(img[s_y+20][s_x+20]) == [0,0,255]):
	 			print("Found odd stimulus at ",int(s_x/width),int(s_y/width))
	 			break
	elif feature_kind == 2:
		for i in coord_list:
			s_x = coord_key[i][0]
			s_y = coord_key[i][1]
			imgg = img.copy()
			for i in range(int(width/2)-7,int(width/2)+8):
				for j in range(int(width/2)-7,int(width/2)+8):
					imgg[s_y+i][s_x+j][0]=255
					imgg[s_y+i][s_x+j][1]=255
					imgg[s_y+i][s_x+j][2]=255
			cv2.imshow('result', imgg)
			cv2.waitKey(2000)
			if (list(img[s_y+20][s_x+20]) == [0,0,255]):
				(res,feature) = process(img[s_y:s_y+width,s_x:s_x+width], filters)
				imgg[s_y:s_y+width,s_x:s_x+width]=res
				for i in range(int(width/2)-7,int(width/2)+8):
					for j in range(int(width/2)-7,int(width/2)+8):
						imgg[s_y+i][s_x+j][0]=255
						imgg[s_y+i][s_x+j][1]=255
						imgg[s_y+i][s_x+j][2]=255
				cv2.imshow('result', imgg)
				cv2.waitKey(2000)
				if (list(feature)==[1,1]):
					continue
				elif (list(feature)==[1,0]):
					print("Found odd stimulus at ",int(s_x/width),int(s_y/width))
					break
				else:
					print("Garbage shape")

	
	end_time = time.time()
	print("Start time is : ",start_time)
	print("End time is : ",end_time)
	print("Time is : ",end_time-start_time)

	 #print(feature)

