# -*- coding: utf-8 -*-
import config
from datetime import datetime
import MySQLdb.cursors
import os,time
import ThreadPool
import sys
import urllib2,urllib
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from notify import sendCustomEmail
from apns import APNs, Payload
from misc import *
import json




def getdevicetokens(message,devtype,test=False,threadpool=None,start=0):
    os.system(config.MY_SQL_RESET_COMMAND)
    mysql_connection = MySQLdb.connect(host=config.database['host'], user=config.database['username'],passwd=config.database['password'], db=config.database['database'], use_unicode=True, charset="utf8", init_command='SET NAMES UTF8')
    cursor = MySQLdb.cursors.DictCursor(mysql_connection)
    mainresult=()
    try:
        if test:
            if devtype=="iphone":
                query = """select count(*) as cnt from  test_device_info;"""
            else:
                query = """select count(*) as cnt from  test_device_info_ipad;"""
        else:
            query = """select count(*) as cnt from  %s_deviceinfo;""" % (devtype)
        cursor.execute(query)
        total=cursor.fetchone()
        #print "total rowssss  "+str(total['cnt'])+" start "+str(start);
        offset=100
        for i in range(start,int(total['cnt']),offset):
            #print "start "+str(i)+" offset "+str(offset)
            if mysql_connection.open==False:
                os.system(config.MY_SQL_RESET_COMMAND)
                mysql_connection = MySQLdb.connect(host=config.database['host'], user=config.database['username'],passwd=config.database['password'], db=config.database['database'], use_unicode=True, charset="utf8", init_command='SET NAMES UTF8')
            if test:
                if devtype=="iphone":
                    query = """select device_token from  test_device_info;"""
                else:
                    query = """select device_token from  test_device_info_ipad;"""
            else:
                query = """select device_token from  %s_deviceinfo limit %d,%d;""" % (devtype,i,offset)
            
            cursor.execute(query)
            results = cursor.fetchall()
            mainresult=mainresult+results
            create_notification_batch(results,message,devtype,test,threadpool)
        return
    except Exception,e:
        logger.exception(str(e))
    mysql_connection.close()
    
    return mainresult;


def create_notification_batch(results,message,devtype,test,threadpool):
    for result in results:
        try:
            threadpool.add_task(send_notification, token=result["device_token"],devtype=devtype,message=message,test=test)
            #threadpool.add_task(test_job, token=result["device_token"],devtype=devtype,message=message)
        except Exception,e:
            logger.exception(str(e))
        
def send_notification(token=None,devtype=None,message=None,test=False,throwexp=None):
    try:
        if test==False:
            ncert_file=config.PEM_FILE_PATH
        else:
            ncert_file=config.TEST_PEM_FILE_PATH
        apns = APNs(use_sandbox=False, cert_file=ncert_file, key_file='')
        # Send a notification
        payload = Payload(alert=message, sound="default", badge=1)
        apns.gateway_server.send_notification(token, payload)
        for (token_hex, fail_time) in apns.feedback_server.items():
            uninstalledDevice(token_hex, fail_time)
    except Exception,e:
        logger.exception(str(e))
        sendCustomEmail("Error sending push notification","Push notification detail deviceid:"+token+" device type:"+devtype+"  message:"+message)
        if throwexp:
            raise 
        

def uninstalledDevice(devicetoken,time):
    file = open(os.path.join(os.path.realpath(os.path.dirname(__file__)),"faileddevices/"+devicetoken), "w")
    file.write(time.strftime("%b %d %Y %H:%M:%S"))
    file.close()

def resetUninstallDevices():
    import os 
    folder = os.path.join(os.path.realpath(os.path.dirname(__file__)),"faileddevices")
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e
            
def updateUninstallDevices():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [ f for f in listdir(os.path.join(os.path.realpath(os.path.dirname(__file__)),"faileddevices")) if isfile(join(os.path.join(os.path.realpath(os.path.dirname(__file__)),"faileddevices"),f)) ]
    print onlyfiles
    return onlyfiles

