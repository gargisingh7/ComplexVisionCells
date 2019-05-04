import numpy as np 
import cv2
import sys

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
		cv2.imshow('result', fimg)
		cv2.waitKey(2000)
		if (count == 0):
			flag1 = 0
			flag2 = 0
			for i in range(39,42):
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
			for i in range(39,42):
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
	 try:
	 	img_fn = sys.argv[1]
	 except:
	 	img_fn = 'result1.png'
	 
	 img = cv2.imread(img_fn)
	 if img is None:
	 	print('Failed to load image file:', img_fn)
	 	sys.exit(1)
	 
	 filters = build_filters()
	 
	 (res1,feature) = process(img, filters)
	 #print(feature)
	 if (list(feature)==[1,1]):
	 	print("Its a square")
	 elif (list(feature)==[1,0]):
	 	print("Its a triangle")
	 else:
	 	print("Garbage shape")

	 cv2.imshow('result', res1)
	 cv2.waitKey(2000)
