from turtle import *
from turtle import TNavigator

def pushT(turt, turt_deg, stack):
	stack.append((turt.xcor(), turt.ycor(), turt_deg))


def popT(turt, turt_deg, stack):
	x = stack[-1][0]
	y = stack[-1][1]
	turt_deg = stack[-1][2]
	del stack[-1]
	turt.penup()
	turt.goto(x, y)
	turt.setheading(turt_deg)
	turt.pendown()


def green_rule(n: int):
	axiom = "f"
	temp_ax = ""
	rules = {"+": "+",
			 "-": "-",
			 "[": "[",
			 "]": "]",
			 "f": "f[+ffh]f[-ff-fg]",
			 "g": "[--f][++ff]f",
			 "h": "[+++ff]"}

	for k in range(n):
		for ch in axiom:
			temp_ax += rules[ch]
		axiom = temp_ax
		temp_ax = ""

	return axiom


def root_rule(n: int):
	axiom = "+wf--xf---yf--zf"
	temp_ax = ""
	rules = {"+": "+",
			"-": "-",
			"f": "f",
			"[": "[",
			"]": "]",
			"w": "yf++zf----xf[-yf----wf]++",
			"x": "+yf--zf[---wf--xf]+",
			"y": "-wf++xf[+++yf+++zf]-",
			"z": "--yf++++wf[+zf++++xf]--xf"}

	for k in range(n):
		for ch in axiom:
			temp_ax += rules[ch]
		axiom = temp_ax
		temp_ax = ""

	return axiom


def draw_lsys(turtle, dd,  rule: str, f: float, deg: float, stack):
	# dd - угол поворота объекта черепахи
	# f - длина линий
	# Текущий поворот черепахи
	# + - поворот направо
	# - - поворот налево 
	# [ - положить угол поворота и координаты в стек
	# ] - достать угол и координаты из стека
	# f - двигаться вперед
	# Любой другой символ используется для генерации строки
	d = dd
	for ch in rule:
		if ch == "+":
			turtle.right(deg)
			d -= deg
		elif ch == "-":
			turtle.left(deg)
			d += deg
		elif ch == "[":
			pushT(turtle, d, stack)
		elif ch == "]":
			d = stack[-1][2]
			popT(turtle, d, stack)
		elif ch == "f":
			turtle.forward(f)


def draw_circe_part(turtle, part: int):
	for circle_part in range(360//part):
		turtle.forward(0.5)
		turtle.right(1)
