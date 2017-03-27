"""
dlanier@illinois.edu
mradmstr514226508@gmail.com
"""
import os

import pandas as pd
import numpy as np


def get_SC_phenotype_viability_df(spreadsheet_data_dir, pheno_data_dir):
    """ sc_test_list_df = get_SC_phenotype_viability_df(spreadsheet_data_dir, pheno_data_dir) """
    sc_test_list_df = get_SC_test_files_list_df(spreadsheet_data_dir, pheno_data_dir)
    sc_test_list_df['spreadsheet_samples'] = 0
    sc_test_list_df['phenotype_samples'] = 0
    sc_test_list_df['samples_intersect'] = 0

    spreadsheet_full_file_x = ''
    phenotype_full_file_x = ''
    for row_index in list(sc_test_list_df.index):
        spreadsheet_full_file = os.path.join(spreadsheet_data_dir, sc_test_list_df['spreadsheet'].loc[row_index])
        phenotype_full_file = os.path.join(pheno_data_dir, sc_test_list_df['phenotype'].loc[row_index])
        if spreadsheet_full_file != spreadsheet_full_file_x:
            spreadsheet_full_file_x = spreadsheet_full_file
            spreadsheet_df = pd.read_csv(spreadsheet_full_file, sep='\t')

        if phenotype_full_file != phenotype_full_file_x:
            phenotype_full_file_x = phenotype_full_file
            phenotype_df = pd.read_csv(phenotype_full_file,sep='\t')

        sc_test_list_df['spreadsheet_samples'].loc[row_index] = spreadsheet_df.shape[1]
        sc_test_list_df['phenotype_samples'].loc[row_index] = phenotype_df.shape[1]
        samples_intersection = list(set(list(spreadsheet_df.columns)) and set(list(phenotype_df.index)) )
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
