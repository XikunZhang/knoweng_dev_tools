import os
import sys
import argparse
import pandas as pd

def main(args):
     parser = argparse.ArgumentParser()
     parser.add_argument('-file_name', type=str)
     args = parser.parse_args()
     fname = args.file_name
     print('fname>>',fname)
     clusters_df = pd.read_csv(fname, sep='\t', header=None, index_col=0)
     print(clusters_df.shape,'\n')
     for k in range(0, clusters_df[1].max()+1):
          print(k, (clusters_df[1] == k).sum())

if __name__ == "__main__":
     main(sys.argv)
