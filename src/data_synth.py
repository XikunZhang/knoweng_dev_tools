import sys
import os
import time

import numpy as np
import pandas as pd
import scipy.linalg as LA
import scipy.sparse as spar
from scipy.sparse import csgraph
import yaml


def get_random_phenotype_data_for_samples(samples_list, n_cols):
    pheno_data_names = get_rand_unique_name_list(n_names=n_cols, name_length=7)
    pheno_data_df = pd.DataFrame(data=None, index=samples_list, columns=pheno_data_names)
    
    for col_name in pheno_data_names:
        col_values, col_type = get_random_col(col_size=5)
        pheno_data_df[col_name] = col_values
    return pheno_data_df


def get_random_col(col_size):
    rand_types = {'catagorical': get_rand_catagorical, 'boolean': get_rand_boolean,
                  'integer': get_rand_integer, 'positive': get_rand_positive,
                  'real':get_rand_real}
    rand_types_names = list(rand_types.keys())
    n_items = len(rand_types_names)
    col_type = rand_types_names[np.random.randint(n_items)]
    return list(rand_types[col_type](n_items)), col_type

def get_rand_catagorical(n_items):
    return get_rand_unique_name_list(n_items, (3 + np.random.randint(9)) )
def get_rand_boolean(n_items):
    return (np.random.random(n_items) > 0.5)
def get_rand_integer(n_items):
    return np.random.randint(0,5,n_items)
def get_rand_positive(n_items):
    return np.random.random(n_items) * 10**(np.round(np.random.randint(6)))
def get_rand_real(n_items):
    return np.random.randn(n_items) * 10**(np.round(np.random.randint(6)))


def get_rand_dataframe(n_rows, n_cols, row_name_chars=5, col_name_chars=8):
    """ get a radom names and numbers dataframe """
    return pd.DataFrame(np.random.random((n_rows, n_cols)),
                        index=get_rand_unique_name_list(n_rows, row_name_chars),
                        columns=get_rand_unique_name_list(n_cols, col_name_chars))

def get_nodes_from_spreadsheet(SSArr):
    """ get the .edge set from a spreadsheet """
    nw = np.int_(np.zeros((sum(sum(SSArr != 0)), 3)))
    nw_row = 0
    for col in range(0, SSArr.shape[1]-1):
        for row in range(col+1, SSArr.shape[0]):
            if SSArr[row, col] != 0:
                nw[nw_row, 0] = int(col)
                nw[nw_row, 1] = int(row)
                nw[nw_row, 2] = 1
                nw_row += 1
    return nw

def get_clustered_spreadsheet(n_clusters, cluster_width, nrows=12):
    """ synthetic spreadsheet data with n_clusters (2 : 7) of n_clusters * cluster_width samples 
    Args:
        n_clusters:       number of distinct clusters
        cluster_width:    how many columns for each cluster
        nrows:            how many rows in the output
        
    Returns:
        spreadsheet_mat: 
    """
    ncols = n_clusters * cluster_width

    SSArr = np.zeros((nrows, ncols))
    row_seg_len = int(nrows / n_clusters)

    row_0 = 0
    col_0 = 0
    row_fin = row_seg_len
    col_fin = cluster_width
    SSArr[row_0:row_fin, col_0:col_fin] += 1
    for k in range(0, n_clusters-1):
        row_0 = row_fin
        col_0 = col_fin
        row_fin = row_0 + row_seg_len
        col_fin = col_0 + cluster_width
        SSArr[row_0:row_fin, col_0:col_fin] += 1

    return SSArr

def node_set_to_adj_mat(node_set):
    """ create and adjacency matrix from a network of nodes with edges
    """
    nw_sz = max(max(node_set[:, 0]), max(node_set[:, 1])) + 1
    adj_mat = np.zeros((nw_sz, nw_sz))
    for nodie in node_set:
        adj_mat[nodie[0], nodie[1]] = nodie[2]
        adj_mat[nodie[1], nodie[0]] = nodie[2]

    return adj_mat

def adjacency_matrix_to_node_set(N):
    """ create a network of nodes with edges from an adjacency matrix
    """
    Ntru = LA.triu(N)
    l = []
    for row in range(0, N.shape[0]):
        for col in range(row, N.shape[0]):
            if Ntru[row, col] == 1:
                l.append([row, col, 1])

    return np.array(l)

def symmetric_random_adjacency_matrix(network_dim, pct_nodes=0.3):
    """ symmetric random adjacency matrix from random set of nodes
    Args:
        network_dim: number of rows and columns in the symmetric output matrix
        pct_nodes: number of connections (nodes) as a function of network size.
    Returns:
        network: a symmetric adjacency matrix (0 or 1 in network_dim x network_dim matrix)
    """
    n_nodes = np.int_(np.round(pct_nodes * network_dim**2))
    network = np.zeros((network_dim, network_dim))
    col_0 = np.random.randint(0, network_dim, n_nodes)
    col_1 = np.random.randint(0, network_dim, n_nodes)
    for node in range(0, n_nodes):
        if col_0[node] != col_1[node]:
            network[col_0[node], col_1[node]] = 1
    network = network + network.T
    network[network != 0] = 1

    return network

