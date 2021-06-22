from dearpygui import core, simple
import parser
from math import *
from sympy import *
import time
from decimal import Decimal

e  = 2.718281828459
pi = 3.141592653589

class Helper:

	def __init__(self):
		self.separator_1 = "Bisection Separator"
		self.cubic = "Cubic"
		self.fixed = "Fixed"
		self.newton = "Newton"
		self.tab_dict = {
			0 : "Horner's Method",
			1 : "Bisection Method",
			2 : "Cubic Roots Extraction",
			3 : "Fixed Point Iteration",
			4 : "Newton Method",
			5 : "Secant Method",
			6 : "Regula Falsi Method",
			7 : "Lagrange Method",
			8 : "Compozite Trap Method",
			9 : "Compozite Simp Method",
			10 : "Numerical Differentiation"
		}

	def set_parameters(self, function, functionG, _range, tolerance, cubic_vals, p_0 , alpha ,digits):
		self.terminate_loop = 5 # in seconds
		self.digits = digits
		self.range = [round(_range[0], 5),  round(_range[1], 5)]
		self.tolerance = tolerance
		self.cubic_vals	= cubic_vals
		self.alpha = alpha
		self.p_0 =  p_0
		try:
			self.raw = function.replace("^", "**")
			self.rawG = functionG.replace("^", "**")
		except ValueError:
			self.raw = function
			self.rawG = functionG
		self.function_code = parser.expr(self.raw.replace(" ", "")).compile() if self.raw.count(" ") > 0 else parser.expr(self.raw).compile()
		self.functionG_code = parser.expr(self.rawG.replace(" ", "")).compile() if self.rawG.count(" ") > 0 else parser.expr(self.rawG).compile()

	def fpa(self, number):
		if float(number) == 0.0: return 0;
		return round(number, self.digits - int(floor(log10(abs(number)))) - 1)

	def draw_horner(self):
		core.delete_item(self.tab_dict[0] + "_table_main")
		# Dimension of the function. Helps us determine the iteration count.
		dimension=int(self.raw[self.raw.index('**')+2:self.raw.index(' ')])	# Problem
		# Getting coefficients of each power.
		x = symbols('x')
		coefficient_list = Poly(self.raw.replace(" ", ""), x).all_coeffs()
		print(dimension)
		print(coefficient_list)
		# Initilizing b_n to a_n 
		bottom_row = [coefficient_list[0]]
		middle_row = []
		## Mathematical calculations and assignments of the values.
		for i in range(dimension):
			print("alpha, bottom row[-1], res: ", self.alpha, bottom_row[-1], self.fpa(self.alpha*bottom_row[-1]))
			middle_row.append(self.fpa(self.alpha*bottom_row[-1]))
			bottom_row.append(self.fpa(coefficient_list[i+1] + middle_row[-1]))
		## Formatting the values so that I can use them on the Table.
		columns = [str(x) for x in range(dimension+2)]	# <- Content does not matter but length does. NoOfColumns
		coefficient_list = [str(x) for x in coefficient_list]
		middle_row = [str(x) for x in middle_row]
		bottom_row = [str(x) for x in bottom_row]
		## Creating the table and placing the rows.
		core.add_table(self.tab_dict[0] + "_table_main", columns, hide_headers=True, parent=self.tab_dict[0]) 
		core.add_row(self.tab_dict[0] + "_table_main", ["a_k"] + coefficient_list)
		core.add_row(self.tab_dict[0] + "_table_main", ["", ""] + middle_row)
		core.add_row(self.tab_dict[0] + "_table_main", ["b_k"] + bottom_row)


	def draw_bisection(self):
		core.delete_item(self.tab_dict[1] + "_table_rootswitch")
		core.delete_item(self.separator_1)
		core.delete_item(self.tab_dict[1] + "_table_main")
		### Root Switch Showcase
		_range = [int(x) for x in self.range]
		results = list()
		for x in range(_range[0], _range[1] + 1):
			fx = self.fpa(eval(self.function_code))
			results.append(str(fx))	# Format it to string and append to results row for our table.
		core.add_table(self.tab_dict[1] + "_table_rootswitch", ["" for _ in range(len(results) + 1)],height=200 ,hide_headers=True, parent=self.tab_dict[1])# Create Table - Define amount of Columns
		core.add_row(self.tab_dict[1] + "_table_rootswitch", ["x"] + [str(x) for x in range(_range[0], _range[1] + 1)])	# First row is our x values.
		core.add_row(self.tab_dict[1] + "_table_rootswitch", ["f(x)"] + results)	 # Second row for the corresponding values inside the function. F(x)
		core.add_separator(name=self.separator_1, parent=self.tab_dict[1])
		### Bisection Method
		first_run = True
		header = ["n", "a_n", "b_n", "p_n", "f(a_n)", "f(p_n)", "RE(p_n = p_n-1)"]
		rows = list() # we need this to make a table.
		# Create variables and initilize if needed.
		prev_p = 0
		p = 0
		n = 1
		a, b = self.range
		relative_error = "" # Initilized to empty string for the first iteration of the calculation.
		b_flag = False
		start_time = time.time()
		while True:
			p = self.fpa((a + b)/2)
			x = self.fpa(a)
			fa = self.fpa(eval(self.function_code))
			x = p
			fp = self.fpa(eval(self.function_code))
			# If it's the first run skip this section. 
			if not first_run:
				relative_error = self.fpa(abs(p - prev_p)/abs(p))
				if relative_error < self.tolerance or time.time() - start_time > self.terminate_loop:
					b_flag = True
			# Append as a list of string elements of each variable
			rows.append([str(n), str(self.fpa(a)), str(self.fpa(b)), str(p), str(fa), str(fp), str(relative_error)])
			# Hot and Cold assignments
			if fa * fp < 0: b = p; 
			else: a = p;
			prev_p = p
			n += 1
			first_run = False
			if b_flag: break;
		# Create Table and Set Table Data.
		core.add_table(self.tab_dict[1]+"_table_main", header, parent=self.tab_dict[1], height=600)
		core.set_table_data(self.tab_dict[1]+"_table_main", rows)


	def draw_cubic(self):
		core.delete_item(self.cubic)
		header = ["n", "p_n-1", "p_n", "RE(p_n = p_n-1)"]
		rows = list()
		n = 1
		b_flag = False
		p = self.fpa(self.cubic_vals[0])
		a = self.fpa(self.cubic_vals[1])
		start_time = time.time()
		while True:
			prev_p = p
			#calculation
			p = self.fpa(1/3*(2*prev_p + a/pow(prev_p,2)))
			relative_error = self.fpa(abs(p - prev_p)/abs(p))
			rows.append([str(n), str(prev_p), str(p), str(relative_error)])
			n += 1
			if relative_error < self.tolerance or time.time() - start_time > self.terminate_loop: break;
		core.add_table(self.cubic, header, parent=self.tab_dict[2])
		core.set_table_data(self.cubic, rows)


	def draw_fixed_point(self):
		core.delete_item(self.fixed)
		header = ["n", "p_n-1", "p_n", "RE(p_n = p_n-1)", "f(p_n)"]
		rows = list()
		p = self.p_0 
		n = 1
		b_flag = False
		start_time = time.time()
		relative_error = ""
		prev_p = ""
		while True:
			prev_p = p
			x = p 
			p = self.fpa(eval(self.functionG_code))
			f_pn = self.fpa(eval(self.function_code))
			#calculation
			relative_error = self.fpa(abs(p - prev_p)/abs(p))
			rows.append([str(n), str(prev_p), str(p), str(relative_error), str(f_pn)])
			if  n != 1 and (relative_error < self.tolerance or time.time() - start_time > self.terminate_loop): break;
			n += 1
		core.add_table(self.fixed, header, height=600, parent=self.tab_dict[3])
		core.set_table_data(self.fixed, rows)

	# no need tbh
	def draw_newton(self):
		core.delete_item(self.newton)
		header = ["n", "p_n-1", "p_n", "RE(p_n = p_n-1)", "f(p_n)"]
		rows = list()
		p = self.p_0 # to be changed
		n = 1
		b_flag = False
		start_time = time.time()
		relative_error = ""
		prev_p = ""
		while True:
			prev_p = p
			x = p 
			p = self.fpa(eval(self.functionG_code))
			f_pn = self.fpa(eval(self.function_code))
			#calculation
			relative_error = self.fpa(abs(p - prev_p)/abs(p))
			rows.append([str(n), str(prev_p), str(p), str(relative_error), str(f_pn)])
			if  n != 1 and (relative_error < self.tolerance or time.time() - start_time > self.terminate_loop): break;
			n += 1
		core.add_table(self.newton, header, height=600, parent=self.tab_dict[4])
		core.set_table_data(self.newton, rows)


	def draw_secant(self, p_0, p_1):			
		def next_p(pb_2, pb_1, f_pb_1, f_pb_2):
			return self.fpa(pb_1 - f_pb_1 * ((pb_1 - pb_2)/(f_pb_1 - f_pb_2)))

		core.delete_item(self.tab_dict[5] + "_table_main")
		header = ["n", "p_n-2", "p_n-1", "p_n", "RE(p_n = p_n-1)", "f(p_n)"]
		rows = list()
		n = 2
		pb_2 = p_0
		pb_1 = p_1
		start_time = time.time()
		while True:
			x = pb_1 
			f_pb_1 = self.fpa(eval(self.function_code))
			x = pb_2 
			f_pb_2 = self.fpa(eval(self.function_code))
			pn = next_p(pb_2, pb_1, f_pb_1, f_pb_2)
			x = pn
			f_pn = self.fpa(eval(self.function_code))
			relative_error = self.fpa(abs(pn - pb_1)/abs(pn))
			rows.append([str(n) , str(pb_2) , str(pb_1), str(pn), str(relative_error), str(f_pn)])
			pb_2 = pb_1
			pb_1 = pn
			if  n != 1 and (relative_error < self.tolerance or time.time() - start_time > self.terminate_loop): break;
			n += 1
		core.add_table(self.tab_dict[5] + "_table_main", header, height=600, parent=self.tab_dict[5])
		core.set_table_data(self.tab_dict[5] + "_table_main", rows)


	def draw_regula_falsi(self):	
		core.delete_item(self.tab_dict[6] + "_table_main")

		header = ["n", "a_n", "b_n", "p_n", "f(a_n)", "f(p_n)"]
		rows = list()
		n = 1
		a, b = self.range
		start_time = time.time()

		while True:
			x = a; f_a = self.fpa(eval(self.function_code));
			x = b; f_b = self.fpa(eval(self.function_code));
			p = self.fpa( (a*f_b-b*f_a)/(f_b - f_a) )
			x = p; f_p = self.fpa(eval(self.function_code));
			rows.append([str(n) , str(a) , str(b), str(p), str(f_a), str(f_p)])
			if  n != 1 and ( abs(f_p) < self.tolerance or time.time() - start_time > self.terminate_loop): break;
			if (f_a * f_p > 0):
				a = p
			else:
				b = p
			n += 1

		core.add_table(self.tab_dict[6] + "_table_main", header, height=600, parent=self.tab_dict[6])
		core.set_table_data(self.tab_dict[6] + "_table_main", rows)


	def draw_lagrange(self, target_x, expected_y, x_list, y_list):	
		core.delete_item(self.tab_dict[7] + "_table_main")
		core.delete_item(self.tab_dict[7] + "_table_main_2")
		core.delete_item(self.tab_dict[7] + "_separator")
		core.delete_item(self.tab_dict[7] + "_result")
		core.delete_item(self.tab_dict[7] + "_separator_2")
		core.delete_item(self.tab_dict[7] + "_relative_error")

		header = ["x_k", str(target_x)+" - x_k"] + [str(x)+" - x_k" for x in x_list]
		rows = list()

		lagrange_dict = dict() 
		for x in x_list:
			lagrange_dict[x] = dict()
			lagrange_dict[x]["Top"] = 1
			lagrange_dict[x]["Bottom"] = 1

		for index, x_k in enumerate(x_list):
			t_x_value = target_x-x_k
			row = [str(x_k), str(t_x_value)]
			for _x in x_list:
				if _x != x_k:
					value = _x - x_k
					row += [str(value)]
					lagrange_dict[_x]["Top"] *= t_x_value
					lagrange_dict[_x]["Bottom"] *= value
				else:
					row += ["||||||"]
			rows.append(row)
		lagrange_vals = [self.fpa(lagrange_dict[x]["Top"]/lagrange_dict[x]["Bottom"]) for x in lagrange_dict]
		rows.append(["L_k(x)", ""] + [str(val) for val in lagrange_vals])
		core.add_table(self.tab_dict[7] + "_table_main", header, height=200, parent=self.tab_dict[7])
		core.set_table_data(self.tab_dict[7] + "_table_main", rows)

		header = [""] + ["" for _ in x_list]
		rows = list()
		rows.append(["x_k"] + [str(x) for x in x_list])
		rows.append(["y_k"] + [str(self.fpa(y)) for y in y_list])
		rows.append(["L_k(x)"] + [str(val) for val in lagrange_vals])
		results = [self.fpa( val * y) for val, y in zip(lagrange_vals, y_list)]
		rows.append(["y_k*L_k(x)"] + [str(res) for res in results])
		core.add_table(self.tab_dict[7] + "_table_main_2", header, hide_headers=True, height=200, parent=self.tab_dict[7])
		core.set_table_data(self.tab_dict[7] + "_table_main_2", rows)
		core.add_separator(name=self.tab_dict[7] + "_separator", parent=self.tab_dict[7])
		final_lag = self.fpa(sum(results))
		core.add_label_text(self.tab_dict[7] + "_result", label=f"L({str(target_x)}): " + str(final_lag), parent=self.tab_dict[7])
		core.add_separator(name=self.tab_dict[7] + "_separator_2", parent=self.tab_dict[7])
		core.add_label_text(self.tab_dict[7] + "_relative_error", label="Relative Error: " + str(self.fpa(abs(expected_y-final_lag)/expected_y)), parent=self.tab_dict[7])


	def draw_comp_trap(self, n, expected_out):
		core.delete_item(self.tab_dict[8] + "_table_main")

		header = ["k", "x_k", "( 1/2 | 1 ) * y_k"]
		rows = list()
		base, last = self.range
		step = self.fpa((last-base)/n)
		y_sum = 0
		for i in range(0, n+1):
			x = self.fpa(base + (i*step))
			if x > last:
				x = last
			y_k = self.fpa(eval(self.function_code))
			if i == 0 or i == n:
				y_k = self.fpa(y_k / 2)
			y_sum = self.fpa(y_sum + y_k)
			rows.append([str(i), str(x), str(y_k)])

		end_res = self.fpa(y_sum * step)
		relative_error = self.fpa(abs(expected_out - end_res)/expected_out)
		core.add_table(self.tab_dict[8] + "_table_main", header, height=300, parent=self.tab_dict[8])
		core.set_table_data(self.tab_dict[8] + "_table_main", rows)
		core.set_value(name="Compozite Trap I*", value=str(end_res))
		core.set_value(name="Compozite Trap Relative Error", value=str(relative_error))

	def draw_comp_simp(self, n, expected_out):
		core.delete_item(self.tab_dict[9] + "_table_main")

		header = ["k", "x_k", "( 1 | 2 | 4 ) * y_k"]
		rows = list()
		base, last = self.range
		step = self.fpa((last-base)/n)
		y_sum = 0
		for i in range(0, n+1):
			x = self.fpa(base + (i*step))
			if x > last:
				x = last
			y_k = self.fpa(eval(self.function_code))
			if x == base or x == last:
				pass
			elif i % 2 == 0:
				y_k = self.fpa( 2 * y_k )
			else:
				y_k = self.fpa( 4 * y_k )

			y_sum = self.fpa(y_sum + y_k)
			rows.append([str(i), str(x), str(y_k)])

		end_res = self.fpa((step/3)*y_sum)
		relative_error = self.fpa(abs(expected_out - end_res)/expected_out)
		core.add_table(self.tab_dict[9] + "_table_main", header, height=300, parent=self.tab_dict[9])
		core.set_table_data(self.tab_dict[9] + "_table_main", rows)
		core.set_value(name="Compozite Simp I*", value=str(end_res))
		core.set_value(name="Compozite Simp Relative Error", value=str(relative_error))

	def draw_num_differentiation(self, h , x_0):
		core.delete_item(self.tab_dict[10] + "_table_main")
		header = ["k", "x_k", "f_k"]
		print("PRINTING FOR NUM Differentiation")
		print("h: ", h)
		print("x_0: ", x_0)
		rows = list()
		x = x_0 + h; f_right = self.fpa(eval(self.function_code));
		x = x_0 - h; f_left = self.fpa(eval(self.function_code));
		x = x_0; f_center = self.fpa(eval(self.function_code));
		f_first_der = self.fpa( (f_right - f_left)/(2*h) )
		f_second_der = self.fpa( self.fpa(f_right - (2*f_center) + f_left) / self.fpa(h*h) )
		print("f_right, f_left, f_center * 2")
		print(f_right, f_left, 2*f_center)
		print("Top: ",self.fpa(f_right - (2*f_center) + f_left))
		for k, x in enumerate([self.fpa(x_0 - h), self.fpa(x_0), self.fpa(x_0 + h)], start=-1):
			f_x = self.fpa(eval(self.function_code))
			rows.append([str(k), str(x), str(f_x)])
		core.add_table(self.tab_dict[10] + "_table_main", header, height=300, parent=self.tab_dict[10])
		core.set_table_data(self.tab_dict[10] + "_table_main", rows)
		core.set_value(name="f'(x_0):Differentiation", value=str(f_first_der))
		core.set_value(name="f''(x_0):Differentiation", value=str(f_second_der))

 