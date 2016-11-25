import argparse,sys



__version__ = '0.1b'
  

p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
p =argparse.ArgumentParser(prog='meas')
p.add_argument('-p','--port',dest='port',type=int,required=False,help='Port to listen')
p.add_argument('-s','--host',dest='host',type=str,required=False,help='host to bind')
p.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__, help='Show version and exit.')

# p.add_argument('-p','--port','-g',dest='port',type=int,required=False,help='Query string in Lucene syntax.')
# p.add_argument('-p','--port','-g',dest='port',type=int,required=False,help='Query string in Lucene syntax.')
# p.add_argument('-p','--port','-g',dest='port',type=int,required=False,help='Query string in Lucene syntax.')

opts = p.parse_args()  