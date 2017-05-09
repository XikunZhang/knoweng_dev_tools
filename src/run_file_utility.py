"""
run_file_utility.py
lanier4@illinois.edu
"""
import os
import pandas as pd
import yaml


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


def update_run_file_post_clean(active_run_file_name):
    """ Update run file after data cleaning """
    STATUS = False
    if os.path.isfile(active_run_file_name):
        with open(active_run_file_name, 'r') as infile:
            run_parameters = yaml.load(infile)
            
        run_parameters['spreadsheet_name_full_path'] = run_parameters['SC_spreadsheet_name_full_path']
        run_parameters['results_directory'] = run_parameters['SC_results_directory']
        if 'phenotype_name_full_path' in run_parameters:
            run_parameters['phenotype_name_full_path'] = run_parameters['SC_phenotype_name_full_path']
        
        with open(active_run_file_name, 'w') as outfile:
            yaml.dump(run_parameters, outfile, default_flow_style=False)
            STATUS = True
            
    return STATUS


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
