import logging
import os
import math
import itertools
import numpy as np
import glob
import csv


def causalvar():
	exp_dir = "Exp_3_run_4"
	filename_dir = "../scripts/datasets/thor_data_all/thor_data_raw/csv_separated_agent/2.5_hz/" + exp_dir + "/thor_causal_aug/"
	curr_dir = os.getcwd()
	csv_dir=  curr_dir + "/" + filename_dir 

	for filename in os.listdir(csv_dir):
		digit = filename.split(".")[0][0]
		file = os.path.join(csv_dir, filename)
		with open(exp_dir+"_Agent"+str(digit)+"_edit.csv", 'w') as out:
			writer = csv.writer(out)
			with open(file, 'r') as inp:
				for row in csv.reader(inp):
					if (row[2] == "nan" or row[2] == "NaN" ):
						#print("row = ", row[2])
						continue
					else:
						#print("row = ", row)
						writer.writerow(row)
				inp.close()
			out.close()




if __name__ == "__main__":
    causalvar()


