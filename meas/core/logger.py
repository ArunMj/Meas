import traceback
import sys

class LOG():
    def info(self,p,*args):
        sys.stdout.write(p + '\n')

    def debug(self,p,*args):
        sys.stdout.write(p + '\n')

    def warn(self,p,*args):
        sys.stdout.write(p + '\n')

    def error(self,p,*args):
        sys.stderr.write(p + '\n')
        traceback.print_exc()

log =  LOG()

__all__ = [log]