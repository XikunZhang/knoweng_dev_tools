"""
run_file_utility.py
lanier4@illinois.edu
"""
import os
import time
import numpy as np
import pandas as pd
import yaml
import knpackage.toolbox as kn


Data_Cleanup_methods_dictionary =               {
    'run_data_cleaning'                         : 'data_cleanup.yml',
    'run_pasted_gene_list'                      : 'pasted_gene_cleanup.yml',
    'run_data_cleaning_small'                   : 'TEST_1_data_cleanup.yml',
    'run_samples_clustering_pipeline'           : 'TEST_1_samples_clustering_pipeline.yml',
    'run_gene_prioritization_pipeline_pearson'  : 'TEST_1_gene_prioritization_pipeline_pearson.yml',
    'run_gene_prioritization_pipeline_t_test'   : 'TEST_1_gene_prioritization_pipeline_t_test.yml',
    'run_geneset_characterization_pipeline'     : 'TEST_1_geneset_characterization_pipeline.yml' }

Samples_Clustering_methods_dictionary = {
    'run_nmf'                           : 'BENCHMARK_1_SC_nmf.yml',
    'run_net_nmf'                       : 'BENCHMARK_2_SC_net_nmf.yml',
    'run_cc_nmf_serial'                 : 'BENCHMARK_3_SC_cc_nmf_serial.yml',
    'run_cc_nmf_parallel_shared'        : 'BENCHMARK_4_SC_cc_nmf_parallel_shared.yml',
    'run_cc_net_nmf_serial'             : 'BENCHMARK_6_SC_cc_net_nmf_serial.yml',
    'run_cc_net_nmf_parallel_shared'    : 'BENCHMARK_7_SC_cc_net_nmf_parallel_shared.yml' }


def get_run_file_key_data(yaml_file_full_path, key_name):
    """ get the data for key name in run_file - yaml file 
    Usage:     key_value, STATUS = get_run_file_key_data(yaml_file_full_path, key_name)
    """
    if os.path.isfile(yaml_file_full_path):
        with open(yaml_file_full_path, 'r') as infile:
            run_parameters = yaml.load(infile)
        if key_name in run_parameters:
            return run_parameters[key_name], True
        else:
            return 'key not found', False


        
def check_cleaning_log(run_file_name):
    """ check data cleanup logfile """
    results_directory, status_null = get_run_file_key_data(run_file_name, 'results_directory')
    if os.path.isdir(results_directory):
        results_dir_list = sorted(os.listdir(results_directory), reverse=True)
        log_prefix = 'log_'
    for l in results_dir_list:
        if l[0:len(log_prefix)] == log_prefix:
            log_file_name = os.path.join(results_directory, l)
            log_dict = get_run_file_dictionary(log_file_name)
            log_dict_keys = log_dict.keys()
            if 'SUCCESS' in log_dict_keys:
                return True, log_dict
            else:
                return False, log_dict
            
    return False, {}
        

def display_log_dict(log_dict):
    key_list = log_dict.keys()
    for k in key_list:
        print(k,'\n')
        msg_list = log_dict[k]
        for msg_item in msg_list:
                    print(msg_item)
    
def update_run_file_post_clean(active_run_file_name):
    """ Update run file after data cleaning """

    if os.path.isfile(active_run_file_name):
        Cleanup_Success, log_dict = check_cleaning_log(active_run_file_name)
        if not Cleanup_Success:
            display_log_dict(log_dict)
            return False
            
        with open(active_run_file_name, 'r') as infile:
            run_parameters = yaml.load(infile)
            
        run_parameters['spreadsheet_name_full_path'] = run_parameters['SC_spreadsheet_name_full_path']
        run_parameters['results_directory'] = run_parameters['SC_results_directory']
        if 'phenotype_name_full_path' in run_parameters:
            run_parameters['phenotype_name_full_path'] = run_parameters['SC_phenotype_name_full_path']
        
        with open(active_run_file_name, 'w') as outfile:
            yaml.dump(run_parameters, outfile, default_flow_style=False)
            return True
            
    return False


