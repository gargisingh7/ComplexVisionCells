import sys
import random
from PIL import Image,ImageDraw

width = int(sys.argv[1])
object_kind = int(sys.argv[2])
color = int(sys.argv[3])
#1 triangle
#2 square
#1 red
#2 blue
if (width<50):
	print("Code is not commpatible for low width range")
	sys.exit(1)

im = Image.new('RGB', (width, width))
draw = ImageDraw.Draw(im)

if object_kind == 2:
	s_x = 0
	s_y = 0
	points = [s_x+20,s_y+20,s_x+width-20,s_y+20,s_x+width-20,s_y+width-20,s_x+20,s_y+width-20,s_x+20,s_y+20]
elif object_kind == 1:
	s_x = 0
	s_y = 0
	points = [s_x+20,s_y+20,s_x+width-20,s_y+int(width/2),s_x+20,s_y+width - 20,s_x+20,s_y+20]
if (color == 1):
	draw.line(points,fill='red',width=5)
else:
	draw.line(points,fill='blue',width=5)
im.save('result.png')
