"""
run_file_utility.py
lanier4@illinois.edu
"""
import os
import pandas as pd
import yaml


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
        out_file_name = os.path.join(run_dir, out_file_name + '_Active.yml')
        with open(out_file_name, 'w') as outfile:
            yaml.dump(run_parameters, outfile, default_flow_style=False)

        return out_file_name
