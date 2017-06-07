
# coding: utf-8

# # A module that contains all 6 notebook transformations. 
# * To import this module in other scripts, use: 
# ```python
# from notebook_transformations import *
# ```


import pandas as pd
import knpackage.toolbox as kn


# ## Transform_0:
# ### Transpose a spreansheet
# 


def transpose(spreadsheet_df):
    '''
    Args:
        spreadsheet_df: the input spreadsheet(panda data frame)
    Return: 
        the output data frame that has been transposed
    '''
    return spreadsheet_df.transpose()


# ## Transform_1:  
# ### Turn two samples-overlapping spreadsheets into two intersection-only spreadsheets.
# * Samples x Phenotypes (SxP) must have the same phenotypes.
# * They must have some sample names in common.


def get_common_samples_data_frames(sxp_1_df, sxp_2_df):
    """ 
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


# ## Transform_2: 
# ### Turn two spreadsheets into one union-samples, union-phenotypes spreadsheet.
# * Samples x Phenotypes input files must have the different phenotypes.


def merge_unique_phenotypes_for_all_samples(spreadsheet_1_df, spreadsheet_2_df):
    """ 
    Args:
        spreadsheet_1_df: samples x phenotypes dataframe
        spreadsheet_2_df: samples x phenotypes dataframe
    Returns:
        union_df:         samples x phenotypes dataframe with combined samples and phenotypes
    """
    spreadsheet_1_samples = kn.extract_spreadsheet_gene_names(spreadsheet_1_df)
    spreadsheet_2_samples = kn.extract_spreadsheet_gene_names(spreadsheet_2_df)
    
    all_samples_list = kn.find_unique_node_names(spreadsheet_1_samples, spreadsheet_2_samples)
    
    spreadsheet_1_phenotypes = list(spreadsheet_1_df.columns)
    spreadsheet_2_phenotypes = list(spreadsheet_2_df.columns)
    
    all_phenotypes_list = kn.find_unique_node_names(spreadsheet_1_phenotypes, spreadsheet_2_phenotypes)
    
    spreadsheet_X_df = pd.concat([spreadsheet_1_df, spreadsheet_2_df], axis=1)
        
    return spreadsheet_X_df


# ## Transform_3: 
# ### Turn two spreadsheets with gene transformation lists into union spreadsheet


def select_spreadsheet_genes(spreadsheet_df, gene_select_list):
    """  
    Args:
        spreadsheet_df:             genes x samples data frame
        gene_select_list:           list of some gene names in the spreadsheet
    Returns:
        spreadsheet_intersected_df: data frame with only the genes in the intersection of input gene names.
    """
    gene_names = kn.extract_spreadsheet_gene_names(spreadsheet_df)
    intersected_names = kn.find_common_node_names(gene_names, gene_select_list)
    return spreadsheet_df.loc[intersected_names]


# ## Transform_4:
# ### Return a dataframe of averages for each catagory given a genes x samples dataframe and a samples classification dictionary


def get_classification_averages_df(spreadsheet_df, labels_df):
    """
    Args:
        spreadsheet_df: genes x samples dataframe
        labels_df:      samples x catagories dataframe
    Returns:
        cluster_ave_df: genes x catagories dataframe where data is catagory row average
    """
    labels_dict = labels_df.to_dict()[1]
    cluster_numbers = list(np.unique(list(labels_dict.values())))
    labels = list(labels_dict.values())
    cluster_ave_df = pd.DataFrame({i: spreadsheet_df.iloc[:, labels == i].mean(axis=1) for i in cluster_numbers})
    return cluster_ave_df


# ## Transform_5:
# ### Select the samples in a phenotype category from a genes x samples spreadsheet and a phenotype


def get_catagory_dataframes(spreadsheet_df, phenotype_df, phenotype_id, select_category):
    """  """
    samples_list = phenotype_df.index[phenotype_df[phenotype_id] == select_category]
    phenotype_category_df = phenotype_df.loc[samples_list]
    
    spreadsheet_category_df = spreadsheet_df[samples_list]
    
    return spreadsheet_category_df, phenotype_category_df

