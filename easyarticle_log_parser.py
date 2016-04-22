# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import glob, logging, os, pprint
import apache_log_parser


class Parser(object):

    def __init__(self):
        self.LOG_FILE_PATH = os.environ['APCH_PRSLG__LOG_PATH']
        self.APACHE_COMBINED_PATTERN = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'

    def gulp( self, log_file_path=None, pattern=None ):
        """ import and parse log files """
        ( log_data_lst, log_file_path, pattern ) = self.get_gulp_vars( log_file_path, pattern )
        line_parser=apache_log_parser.make_parser( pattern )
        paths = glob.glob( log_file_path )
        pprint.pprint( 'paths, ```{}```'.format(pprint.pprint(paths)) )
        for file_name in paths:
            logging.info( "file_name: %s" % file_name )
            file = open( file_name, 'r' )
            lines = file.readlines()
            file.close()
            logging.info(" read %s lines" % len(lines))
            for line in lines:
                line_data=line_parser( line )
                log_data_lst.append( line_data )
        logging.info( "total number of events parsed: %s" % len(log_data_lst) )
        return log_data_lst

    def get_gulp_vars( self, log_file_path, pattern ):
        log_data_lst = []
        if log_file_path is None:
            log_file_path = self.LOG_FILE_PATH
        if pattern is None:
            pattern = self.APACHE_COMBINED_PATTERN
        return ( log_data_lst, log_file_path, pattern )
