# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, json, logging, os, pprint
import apache_log_parser


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )


class Parser(object):

    def __init__(self):
        self.APACHE_LOG_FILEPATH = os.environ['APCH_PRSLG__LOG_PATH']
        self.APACHE_COMBINED_PATTERN = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
        self.APACHE_COMMON_PATTERN = '%h %l %u %t \"%r\" %>s %b'
        self.PROCESSED_JSON_FILEPATH = os.environ['APCH_PRSLG__PROCESSED_JSON_PATH']

    def gulp( self, APACHE_LOG_FILEPATH=None ):
        """ Opens log-file, creates list of dcts for entries containing 'easyarticle'
            Called by parse_log() """
        ( url_lst, extracted_lst, discounted_lst, filepath, line_parser ) = self.get_gulp_vars( APACHE_LOG_FILEPATH )
        with open( filepath, 'r' ) as f:
            lines = f.readlines()
            logging.debug( 'found `{}` lines'.format(len(lines)) )
        for (i, line) in enumerate( lines ):
            if i%10000 == 0:
                logging.debug( 'processed `{}` lines'.format(i) )
            self.process_line( line, line_parser, url_lst, extracted_lst, discounted_lst )
        output_dct = {
            'url_lst': url_lst, 'url_lst_count': len(url_lst), 'extracted_lst': extracted_lst, 'extracted_lst_count': len(extracted_lst), 'discounted_lst': discounted_lst, 'discounted_lst_count': len(discounted_lst) }
        return output_dct

    def get_gulp_vars( self, APACHE_LOG_FILEPATH=None, pattern=None ):
        """ Initializes vars.
            Called by gulp() """
        url_lst = []
        extracted_lst = []
        discounted_lst = []
        if APACHE_LOG_FILEPATH is None:
            APACHE_LOG_FILEPATH = self.APACHE_LOG_FILEPATH
        if pattern is None:
            pattern = self.APACHE_COMBINED_PATTERN
            # pattern = self.APACHE_COMMON_PATTERN
        line_parser=apache_log_parser.make_parser( pattern )
        logging.debug( 'path, ```{}```'.format(APACHE_LOG_FILEPATH) )
        return ( url_lst, extracted_lst, discounted_lst, APACHE_LOG_FILEPATH, line_parser )

    def process_line( self, line, line_parser, url_lst, extracted_lst, discounted_lst ):
        """ Process logic of line-check.
            Called by gulp() """
        if 'easyarticle' in line:
            # logging.debug( 'easyarticle string found; line, ```{}```'.format(line) )
            line_data=line_parser( line )
            logging.debug( 'line_data, ```{}```'.format(pprint.pformat(line_data)) )
            if 'easyarticle' in line_data.get('request_url_path', ''):
                if 'login' not in line_data.get('request_url_path', ''):
                    if len(line_data.get('request_url_query', '')) > 0:  # if there's a good path and querystring...
                        extracted_lst.append( line_data )  # grab it
                        if line_data['request_url_query'] not in url_lst:
                            url_lst.append( line_data['request_url_query'] )
                            if len( url_lst ) > 2:
                                raise Exception( 'done' )
            else:
                discounted_lst.append( line_data )  # otherwise save it for a cursory look
        return

    # end class Parser


def parse_log():
    """ Calls Parser(); saves list of openurls to json file.
        Called by __main__ to gather logs. """
    prsr = Parser()
    output_dct = prsr.gulp()
    # logging.debug( 'entries, ```{}```'.format(pprint.pformat(output_dct)) )
    logging.debug( 'entries, ```{}```'.format(pprint.pformat(output_dct['url_lst_count'])) )
    logging.debug( 'entries, ```{}```'.format(pprint.pformat(sorted(output_dct['url_lst']))) )
    with open( prsr.PROCESSED_JSON_FILEPATH, 'w' ) as f:
        timestamp_key = '{}'.format( unicode(datetime.datetime.now()) ).replace( ' ', '_' )
        jdct = {
            timestamp_key: { 'url_lst': sorted(output_dct['url_lst']), 'url_lst_count': len(output_dct['url_lst']) }
            }
        f.write( json.dumps(jdct, sort_keys=True, indent=2) )

    # end def parse_log()


class Merger( object ):

    def __init__( self ):
        self.full_lst = []
        self.extracts_paths_lst = json.loads( os.environ['APCH_PRSLG__EXTRACTS_DIRECTORY_LIST_JSON'] )
        self.output_path = os.environ['APCH_PRSLG__ALL_OPENURLS_JSONPATH']

    def merge_extracts( self ):
        """ Creates list of unique openurls from the different extract runs.
            Called by __main__ """
        for directory_path in self.extracts_paths_lst:
            file_lst_paths = self.grab_filepaths( directory_path )
            for filepath in file_lst_paths:
                logging.debug( 'processing file, ```{}```'.format(filepath) )
                with open( filepath, 'r' ) as f:
                    jdct = json.loads( f.read() )
                ( datestamp_key, data_dct_value ) = jdct.items()[0]
                for openurl in data_dct_value['url_lst']:
                    if openurl not in self.full_lst:
                        self.full_lst.append( openurl )
        self.save_full_list()

    def grab_filepaths( self, directory_path ):
        """ Returns a lst of filepaths from givin directory.
            Called by merge_extracts() """
        filenames = os.listdir( directory_path )
        filepaths = [ os.path.join(directory_path,filename) for filename in filenames ]
        logging.debug( 'filepaths, ```{}```'.format(pprint.pformat(filepaths)) )
        return filepaths

    def save_full_list( self ):
        """ Saves json file.
            Called by merge_extracts() """
        with open( self.output_path, 'w' ) as f:
            timestamp_key = '{}'.format( unicode(datetime.datetime.now()) ).replace( ' ', '_' )
            jdct = {
                timestamp_key: { 'url_lst': sorted(self.full_lst), 'url_lst_count': len(self.full_lst) }
                }
            f.write( json.dumps(jdct, sort_keys=True, indent=2) )

    # end class Merger


if __name__ == '__main__':
    parse_log()
    # mrgr = Merger()
    # mrgr.merge_extracts()
