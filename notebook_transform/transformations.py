
# coding: utf-8

# # A module that contains all 6 notebook transformations. 
# * To import this module in other scripts, use: 
# ```python
# from notebook_transformations import *
# ```


import pandas as pd
import knpackage.toolbox as kn
from tkinter import Button, Tk, constants, filedialog, END

    

# ## Transform_0:
# ### Transpose a spreadsheet
# 


def transpose(input_path,output_path):
    spreadsheet_df = pd.read_csv(input_path, sep='\t', index_col=0, header=0)
    spreadsheet_df_tranpose = spreadsheet_df.transpose()
    spreadsheet_df_tranpose.to_csv(output_path, sep='\t', index=True, header=True)


# ## Transform_1:  
# ### Turn two samples-overlapping spreadsheets into two intersection-only spreadsheets.
# * Samples x Phenotypes (SxP) must have the same phenotypes.
# * They must have some sample names in common.


def common_samples(input_path1, input_path2,output_path1,output_path2):
    sxp_1_df = pd.read_csv(input_path1, sep='\t', index_col=0, header=0)
    sxp_2_df = pd.read_csv(input_path2, sep='\t', index_col=0, header=0)
    sxp_1_gene_names = kn.extract_spreadsheet_gene_names(sxp_1_df)
    sxp_2_gene_names = kn.extract_spreadsheet_gene_names(sxp_2_df)
    common_samples_list = kn.find_common_node_names(sxp_1_gene_names, sxp_2_gene_names)
    sxp_1_trim_df,sxp_2_trim_df = sxp_1_df.loc[common_samples_list], sxp_2_df.loc[common_samples_list]
    sxp_1_trim_df.to_csv(output_path1, sep='\t', index=True, header=True)
    sxp_2_trim_df.to_csv(output_path2, sep='\t', index=True, header=True)

# ## Transform_2: 
# ### Turn two spreadsheets into one union-samples, union-phenotypes spreadsheet.
# * Samples x Phenotypes input files must have the different phenotypes.


def merge(input_path1, input_path2,output_path):
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


# ## Transform_3: 
# ### Turn two spreadsheets with gene transformation lists into union spreadsheet


def select_genes(input_path, gene_select_list,output_path):
    spreadsheet_df = pd.read_csv(input_path, sep='\t', index_col=0, header=0)
    gene_names = kn.extract_spreadsheet_gene_names(spreadsheet_df)
    intersected_names = kn.find_common_node_names(gene_names, gene_select_list)
    spreadsheet_df.loc[intersected_names].to_csv(output_path, sep='\t', index=True, header=True)


# ## Transform_4:
# ### Return a dataframe of averages for each catagory given a genes x samples dataframe and a samples classification dictionary


def cluster_averages(input_path1, input_path2,output_path):
    spreadsheet_df = pd.read_csv(input_path1, sep='\t', index_col=0, header=0)
    labels_df = pd.read_csv(input_path2, sep='\t', index_col=0, header=0)
    labels_dict = labels_df.to_dict()[1]
    cluster_numbers = list(np.unique(list(labels_dict.values())))
    labels = list(labels_dict.values())
    cluster_ave_df = pd.DataFrame({i: spreadsheet_df.iloc[:, labels == i].mean(axis=1) for i in cluster_numbers})
    cluster_ave_df.to_csv(output_path, sep='\t', index=True, header=True)


# ## Transform_5:
# ### Select the samples in a phenotype category from a genes x samples spreadsheet and a phenotype


def select_categorical(input_path1, input_path2, phenotype_id, select_category,output_path1,output_path2):
    """  """
    spreadsheet_df = pd.read_csv(input_path1, sep='\t', index_col=0, header=0)
    phenotype_df = pd.read_csv(input_path2, sep='\t', index_col=0, header=0)
    
    samples_list = phenotype_df.index[phenotype_df[phenotype_id] == select_category]
    phenotype_category_df = phenotype_df.loc[samples_list]
    
    spreadsheet_category_df = spreadsheet_df[samples_list]
    
    spreadsheet_category_df.to_csv(output_path1, sep='\t', index=True, header=True)
    phenotype_category_df.to_csv(output_path2, sep='\t', index=True, header=True)


# a function to choose which specific transforamtion function to use
def read_transform_write_df(*args,**kwargs):
    '''
    Args:
        args: generally are the input full path(s) and output full path(s)
        kwargs: will have one item that represents the transformation number(0-5)
    '''
    func_dict = {0:transpose,1:common_samples,2:merge,3:select_genes,4:cluster_averages,5:select_categorical}
    func_dict[kwargs['num']](*args)


# GUI for the user to push a button to read, transform and write the dataframe(s)

def gui(*args,**kwargs):
    '''
    Args:
        args: generally are the input full path(s) and output full path(s)
        kwargs: will have one item that represents the transformation number(0-5)
    '''
    root = Tk()
    root.minsize(width=400, height=247)
    root.lift()
    root.attributes('-topmost', True)
    root.wm_title("Trasform")
    
    # init_frame(root)
    Button(root,text="Transform", command = lambda: read_transform_write_df(*args,**kwargs), font=("Helvetica", 21)).pack()
    root.mainloop()
