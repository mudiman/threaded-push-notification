import config
from datetime import datetime
import MySQLdb.cursors
import os,time
import ThreadPool
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from notify import sendCustomEmail
from apns import APNs, Payload
from misc import *
import json
from main import *

if __name__=="__main__":
    try:
        command=loadCommand()
        message=getPushMessage()
        check_job_status()
        print str(config.TOTAL_COMPLETED)+","+str(config.OLD_TOTAL)
        recursiverun_job_until_completed(command,message)
    except Exception,e:
        logger.exception(str(e))
    finally:
        recursiverun_job_until_completed(command,message)