
from meas.core.logger import set_logger
set_logger("test.log")
from meas.core.utils import getconfdir, pathjoin
from meas.core import alertmanager


conf_dir = getconfdir()
mail_conf_file = pathjoin(conf_dir, 'meas.json')
alertmanager.parse_conf(mail_conf_file)


alertmanager.send_mail_alert("subject", "body")
