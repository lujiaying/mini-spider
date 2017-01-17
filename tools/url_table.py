import hashlib
import math
import array
import Queue
import sys
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

from logger import data_analysis_logger as logger

__all__ = ['get_url_table', 'get_webpage_buffer', 'UrlNode']

# --- Infrastructure --
def hash_f(x):
    h = hashlib.sha256(x)
    return int(h.hexdigest(), base=16)

class BloomFilter:
    """
    A naive Bloom Filter
    math proof from http://blog.csdn.net/houzuoxin/article/details/20907911

    Methods:
        add(item)
        contains(item) 
    """
    def __init__(self):
        self.inited = False

    def init(self, capacity, error_rate=0.001, hash_fun=hash_f):
        """
        Args:
            capacity: int, self._n
            error_rate: float, self,_p
            hash_fun: function
        """
        self.inited = True
        self._n = capacity
        self._p = error_rate
        self._m = int(math.ceil(-1 * self._n * math.log(self._p) / 
                                (math.log(2)**2)))
        self._k = int(math.ceil(math.log(2) * self._m / self._n))

        self._bitmap = array.array('b', [0]*self._m)
        self._hash_fun = hash_fun

        self.mutex = _threading.Lock()

    def add(self, item):
        """
        Add item into BloomFilter
        """
        if not self.inited:
            logger.error("BloomFilter instance should invoke init() first")
            sys.exit(-1)
        item = str(item)
        self.mutex.acquire()
        for _ in range(self._k):
            self._bitmap[self._hash_fun(item+str(_)) % self._m] = 1
        self.mutex.release()

    def contains(self, item):
        """
        Check if item is in BloomFilter

        Returns:
             ret: boolean
        """
        if not self.inited:
            logger.error("BloomFilter instance should invoke init() first")
            sys.exit(-1)
        item = str(item)
        self.mutex.acquire()
        for _ in range(self._k):
            if 0 == self._bitmap[self._hash_fun(item+str(_)) % self._m]:
                self.mutex.release()
                return False
        self.mutex.release()
        return True

    def __contains__(self, item):
        return self.contains(item)


class UrlNode:
    def __init__(self, raw_url):
        self._raw_url = raw_url
        self._url = raw_url
        self._father_url = ''
        self._depth = 0

    @property
    def raw_url(self):
        return self._raw_url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def father_url(self):
        return self._father_url

    @father_url.setter
    def father_url(self, father_url):
        self._father_url = father_url

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        self._depth = depth

    def __str__(self):
        return "UrlNode %s: url-%s, depth-%s, father_url-%s, raw_url-%s" % (
                id(self), self._url, self._depth, self._father_url, self._raw_url)


class UrlTable:
    def __init__(self):
        self._queue = None
        self._bloomfilter = BloomFilter()

    def init(self, capacity, queue_max_size):
        """
        Args:
            capacity: int, predict num of urls
            queue_max_size: int
        """
        self._bloomfilter.init(capacity)
        self._queue = Queue.Queue(queue_max_size)

    def put(self, url):
        """
        Put url into url table if url never been visited

        Args:
            url: instance of UrlNode
        """
        if url.url not in self._bloomfilter:
            self._bloomfilter.add(url)
            self._queue.put(url)

    def get(self):
        return self._queue.get()

    def task_done(self):
        self._queue.task_done()

    def join(self):
        self._queue.join()

    def __len__(self):
        return self._queue.qsize()

    def __str__(self):
        return "%s" % (self._queue.queue)


class WebpageBuffer:
    def __init__(self):
        self._queue = None

    def init(self, queue_max_size):
        """
        Args:
            queue_max_size: int
        """
        self._queue = Queue.Queue(queue_max_size)

    def put(self, web_object):
        """
        Args:
            web_object: instance of urllib2.addinfourl
        """
        self._queue.put(web_object)

    def get(self):
        return self._queue.get()

    def task_done(self):
        self._queue.task_done()

    def join(self):
        self._queue.join()

    def __len__(self):
        return self._queue.qsize()
        
    def __str__(self):
        return "%s" % (self._queue.queue)
# --- End Infrastructure --


# --- Sigleton ---
_url_table_ins = UrlTable()
_webpage_buffer_ins = WebpageBuffer()
# --- End Sigleton ---


# --- API ---
def get_url_table():
    return _url_table_ins

def get_webpage_buffer():
    return _webpage_buffer_ins
# --- End API ---
