"""
Mini spider
Author: lujiaying@baidu.com
Date: 2017/1/10
"""

__version__ = "1.0"

import sys
import argparse

if __name__ == "__main__":
    version_msg = "%%(prog)s %s" % (__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--conf", action="store", type=str, dest="conf_file", required=True, help="specific config file")
    parser.add_argument('-v', "--version", action="version", version=version_msg)

    options = parser.parse_args()
    """
    if len(sys.argv) != 3:
        parser.error("incorrect number of arguments")
    if not options.conf_file:
        parser.error("incorrect use of -c or --conf")
    """
