import os
import sys
import argparse
import pandas as pd

def get_cluster_dict(clusters_df):
     cluster_dict = {}
     for k in range(0, clusters_df[1].max()+1):
          cluster_dict['%d'%k] = (clusters_df[1] == k).sum()
     return cluster_dict

def main(args):
     parser = argparse.ArgumentParser()
     parser.add_argument('-dir_name', type=str)
     args = parser.parse_args()
     dir_name = args.dir_name
     print('dir_name>>',dir_name)
     clusters_df = pd.read_csv(fname, sep='\t', header=None, index_col=0)
     print(clusters_df.shape,'\n')

     cluster_dict = get_cluster_dict(clusters_df)
     for k in cluster_dict.keys():
          print(k, cluster_dict[k])


if __name__ == "__main__":
     main(sys.argv)
