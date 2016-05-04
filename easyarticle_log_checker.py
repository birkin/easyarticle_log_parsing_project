# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, json, logging, os, pprint, random, time
import redis, requests, rq


log_output_path = unicode( os.environ['APCH_PRSLG__LOG_OUTPUT_PATH'] )
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S',
    filename=log_output_path
    )


queue_name = 'APACHE_PARSELOG_CHECKER_QUEUE'
q = rq.Queue( queue_name, connection=redis.Redis() )
r = redis.StrictRedis( host='localhost', port=6379, db=0 )


# class Checker(object):
#     """ Hits url and stores url and status-code. """



## runners ##

def run_enqueue_check_jobs():
    """ Enqueues jobs.
        Called manually. """
    URLS_JSON = unicode( os.environ['APCH_PRSLG__URLS_JSON_PATH'] )
    with open( URLS_JSON ) as f:
        dct = json.loads( f.read() )
    url_lst = dct['url_lst']
    extract_len = 3
    extract_lst = []
    i = len( url_lst )
    while i > 0:
        i -= 1
        if len(extract_lst) >= extract_len:
            break
        idx = random.randint( 0, len(url_lst)-1 )
        openurl = url_lst[idx]
        if openurl not in extract_lst:
            extract_lst.append( openurl )
        # print 'extract_lst now, ```{}```'.format( pprint.pformat(extract_lst) )
        q.enqueue_call(
          func='apache_log_parsing_project.easyarticle_log_checker.run_check',
          kwargs={ 'openurl': openurl },
          timeout=600 )
    print 'done'
    print 'final extract_lst, ```{}```'.format( pprint.pformat(extract_lst) )
    return

def run_check( openurl ):
    """ Runner for Checker.check_url()
        Called by queued job created by run_enqueue_check_jobs() """
    # chkr = Checker()
    # chkr.check_url( url )
    time.sleep( 2 )
    url_base = 'https://library.brown.edu/easyaccess/find/'
    url = '{base}?{ourl}'.format( base=url_base, ourl=openurl )
    r = requests.get( url )
    logging.info( 'status_code, `{code}`; url, ```{url}```'.format(code=r.status_code, url=url) )
    return
