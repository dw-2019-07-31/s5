#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers

class logger:
  
        #しんぐるとん
    _instance = None
    def __new__(self, cls, name = __name__):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

            # stdout
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            # fileout
            handler = logging.handlers.RotatingFileHandler(filename = '.\log\log.log'
                                                          #,maxBytes = 1048576
                                                          #,backupCount = 3
                                                          , mode='w')
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            return cls._instance
        else:
            return cls._instance

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)
        
    def critical(self, msg):
        self.logger.critical(msg)