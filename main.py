import os
import argparse
from category import *
from developer import *
from datetime import datetime

def _parse_args():
    parser = argparse.ArgumentParser(description="Output all related package names, given a developer or category")
    parser.add_argument('--dev', '-d', help="Google Play Store developer ID")
    parser.add_argument('--category', '-c', help="Enter the interested category name here")
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all logging messages')

    return parser.parse_args()

def _show_output(apk_list):
    for apk in apk_list:
        print(apk)

if __name__ == "__main__":
    args = _parse_args()
    output = set()

    if(args.verbose):
        logging.basicConfig(level=logging.INFO)
    else:
        logging.disable(logging.CRITICAL)

    if(args.dev):
        output.update(get_developer_related(args.dev))

    if(args.category):
        output.update(get_category_related(args.category))

    _show_output(output)

