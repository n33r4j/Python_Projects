# Cistercian Numeral Generator

# Original 0 - 9999
# Extended 0 - inf

# Outputs
# - UTF-8 chars (left for later since windows doesn't support UTF-8 in cmd and powershell by default.
# - Images (png/jpg or svg?)

from PIL import Image, ImageDraw

COLOR = "black"
SCALE = 20.0
PLACE = {0: "RT", 1: "LT", 2: "RB", 3: "LB"}
LINE_WIDTH = 3 # Odd numbers lead to better results. Why?
CHAR_SIZE = (2*SCALE, 3*SCALE)
MARGINS = (2*SCALE, 2*SCALE)

# SCALE | LINE WIDTH
# 20    | 4
# 10    | 3

def cistercian_stem(canvas, pos, scale):
	"""
	zero
	pos: center position of the numeral
	scale: size
	"""
	s_x = pos[0]
	s_y = pos[1]-(scale*1.5)
	f_x = s_x
	f_y = s_y+(scale*3.0)
	canvas.line([(s_x, s_y), (f_x, f_y)], fill=COLOR, width=LINE_WIDTH, joint="curve")

def cistercian_one(canvas, ref, place, scale):
	"""
	reference point
	ref: (x,y) -> the position of the top(1,10) or bottom(10,1000) of 
				  the stem.
	place: "RT","LT","RB","LB"
	"""
	s_x = ref[0]
	s_y = ref[1]
	f_x = ref[0]+(scale*1.0 if "R" in place else scale*-1.0)
	f_y = ref[1]
	canvas.line([(s_x, s_y), (f_x, f_y)], fill=COLOR, width=LINE_WIDTH, joint="curve")
	
def cistercian_two(canvas, ref, place, scale):
	s_x = ref[0]
	s_y = ref[1]+(scale*1.0 if "T" in place else scale*-1.0)
	f_x = s_x+(scale*1.0 if "R" in place else scale*-1.0)
	f_y = s_y
	canvas.line([(s_x, s_y), (f_x, f_y)], fill=COLOR, width=LINE_WIDTH, joint="curve")
	
def cistercian_three(canvas, ref, place, scale):
	s_x = ref[0]
	s_y = ref[1]
	f_x = s_x+(scale*1.0 if "R" in place else scale*-1.0)
	f_y = s_y+(scale*1.0 if "T" in place else scale*-1.0)
	canvas.line([(s_x, s_y), (f_x, f_y)], fill=COLOR, width=LINE_WIDTH, joint="curve")

def cistercian_four(canvas, ref, place, scale):
	s_x = ref[0]
	s_y = ref[1]+(scale*1.0 if "T" in place else scale*-1.0)
	f_x = s_x+(scale*1.0 if "R" in place else scale*-1.0)
	f_y = ref[1]
	canvas.line([(s_x, s_y), (f_x, f_y)], fill=COLOR, width=LINE_WIDTH, joint="curve")

def cistercian_five(canvas, ref, place, scale):
	cistercian_one(canvas, ref, place, scale)
	cistercian_four(canvas, ref, place, scale)

def cistercian_six(canvas, ref, place, scale):
	s_x = ref[0]+(scale*1.0 if "R" in place else scale*-1.0)
	s_y = ref[1]
	f_x = s_x
	f_y = s_y+(scale*1.0 if "T" in place else scale*-1.0)
	canvas.line([(s_x, s_y), (f_x, f_y)], fill=COLOR, width=LINE_WIDTH, joint="curve")
	
def cistercian_seven(canvas, ref, place, scale):
	cistercian_one(canvas, ref, place, scale)
	cistercian_six(canvas, ref, place, scale)
	
def cistercian_eight(canvas, ref, place, scale):
	cistercian_two(canvas, ref, place, scale)
	cistercian_six(canvas, ref, place, scale)

def cistercian_nine(canvas, ref, place, scale):
	cistercian_seven(canvas, ref, place, scale)
	cistercian_two(canvas, ref, place, scale)

cistercian = {
	1: cistercian_one,
	2: cistercian_two,
	3: cistercian_three,
	4: cistercian_four,
	5: cistercian_five,
	6: cistercian_six,
	7: cistercian_seven,
	8: cistercian_eight,
	9: cistercian_nine,
}


def write_cistercian(canvas, num: int|str):
	if isinstance(num, int):
		num = str(num)
	if len(num) > 4:
		raise Exception("Classical Cistercian can't represent numbers > 9999. Try the extended version.")
	else:
		# Needs to be updated to be dynamic
		cistercian_stem(canvas, (50,50), SCALE)
		top = (50, 50 - (SCALE*1.5))
		bottom = (50, 50 + (SCALE*1.5))
		
		for i, digit in enumerate(num):
			if digit != "0":
				pos = top if i < 2 else bottom
				cistercian[int(digit)](canvas, pos, PLACE[i], SCALE)


def create_cistercian(num):
	# Find canvas size
	
	pass

if __name__ == "__main__":
	
	for i in range(10000):
		filename = f"output\\{i}_cis.jpg"
		width, height = 100, 100
		im = Image.new('RGB', (width, height), color="white")
		canvas = ImageDraw.Draw(im)
		write_cistercian(canvas, i)
		im.save(filename)
