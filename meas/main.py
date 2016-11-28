import argparse

from core.measerver import MeasServer
from core.logger import log
from core.utils import getconfdir,pathjoin
from core import alertmanager

__version__ = '0.1b'

conf_dir = getconfdir()
mail_conf_file = pathjoin(conf_dir,'mail.json')
alertmanager.parse_mail_conf(mail_conf_file)


# if __name__ == '__main__':

#     p =argparse.ArgumentParser(prog='meas')
#     p.add_argument('-p','--port',dest='port',type=int,required=False,help='Port to listen')
#     p.add_argument('-s','--host',dest='host',type=str,required=False,help='host to bind')
#     p.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__, help='Show version and exit.')

#     p.set_defaults(host='0.0.0.0',port=7080)
    
#     opt = p.parse_args()


    
#     try:
#         meas_server = MeasServer(opt.host,opt.port)
#         meas_server.run_for_ever()
#     except Exception as oops:
#         print oops.__class__.__name__,oops