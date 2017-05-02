import os
import sys
import pandas as pd


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-file_name', type=str)
	args = parser.parse_args()
	f_name = args.file_name
	print('Opening:\t',f_name)
	clusters_df = pd.read_csv(f_name, sep='\t',header=None,index_col=0)
	print('success\n')
	for k in range(0,clusters_df[1].max()+1):
		print(k, (clusters_df[1] == k).sum())


if __name__ is "__main__":
	print('Main')
	main()