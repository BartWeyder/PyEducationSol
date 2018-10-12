import consolemenu as cs
import AdamsMethod as ad

#globals
a = None
b = None
y0 = None
solution = None
def func(x, y):
	return (0.3 * x) + (y ** 2)

def input_boundaries():
	global a, b
	print("Type 'cancel' to exit input.")
	while 1:
		a = input("Enter left boundary: ")
		if a == 'cancel': 
			a = None
			break
		try: 
			a = float(a)
		except:
			print("Must be numeric value! Try again or type 'cancel' to exit.")
			continue
		break

	while 1:
		b = input("Enter right boundary that > than left (%f): " % a)
		if b == 'cancel': 
			a = None
			b = None
			break
		try: 
			b = float(b)
		except:
			print("Must be numeric value! Try again or type 'cancel' to exit.")
			continue

		if b <= a:
			print("Must be bigger than left boundary (%f), try again or type 'cancel' to exit." % a)
		elif b - a > 500000: print("Too big range, try smaller.")
		else: break

	a = round(a, 3)
	b = round(b, 3)

def input_y0():
	global a, b, y0
	if a == None:
		print("Enter boundaries first!")
		return
	print("Type 'cancel' to exit input.")
	while 1:
		y0 = input("y(%f): " % a)
		if y0 == 'cancel': 
			y0 = None
			break
		try: 
			y0 = float(y0)
		except:
			print("Must be numeric value! Try again or type 'cancel' to exit.")
			continue
		break

def get_by_x():
	global a, b, y0, solution
	if a != None and b != None and y0 != None:
		if solution == None:
			solution = ad.AdamsMethod(a, b, y0, 0.001, func)

		x = ''
		while 1:
			x = input("x=")
			if x == 'cancel': 
				break
			try: 
				x = float(x)
			except:
				print("Must be numeric value! Try again or type 'cancel' to exit.")
			if x < a or x > b: print("Value shoud be between %f and %f" % (a, b))
			else: break
		sol_res = solution.get_value(round(x, 3))
		print(sol_res)
		if sol_res == float("inf"): 
			print("Warning! Method catched extremum on x = %.3f" % solution.values[0][len(solution.values[0]) - 1])
			print("Try to use other boundaries and y0.")
		input("Press ENTER to continue...")
		return
	print("To get value enter boundaries and y0 first!")
	input("Press ENTER to continue...")

menu = cs.ConsoleMenu("Numerical solution of ordinary differential equations")
bound_input_item = cs.items.FunctionItem("Input Boundaries", input_boundaries)
y_input = cs.items.FunctionItem("Input y0", input_y0)
calculate = cs.items.FunctionItem("Enter x and calculate value", get_by_x)


menu.append_item(bound_input_item)
menu.append_item(y_input)
menu.append_item(calculate)
menu.show()