import sys
import random
from PIL import Image,ImageDraw
#makes 100 blocks of width 80
object_num = int(sys.argv[1])
feature_kind = int(sys.argv[2])
#1 feature
#2 conjunction
width = 150
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