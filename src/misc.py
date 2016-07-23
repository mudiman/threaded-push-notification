import logging
from logging import handlers
from logging.handlers import RotatingFileHandler
import os
import stat
import json
import sys
from config import *
from config import NOTIFICATION_LOG_PATH

class GiveWriteRotatingFileHandler(handlers.RotatingFileHandler):

    def doRollover(self):
        """
        Override base class method to make the new log file group writable.
        """
        # Rotate the file first.
        handlers.RotatingFileHandler.doRollover(self)

        # Add group write to the current permissions.
        currMode = os.stat(self.baseFilename).st_mode
        os.chmod(self.baseFilename, currMode | stat.S_IRWXO)
        
formatter = logging.Formatter('%(asctime)s %(levelname)-15s %(message)s')
logging.basicConfig()

logger = logging.getLogger("SERVICE")
logger.setLevel(logging.INFO)

path=os.path.join(os.path.abspath(os.path.dirname(__file__)), NOTIFICATION_LOG_PATH)
try:
    rfhandler = GiveWriteRotatingFileHandler(filename=path, mode='a', maxBytes=500000 , backupCount=100)
    rfhandler.setFormatter(formatter)
    rfhandler.setLevel(logging.NOTSET)
    logger.addHandler(rfhandler)
except Exception, e:
    print e