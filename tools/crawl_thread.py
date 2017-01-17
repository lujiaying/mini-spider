import urllib2
import time

import url_table as url_table_lib
from logger import data_analysis_logger as logger

def crawler(cid):
    """
    Args:
        cid: int, crawler id
    """
    url_table = url_table_lib.get_url_table()
    while True:
        start_t = time.time()
        url_node = url_table.get()
        addinfourl = urllib2.urlopen(url_node.url)
        url_table.task_done()
        end_t = time.time()
        logger.info("Crawler #%s crawl %s done, cost %s ms" % (cid, 
                     url_node.url,
                     int(end_t*1000 - start_t*1000) ))

