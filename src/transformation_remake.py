"""
lanier4@illinois.edu
(samples x phenotypes) spreadsheet transformations - "main" function
"""

def transpose(run_parameters):
    from transformation_toolbox import read_transpose_write
    read_transpose_write(run_parameters)

def get_common_samples(run_parameters):
    from transformation_toolbox import read_get_common_samples_write
    read_get_common_samples_write(run_parameters)

def merge(run_parameters):
    from transformation_toolbox import read_merge_write
    read_merge_write(run_parameters)
    
def select_genes(run_parameters):
    from transformation_toolbox import read_select_genes_write
    read_select_genes_write(run_parameters)
    
def cluster_averages(run_parameters):
    from transformation_toolbox import read_cluster_averages_write
    read_cluster_averages_write(run_parameters)

SELECT = {
            'transpose': transpose,
            'get_common_samples': get_common_samples,
            'merge': merge, 
            'select_genes': select_genes,
            'cluster_averages': cluster_averages}

def main():
    import sys
    from knpackage.toolbox import get_run_directory_and_file
    from knpackage.toolbox import get_run_parameters

    run_directory, run_file = get_run_directory_and_file(sys.argv)
    run_parameters = get_run_parameters(run_directory, run_file)
    SELECT[run_parameters["method"]](run_parameters)

if __name__ == "__main__":
    main()
