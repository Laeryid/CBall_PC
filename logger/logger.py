import config
import io
from kivy.uix.relativelayout import RelativeLayout
from datetime import datetime
import inspect

log_file = config.log_file_adress
            
def ClearLog():
    file = io.open(log_file, 'w')
    file.close()

def InsertLog(log):
    if config.RELEASE_MOD == 'debug':
        logstr = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        logstr = logstr + ' in ' + mod.__name__
        logstr = logstr + ' func ' + frm[3]
        logstr = logstr + ': ' + str(log)
        logstr = logstr + '\n'
        file = io.open(log_file, 'a')
        file.write(logstr)
        file.close()

