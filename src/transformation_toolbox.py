"""
lanier4@illinois.edu
(samples x phenotypes) spreadsheet transformations
"""
import pandas as pd
import knpackage.toolbox as kn

# utility
def read_a_list_file(input_file_name):
    with open(input_file_name, 'r') as fh:
        str_input = fh.read()
    return list(str_input.split())


# transform_0
def transpose_df(spreadsheet_df):
    """ Transpose a spreadsheet data frame.
    Args:       
        spreadsheet_df: a pandas dataframe
    Returns:    
        spreadsheet_transpose_df: transposed dataframe
    """
    return spreadsheet_df.transpose()


def read_transpose_write(run_parameters):
    """ Read, transpose a spreadsheet data frame, and write it to a new file.
    Args:
        run_parameters:     dict with the following keys:
            input_file_name:    full path name of the input file
            output_file_name:   full path name of the output file
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
def get_common_samples_df(sxp_1_df, sxp_2_df):
    """Turn two dataframes with sample names in common into one with only the common samples in each. 
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
    """ Read, turn two dataframes with sample names in common into one with only the common samples in each, and write them into new files.
    Args:
        run_parameters:     dict with the following keys:
            full_file_name_1:   full path name of first input file
            full_file_name_2:   full path name of second input file
            out_file_name_1:    output file name for full_file_name_1
            out_file_name_2:    output file name for full_file_name_2
    Returns:                
        STATUS:                 0 if successful
    """
    full_file_name_1 = run_parameters['full_file_name_1']
    full_file_name_2 = run_parameters['full_file_name_2']
    out_file_name_1 = run_parameters['out_file_name_1']
    out_file_name_2 = run_parameters['out_file_name_2']
    
    try:
        sxp_1_df = kn.get_spreadsheet_df(full_file_name_1)
        sxp_2_df = kn.get_spreadsheet_df(full_file_name_2)
        cs_df_1, cs_df_2 = get_common_samples_df(sxp_1_df, sxp_2_df)
        cs_df_1.to_csv(out_file_name_1, sep='\t', index=True, header=True)
        cs_df_2.to_csv(out_file_name_2, sep='\t', index=True, header=True)
        return 0
    except:
        pass
        return -1


# transform_2
def merge_df(spreadsheet_1_df, spreadsheet_2_df):
    """ Combine two spreadsheets into one with all samples and phenotypes. (NaN filled)
    Args:
        spreadsheet_1_df: samples x phenotypes dataframe
        spreadsheet_2_df: samples x phenotypes dataframe
    Returns:
        spreadsheet_union_df:         samples x phenotypes dataframe with combined samples and phenotypes
    """
    spreadsheet_X_df = pd.concat([spreadsheet_1_df, spreadsheet_2_df], axis=1)
        
    return spreadsheet_X_df

def read_merge_write(run_parameters):
    """Read, combine two spreadsheets into one with all samples and phenotypes(NaN filled), and write it into a new file. 
    Args:
        run_parameters:         dict with the following keys:
            full_file_name_1:   full path name of first input file
            full_file_name_2:   full path name of second input file
            out_file_name:      output file name for input_path1
    Returns:
        STATUS:                 0 if successful
    """
    input_path1 = run_parameters['full_file_name_1']
    input_path2 = run_parameters['full_file_name_2']
    output_path = run_parameters['out_file_name']
    
    try:
        spreadsheet_1_df = pd.read_csv(input_path1, sep='\t', index_col=0, header=0)
        spreadsheet_2_df = pd.read_csv(input_path2, sep='\t', index_col=0, header=0)
        spreadsheet_X_df = merge_df(spreadsheet_1_df,spreadsheet_2_df)

        spreadsheet_X_df.to_csv(output_path, sep='\t', index=True, header=True)
        
        return 0
    
    except:
        pass
        return -1
    
# transform_3
def select_genes_df(spreadsheet_df, gene_select_list):
    """Turn one spreadsheet into one with only those genes selected from an input list.  
    Args:
        spreadsheet_df:             genes x samples data frame
        gene_select_list:           list of some gene names in the spreadsheet
    Returns:
        spreadsheet_intersected_df: data frame with only the genes in the intersection of input gene names.
    """
    gene_names = kn.extract_spreadsheet_gene_names(spreadsheet_df)
    intersection_names = kn.find_common_node_names(gene_names, gene_select_list)
    return spreadsheet_df.loc[intersection_names]


def read_select_genes_write(run_parameters):
    """Read, turn one spreadsheet into one with only those genes selected from an input list, and write it to a new file. 
    Args:
        run_parameters:     dict with the following keys:
            full_file_name: full path name of input file
            gene_select_list:list of some gene names in the spreadsheet
            out_file_name:  full path name of output file
    Returns:
        STATUS:                 0 if successful
    """
    try:
        input_path = run_parameters['full_file_name']
        gene_select_list = read_a_list_file['gene_select_list']
        output_path = run_parameters['out_file_name']
        spreadsheet_df = pd.read_csv(input_path, sep='\t', index_col=0, header=0)
        spreadsheet_intersected_df = select_genes_df(spreadsheet_df, gene_select_list)
        spreadsheet_intersected_df.to_csv(output_path, sep='\t', index=True, header=True)
        return 0
    except:
        return -1
    
def read_cluster_averages_write(run_parameters):
    """Read, return a dataframe of averages for each catagory given a genes x samples dataframe and a samples classification dictionary, and write it into a new file. 
    Args:
        run_parameters:          dict with the following keys:
            full_file_name1:full path name of the first input file
            full_file_name2:full path name of the second input file
            out_file_name:  full path name of the output file
    Returns:
        STATUS:                 0 if successful
    """
    try:
        input_path1 = run_parameters['full_file_name1']
        input_path2 = run_parameters['full_file_name2']
        out_file_name = run_parameters['out_file_name']
        spreadsheet_df = pd.read_csv(input_path1, sep='\t', index_col=0, header=0)
        labels_df = pd.read_csv(input_path2, sep='\t', index_col=0, header=0)
        labels_dict = labels_df.to_dict()[1]
        cluster_numbers = list(np.unique(list(labels_dict.values())))
        labels = list(labels_dict.values())
        cluster_ave_df = pd.DataFrame({i: spreadsheet_df.iloc[:, labels == i].mean(axis=1) for i in cluster_numbers})
        cluster_ave_df.to_csv(output_path, sep='\t', index=True, header=True)
        return 0
    except:
        return -1