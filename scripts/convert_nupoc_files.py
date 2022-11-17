#!/usr/bin/env python3
# Scripts to convert nupoc logfile/matfile into
# simple format for data processing

# Python imports
import argparse
import os
import sys

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import create_simple_file, make_simple_filename, parse_action_dict,\
    parse_mat_file, parse_trimmed_file

# 3rd-party Import

def convert_nupoc_file(file, action_dict, parser_args):
    # Get args from argparser
    waypoint_key = parser_args.waypoint_key
    sample_rate = parser_args.sample_rate
    target_dir = parser_args.target_dir

    filename = os.path.basename(file)
    fileext = os.path.splitext(filename)[1]
    if fileext == ".mat":
        activity, df = parse_mat_file(file, waypoint_key)
    else:
        activity, df = parse_trimmed_file(file, waypoint_key, action_dict)
    
    new_filename = make_simple_filename(activity, waypoint_key)
    new_filepath = os.path.join(target_dir, new_filename)

    create_simple_file(new_filepath, activity, sample_rate, df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Files from Nupoc\
        into simple format.")
    parser.add_argument("convert_target", type=str, help="File to be converted\
         or directory containing files to be converted")
    parser.add_argument("waypoint_key", type=str, help="Identify which waypoint\
         should be the focus of conversion")
    parser.add_argument("-a", "--action_path", type=str, help="filepath to action\
         key file which contains id-task key value pairs. The absence of this\
         will have the action assumed to be 'walking'")
    parser.add_argument("-s", "--sample_rate", type=float, default=120.0, help="\
         Sample rate of the logged data")
    parser.add_argument("-d", "--is_dir", action="store_true", help="Use to indicate\
         if convert target is a single file or directory")
    parser.add_argument("-x", "--target_dir", type=str, help="location to place\
         newly-converted files")

    args = parser.parse_args()

    if args.action_path:
        action_dict = parse_action_dict(args.action_path)
    else:
        action_dict = {}
    if args.is_dir:
        files = [f for f in os.listdir(args.convert_target) \
            if os.path.isfile(os.path.join(args.convert_target, f))]
        for file in files:
            convert_nupoc_file(os.path.join(args.convert_target,file), action_dict, args)
    else:
        convert_nupoc_file(args.convert_target, action_dict, args)
