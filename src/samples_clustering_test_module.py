"""
dlanier@illinois.edu
mradmstr514226508@gmail.com
"""
import os
import sys
import time

import pandas as pd
import numpy as np

sys.path.insert(1, '../../Data_Cleanup_Pipeline/src')
import data_cleanup_toolbox as dc

import knpackage.toolbox as kn

def cleanup_test_SC(run_parameters):
    """ sc_test_list_df = cleanup_test_SC(run_parameters)
    Args:
        run_parameters:     python dict with keys- 'spreadsheet_data_dir', 'pheno_data_dir',
                            and all data cleaning keys set for samples clustering

    Returns:
        sc_test_list_df:
    """
    results_directory_base = run_parameters['results_directory']

    sc_test_list_df = get_SC_phenotype_viability_df(
        run_parameters['spreadsheet_data_dir'], run_parameters['pheno_data_dir'])
    sc_test_list_df['STATUS'] = 0
    sc_test_list_df['cleanup_runtime'] = 0
    sc_test_list_df['message_logfile'] = 0

    for row_n in list(sc_test_list_df.index):
        if sc_test_list_df['samples_intersect'].loc[row_n] > 0:
            spreadsheet_name = sc_test_list_df['spreadsheet'].loc[row_n]
            run_parameters['spreadsheet_name_full_path'] = os.path.join(
                run_parameters['spreadsheet_data_dir'], spreadsheet_name)

            phenotype_name = sc_test_list_df['phenotype'].loc[row_n]
            run_parameters['phenotype_name_full_path'] = os.path.join(
                run_parameters['pheno_data_dir'], phenotype_name)

            dir_extra = '_' + spreadsheet_name + '_' + phenotype_name
            run_parameters['results_directory'] = kn.create_dir(results_directory_base, dir_extra)

            start_cleanup_time = time.time()
            validation_flag, message = dc.run_samples_clustering_pipeline(run_parameters)
            cleanup_runtime = time.time() - start_cleanup_time
            sc_test_list_df['STATUS'].loc[row_n] = validation_flag
            sc_test_list_df['cleanup_runtime'] = '%0.4f'%(cleanup_runtime)

            log_filename = os.path.join(run_parameters["results_directory"], "log_samples_clustering_pipeline.yml")
            sc_test_list_df['message_logfile'].loc[row_n] = log_filename
            dc.generate_logging(validation_flag, message, log_filename)

    out_file_name = os.path.join(results_directory_base, run_parameters['pipeline_type'])
    sc_test_list_df.to_csv(out_file_name, sep='\t', header=True, index=True)

def get_SC_phenotype_viability_df(spreadsheet_data_dir, pheno_data_dir):
    """ sc_test_list_df = get_SC_phenotype_viability_df(spreadsheet_data_dir, pheno_data_dir) """
    sc_test_list_df = get_SC_test_files_list_df(spreadsheet_data_dir, pheno_data_dir)

    sc_test_list_df['spreadsheet_genes'] = 0
    sc_test_list_df['spreadsheet_samples'] = 0
    sc_test_list_df['samples_intersect'] = 0
    sc_test_list_df['phenotype_samples'] = 0
    sc_test_list_df['phenotype_keys'] = 0

    spreadsheet_full_file_x = ''
    phenotype_full_file_x = ''
    for row_index in list(sc_test_list_df.index):
        spreadsheet_full_file = os.path.join(spreadsheet_data_dir, sc_test_list_df['spreadsheet'].loc[row_index])
        phenotype_full_file = os.path.join(pheno_data_dir, sc_test_list_df['phenotype'].loc[row_index])
        if spreadsheet_full_file != spreadsheet_full_file_x:
            spreadsheet_full_file_x = spreadsheet_full_file
            spreadsheet_df = pd.read_csv(spreadsheet_full_file, sep='\t', index_col=0, header=0)

        if phenotype_full_file != phenotype_full_file_x:
            phenotype_full_file_x = phenotype_full_file
            phenotype_df = pd.read_csv(phenotype_full_file,sep='\t', index_col=0, header=0)

        sc_test_list_df['spreadsheet_genes'].loc[row_index] = spreadsheet_df.shape[0]
        sc_test_list_df['spreadsheet_samples'].loc[row_index] = spreadsheet_df.shape[1]

        sc_test_list_df['phenotype_samples'].loc[row_index] = phenotype_df.shape[0]
        sc_test_list_df['phenotype_keys'].loc[row_index] = phenotype_df.shape[1]

        samples_intersection = list( set(list(spreadsheet_df.columns)) & set(list(phenotype_df.index)) )
        sc_test_list_df['samples_intersect'].loc[row_index] = max(len(samples_intersection), 0)

    return sc_test_list_df


