import logging
import os
import math
import itertools
import numpy as np
import glob
import json
import csv


def causalvar():
	filename_dir = "../scripts/datasets/thor_data_all/thor_data_raw/csv_separated_agent/2.5_hz/Exp_3_run_4/"
	curr_dir = os.getcwd()
	csv_dir=  curr_dir + "/" + filename_dir 
	peds_dic = {}
	causal_vars = {}
	for filename in os.listdir(csv_dir):
		file = os.path.join(csv_dir, filename)
	    # checking if it is a file
		if os.path.isfile(file):
			with open(file) as f:
				labels = [line.strip() for line in f.readlines()] # removes newline \n character at end of each effective line 

				agent_id = str(labels[0].split(",")[1]).rstrip('0').rstrip('.') 
				peds_dic[agent_id] = {"x":[], "y":[], "frame":[], "ID":[], "v":[] }

				for sample in labels:
				    peds_dic[agent_id]["x"].append(float(sample.split(",")[2])) 
				    peds_dic[agent_id]["y"].append(float(sample.split(",")[3])) 
				    peds_dic[agent_id]["frame"].append(float(sample.split(",")[0]))
				    peds_dic[agent_id]["ID"].append(float(sample.split(",")[1]))

		#print("peds_dic size=", len(peds_dic))
		#print("peds_dic = ", peds_dic)


	total_causal_closest_neighs = {}
	total_peds_dic = {}

	for ped_longest_ts in (peds_dic.keys()):
		print(len(peds_dic))
		longest_ts = peds_dic[ped_longest_ts]
		#print("longest_ts = ", longest_ts)
		peds_dic_neigh = peds_dic.copy()
		peds_dic_neigh.pop(ped_longest_ts)
		#del peds_dic_neigh[ped_longest_ts]

		# 1st causal variable to extract from the longest time series: absolute pose
		#causal_d_longest_ts = [np.sqrt((longest_ts['x'][i])**2 + (longest_ts['y'][i])**2) for i in range(len(longest_ts['x']))]

		# 2nd and 3rd causal variables to extract from the longest time series: closest neighbor rel_d and dtheta
		causal_closest_neighs = {"ID":[], "rel_d":[], "frame":[], "x":[], "y":[], "v":[], "dtheta":[]}

		#delt = longest_ts["frame"][1] - longest_ts["frame"][0]
		delt = 0.4

        
		for f in longest_ts['frame']:
			t = int(longest_ts['frame'].index(f))
			d_neighs_t = []
			neighs_id_t = []
			for neigh in peds_dic_neigh:
				neib = peds_dic_neigh[neigh]
				#if f in neib['frame']:
				#f_neigh_ind = int(neib["frame"].index(f))
				f_neigh_ind = t
				if (math.isnan(longest_ts['x'][t]) or math.isnan(neib['x'][f_neigh_ind])):
					d_neighs_t.append(1000000)
					neighs_id_t.append(neigh)
				else:
					d_neighs_t.append(np.sqrt((neib['x'][f_neigh_ind]-longest_ts['x'][t])**2 + (neib['y'][f_neigh_ind]-longest_ts['y'][t])**2))
					neighs_id_t.append(neigh)

			print("d_neighs_t ==============", d_neighs_t)

			if (len(d_neighs_t) !=0 and any(item !=1000000 for item in d_neighs_t) ):
				min_dist = min(d_neighs_t)
				min_dist_ind = d_neighs_t.index(min_dist)
				min_dist_id = neighs_id_t[min_dist_ind]
				causal_closest_neighs["rel_d"].append(min_dist)
				causal_closest_neighs["frame"].append(f)
				causal_closest_neighs["ID"].append(min_dist_id)
				causal_closest_neighs["x"].append(peds_dic_neigh[min_dist_id]["x"][f_neigh_ind])
				causal_closest_neighs["y"].append(peds_dic_neigh[min_dist_id]["y"][f_neigh_ind])
				if (t < (len(longest_ts['frame'])-1)):
					v_closest_neigh = np.array([(peds_dic_neigh[min_dist_id]["x"][t+1]-peds_dic_neigh[min_dist_id]["x"][t])/delt , (peds_dic_neigh[min_dist_id]["y"][t+1]-peds_dic_neigh[min_dist_id]["y"][t])/delt]) 
					causal_closest_neighs["v"].append(v_closest_neigh) 
			else:
				causal_closest_neighs["rel_d"].append(float("NaN"))
				causal_closest_neighs["frame"].append(f)
				causal_closest_neighs["ID"].append(float("NaN"))
				causal_closest_neighs["x"].append(float("NaN"))
				causal_closest_neighs["y"].append(float("NaN"))
				if (t < (len(longest_ts['frame'])-1)):
					causal_closest_neighs["v"].append(np.array([float("NaN"), float("NaN")]))



		# 4th causal variable to extract from longest time series: absolute velocity 
		for tm1 in range(len(longest_ts["frame"])-1):
			if (math.isnan(longest_ts['x'][tm1]) or math.isnan(longest_ts['x'][tm1+1])):
				longest_ts["v"].append(np.array([float("NaN"), float("NaN")]))
				causal_closest_neighs["dtheta"].append(float("NaN")) 
			else:
				longest_ts["v"].append(np.array([(longest_ts["x"][tm1+1]-longest_ts["x"][tm1])/delt, (longest_ts["y"][tm1+1]-longest_ts["y"][tm1])/delt]).tolist())
				deltheta = np.arccos(np.dot(causal_closest_neighs["v"][tm1], longest_ts["v"][tm1])/(np.linalg.norm(causal_closest_neighs["v"][tm1])* np.linalg.norm(longest_ts["v"][tm1])))
				causal_closest_neighs["dtheta"].append(deltheta) 
		
		longest_ts["v"].append(np.array([float("NaN"), float("NaN")]))
		causal_closest_neighs["dtheta"].append(float("NaN")) 

		total_causal_closest_neighs[ped_longest_ts] = causal_closest_neighs
		total_peds_dic[ped_longest_ts] = longest_ts

	# Serializing json
	causal_dic = {"cvar2":causal_closest_neighs["rel_d"], "cvar3":causal_closest_neighs["dtheta"], "cvar4":longest_ts["v"]}
	#causal_dic = {"cvar1": causal_d_longest_ts, "cvar2":causal_closest_neighs["rel_d"], "cvar3":causal_closest_neighs["dtheta"], "cvar4":longest_ts["v"]}



	for ped in total_peds_dic.keys():
		data_tg = total_peds_dic[ped]
		data_n = total_causal_closest_neighs[ped]
		#os.chdir('../scripts/datasets/thor_data_all/thor_data/csv_separated_agent/2.5_hz/Exp_1_run_3_causal/')
		with open("%s_causal.csv" % str(ped), "w") as f:
			writer = csv.writer(f)
			for t in range(len(data_tg["frame"])):
				ts = [data_tg["frame"][t], data_tg["ID"][t], data_tg["x"][t], data_tg["y"][t], data_tg["v"][t][0], data_tg["v"][t][1], data_n["rel_d"][t], data_n["dtheta"][t] ]
				writer.writerow(ts)
				#writer.writerow("\t")

			f.close()



if __name__ == "__main__":
    causalvar()