def set_run_file_path_to_abs(run_file_name, run_dir):
    """ set all path fields to absolute paths and write an active run file """
    if os.path.isfile(run_file_name):
        with open(run_file_name, 'r') as infile:
            run_parameters = yaml.load(infile)
        if 'spreadsheet_name_full_path' in run_parameters:
            run_parameters['spreadsheet_name_full_path'] = os.path.abspath(run_parameters['spreadsheet_name_full_path'])
        if 'phenotype_name_full_path' in run_parameters:
            run_parameters['phenotype_name_full_path'] = os.path.abspath(run_parameters['phenotype_name_full_path'])
            
        if 'SC_spreadsheet_name_full_path' in run_parameters:
            run_parameters['SC_spreadsheet_name_full_path'] = os.path.abspath(run_parameters['SC_spreadsheet_name_full_path'])
        if 'SC_phenotype_name_full_path' in run_parameters:
            run_parameters['SC_phenotype_name_full_path'] = os.path.abspath(run_parameters['SC_phenotype_name_full_path'])
        if 'gg_network_name_full_path' in run_parameters:
            run_parameters['gg_network_name_full_path'] = os.path.abspath(run_parameters['gg_network_name_full_path'])
            
        if 'results_directory' in run_parameters:
            run_parameters['results_directory'] = os.path.abspath(run_parameters['results_directory'])
        if 'SC_results_directory' in run_parameters:
            run_parameters['SC_results_directory'] = os.path.abspath(run_parameters['SC_results_directory'])
            
        if 'tmp_directory' in run_parameters:
            run_parameters['tmp_directory'] = os.path.abspath(run_parameters['tmp_directory'])
        
        null_dir, out_file_name = os.path.split(run_file_name)
        out_file_name, null_ext = os.path.splitext(out_file_name)
        out_file_name = os.path.abspath( os.path.join( run_dir, out_file_name + '_Active.yml' ) )
        with open(out_file_name, 'w') as outfile:
            yaml.dump(run_parameters, outfile, default_flow_style=False)

        return out_file_name


def get_run_file_dictionary(full_path_file_name):
    """ get a python dictionary from a yaml file """
    run_parameters = {}
    if os.path.isfile(full_path_file_name):
        with open(full_path_file_name, 'r') as file_handle:
            run_parameters = yaml.load(file_handle)
            
    return run_parameters
    
def display_run_file(full_path_file_name):
    """ display the contents of a yaml file """
    run_parameters = get_run_file_dictionary(full_path_file_name)

    if len(run_parameters) > 0:
        view_dictionary(run_parameters)

def view_dictionary(run_parameters):
    """ display the contents of a python dictionary """
    for k in sorted(run_parameters.keys()):
        print('%-40s: %s'%(k,run_parameters[k]))

def show_yaml_file(directory_path, file_name):
    """  """
    display_run_file(os.path.join(directory_path, file_name))
    
    
def show_result_directory(results_directory):
    if os.path.isdir(results_directory):
        print(results_directory,'\n')
        dir_list = os.listdir(results_directory)
        if len(dir_list) > 0:
            for f_name in sorted(dir_list):
                print(f_name)

def read_cluster_evaluation_result(results_directory, cluster_eval_filename=None):
    if cluster_eval_filename is not None and os.path.isfile(os.path.join(results_directory, cluster_eval_filename)):
        cluster_eval_filename = os.path.join(results_directory, cluster_eval_filename)
        cluster_eval_df = pd.read_csv(cluster_eval_filename, sep='\t', header=0, index_col=0)
        
        return cluster_eval_df, cluster_eval_filename
    
    results_dir_list = sorted(os.listdir(results_directory), reverse=True)
    cluster_evaluation_prefix = 'clustering_evaluation_result'
    for l in results_dir_list:
        if l[0:len(cluster_evaluation_prefix)] == cluster_evaluation_prefix:
            cluster_eval_filename = os.path.join(results_directory, l)
            cluster_eval_df = pd.read_csv(cluster_eval_filename, sep='\t', header=0, index_col=0)
            
            return cluster_eval_df, l
    
    return None, ''
    
    
