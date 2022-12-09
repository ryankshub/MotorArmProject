#! /usr/bin/env python3
"""
Create the utilities python package
"""

# Project imports

from utils.animation_fcns import animate_simple_pend
from utils.data_helper_fcns import apply_filter, apply_zero_phase_filter,\
    build_training_set, extract_feat, get_prec_and_recall, shred_data, read_imu 
from utils.nupoc_convert_fcns import make_simple_filename, parse_action_dict,\
    parse_mat_file, parse_trimmed_file
from utils.parser_fcns import create_simple_file, parse_mt_file, parse_simple_file

def x_version():
    """
    Return current software version
    """
    return "v0.3"