# -*- coding: utf-8 -*-
from config import *
from datetime import datetime
import MySQLdb.cursors
import os,time
import ThreadPool
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from notify import sendCompletedEmail,sendCustomEmail
from apns import APNs, Payload
from misc import *
import json
from main import *


if __name__=="__main__":
    path=os.path.join(os.path.realpath(os.path.dirname(__file__)),"command")
    content="";
    with open(path, 'r') as content_file:
        content = content_file.read()
    try:
        command=json.loads(content)
    except Exception,e:
        logger.exception(str(e))
        command={"devicetype":"iphone","environment":"","start":0}
    
    start=0
    if (command.has_key("start")):
        start=command['start']
    try:
        f = open(PROGRESS_LOG, 'w')
        command=json.loads(PROGRESS_LOG)
    except Exception,e:
        logger.exception(str(e))
    
    devtype=command['devicetype']
    test=command['environment']
    if test=="1":
        test=True
    else:
        test=False

    threadpool = ThreadPool.ThreadPool(100)
    message=""
    path=os.path.join(os.path.realpath(os.path.dirname(__file__)),"notification.msg")
    with open(path,"r") as f:
        message=f.read()
    logger.info("Notification start message :"+message)

    devices=getdevicetokens(devtype,test,start)
    #create_notification_batch(devices,message,devtype)
    
    threadpool.wait_completion()
    logger.info("Notification End message :"+message)
    sendCompletedEmail()
    #os.system("sudo init 0")