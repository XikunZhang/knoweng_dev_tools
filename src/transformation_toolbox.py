"""
lanier4@illinois.edu
(samples x phenotypes) spreadsheet transformations
"""
import pandas as pd
import knpackage.toolbox as kn

# transform_0
def transpose_df(spreadsheet_df):
    """ Transpose a spreadsheet data frame.
    Args:       
        spreadsheet_df: a pandas dataframe
    Returns:    
        spreadsheet_transpose_df
    """
    return spreadsheet_df.transpose()

def read_transpose_write(run_parameters):
    """ Read, transpose a spreadsheet data frame, and write it to a new file.
    Args:
        input_file_name:     valid full path file name
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



# transform_1
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

def read_get_common_samples_write(run_parameters):
    """ Two spreadsheets with sample names in common are written with only the common samples in each.
    Args:
        full_file_name_1:   full path name of first input file
        full_file_name_2:   full path name of second input file
        out_file_name_1:    output file name for full_file_name_1
        out_file_name_2:    output file name for full_file_name_2
    Returns:                
        STATUS = 0 if successful
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


# transform_2
def merge_df(spreadsheet_1_df, spreadsheet_2_df):
    """ 
    Args:
        spreadsheet_1_df: samples x phenotypes dataframe
        spreadsheet_2_df: samples x phenotypes dataframe
    Returns:
        spreadsheet_union_df:         samples x phenotypes dataframe with combined samples and phenotypes
    """
    spreadsheet_1_samples = kn.extract_spreadsheet_gene_names(spreadsheet_1_df)
    spreadsheet_2_samples = kn.extract_spreadsheet_gene_names(spreadsheet_2_df)
    
    #all_samples_list = kn.find_unique_node_names(spreadsheet_1_samples, spreadsheet_2_samples)
    
    spreadsheet_1_phenotypes = list(spreadsheet_1_df.columns)
    spreadsheet_2_phenotypes = list(spreadsheet_2_df.columns)
    
    #all_phenotypes_list = kn.find_unique_node_names(spreadsheet_1_phenotypes, spreadsheet_2_phenotypes)
    
    spreadsheet_X_df = pd.concat([spreadsheet_1_df, spreadsheet_2_df], axis=1)
        
    return spreadsheet_X_df

def read_merge_write(run_parameters):
    """Two spreadsheets are combined into one with all samples and phenotypes. (NaN filled)
    Args:
        input_path1: full path name of first input file
        input_path2: full path name of second input file
        output_path: output file name for input_path1
    Returns:
        STATUS = 0 if successful
    """
    input_path1 = run_parameters['input_path1']
    input_path2 = run_parameters['input_path2']
    output_path = run_parameters['output_path']
    
    try:
        spreadsheet_1_df = pd.read_csv(input_path1, sep='\t', index_col=0, header=0)
        spreadsheet_2_df = pd.read_csv(input_path2, sep='\t', index_col=0, header=0)
        spreadsheet_1_samples = kn.extract_spreadsheet_gene_names(spreadsheet_1_df)
        spreadsheet_2_samples = kn.extract_spreadsheet_gene_names(spreadsheet_2_df)

        #all_samples_list = kn.find_unique_node_names(spreadsheet_1_samples, spreadsheet_2_samples)

        spreadsheet_1_phenotypes = list(spreadsheet_1_df.columns)
        spreadsheet_2_phenotypes = list(spreadsheet_2_df.columns)

        #all_phenotypes_list = kn.find_unique_node_names(spreadsheet_1_phenotypes, spreadsheet_2_phenotypes)

        spreadsheet_X_df = pd.concat([spreadsheet_1_df, spreadsheet_2_df], axis=1)

        spreadsheet_X_df.to_csv(output_path, sep='\t', index=True, header=True)
        
        return 0
    
    except:
        pass
        return -1