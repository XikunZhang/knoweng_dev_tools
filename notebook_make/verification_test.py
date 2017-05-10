"""
code for managing KnowEnG verification
"""
import os
import pandas as pd
import yaml

GP_options = {'run_pearson': 'BENCHMARK_1_GP_pearson',
                'run_net_pearson': 'BENCHMARK_3_GP_net_pearson',
                'run_bootstrap_pearson': 'BENCHMARK_2_GP_bootstrap_pearson',
                'run_bootstrap_net_pearson': 'BENCHMARK_4_GP_bootstrap_net_pearson',
                'run_t_test': 'BENCHMARK_5_GP_t_test',
                'run_net_t_test': 'BENCHMARK_7_GP_net_t_test',
                'run_bootstrap_t_test': 'BENCHMARK_6_GP_bootstrap_t_test',
                'run_bootstrap_net_t_test': 'BENCHMARK_8_GP_bootstrap_net_t_test',
                'run_single_drug_pearson': 'TEST_1_GP_single_drug_pearson',
                'run_multidrug_pearson': 'TEST_2_GP_many_drugs_pearson',
                'run_single_drug_t_test': 'TEST_3_GP_single_drug_t_test',
                'run_multidrug_t_test': 'TEST_4_GP_many_drugs_t_test'}


def get_run_file_key_data(yaml_file_full_path, key_name):
    """ get the data for key name in run_file - yaml file 
    Usage: key_value, STATUS = get_run_file_key_data(yaml_file_full_path, key_name)
    """
    if os.path.isfile(yaml_file_full_path):
        with open(yaml_file_full_path, 'r') as infile:
            run_parameters = yaml.load(infile)
        if key_name in run_parameters:
            return run_parameters[key_name], True
        else:
            return 'key not found', False


def view_dictionary(run_parameters):
    for k in sorted(run_parameters.keys()):
        print('%-40s: %s'%(k,run_parameters[k]))


def display_run_file(full_path_file_name):
    if os.path.isfile(full_path_file_name):
        run_parameters = {}
        with open(full_path_file_name, 'r') as file_handle:
            run_parameters = yaml.load(file_handle)
        view_dictionary(run_parameters)


def show_yaml_file(directory_path, file_name):
    display_run_file(os.path.join(directory_path, file_name))


def verify_one_file(file_name, verification_dir, results_dir):

    if os.path.isfile(os.path.join(verification_dir, file_name)):
        rank_v_df = pd.read_csv(os.path.join(verification_dir, file_name), sep='\t', header=0, index_col=0)
    else:
        return 1, "verification file not found"

    file_name_prefix = file_name[:-4]
    result_dir_list = os.listdir(results_dir)
    rank_r_df = None
    for f_name in result_dir_list:
        if os.path.isfile(os.path.join(results_dir, f_name)):
            if f_name[0:(len(file_name_prefix))] == file_name_prefix:
                rank_r_df = pd.read_csv(os.path.join(results_dir, f_name), sep='\t', header=0, index_col=0)
                break

    if rank_r_df is None:
        return 1, "result file not found"

    diff_dict = {}
    sum_of_differences = 0
    for col_name in list(rank_v_df.columns):
        S = (rank_v_df[col_name] != rank_r_df[col_name]).sum()
        sum_of_differences = sum_of_differences + S
        diff_dict[col_name] = S

    return sum_of_differences, diff_dict


def verification_directory_compare(verification_dir, results_dir):
    """ find the verification directory files in the results directory and compare the data """
    dir_differ_dict = {}
    veri_dir_list = os.listdir(verification_dir)
    for file_name in veri_dir_list:
        if os.path.isfile(os.path.join(verification_dir, file_name)):
            sum_of_differences, diff_dict = verify_one_file(file_name, verification_dir, results_dir)
            dir_differ_dict[file_name] = sum_of_differences

    return dir_differ_dict



def remove_time_stamp_names(directory_name, STAMP_START):
    """ copy to cell - code for creating new set of verification files:
    resu_dir = '../../Gene_Prioritization_Pipeline/test/run_dir/results'
    STAMP_START = '_Tue'
    verification_test.remove_time_stamp_names(resu_dir, STAMP_START)
    print('\n\n\t\tafter:\n')
    os.listdir(resu_dir)
    """
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
