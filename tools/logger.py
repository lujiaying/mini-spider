'''
Easy and basic configure for print log
'''

__author__ = 'jiaying.lu'

import logging
from logging.handlers import RotatingFileHandler
import os

################################
# Conf to edit
################################
# control log print to screen
DebugConf = True
#DebugConf = False


################################
# Init Loggers
################################
data_analysis_logger = logging.getLogger('data_analysis')


################################
# Init Handlers
################################
formatter = logging.Formatter('[%(asctime)s][pid:%(process)s-tid:%(thread)s] %(module)s.%(funcName)s: %(levelname)s: %(message)s')

# StreamHandler for print log to console
hdr = logging.StreamHandler()
hdr.setFormatter(formatter)
hdr.setLevel(logging.DEBUG)

# RotatingFileHandler
## Set log dir
abs_path = os.path.dirname(os.path.abspath(__file__))
abs_father_path = os.path.dirname(abs_path)
log_dir_path = abs_father_path + '/log'
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

## Specific file handler
fhr_ana = RotatingFileHandler('%s/spider.log'%(log_dir_path), maxBytes=10*1024*1024, backupCount=3)
fhr_ana.setFormatter(formatter)
fhr_ana.setLevel(logging.DEBUG)


################################
# Add Handlers
################################
data_analysis_logger.addHandler(fhr_ana)
if DebugConf:
    data_analysis_logger.addHandler(hdr)
    data_analysis_logger.setLevel(logging.DEBUG) #lowest debug level for logger
else:
    data_analysis_logger.setLevel(logging.ERROR) #lowest debug level for logger


if __name__ == '__main__':
    '''
    Usage:
    from tools.log_tools import data_process_logger as logger
    logger.debug('debug debug')
    '''
    data_analysis_logger.debug('My logger configure success')
    data_analysis_logger.info('My logger configure success')
    data_analysis_logger.error('analysis error test')