def read_consensus_result(results_directory, consensus_matrix_file=None):
    if consensus_matrix_file is not None and os.path.isfile(os.path.join(results_directory, consensus_matrix_file)):
        consensus_matrix_file = os.path.join(results_directory, consensus_matrix_file)
        consensus_df = pd.read_csv(consensus_matrix_file, sep='\t', header=0, index_col=0)
        consensus_matrix = consensus_df.as_matrix()
        return consensus_matrix, consensus_matrix_file
    
    results_dir_list = sorted(os.listdir(results_directory), reverse=True)
    cc_prefix = 'consensus_matrix'
    consensus_matrix = None
    for l in results_dir_list:
        if l[0:len(cc_prefix)] == cc_prefix:
            consensus_matrix_file = os.path.join(results_directory, l)
            consensus_df = pd.read_csv(consensus_matrix_file, sep='\t', header=0, index_col=0)
            consensus_matrix = consensus_df.as_matrix()
            return consensus_matrix, l
    
    return 0, ''
    
    
def form_consensus_matrix_graphic(consensus_matrix, k=3):
    """ use K-means to reorder the consensus matrix for graphic display.

    Args:
        consensus_matrix: calculated consensus matrix in samples x samples order.
        k: number of clusters estimate (inner diminsion k of factored h_matrix).

    Returns:
        cc_cm: consensus_matrix with rows and columns in K-means sort order.
    """
    cc_cm = consensus_matrix.copy()
    labels = kn.perform_kmeans(consensus_matrix, k)
    sorted_labels = np.argsort(labels)
    cc_cm = cc_cm[sorted_labels[:, None], sorted_labels]

    return cc_cm

def run_data_cleanup(run_dir, run_file):
    """ run the data cleanup pipeline """
    data_cleanup_start_time = time.time()
    DC_call_string = 'python3 ../../Data_Cleanup_Pipeline/src/data_cleanup.py -run_directory' + ' ' + run_dir
    DC_call_string = DC_call_string + ' -run_file' + ' ' + run_file
    os.system(DC_call_string)
    run_file_name = os.path.join(run_dir, run_file)
    SUCCESS, log_dict = check_cleaning_log(run_file_name)
    return SUCCESS, log_dict, time.time() - data_cleanup_start_time


def run_samples_clustering(run_dir, run_file, SC_src_directory='../../Samples_Clustering_Pipeline/src'):
    """ run the samples clustering pipeline """
    SC_src_directory = os.path.join(os.path.abspath(SC_src_directory), 'samples_clustering.py')
    SC_call_string = 'python3' + ' ' + SC_src_directory + ' ' + '-run_directory' + ' ' + run_dir
    SC_call_string = SC_call_string + ' -run_file' + ' ' + run_file

    samples_clustering_start_time = time.time()
    os.system(SC_call_string)

    return time.time() - samples_clustering_start_time

def git_clone_Samples_Clustering(pipelines_directory):
    """  clone samples clustering and data cleaning if they are not installed relative to the calling notebook """
    working_directory = os.getcwd()
    os.chdir(pipelines_directory)

    DC_name = 'Data_Cleanup_Pipeline'
    Data_Cleanup_Exists = False
    SC_name = 'Samples_Clustering_Pipeline'
    Samples_Clustering_Exists = False

    dir_listing = os.listdir()
    for d in dir_listing:
        if os.path.isdir(d):
            if d == DC_name:
                Data_Cleanup_Exists = True
            elif d == SC_name:
                Samples_Clustering_Exists = True

    if Data_Cleanup_Exists == False:
        dc_git_string = 'git clone https://github.com/KnowEnG-Research/Data_Cleanup_Pipeline.git'
        os.system(dc_git_string)

    if Samples_Clustering_Exists == False:
        sc_git_string = 'git clone https://github.com/KnowEnG-Research/Samples_Clustering_Pipeline.git'
        os.system(sc_git_string)

    os.chdir(working_directory)





















