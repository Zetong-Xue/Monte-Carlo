import math
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import sympy
from sobol import *
import random
import statistics
import scipy.integrate as it
from random import randrange
import sobol

PI = 3.1415926
e = 2.71828


seed = 12345 # is is basically index in the sobol sequence
ndim = 1 # dimension of the problem

def sobol_ran(col, row):
	list = sobol.sample(dimension=1, n_points=row)
	return(list)

#generate random number for MC
def get_rand_number(min_value, max_value):
    range = max_value - min_value
    choice = random.uniform(0,1)
    return min_value + range*choice


products = []
cost_list = []
cost_list_for_var = []
var_loop = []
var_list = []


def QMC_fail_rate(n, a_s, num_samples, r):
	tot_p = 0
	tot_1 = 0
	tot_2 = 0
	tot_p_list = []
	var_loop = []
	for t in range(num_samples):
		a = a_s
		s = np.random.weibull(a, 1000)
		# print("s",s)
		ftimes = r

		vec = []
		#generate random vector in [0,1]^n 
		for h in range(ftimes):
			vec = np.append(vec, sobol_ran(num_samples, ftimes))
			# print("this is vec", vec)

		vec_loop = np.append([0], vec)
		vec_loop.sort()

		# print("this is vec_loop", vec_loop)	



		x = np.arange(1,101.)/50.
		def weib(x,n,a):
		    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)

		wei_l = weib(x, n, a_s)

		#normalize Weibull distribution
		inte = scipy.integrate.simps(wei_l)
		wei_nor =  weib(x, n, a_s) / inte
		# print("this is len(wei_nor)", len(wei_nor))

		# plt.plot(x, wei_nor)
		# plt.show()

		# print("inte is ", inte)

		#design n distribution for possible n failures
		def gen_tot_pro(ftimes):
			one_list = [1] * len(wei_nor)
			for i in range(ftimes):
				# print("this is i", i)
				new_wei = wei_nor[:int((1- vec_loop[i])*100)] 
				# new_wei = wei_nor[:int(len(wei_nor)*randrange(1000)/1000)] 
				dif_len = len(wei_nor) - len(new_wei)
				lst = [0] * dif_len
				#creating shifted Weibull distributions
				new_wei_f = [*lst, *new_wei]
				one_list = [a * b for a, b in zip(one_list , new_wei_f)]
				products = one_list
				# print("this is new_wei", products)

			return(products)
		# lb = 0
		# ub = len(gen_tot_pro(ftimes))

		# sos = 0

		prob = gen_tot_pro(ftimes)[int(vec_loop[ftimes] * 100)]


		# print("this is the len of prob", len(gen_tot_pro(ftimes)))

		#vector probability density function at vec_loop

		# print("this is the prob at vec_loop",prob)
		# plt.plot(x, gen_tot_pro(ftimes))
		# plt.show()

		tot_p += prob / num_samples
		# print("this is total prob", tot_p)
		# cost_list_for_var = np.append(cost_list_for_var, values)

		
		tot_p_list = np.append(tot_p_list, tot_p * 100000 * r)
	print("this is total p list", tot_p_list)
	var_each_r = np.var(tot_p_list) / num_samples
	var_loop = np.append(var_loop, var_each_r)

	print("this is variance", var_loop)


		# for l in range(num_samples):
		# 	x = get_rand_number(lb,ub)
		# 	# print("this is x",x)
		# 	sos += (gen_tot_pro(ftimes)[int(x)])
		# 	psos = sos /l
		# 	print("this is sos", psos)
	return(tot_p,var_each_r)
f_max = list(range(1,3+1))
for r in f_max:
	print("this is loop r = ********************************", r)
	cost_ind = QMC_fail_rate(1, 5, 400, r)[0]
	variance = QMC_fail_rate(1, 5, 400, r)[1]
	print("this is cost_ind",cost_ind)
	cost_list = np.append(cost_list, cost_ind * 100000 * r)
	print("this is cost_list",cost_list)
	var_list = np.append(var_list, variance)
	print("this is cost_list", cost_list, "and here is the total cost for 1 year", sum(cost_list), "with variance", sum(var_list))