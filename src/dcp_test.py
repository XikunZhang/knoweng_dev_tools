""" lanier4@illinois.edu """

import os
import sys
import time

import numpy as np
import pandas as pd

import knpackage.toolbox as kn

# IF Data_Cleanup_Pipeline/src is NOT on Path; insert the absolute path & uncomment next line.
# sys.path.insert(1, '/Users/lanier4/dlanier_KnowEnG/Data_Cleanup_Pipeline/src')
import data_cleanup_toolbox as dc

def test_data_cleanup(run_parameters, run_cleanup=True):
    """ test_samples_clustering_cleanup(run_parameters, run_cleanup) 
    Args:
        run_parameters: with keys - pipeline_type, spreadsheet_data_dir (opt pheno_data_dir)
        run_cleanup:    (default True) set to false to display files processed only
    """
    pipeline_type = run_parameters['pipeline_type']
    print('\n\tStart testing %s at %s'%(pipeline_type, time.strftime("%c", time.localtime() ) ) )
    
    spreadsheet_data_dir = run_parameters['spreadsheet_data_dir']
    
    if pipeline_type == 'geneset_characterization_pipeline' or pipeline_type == 'geneset_characterization':
        pheno_data_dir = None
    else:
        pheno_data_dir = run_parameters['pheno_data_dir']
    
    test_result_df = get_phenotype_spreadsheet_dataframe(spreadsheet_data_dir, pheno_data_dir)
    
    for spreadsheet_file in list(test_result_df.index):
        tt = 0.0
        validation_flag = False
        message = "Failed to finish"
        err_message = ''

        run_parameters['spreadsheet_name_full_path'] = os.path.join(spreadsheet_data_dir, spreadsheet_file)
        phenotype_file = test_result_df.loc[spreadsheet_file, 'samples_phenotypes']
        if phenotype_file != 0:
            print('\n', spreadsheet_file)
            print('\t', phenotype_file)
            run_parameters['phenotype_full_path'] = os.path.join(pheno_data_dir, phenotype_file)
            if run_cleanup:
                try:
                    t0 = time.time()
                    if pipeline_type == 'samples_clustering_pipeline':
                        validation_flag, message = dc.run_samples_clustering_pipeline(run_parameters)
                    elif pipeline_type == 'gene_prioritization_pipeline':
                        validation_flag, message = dc.run_gene_prioritization_pipeline(run_parameters)
                    tt = time.time() - t0
                except:
                    err_message = str(sys.exc_info())
                    print("Unexpected error: {}".format(err_message))
                    pass
            log_file_name = os.path.join(run_parameters['results_directory'], 'log_' + spreadsheet_file + phenotype_file)
        elif pipeline_type == 'geneset_characterization_pipeline':
            print('\t', spreadsheet_file)
            if run_cleanup:
                try:
                    t0 = time.time()
                    validation_flag, message = dc.run_geneset_characterization_pipeline(run_parameters)
                    tt = time.time() - t0
                except:
                    err_message = str(sys.exc_info())
                    print("Unexpected error: {}".format(err_message))
                    pass
            log_file_name = os.path.join(run_parameters['results_directory'], 'log_' + spreadsheet_file)

        dc.generate_logging(validation_flag, message, log_file_name)
        test_result_df.loc[spreadsheet_file, 'message'] = log_file_name
        test_result_df.loc[spreadsheet_file, 'cleanup_time'] = tt
        test_result_df.loc[spreadsheet_file, 'validation_flag'] = validation_flag
        test_result_df.loc[spreadsheet_file, 'err_message'] = err_message

    #col_list = ['genes','samples','samples_phenotypes','s','p','validation_flag','message','cleanup_time']
        try:
            tmp_df = pd.read_csv(run_parameters['spreadsheet_name_full_path'], sep='\t', header=0, index_col=0)
            test_result_df.loc[spreadsheet_file, 'genes'] = tmp_df.shape[0]
            test_result_df.loc[spreadsheet_file, 'samples'] = tmp_df.shape[1]
            if phenotype_file != 0:
                tmp_df = pd.read_csv(run_parameters['phenotype_full_path'], sep='\t', header=0, index_col=0)
                test_result_df.loc[spreadsheet_file, 's'] = tmp_df.shape[0]
                test_result_df.loc[spreadsheet_file, 'p'] = tmp_df.shape[1]
        except:
            err_message = str(sys.exc_info())
            print("Unexpected error: {}".format(err_message))
            pass

    if run_cleanup and not test_result_df.empty:
        result_df_file_name = os.path.join(run_parameters['results_directory'], pipeline_type)
        result_df_file_name = kn.create_timestamped_filename(result_df_file_name) + '.tsv'
        test_result_df.to_csv(result_df_file_name, sep='\t', index=True, header=True, na_rep='NA')
        print('\n\tResults file\n%s\n'%result_df_file_name)
    
    return test_result_df