def get_SC_test_files_list_df(spreadsheet_data_dir, pheno_data_dir):
    """ sc_test_list_df = get_SC_test_files_list_df(spreadsheet_data_dir, pheno_data_dir) """

    pheno_file_list = []
    pheno_file_dir_list = sorted(os.listdir(pheno_data_dir))
    for l in pheno_file_dir_list:
        if l[0] == '.' or os.path.isdir(os.path.join(pheno_data_dir, l)):
            pass
        else:
            pheno_file_list.append(l)

    spreadsheet_file_list = []
    spreadsheet_file_dir_list = sorted(os.listdir(spreadsheet_data_dir))
    for l in spreadsheet_file_dir_list:
        if l[0] == '.' or os.path.isdir(os.path.join(spreadsheet_data_dir, l)):
            pass
        else:
            spreadsheet_file_list.append(l)

    number_of_dataframe_rows = 0
    dataframe_row_index = []
    count = 0
    for spreadsheet_file_name in spreadsheet_file_dir_list:
        phenotype_list = get_phenotypes_for_spreadsheet(spreadsheet_file_name, pheno_file_list)
        if len(phenotype_list) > 0:
            number_of_dataframe_rows += len(phenotype_list)
            for f_name in phenotype_list:
                count += 1
                dataframe_row_index.append('%04d'%count)

    col_list = ['spreadsheet', 'phenotype']
    sc_test_list_df = pd.DataFrame(data=np.zeros((count,2)), index=dataframe_row_index, columns=col_list)

    count = 0
    for spreadsheet_file_name in spreadsheet_file_dir_list:
        phenotype_list = get_phenotypes_for_spreadsheet(spreadsheet_file_name, pheno_file_list)
        if len(phenotype_list) > 0:
            number_of_dataframe_rows += len(phenotype_list)
            for f_name in phenotype_list:
                sc_test_list_df.iloc[count] = [spreadsheet_file_name, f_name]
                count += 1

    return sc_test_list_df


def get_phenotypes_for_spreadsheet(spreadsheet_file_name, phenotype_file_list):
    """ phenotype_list = get_phenotypes_for_spreadsheet(spreadsheet_file_name, phenotype_file_list) """
    x = spreadsheet_file_name.find('.G.')
    g_str = spreadsheet_file_name[:x]
    phenotype_list = []
    for f in phenotype_file_list:
        if f.find(g_str) >= 0:
            phenotype_list.append(f)

    return sorted(phenotype_list)


def main():
    """ python3 test_data_cleanup.py -run_directory /one_with/yaml_file -run_file yaml_file.yml """
    import sys
    from knpackage.toolbox import get_run_directory_and_file, get_run_parameters, create_dir
    run_directory, run_file = get_run_directory_and_file(sys.argv)
    run_parameters = get_run_parameters(run_directory, run_file)

    pipeline_type = run_parameters['pipeline_type']
    run_parameters['results_directory'] = create_dir(run_parameters['results_directory'], pipeline_type)

    for k in sorted(run_parameters.keys()):
        print(k,':\t',run_parameters[k])

    cleanup_test_SC(run_parameters)


if __name__ == "__main__":
    main()
