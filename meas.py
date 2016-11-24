from measerver import MeasServer
from logger import log

if __name__ == '__main__':
    port = 7080
    ip ='0.0.0.0'
    meas_server = MeasServer(ip,port)
    meas_server.run_for_ever()


