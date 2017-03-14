
# coding: utf-8

# ### KnowEnG-Research/Data_Cleanup_Pipeline test all methods notebook (for script run on cloud)

# In[1]:

SHOW_COMMAND_LINE_OUTPUT = False

import os
import sys

sys.path.insert(1, '../../src/')
import data_cleanup_toolbox as dc

sys.path.insert(1, '../../keg_test_tools/src')
import dcp_test

import knpackage.toolbox as kn

output_data_dir = '../../keg_test_tools/test'


# In[2]:

#                   Data_Cleanup_Pipeline   Samples Clustering
yaml_dir = '../../../Data_Cleanup_Pipeline/data/run_files'
yaml_file = 'TEMPLATE_data_cleanup.yml'
run_parameters = kn.get_run_parameters(yaml_dir, yaml_file)   

run_parameters['pheno_data_dir'] = '../../keg_test_tools/data/samples_clustering/phenotypes_SC'
run_parameters['spreadsheet_data_dir'] = '../../keg_test_tools/data/samples_clustering/spreadsheets_SC'
run_parameters['pipeline_type'] = 'samples_clustering_pipeline'
run_parameters['run_directory'] = '../../../Data_Cleanup_Pipeline/src/'
run_parameters['results_directory'] = kn.create_dir(dir_path=output_data_dir, dir_name='samples_clustering')

run_parameters['SHOW_COMMAND_LINE_OUTPUT'] = SHOW_COMMAND_LINE_OUTPUT

if SHOW_COMMAND_LINE_OUTPUT:
    for p in list(run_parameters.keys()):
        print(p, ':\t\t', run_parameters[p])

test_result_df = dcp_test.test_data_cleanup(run_parameters)


# In[3]:

#                   Data_Cleanup_Pipeline   Gene_Prioritization pearson
yaml_dir = '../../../Data_Cleanup_Pipeline/data/run_files'
yaml_file = 'TEMPLATE_data_cleanup.yml'
run_parameters = kn.get_run_parameters(yaml_dir, yaml_file)   

run_parameters['pheno_data_dir'] = '../../keg_test_tools/data/gene_prioritization/phenotypes_pearson'
run_parameters['spreadsheet_data_dir'] = '../../keg_test_tools/data/gene_prioritization/spreadsheets_GP'
run_parameters['pipeline_type'] = 'gene_prioritization_pipeline'
run_parameters['correlation_measure'] = 'pearson'
run_parameters['run_directory'] = '../../../Data_Cleanup_Pipeline/src/'
run_parameters['results_directory'] = kn.create_dir(dir_path=output_data_dir, dir_name='gene_prioritaization_t_test')

run_parameters['SHOW_COMMAND_LINE_OUTPUT'] = SHOW_COMMAND_LINE_OUTPUT

if SHOW_COMMAND_LINE_OUTPUT:
    for p in list(run_parameters.keys()):
        print(p, ':\t\t', run_parameters[p])

test_result_df = dcp_test.test_data_cleanup(run_parameters)


# In[4]:

#                   Data_Cleanup_Pipeline   Gene_Prioritization t_test
yaml_dir = '../../../Data_Cleanup_Pipeline/data/run_files'
yaml_file = 'TEMPLATE_data_cleanup.yml'
run_parameters = kn.get_run_parameters(yaml_dir, yaml_file)   

run_parameters['pheno_data_dir'] = '../../keg_test_tools/data/gene_prioritization/phenotypes_t_test'
run_parameters['spreadsheet_data_dir'] = '../../keg_test_tools/data/gene_prioritization/spreadsheets_GP'
run_parameters['pipeline_type'] = 'gene_prioritization_pipeline'
run_parameters['correlation_measure'] = 't_test'
run_parameters['run_directory'] = '../../../Data_Cleanup_Pipeline/src/'
run_parameters['results_directory'] = kn.create_dir(dir_path=output_data_dir, dir_name='gene_prioritaization_pearson')

run_parameters['SHOW_COMMAND_LINE_OUTPUT'] = SHOW_COMMAND_LINE_OUTPUT

if SHOW_COMMAND_LINE_OUTPUT:
    for p in list(run_parameters.keys()):
        print(p, ':\t\t', run_parameters[p])

test_result_df = dcp_test.test_data_cleanup(run_parameters)


# In[5]:

#                   Data_Cleanup_Pipeline   GeneSet_Characterization
yaml_dir = '../../../Data_Cleanup_Pipeline/data/run_files'
yaml_file = 'TEMPLATE_data_cleanup.yml'
run_parameters = kn.get_run_parameters(yaml_dir, yaml_file)

run_parameters.pop('phenotype_full_path', None)
run_parameters['spreadsheet_data_dir'] = '../../keg_test_tools/data/geneset_characterization/spreadsheets_GSC'
run_parameters['pipeline_type'] = 'geneset_characterization_pipeline'
run_parameters['run_directory'] = '../../../Data_Cleanup_Pipeline/src/'
run_parameters['results_directory'] = kn.create_dir(dir_path=output_data_dir, dir_name='geneset_charictarization')

run_parameters['SHOW_COMMAND_LINE_OUTPUT'] = SHOW_COMMAND_LINE_OUTPUT

if SHOW_COMMAND_LINE_OUTPUT:
    for p in list(run_parameters.keys()):
        print(p, ':\t\t', run_parameters[p])

test_result_df = dcp_test.test_data_cleanup(run_parameters)


# In[ ]:




# In[ ]:



