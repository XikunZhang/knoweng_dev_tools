import os
import sys
import pandas as pd
from knpackage.toolbox import get_run_directory_and_file

def flip_ss(data_directory, spreadsheet_file):
    read_copy_transpose_write_df(data_directory, spreadsheet_file)
    #data_directory, spreadsheet_file = get_run_directory_and_file(sys.argv)
    # full_file_name = os.path.join(data_directory, spreadsheet_file)
    # spreadsheet_df = pd.read_csv(full_file_name, sep='\t', index_col=0, header=0)
    # spreadsheet_df = spreadsheet_df.transpose()
    # spreadsheet_df.to_csv(full_file_name, sep='\t', index=True, header=True)
    
def read_copy_transpose_write_df(data_directory, spreadsheet_file):
    #data_directory, spreadsheet_file = get_run_directory_and_file(sys.argv)
    full_file_name = os.path.join(data_directory, spreadsheet_file)
    spreadsheet_df = pd.read_csv(full_file_name, sep='\t', index_col=0, header=0)
    spreadsheet_df = spreadsheet_df.transpose()
    output_file_name = os.path.join(data_directory, spreadsheet_file[0:-4] + '_T.tsv')
    spreadsheet_df.to_csv(output_file_name, sep='\t', index=True, header=True)
    # return output_file_name

if __name__ == "__main__":
    data_directory, spreadsheet_file = get_run_directory_and_file(sys.argv)
    read_copy_transpose_write_df(data_directory, spreadsheet_file)