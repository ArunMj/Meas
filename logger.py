import traceback
class LOG():
    def info(self,p,*args):
        print p
    def debug(self,p,*args):
        print p
    def warn(self,p,*args):
        print p
    def error(self,p,*args):
        print p
        traceback.print_exc()

log =  LOG()


__all__ = [log]