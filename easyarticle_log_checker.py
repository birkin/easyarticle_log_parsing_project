# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, json, logging, os, pprint
import redis, requests, rq


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )


queue_name = 'APACHE_PARSELOG_CHECKER_QUEUE'
q = rq.Queue( queue_name, connection=redis.Redis() )
r = redis.StrictRedis( host='localhost', port=6379, db=0 )


class Checker(object):
    """ Hits url and stores url and status-code. """



## runners ##

def run_enqueue_check_jobs():
    """ Enqueues jobs.
        Called manually. """
    URLS_JSON = unicode( os.environ['APCH_PRSLG__URLS_JSON_PATH'] )
    with open( URLS_JSON ) as f:
        dct = json.loads( f.read() )
    url_lst = dct['url_lst']
    extract_len = 5
    extract_lst = []
    for i in len(url_lst):
        if len(extract_lst) >= extract_len:
            break
        idx = random.randint( 0, len(url_lst)-1 )
        openurl = url_lst[idx]
        if openurl not in extract_lst:
            extract_lst.append( openurl )
        q.enqueue_call(
          func='apache_log_parsing_project.easyarticle_log_checker.run_check',
          kwargs={ 'openurl': openurl },
          timeout=600 )
    print 'done'
    return

def run_check( openurl=openurl ):
    """ Runner for Checker.check_url()
        Called by queued job created by run_enqueue_check_jobs() """
    # chkr = Checker()
    # chkr.check_url( url )
    print 'hi'
    return
