import os
import sys
import argparse
import pyverify as pv


def main(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-verification_dir', type=str)
	parser.add_argument('-results_dir', type=str)
	args = parser.parse_args()
	verification_dir = args.verification_dir
	results_dir = args.results_dir
	dir_differ_dict = pv.verification_directory_compare(verification_dir, results_dir)
	for k in sorted(dir_differ_dict.keys()):
		print(k, '\t\t', dir_differ_dict[k], 'differences')


if __name__ == "__main__":
	main(sys.argv)
