"""
lanier4@illinois.edu
(samples x phenotypes) spreadsheet transformations
"""
import pandas as pd
import knpackage.toolbox as kn


def transpose_df(spreadsheet_df):
    """ Transpose a spreadsheet data frame.
    Args:       spreadsheet_df a pandas dataframe
    Returns:    spreadheet_df transposed.
    """
    return spreadsheet_df.transpose()


def read_transpose_write(run_parameters):
    """ Read, ranspose a spreadsheet data frame, and write it to a new file.
    Args:
        full_file_name:     valid full path file name
        output_file_name:   valid full path file name
    Returns:
        STATUS:             0 if written successfully
    """
    input_file_name = run_parameters['input_file_name']
    output_file_name = run_parameters['output_file_name']
    try:
        spreadsheet_df = pd.read_csv(input_file_name, sep='\t', index_col=0, header=0)
        spreadsheet_T_df = transpose_df(spreadsheet_df)
        spreadsheet_T_df.to_csv(output_file_name, sep='\t', index=True, header=True)
        return 0
    except:
        pass
        return -1


def read_get_common_samples_write(run_parameters):
    """ Two spreadsheets with sample names in common are written with only the common samples in each.
    Args:
        full_file_name_1:   full path name of first input file
        full_file_name_2:   full path name of second input file
        out_file_name_1:    output file name for full_file_name_1
        out_file_name_2:    output file name for full_file_name_2
    Returns:                STATUS = 0 if successful
    """
    full_file_name_1 = run_parameters['full_file_name_1']
    full_file_name_2 = run_parameters['full_file_name_2']
    out_file_name_1 = run_parameters['out_file_name_1']
    out_file_name_2 = run_parameters['out_file_name_2']
    
    try:
        sxp_1_df = kn.get_spreadsheet_df(full_file_name_1)
        sxp_2_df = kn.get_spreadsheet_df(full_file_name_2)
        cs_df_1, cs_df_2 = get_common_samples_data_frames(sxp_1_df, sxp_2_df)
        cs_df_1.to_csv(out_file_name_1, sep='\t', index=True, header=True)
        cs_df_2.to_csv(out_file_name_2, sep='\t', index=True, header=True)
        return 0
    except:
        pass
        return -1

def get_common_samples_data_frames(sxp_1_df, sxp_2_df):
    """ Two dataframes with sample names in common are returned with only the common samples in each.
    Args:
        sxp_1_df:      samples x phenotypes dataframe (sxp_1_df = kn.get_spreadsheet_df(sxp_filename_1))
        sxp_2_df:      samples x phenotypes dataframe
    Returns:
        sxp_1_trim_df: samples x phenotypes with only sample names in both input dataframes
        sxp_2_trim_df: samples x phenotypes with only sample names in both input dataframes
    """
    sxp_1_gene_names = kn.extract_spreadsheet_gene_names(sxp_1_df)
    sxp_2_gene_names = kn.extract_spreadsheet_gene_names(sxp_2_df)
    common_samples_list = kn.find_common_node_names(sxp_1_gene_names, sxp_2_gene_names)

    return sxp_1_df.loc[common_samples_list], sxp_2_df.loc[common_samples_list]