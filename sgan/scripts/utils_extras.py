import logging
import os
import math
import itertools
import numpy as np
import glob
import csv


def timestamp_to_float():
	exp_dir = "test_ARENA"
	file_name = "2023-05-11-human-group-interaction_02"
	delim = '\t'
	filename_dir = "../scripts/datasets/thor_data_all/thor_data/"+exp_dir+"/"
	curr_dir = os.getcwd()
	csv_dir=  curr_dir + "/" + filename_dir 
	peds_dic = {}
	tsp_tm1 = 0
	row_tm1 = 0
	row_ind = 0
	with open(file_name+"_tsp_to_float.csv", 'a') as out:
		writer = csv.writer(out)
		for filename in os.listdir(csv_dir):
			file = os.path.join(csv_dir, filename)
			with open(file, 'r') as inp:
				for row in csv.reader(inp):
					row_ind += 1
					row_split = [elem.strip().split(delim) for elem in row]
					#print("row[0][0]=", row_split[0][0])
					#row_split[0][1] = ''.join([str(i) for i in row_split[0][1].split() if i.isdigit()])
					#row_split[0][1] = float(row_split[0][1])
					#print(row_split[0][1])
					if (row_split[0][1].isdigit() == False):
						print("I GOT FALSEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
						print("index of non digit pedestrian is =", row_ind)
					if(row_split[0][0] != tsp_tm1):
						row_tm1 += 1
						writer.writerow([row_tm1, row_split[0][1], row_split[0][2], row_split[0][3]])
						tsp_tm1 = row_split[0][0]
					else:
						writer.writerow([row_tm1, row_split[0][1], row_split[0][2], row_split[0][3]])

				inp.close()
		out.close()



if __name__ == "__main__":
    timestamp_to_float()