def get_random_clusters(ncols, number_of_clusters=3):
    """ get a random set of clusters and construct an encoding matrix from those

    Args:
        ncols: number of columns
        number_of_clusters: number of rows

    Returns:
        H: encoding of the cluster number array
        C: cluster number array
    """
    H0 = np.random.rand(number_of_clusters, ncols)
    C = np.argmax(H0, axis=0)
    H = np.zeros(H0.shape)
    for row in range(0, max(C)+1):
        rowdex = C == row
        H[row, rowdex] = 1

    return H, C

def ensembl_like_names(n_vectors, str_pfx='ONESN', start_v=1, str_len=15, inter_v=3):
    """ str_list = ensembl_like_names(n_vectors, str_pfx='ONESN', start_v=1, str_len=15, inter_v=3) """
    pad_size = str_len - len(str_pfx)
    format_string = '%s%0.'+'%dd'%pad_size
    out_str_list = list('0'*n_vectors)
    p = np.random.permutation(n_vectors)
    for n in range(0, len(out_str_list)):
        out_str_list[p[n]] = format_string%(str_pfx, start_v + n * inter_v)
    
    return out_str_list

def get_rand_unique_name_list(n_names, name_length):
    """ get a list of unique random names with same number of characters (dog-slow if n_names >100k)
    Args:
        n_names: number of unique names in the output
        name_length: number of characters in each name
    Returns:
        rand_uniq_name_list: list of names
    """
    name_length = min(name_length, 13)
    bas = 26
    rand_uniq_name_list = []
    p = np.int_(np.random.random(n_names) * bas**name_length)
    for nm in range(0, n_names):
        rand_uniq_name_list.append(get_character_seq(base_coef_arr(p[nm], bas, name_length) ))

    return rand_uniq_name_list

def get_character_seq(bas_arr, caps=True):
    """ get a random sequence of characters
    Args:
        bas_arr: array of numbers in range 0, 25
        caps:  use Capital letters ? True or False
    Returns:
        char_arr
    """
    if caps:
        alf = np.array(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    else:
        alf = np.array(list('abcdefghijklmnopqrstuvwxyz'))

    if bas_arr.size == 1:
        char_arr = alf[bas_arr]
    else:
        char_arr = ''
        for c in range(0, int(bas_arr.size)):
            char_arr = char_arr + alf[bas_arr[c]]

    return char_arr

def base_coef_arr(big_n, bas, arr_len):
    """ convert an integer to an array of position multipliers in input base
    Args:
        big_n: an integer
        bas: the base to convert it to
        arr_len: pad the output with zeros to make it this length
    Returns:
        base_coef_arr: array of integers input integer in new base
    """
    n = 1
    while big_n - bas ** n > bas:
        n += 1
    if big_n < bas ** n and n > 1:
        n = n - 1

    base_coef_arr = np.int_(np.zeros(arr_len))
    start_pos = arr_len - (n + 1)
    for nb in range(0, n):
        this_pwr = bas ** (n - nb)
        this_digit = int(np.floor(big_n / this_pwr))
        big_n = big_n - this_pwr * this_digit
        base_coef_arr[start_pos] = this_digit
        start_pos += 1

    base_coef_arr[start_pos] = int(big_n)
    
    return base_coef_arr

def append_dictionary_file(full_file, run_pars):
    """ Append or create a log file using yaml compatible format """
    writ_status = 'Unk'
    try:
        with open(full_file, 'a') as appendectomyfile:
            for p in sorted(run_pars.keys()):
                appendectomyfile.write('\n%s:\t\t%s\n'%(p, run_pars[p]))
        writ_status = 'OK'
    except:
        print('an err occurred while trying to append dictionary file')
    return writ_status
    

def get_test_paramters_dictionary():
    """ universal dctionary of run parameters """
    test_parameters = {
        'method': 'cc_net_cluster_nmf',
        'method_1': 'cluster_nmf',
        'method_2': 'cc_cluster_nmf',
        'method_3': 'net_cluster_nmf',
        'method_4': 'cc_net_cluster_nmf',
        'use_parallel_processing': "0",
        'gg_network_name_full_path': './run_dir/input_data/final_clean_4col.edge',
        'spreadsheet_name_full_path': './run_dir/input_data/final_clean_full_matrix.df',
        'results_directory': './run_dir/results',
        'tmp_directory': './run_dir/tmp',
        'number_of_clusters': '3',
        'display_clusters': "0",
        'nmf_conv_check_freq': "50",
        'nmf_max_iterations': "10000",
        'nmf_max_invariance': "200",
        'rwr_max_iterations': "100",
        'rwr_convergence_tolerence': "0.0001",
        'rwr_restart_probability': "0.7",
        'nmf_penalty_parameter': "1400",
        'rows_sampling_fraction': "0.8",
        'cols_sampling_fraction': "0.8",
        'number_of_bootstraps': "5"}
    return test_parameters