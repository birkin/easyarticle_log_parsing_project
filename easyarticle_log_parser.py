# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import glob, logging, os
import apache_log_parser


LOG_FILE_PATH = os.environ['EASYART__APACHE_LOG_FILEPATH']
APACHE_COMBINED="%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""


def gulp(log_file_path=LOG_FILE_PATH, pattern=APACHE_COMBINED):
    """ import and parse log files """
    log_data=[]
    line_parser=apache_log_parser.make_parser(pattern)
    for file_name in glob.glob(log_file_path):
        logging.info("file_name: %s" % file_name)
        file = open(file_name, 'r')
        lines = file.readlines()
        file.close()
        logging.info(" read %s lines" % len(lines))
        for line in lines:
            line_data=line_parser(line)
            log_data.append(line_data)
    logging.info("total number of events parsed: %s" % len(log_data))
    return log_data
