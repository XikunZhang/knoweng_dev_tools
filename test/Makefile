SCRIPT = ../src/dcp_test.py
RUN_DIR = ./run_dir
RUN_FILES = ../data/run_files
RESULTS_DIR = $(RUN_DIR)/results
INPUT_DATA_DIR = ../data


RMR = rm -rf
MKDIR_P = mkdir -p

# ----------------------------------------------------------------
# Benchmarks setup Section                                       -
# ----------------------------------------------------------------
env_setup: create_run_dir copy_run_files

create_run_dir:
	$(MKDIR_P) $(RESULTS_DIR) 

copy_run_files:
	cp $(RUN_FILES)/*.yml $(RUN_DIR) 

clean_dir_recursively:
	$(RMR) $(RUN_DIR)

# ----------------------------------------------------------------
# Small Benchmarks RUN Section                                   -
# ----------------------------------------------------------------
run_gene_prioritization_pearson_cleanup_tests:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file BENCHMARK_1_G_P_pearson.yml

run_gene_prioritization_t_test_cleanup_tests:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file BENCHMARK_2_G_P_t_test.yml

run_samples_clustering_cleanup_tests:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file BENCHMARK_3_S_C.yml

