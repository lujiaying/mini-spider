"""
Mini spider
Author: lujiaying
Date: 2017/1/10
"""

__version__ = "1.0"

import sys
import argparse

if __name__ == "__main__":
    # commad arg parse
    version_msg = "%%(prog)s %s" % (__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--conf", action="store", type=str, dest="conf_file", required=True, help="specific config file")
    parser.add_argument('-v', "--version", action="version", version=version_msg)
    options = parser.parse_args()

    # conf load
