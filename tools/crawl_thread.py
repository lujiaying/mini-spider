import urllib2
import time

import url_table as url_table_lib

def crawler(cid):
    """
    Args:
        cid: int, crawler id
    Returns:
    """
    url_table = url_table_lib.get_url_table()
    while True:
        url_node = url_table.get()
        print("In crawler#%s, get %s" % (cid, url_node))
        print("Now url_table is %s" % (url_table))
        time.sleep(1)
        url_table.task_done()
