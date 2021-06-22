from dearpygui import core, simple
from helper import Helper

core.set_main_window_title("Numerical Analysis - Ceyhun B.")
core.set_theme("Light")
helper = Helper()


input_labels = ["x_0", "x_1", "x_2", "x_3", "x_4", "x_5", "x_6", "x_7"]
input2_labels = ["y_0", "y_1", "y_2", "y_3", "y_4", "y_5", "y_6", "y_7"]

# (35/1152)*x^9 - (5/112)*x^7 + (3/40)*x^5 - (1/6)*x^3 + x
# α = 13/84 

def magic(data, sender):
	print("Magic")
	print(core.get_value("From - To"))
	try:
		tolerance = float(core.get_value("Tolerance"))
	except ValueError:
		print("Enter correct type of input for tolerance")
		tolerance = 0.0

	print(tolerance)

	helper.set_parameters(core.get_value("Function"), core.get_value("FunctionG"), core.get_value("From - To"), \
		tolerance, core.get_value("P_0 - A for Extraction of Cubic Roots"),\
		core.get_value("P_0 - Fixed/Newton"), core.get_value("Alpha for Horner"), core.get_value("FPA"))
	
	try:
		helper.draw_horner()
	except Exception as e:
		print("Horner error: ", e)
	try:
		helper.draw_bisection()
	except Exception as e:
		print("Bisection error: ", e)
	try:
		helper.draw_cubic()
	except Exception as e:
		print("Cubic error: ", e)
	try:
		helper.draw_fixed_point()
	except Exception as e:
		print("Fixed error: ", e)
	# ///// NEWTON Zaten bir fixed point iteration methodu. When g(x) = x - f(x)/f'(x)
	#try:
	#	helper.draw_newton()
	#except Exception as e:
	#	print(e)
	try:
		p_0 ,p_1 = core.get_value("P_0 - P_1 Secant")
		helper.draw_secant(round(p_0, 5) , round(p_1, 5))
	except Exception as e:
		print("Secant error: ", e)
	try:
		helper.draw_regula_falsi()
	except Exception as e:
		print("Regula Falsi error: ", e)

	try:
		x_list = list()
		y_list = list()

		for label1, label2 in zip(input_labels, input2_labels):
			try:
				a = float(core.get_value(label1))
				b = float(core.get_value(label2))
			except ValueError:
				break
			x_list.append(a)
			y_list.append(b)

		target_x = float(core.get_value("Target X"))
		expected_y = float(core.get_value("F(Target X)"))
		print(x_list)
		print(y_list)
		print(target_x, expected_y)
		helper.draw_lagrange(target_x, expected_y, x_list, y_list)
	except Exception as e:
		print("Lagrange error: ", e)

	try:
		try:
			arg = round(float(core.get_value("Compozite Trap Expected Value (Wolfram)")), 13)
		except ValueError as e:
			arg = 1
		helper.draw_comp_trap(core.get_value("Compozite Trap N"),  arg)
	except Exception as e:
		print("Comp Trap error: ", e)
	try:
		try:
			arg = round(float(core.get_value("Compozite Simp Expected Value (Wolfram)")), 13)
		except ValueError as e:
			arg = 1
		helper.draw_comp_simp(core.get_value("Compozite Simp N"), arg)
	except Exception as e:
		print("Comp Simp error: ", e)

	try:
		h = round(float(core.get_value("h:Differentiation")), 13)
		x_0 = round(float(core.get_value("x_0:Differentiation")), 13)
		helper.draw_num_differentiation(h, x_0)
	except Exception as e:
		print("Num Differentiation error: ", e)

# question 1 F(x) : ( ( (x - sin(x)) / (1 - cos(x)) ) - 0.7 )
# question 3 F(x) : x - sin(3.56*x + 3.016) + 3.56

with simple.window("Primary Window"):
	core.add_input_text("Function", label="F(x)", default_value="atan( 1 + (atan( 1 + (atan(x)^6) )^3) )^4")
	core.add_input_float2("From - To", default_value=[1, 2])
	core.add_input_text("Tolerance", default_value="0.00001")
	core.add_input_int("FPA", default_value=9)
	core.add_button("Magic", callback=magic)
	
	with simple.tab_bar("Tabs"):
		
		with simple.tab("Horner's Method"):
			core.add_input_float("Alpha for Horner", default_value=1.150)
			pass
		
		with simple.tab("Bisection Method"):
			pass
		
		with simple.tab("Cubic Roots Extraction"):
			core.add_input_float2("P_0 - A for Extraction of Cubic Roots", default_value=[18.87, 18.87])
			pass
		
		with simple.tab("Fixed Point Iteration"):
			core.add_input_text("FunctionG", label="G(x)", default_value="x - ((x^1 + e^(6*x)) / (6*e^(6*x) + 1))")
			core.add_input_float("P_0 - Fixed/Newton", label="P_0", default_value=-1.0)
			pass
		
		with simple.tab("Secant Method"):
			core.add_input_float2("P_0 - P_1 Secant", default_value=[2.6, 2.8])
			pass
		
		with simple.tab("Regula Falsi Method"):
			pass
		
		with simple.tab("Lagrange Method"):
			for index, label in enumerate(input_labels):
				core.add_input_text(label, width=80)
				if index != len(input_labels)-1: core.add_same_line();
			for index, label in enumerate(input2_labels):
				core.add_input_text(label, width=80)
				if index != len(input2_labels)-1: core.add_same_line();
			core.add_input_text("Target X", width=80)
			core.add_same_line();
			core.add_input_text("F(Target X)", width=150)
		
		with simple.tab("Compozite Trap Method"):
			core.add_input_int("Compozite Trap N", width=80, default_value=10)
			core.add_same_line();
			core.add_input_text("Compozite Trap Expected Value (Wolfram)", width=150)
			core.add_same_line();
			core.add_input_text("Compozite Trap I*",label="I* (This is output.)", width=150)
			core.add_same_line();
			core.add_input_text("Compozite Trap Relative Error",label="RE (This is output.)", width=150)
			pass
		
		with simple.tab("Compozite Simp Method"):
			core.add_input_int("Compozite Simp N", width=80, default_value=10)
			core.add_same_line();
			core.add_input_text("Compozite Simp Expected Value (Wolfram)", width=150)
			core.add_same_line();
			core.add_input_text("Compozite Simp I*",label="I* (This is output.)", width=150)
			core.add_same_line();
			core.add_input_text("Compozite Simp Relative Error",label="RE (This is output.)", width=150)
			pass
		
		with simple.tab("Numerical Differentiation"):
			core.add_input_text("h:Differentiation", label="h", width=120, default_value="0.00001")
			core.add_same_line();
			core.add_input_text("x_0:Differentiation", label="x_0", width=120, default_value="1.0471975511963")
			core.add_same_line();
			core.add_input_text("f'(x_0):Differentiation",label="f'(x_0) (This is output.)", width=150)
			core.add_same_line();
			core.add_input_text("f''(x_0):Differentiation",label="f''(x_0) (This is output.)", width=150)
			pass
					

					
core.set_primary_window("Primary Window", True)
core.start_dearpygui()



