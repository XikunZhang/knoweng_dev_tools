"""
code for managing KnowEnG verification
"""
import os
import pandas as pd
import yaml

def update_SC_run_file(Data_Cleanup_Run_File, Samples_Clustering_Run_File):
    """ take the results of data cleaning and update the yaml file """
    results_path = os.path.abspath(get_results_directory(Data_Cleanup_Run_File))
    null_dir, spreadsheet_name_full_path = os.path.split(get_spreadsheet_name(Data_Cleanup_Run_File))
    spreadsheet_name_full_path, null_ext = os.path.splitext(spreadsheet_name_full_path)
    spreadsheet_name_full_path = spreadsheet_name_full_path + '_ETL.tsv'
    spreadsheet_name_full_path = os.path.join(results_path, spreadsheet_name_full_path)
    if os.path.isfile(spreadsheet_name_full_path):
        set_spreadsheet_name(Samples_Clustering_Run_File, spreadsheet_name_full_path)
    else:
        print('failed to find', spreadsheet_name_full_path)
    null_dir, phenotype_name_full_path = os.path.split(get_phenotype_name(Data_Cleanup_Run_File))
    phenotype_name_full_path, null_ext = os.path.splitext(phenotype_name_full_path)
    phenotype_name_full_path = phenotype_name_full_path + '_ETL.tsv'
    phenotype_name_full_path = os.path.join(results_path, phenotype_name_full_path)
    if os.path.isfile(phenotype_name_full_path):
        set_phenotype_name(Samples_Clustering_Run_File, phenotype_name_full_path)
    else:
        print('failed to find', phenotype_name_full_path)

def set_results_directory(yaml_file_full_path, results_dir_full_path='nix'):
    """ try to set the results directory; or if results_directory is in the file make the path absolute """
    if os.path.isfile(yaml_file_full_path):
        with open(yaml_file_full_path, 'r') as infile:
            run_parameters = yaml.load(infile)
            if os.path.isdir(results_dir_full_path):
                run_parameters['results_directory'] = os.path.abspath(results_dir_full_path)
                with open(yaml_file_full_path, 'w') as outfile:
                    yaml.dump(run_parameters, outfile, default_flow_style=False)
            elif 'results_directory' in run_parameters:
                run_parameters['results_directory'] = os.path.abspath(run_parameters['results_directory'])
                with open(yaml_file_full_path, 'w') as outfile:
                    yaml.dump(run_parameters, outfile, default_flow_style=False)


def write_yaml_key_file_name(yaml_file_full_path, key_file_name, key_name):
    if os.path.isfile(yaml_file_full_path):
        with open(yaml_file_full_path, 'r') as infile:
            run_parameters = yaml.load(infile)
        if os.path.isfile(key_file_name):
            run_parameters[key_name] = os.path.abspath(key_file_name)
            with open(yaml_file_full_path, 'w') as outfile:
                yaml.dump(run_parameters, outfile, default_flow_style=False)


def set_phenotype_name(yaml_file_full_path, key_file_name):
    """
    """
    if os.path.isfile(key_file_name):
        key_name = 'phenotype_name_full_path'
        write_yaml_key_file_name(yaml_file_full_path, key_file_name, key_name)
    else:
        print('File Not Found:\n\t',key_file_name)

def get_phenotype_name(yaml_file_full_path):
    with open(yaml_file_full_path, 'r') as infile:
        run_parameters = yaml.load(infile)
    if 'phenotype_name_full_path' in run_parameters:
        return run_parameters['phenotype_name_full_path']
    else:
        return 'key not found'


def set_spreadsheet_name(yaml_file_full_path, key_file_name):
    """ """
    if os.path.isfile(key_file_name):
        key_name = 'spreadsheet_name_full_path'
        write_yaml_key_file_name(yaml_file_full_path, key_file_name, key_name)
    else:
        print('File Not Found:\n\t',key_file_name)

def get_spreadsheet_name(yaml_file_full_path):
    with open(yaml_file_full_path, 'r') as infile:
        run_parameters = yaml.load(infile)
    if 'spreadsheet_name_full_path' in run_parameters:
        return run_parameters['phenotype_name_full_path']
    else:
        return 'key not found'


def set_gg_network_name(yaml_file_full_path, key_file_name):
    """ """
    if os.path.isfile(key_file_name):
        key_name = 'gg_network_name_full_path'
        write_yaml_key_file_name(yaml_file_full_path, key_file_name, key_name)
    else:
        print('File Not Found:\n\t',key_file_name)

def get_gg_network_name(yaml_file_full_path):
    with open(yaml_file_full_path, 'r') as infile:
        run_parameters = yaml.load(infile)
    if 'gg_network_name_full_path' in run_parameters:
        return run_parameters['gg_network_name_full_path']
    else:
        return 'key not found'


def get_results_directory(yaml_file_full_path):
    if os.path.isfile(yaml_file_full_path):
        with open(yaml_file_full_path, 'r') as infile:
            run_parameters = yaml.load(infile)
        if 'results_directory' in run_parameters:
            return run_parameters['results_directory']
        else:
            return 'key not found'


def view_dictionary(run_parameters):
    for k in sorted(run_parameters.keys()):
        print('%-40s: %s'%(k,run_parameters[k]))


def print_out_the_yml_file(full_path_file_name):
    if os.path.isfile(full_path_file_name):
        run_parameters = {}
        with open(full_path_file_name, 'r') as file_handle:
            run_parameters = yaml.load(file_handle)
        view_dictionary(run_parameters)


def show_yaml_file(directory_path, file_name):
    full_path_file_name = os.path.join(directory_path, file_name)
    print_out_the_yml_file(full_path_file_name)



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