def get_spreadsheets_for_pheno(pheno_file, sp_list):
    """ spreadsheet_list = get_spreadsheets_for_pheno(pheno_file, sp_list) """
    x = pheno_file.find('.P.')
    g_str = pheno_file[:x]
    spreadsheet_list = []
    for f in sp_list:
        if f.find(g_str) >= 0: spreadsheet_list.append(f)
    return sorted(spreadsheet_list)


def get_phenotype_spreadsheet_dataframe(spreadsheet_data_dir, pheno_data_dir=None):
    """ test_result_df = get_spreadsheet_phenotype_dataframe(spreadsheet_data_dir, pheno_data_dir) """
    pheno_file_dir_list = sorted(os.listdir(pheno_data_dir))
    pheno_file_list = []
    for l in pheno_file_dir_list:
        if l[0] == '.' or os.path.isdir(os.path.join(pheno_data_dir, l)):
            pass
        else:
            pheno_file_list.append(l)

    if len(pheno_file_list) < 1:
        test_result_df = get_spreadsheet_phenotype_dataframe(spreadsheet_data_dir, None)
    else:
        sp_dir_list = sorted(os.listdir(spreadsheet_data_dir))
        sp_file_list = []
        for l in sp_dir_list:
            if l[0] == '.' or os.path.isdir(os.path.join(pheno_data_dir, l)):
                pass
            else:
                sp_file_list.append(l)

        pheno_dict = {}
        for pheno_file in pheno_file_list:
            pheno_dict[pheno_file] = get_spreadsheets_for_pheno(pheno_file, sp_file_list)

        row_names = []
        pheno_4_row_names = []

        for pheno in pheno_file_list:
            if len(pheno_dict[pheno]) > 0:
                for sp_name in pheno_dict[pheno]:
                    row_names.append(sp_name)
                    pheno_4_row_names.append(pheno)

        col_list = ['genes','samples','samples_phenotypes','s','p','validation_flag',
                    'message','cleanup_time', 'err_message']

        test_result_df = pd.DataFrame(data=np.zeros((len(row_names), len(col_list))),
                                        index=row_names, columns=col_list)

        test_result_df['samples_phenotypes'] = pheno_4_row_names
        print(test_result_df)
    return test_result_df


def get_spreadsheet_phenotype_dataframe(spreadsheet_data_dir, pheno_data_dir=None):
    """ test_result_df = get_spreadsheet_phenotype_dataframe(spreadsheet_data_dir, pheno_data_dir) """
    
    col_list = ['genes','samples','samples_phenotypes','s','p','validation_flag','message','cleanup_time', 'err_message']
    
    spreadsheet_file_list_0 = sorted(os.listdir(spreadsheet_data_dir))
    spreadsheet_file_list = []
    for l in spreadsheet_file_list_0:
        if l[0] == '.' or os.path.isdir(os.path.join(spreadsheet_data_dir, l)):
            pass
        elif l.find('.G.') >= 0:
            spreadsheet_file_list.append(l)
            
    test_result_df = pd.DataFrame(data=np.zeros((len(spreadsheet_file_list), len(col_list))),
                                  index=spreadsheet_file_list, columns=col_list)
    
    test_result_df.index.name = 'genes_x_samples'
    
    if pheno_data_dir is not None:
        pheno_file_list = sorted(os.listdir(pheno_data_dir))
        for pheno_file in pheno_file_list:
            spreadsheet_list = get_spreadsheets_for_pheno(pheno_file, spreadsheet_file_list)
            for spreadsheet_file in spreadsheet_list:
                test_result_df.loc[spreadsheet_file, 'samples_phenotypes'] = pheno_file
    
    return test_result_df


def main():
    """ python3 test_data_cleanup.py -run_directory /one_with/yaml_file -run_file yaml_file.yml """
    import sys
    from knpackage.toolbox import get_run_directory_and_file, get_run_parameters
    run_directory, run_file = get_run_directory_and_file(sys.argv)
    run_parameters = get_run_parameters(run_directory, run_file)
    if 'data_cleanup_toolbox_directory' in run_parameters['data_cleanup_toolbox_directory']:
        sys.path.insert(1, run_parameters['data_cleanup_toolbox_directory'])

    pipeline_type = run_parameters['pipeline_type']
    run_parameters['results_directory'] = kn.create_dir(run_parameters['results_directory'], pipeline_type)

    for k in sorted(run_parameters.keys()):
        print(k,':\t',run_parameters[k])
        
    test_data_cleanup(run_parameters)

    
if __name__ == "__main__":
    main()