def deleteDevicesFromDb(devtype,devices):
    mysql_connection = MySQLdb.connect(host=config.database['host'], user=config.database['username'],passwd=config.database['password'], db=config.database['database'], use_unicode=True, charset="utf8", init_command='SET NAMES UTF8')
    cursor = MySQLdb.cursors.DictCursor(mysql_connection)
    try:
        query = """delete from %s_deviceinfo where device_token in (%s);""" % (devtype,",".join(devices))
        print query
        #cursor.execute(query)
    except Exception,e:
        logger.exception(str(e))
    mysql_connection.close()
    
def test_job(token=None,devtype=None,message=None):
    try:
        time.sleep(60)
        f = open('testdump/'+token,'w')
        f.write(message)
        f.close()
    except Exception,e:
        logger.exception(str(e))

def test_pem_file():
    send_notification(config.TEST_DEVICE_ID,"iphone","Testing pem file",True)
    
def callbackfunc(*args,**kwargs):
    pass

def loadCommand():
    try:
        path=config.COMMAND_PATH
        content="";
        with open(path, 'r') as content_file:
            content = content_file.read()
        command=json.loads(content)
        if not command.has_key("start"):
            command['start']=0
#         devtype=command['devicetype']
#         test=command['environment']
        if command['environment']=="1":
            command['environment']=True
        else:
            command['environment']=False
            
    except Exception,e:
        logger.exception(str(e))
        command={"devicetype":"iphone","environment":"","start":0}
    finally:
        return command


        
def check_job_status():
    try:
        status=""
        with open(config.PROGRESS_LOG,"r") as f:
            status=f.read()
        temp=status.split(',')
        if len(temp)==2:
            if temp[0]==temp[1]:
                return "OK"
        
        config.TOTAL_COMPLETED=int(temp[0])
        config.OLD_TOTAL=int(temp[1])
        
        return temp[0]
    except Exception,e:
        logger.exception(str(e))


def getPushMessage():
    message=""
    path=os.path.join(os.path.realpath(os.path.dirname(__file__)),"notification.msg")
    with open(path,"r") as f:
        message=f.read()
    return message

def runjob(command,message):
    threadpool = ThreadPool.ThreadPool(config.THREAD_POOL_SIZE)
    devices=getdevicetokens(message,command['devicetype'],command['environment'],threadpool,command['start'])
    #create_notification_batch(devices,message,devtype)
    
    threadpool.wait_completion()

def reset_progress_file():
    with open(config.PROGRESS_LOG,"r+") as f:
        f.write("0,1000")
        
def recursiverun_job_until_completed(command,message):
    try:
        temp=check_job_status()
        if temp!="OK":
            logger.info("Running fallback")
            if temp=="":
                temp="0"
            command['start']=int(temp)
            runjob(command, message)
            recursiverun_job_until_completed(command,message)
        else:
            logger.info("Notification Ended with fallback message :"+message)
            sendCustomEmail("COMPLETED AFTER FALLBACK","DONE")
            shutdownSystem()
    except Exception,e:
        recursiverun_job_until_completed(command,message)


def shutdownSystem():
    #os.system("sudo init 0")
    #sys.exit()
    pass

def addPushNotificationHistory(message,devicetype,uninstallcount):
    try:
        tempmessage=urllib.quote_plus(message)
        url="""http://widget.company.com/companyapps/addPushNotification.php?message=%s&devicetype=%s&uninstall=%d""" % (tempmessage,devicetype,uninstallcount)
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        print res.read()
    except Exception,e:
        logger.exception(str(e))

    
if __name__=="__main__":
    try:
        test_pem_file()
        sendCustomEmail("","PEM file is valid continuing next step")
        reset_progress_file()
        resetUninstallDevices()
        
        command=loadCommand()
        message=getPushMessage()
        
        logger.info("Notification start message :"+message)
        runjob(command, message)
        logger.info("Notification End message :"+message)
        
        devices=updateUninstallDevices()
        deleteDevicesFromDb(command['devicetype'],devices)
        addPushNotificationHistory(message,command['devicetype'],len(devices))
        
        sendCustomEmail("","COMPLETED")
        shutdownSystem()
    except Exception,e:
        logger.exception(str(e))
    finally:
        pass
        #recursiverun_job_until_completed(command,message)
