
# coding: utf-8

# ### Run this notebook to confirm that changes to Gene Prioritization Pipeline code did not change the outupt.
# * after running notebook use  "File" > "Download as"  >  (html) to save test results.
# 
# ###### Be advised: running this notebook in the same directory at the same time as the script will eat the temporary directories and fail tests.
# * And display _**disparaging error messages**_ on the command line.

# In[ ]:

# <- must be == In [1]  only run this cell first (or) after restarting kernel
import os
import sys
import time

import pandas as pd
import knpackage.toolbox as kn

sys.path.insert(1, '../verification')
import verification_test as vt
run_dir = os.path.abspath('../')

t_start_test = time.time()
sum_of_all_differences = 0


# In[ ]:

#                           Set up variables
yaml_methods_dict = {v: k for k, v in (vt.GP_options).items()}
yaml_methods_dict_keys = list(yaml_methods_dict.keys())

vt.view_dictionary(yaml_methods_dict)

os.chdir(run_dir)
os.system("make env_setup")
verification_root = os.path.abspath('../data/verification')
resu_dir = os.path.abspath('run_dir/results')
print('\nStart Tests:\t',time.strftime("%a %b %d, %Y %H:%M (%S s)", time.localtime()))


# In[ ]:

#                          run_single_drug_pearson - test the directory setup first
dictionary_key = 'TEST_1_GP_single_drug_pearson'
veri_dir = os.path.join(verification_root, dictionary_key)
os.system("make clean_dir_recursively create_run_dir copy_run_files")

t0 = time.time()
make_run_string = 'make' + ' ' + yaml_methods_dict[dictionary_key]
os.system(make_run_string)

print('Gene Prioritization %s run in %0.2f seconds\n'%(dictionary_key, time.time() - t0))

dir_differ_dict = vt.verification_directory_compare(veri_dir, resu_dir)

for k in sorted(dir_differ_dict.keys()):
    print(k, '\t', dir_differ_dict[k], 'differences')
print('\n\n')


# ###### Optional run all small test methods and compare with BENCHMARK and TEST files.

# In[ ]:

#                           Run all tests: option
run_all_tests_Y_or_whatever = input('Continue with all tests? (only capital Y will run)')

if run_all_tests_Y_or_whatever == "Y":
    t_start_test = time.time()
    print('\nStart Tests:\t',time.strftime("%a %b %d, %Y %H:%M (%S s)", time.localtime()))

    for y in sorted(yaml_methods_dict.keys(),reverse=True):
        t0 = time.time()
        print('\n', y)
        os.system("make clean_dir_recursively create_run_dir copy_run_files")
        veri_dir = os.path.join(verification_root, y)
        make_run_string = 'make' + ' ' + yaml_methods_dict[y]
        os.system(make_run_string)
        dir_differ_dict = vt.verification_directory_compare(veri_dir, resu_dir)
        for k in sorted(dir_differ_dict.keys()):
            if dir_differ_dict[k] != 0:
                sum_of_all_differences += 1
                print(k, '\t', dir_differ_dict[k], 'differences')
        
        print(yaml_methods_dict[y],'\t', time.time()-t0, '\n')
        
    m, s = divmod(time.time() - t_start_test, 60)
    h, m = divmod(m, 60)
    print('Gene Prioritization All tests run time:\t%d:%02d:%02d'%(h, m, s))
    print('\nFinished Tests:\t',time.strftime("%a %b %d, %Y %H:%M (%S s)", time.localtime()))
    print('Total number of differences = ', sum_of_all_differences)


# In[ ]:



