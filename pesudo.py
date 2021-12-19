import math
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import sympy
from scipy.interpolate import interp1d
from sobol import *
import random
import statistics
import scipy.integrate as it
from random import randrange
import sobol
import matplotlib.cm as cm
import sobol_seq
from scipy.optimize import curve_fit
r = 4     
var_list = []
var_list_r = []
abso = []

low_b = 1
up_b = 2000
step = 1

abso_r = []
N = 200
for k in range(low_b, up_b, step):
	sample_times = k
	list_p = []
	len_list = []
	count = 0
	var = 0
	sobol_se = sobol_seq.i4_sobol_generate(r, sample_times)

	for i in range(sample_times):
		if sobol_se[i][0] > sobol_se[i][1] > sobol_se[i][2]   :
			count += 1
			list_p = np.append(list_p, sobol_se[i][0])
			len_list = np.append(len_list, 1)
			# print("this is len_list", len_list)
			#calculating <x>
		else:
			len_list = np.append(len_list, 0)

		var = np.log(i) * np.sqrt((np.sum(len_list[i] - np.sum(len_list) / i) ** 2) / i) / (i)
		absoerror = (np.sum(np.absolute(len_list[i] - 1/6)))/i
		# print("this is variance", var)

	# print(sobol_se[1][0])
	var_list = np.append(var_list, var)
	abso = np.append(abso, absoerror)

	# print("expectation is", np.sum(len_list) / sample_times, 
	# 	"with variance", var,"N =",N, "variance ratio = last var / first var = 1/",
	# 	 var_list[0]/var_list[-1], "absolute error ratio 1/",  abso[0]/abso[-1])


for k in range(low_b, up_b, step):
	sample_times_r = k
	list_p_r = []
	len_list_r = []
	count_r = 0
	var_r = 0
	N_r = 3
	rand_sq = np.random.random((sample_times,r))

	for q in range(sample_times_r):
		if rand_sq[q][0] > rand_sq[q][1] > rand_sq[q][2]:
			count_r += 1
			list_p_r = np.append(list_p_r, rand_sq[q][0])
			len_list_r = np.append(len_list_r, 1)
			# print("this is len_list", len_list)
			#calculating <x>
		else:
			len_list_r = np.append(len_list_r, 0)

		# print("this is len_list_r",len_list_r)

		var_r = np.sqrt((np.sum(len_list_r[q] - np.sum(len_list_r) / q) ** 2) / q) / np.sqrt(q)
		absoerror_r = (np.sum(np.absolute(len_list_r[q] - 1/6)))/q
		# print("this is variance", var)

	# print(sobol_se[1][0])
	var_list_r = np.append(var_list_r, var_r)
	abso_r = np.append(abso_r, absoerror_r)

def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')

# def func(a, b):
#     return (a / 8000) **(-b)

# xdata = np.linspace(0, 30, 500)
# y = func(xdata, 0.5)


# rng = np.random.default_rng()
# y_noise = 0.2 * rng.normal(size=xdata.size)
# ydata = y + y_noise
# # plt.plot(xdata, ydata, 'b-', label='data')
# popt, pcov = curve_fit(func, xdata, ydata)
x = np.linspace(0, 1, up_b - 1,endpoint=True)
# xnew = np.linspace(low_b, up_b, num=401, endpoint=True)
f_s = movingaverage(abso, 30)
f_r = movingaverage(abso_r, 30)
f_k = movingaverage(var_list, 30)
f_j = movingaverage(var_list_r, 30)
# pfit = np.polyfit(x, abso, 1)
# trend_line_model = np.poly1d(pfit)
xnew = range(0, (up_b-1), 1)

# plt.plot(x, trend_line_model(x), "m--") 

plt.plot(x, f_s, 'b')
plt.plot(x, f_r, 'r')
plt.plot(x, f_k, 'y')
plt.plot(x, f_j, 'g')
# plt.plot(x, abso, 'y')
# plt.plot(x, abso_r, 'g')
plt.title("sample times =" + str(up_b) + ",x1 > x2 > x_3")
plt.tight_layout()
plt.xlim([0, 1])
plt.legend(["moving_average_sobol", "moving_average_random", "sobol_var", "random_var"], loc ="lower right")
plt.show()