import sobol_seq
import numpy as np
r = 3     
var_list = []
abso = []
N = 50
for k in range(100, 1000, 1):
	sample_times = k
	list_p = []
	len_list = []
	count = 0
	var = 0
	sobol_se = sobol_seq.i4_sobol_generate(r, sample_times)

	for i in range(sample_times):
		if sobol_se[i][0] > sobol_se[i][1] > sobol_se[i][2]:
			count += 1
			list_p = np.append(list_p, sobol_se[i][0])
			len_list = np.append(len_list, 1)
			# print("this is len_list", len_list)
			#calculating <x>
		else:
			len_list = np.append(len_list, 0)

		var = (np.sum(len_list[i] - np.sum(len_list) / i) ** 2) / i
		absoerror = (np.sum(np.absolute(len_list[i] - 1/6)))/i
	# print(sobol_se[1][0])
	var_list = np.append(var_list, var)
	abso = np.append(abso, absoerror)
	print("this is abso", abso)


	print("expectation is", np.sum(len_list) / sample_times, 
		"with variance", var,"N =",N, "variance ratio = last var / first var = 1/",
		 var_list[0]/var_list[-1], "absolute error ratio 1/",  abso[0]/abso[-1])
