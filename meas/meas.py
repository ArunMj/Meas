#!/usr/bin/env python


import argparse
import logging

from core.utils import getconfdir, pathjoin
from core.logger import LoggerFactory

__version__ = '0.1b'


if __name__ == '__main__':

    p = argparse.ArgumentParser(prog='meas')
    p.add_argument('-p', '--port', dest='port', type=int, required=False, help='Port to listen')
    p.add_argument('-s', '--host', dest='host', type=str, required=False, help='host to bind')
    p.add_argument('-v', '--version', action='version',
                   version='%(prog)s ' + __version__, help='Show version and exit.')
    p.add_argument('-l', '--log', dest='logfile', type=str, required=False, help='location of log file')
    p.add_argument('--debug', action='store_true', required=False, help='enable debug?')
    p.set_defaults(host='0.0.0.0', port=7080, logfile='measlog.log')

    opt = p.parse_args()

    LoggerFactory.init(opt.logfile, level=logging.DEBUG if opt.debug else logging.INFO)
    logger = LoggerFactory.get_logger()
    
    from core import alertmanager
    from core.measerver import MeasServer

    conf_dir = getconfdir()
    mail_conf_file = pathjoin(conf_dir, 'meas.json')
    alertmanager.parse_conf(mail_conf_file)

    try:
        meas_server = MeasServer(opt.host, opt.port)
        meas_server.run_for_ever()

    except Exception as oops:
        logger.excepttion("could not start meas server")
        # print oops.__class__.__name__,oops
