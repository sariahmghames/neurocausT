import logging
import os
import math
import itertools
import numpy as np
import glob
import csv


def causalvar():
	exp_dir = "Exp_3_run_4"
	filename_dir = "../scripts/datasets/thor_data_all/thor_data_raw/csv_separated_agent/2.5_hz/"+ exp_dir+"/thor_causal_aug_edit/"
	curr_dir = os.getcwd()
	csv_dir=  curr_dir + "/" + filename_dir 
	peds_dic = {}

	with open(exp_dir+"_cat_edit.csv", 'a') as out:
		writer = csv.writer(out)
		for filename in os.listdir(csv_dir):
			file = os.path.join(csv_dir, filename)
			with open(file, 'r') as inp:
				for row in csv.reader(inp):
					writer.writerow(row)
				inp.close()
		out.close()



if __name__ == "__main__":
    causalvar()


