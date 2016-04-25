# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import glob, logging, os, pprint
import apache_log_parser


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )


class Parser(object):

    def __init__(self):
        self.APACHE_LOG_FILE_PATH = os.environ['APCH_PRSLG__LOG_PATH']
        self.APACHE_COMBINED_PATTERN = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'

    def gulp( self, APACHE_LOG_FILE_PATH=None ):
        """ Opens log-file, creates list of dcts for entries containing 'easyarticle'
            Called by parse_log() """
        ( log_data_lst, filepath, line_parser ) = self.get_gulp_vars( APACHE_LOG_FILE_PATH )
        with open( filepath, 'r' ) as f:
            lines = f.readlines()
            logging.debug( 'found `{}` lines'.format(len(lines)) )
        for (i, line) in enumerate( lines ):
            if i%1000 == 0:
                logging.debug( 'processed `{}` lines'.format(i) )
            if 'easyarticle' in line:
                line_data=line_parser( line )
                log_data_lst.append( line_data )
        return log_data_lst

    def get_gulp_vars( self, APACHE_LOG_FILE_PATH=None, pattern=None ):
        """ Initializes vars.
            Called by gulp() """
        log_data_lst = []
        if APACHE_LOG_FILE_PATH is None:
            APACHE_LOG_FILE_PATH = self.APACHE_LOG_FILE_PATH
        if pattern is None:
            pattern = self.APACHE_COMBINED_PATTERN
        line_parser=apache_log_parser.make_parser( pattern )
        logging.debug( 'path, ```{}```'.format(APACHE_LOG_FILE_PATH) )
        return ( log_data_lst, APACHE_LOG_FILE_PATH, line_parser )

    # end class Parser


def parse_log():
    """ Calls parser. """
    prsr = Parser()
    log_data_lst = prsr.gulp()
    logging.debug( 'len, log_data_lst, `{}`'.format(len(log_data_lst)) )
    logging.debug( 'first entry, ```{}```'.format(pprint.pformat(log_data_lst[0])) )

    # end def parse_log()


if __name__ == '__main__':
    parse_log()
