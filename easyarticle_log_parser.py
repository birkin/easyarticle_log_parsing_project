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
        ( url_lst, extracted_lst, discounted_lst, filepath, line_parser ) = self.get_gulp_vars( APACHE_LOG_FILE_PATH )
        with open( filepath, 'r' ) as f:
            lines = f.readlines()
            logging.debug( 'found `{}` lines'.format(len(lines)) )
        for (i, line) in enumerate( lines ):
            if i%1000 == 0:
                logging.debug( 'processed `{}` lines'.format(i) )
            self.process_line( line, line_parser, url_lst, extracted_lst, discounted_lst )
        output_dct = {
            'url_lst': url_lst, 'url_lst_count': len(url_lst), 'extracted_lst': extracted_lst, 'extracted_lst_count': len(extracted_lst), 'discounted_lst': discounted_lst, 'discounted_lst_count': len(discounted_lst) }
        return output_dct

    def get_gulp_vars( self, APACHE_LOG_FILE_PATH=None, pattern=None ):
        """ Initializes vars.
            Called by gulp() """
        url_lst = []
        extracted_lst = []
        discounted_lst = []
        if APACHE_LOG_FILE_PATH is None:
            APACHE_LOG_FILE_PATH = self.APACHE_LOG_FILE_PATH
        if pattern is None:
            pattern = self.APACHE_COMBINED_PATTERN
        line_parser=apache_log_parser.make_parser( pattern )
        logging.debug( 'path, ```{}```'.format(APACHE_LOG_FILE_PATH) )
        return ( url_lst, extracted_lst, discounted_lst, APACHE_LOG_FILE_PATH, line_parser )

    def process_line( self, line, line_parser, url_lst, extracted_lst, discounted_lst ):
        """ Process logic of line-check.
            Called by gulp() """
        if 'easyarticle' in line:
            line_data=line_parser( line )
            if 'easyarticle' in line_data.get('request_url_path', ''):
                if 'login' not in line_data.get('request_url_path', ''):
                    if len(line_data.get('request_url_query', '')) > 0:  # if there's a good path and querystring...
                        extracted_lst.append( line_data )  # grab it
                        if line_data['request_url_query'] not in url_lst:
                            url_lst.append( line_data['request_url_query'] )
            else:
                discounted_lst.append( line_data )  # otherwise save it for a cursory look
        return

    # end class Parser


def parse_log():
    """ Calls parser. """
    prsr = Parser()
    output_dct = prsr.gulp()
    # logging.debug( 'first entry, ```{}```'.format(pprint.pformat(extracted_lst[0])) )
    # logging.debug( 'entries, ```{}```'.format(pprint.pformat(output_dct)) )
    logging.debug( 'entries, ```{}```'.format(pprint.pformat(output_dct['url_lst_count'])) )
    logging.debug( 'entries, ```{}```'.format(pprint.pformat(output_dct['url_lst'])) )

    # end def parse_log()


if __name__ == '__main__':
    parse_log()
