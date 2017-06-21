"""
lanier4@illinois.edu
"""
import os
import sys
import yaml

def get_run_file_dictionary(full_path_file_name):
    """ get a python dictionary from a yaml file
    Args:
        full_path_file_name: valid file name
    Returns:
        run_parameters:      python dictionary structure (may not preserve order)
    """
    run_parameters = {}
    try:
        if os.path.isfile(full_path_file_name):
            with open(full_path_file_name, 'r') as file_handle:
                run_parameters = yaml.load(file_handle)
    except:
        pass

    return run_parameters

def run_parameters_to_yaml(run_parameters, yaml_file_name):
    """ write a python dictionary to a yaml file
    Args:
        run_parameters: python dictionary struct (order may not be preserved)
        yaml_file_name: valid (path ) file name (will be overwritten if exists)
    Returns:
        STATUS:         0 if successful, -1 if not
    """
    STATUS = -1
    try:
        with open(yaml_file_name, 'w', encoding="utf-8") as yaml_file_handle:
            yaml_file_handle.write(yaml.dump(run_parameters))

        STATUS = 0
    except:
        pass

    return STATUS