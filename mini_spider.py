"""
Mini spider
Author: lujiaying
Date: 2017/1/10
"""

__version__ = "1.0"

import sys
import argparse
import threading

from tools.logger import data_analysis_logger as logger
from tools import config_load as config_load_lib
from tools import seedfile_load as seedfile_load_lib
from tools import url_table as url_table_lib
from tools import crawl_thread as crawl_thread_lib

if __name__ == "__main__":
    # commad arg parse
    version_msg = "%%(prog)s %s" % (__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--conf", action="store", type=str, dest="conf_file", required=True, help="specific config file")
    parser.add_argument('-v', "--version", action="version", version=version_msg)
    options = parser.parse_args()

    # conf load
    config_loader = get_config_loader() 
    if 0 != config_loader.read(options.conf_file):
        logger.error("conf file [%s] not exist" % (options.conf_file))
        sys.exit(1)

    # seedfile load
    seedfile_path = config_loader.get('spider', 'url_list_file')
    seed_urls = []
    if 0 != seedfile_load_lib.load(seedfile_path, seed_urls):
        logger.error("seed file [%s] not exist" % (seedfile_path))
        sys.exit(1)
    logger.debug("seed url len = %s" % (len(seed_urls)))

    # Init url_table, webpage_buffer
    url_table = url_table_lib.get_url_table()
    webpage_buffer = url_table_lib.get_webpage_buffer()
    url_table.init(int(config_loader.get('spider', 'predict_url_to_crawl')), 
                   int(config_loader.get('spider', 'queue_max_size')))
    webpage_buffer.init(config_loader.get('spider', 'queue_max_size'))
    ## put seed url into url_table
    for url in seed_urls:
        url_node = url_table_lib.UrlNode(url)
        logger.debug("seed url: %s" % (url_node))
        url_table.put(url_node)
    logger.debug("url table len = %s, content: %s" % (len(url_table), url_table))

    # Start crawl threads
    for cid in range(int(config_loader.get('spider', 'thread_count'))):
        crawl_thread = threading.Thread(target=crawl_thread_lib.crawler, 
                                        args=(cid,))
        crawl_thread.daemon = True
        crawl_thread.start()

    url_table.join()
    logger.debug("Elegantly exit")
