#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import os

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = '%s/../log/salebot.log' % os.path.split(os.path.realpath(__file__))[0]
print('Saving logs into', log_file)

fh = RotatingFileHandler(log_file, maxBytes=50*1024*1024, backupCount=5)
fh.setFormatter(formatter)
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.WARNING)


def get_logger(logger_name):
    loger = logging.getLogger(logger_name)
    loger.addHandler(fh)
    loger.addHandler(ch)
    loger.setLevel(logging.INFO)
    return loger

if __name__ == "__main__":
    logger = get_logger('foo')
    logger.info('bar')
    logger.debug('what are you sayingggggggggg')
