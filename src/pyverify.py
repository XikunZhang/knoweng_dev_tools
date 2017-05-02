"""
code for managing KnowEnG verification
"""
import os
import pandas as pd

def verify_one_file(file_name, verification_dir, results_dir):

    if os.path.isfile(os.path.join(verification_dir, file_name)):
        rank_v_df = pd.read_csv(os.path.join(verification_dir, file_name), sep='\t', header=0, index_col=0)
    else:
        return 'not compared', "verification file not found"

    file_name_prefix = file_name[:-4]
    result_dir_list = os.listdir(results_dir)
    rank_r_df = None
    for f_name in result_dir_list:
        if os.path.isfile(os.path.join(results_dir, f_name)):
            if f_name[0:(len(file_name_prefix))] == file_name_prefix:
                rank_r_df = pd.read_csv(os.path.join(results_dir, f_name), sep='\t', header=0, index_col=0)
                break

    if rank_r_df is None:
        return 'not compared', "result file not found"

    diff_dict = {}
    sum_of_differences = 0
    for col_name in list(rank_v_df.columns):
        S = (rank_v_df[col_name] != rank_r_df[col_name]).sum()
        sum_of_differences = sum_of_differences + S
        diff_dict[col_name] = S

    return sum_of_differences, diff_dict


def verification_directory_compare(verification_dir, results_dir):
    """ fine the verification directory files in the results directory and compare the data """
    dir_differ_dict = {}
    veri_dir_list = os.listdir(verification_dir)
    for file_name in veri_dir_list:
        if os.path.isfile(os.path.join(verification_dir, file_name)):
            sum_of_differences, diff_dict = verify_one_file(file_name, verification_dir, results_dir)
            dir_differ_dict[file_name] = sum_of_differences

    return dir_differ_dict


def remove_time_stamp_names(directory_name, STAMP_START):
    f_list = os.listdir(directory_name)
    for f_name in f_list:
        base_name, f_ext = os.path.splitext(f_name)
        n = base_name.find(STAMP_START)
        if n > 0:
            new_name = os.path.join(directory_name, base_name[0:n] + f_ext)
            try:
                os.rename(os.path.join(directory_name, f_name), new_name)
            except:
                print('blah! EXCEPTION? with rename\t', new_name)
                pass

