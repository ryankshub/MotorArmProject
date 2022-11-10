#! /usr/bin/env python3
"""
Create the utilities python package
"""

# Project imports

from utils.parser_fcns import create_simple_file, parse_mt_file, parse_simple_file
from utils.data_helpers import apply_filter, apply_zero_phase_filter,\
    build_training_set, extract_feat, get_prec_and_recall, shred_data 
from utils.nupoc_convert_fcns import parse_action_dict, parse_trimmed_file

def x_version():
    """
    Return current software version
    """
    return "v0.1"