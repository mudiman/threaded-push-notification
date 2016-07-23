# -*- coding: utf-8 -*-
from datetime import datetime
import MySQLdb.cursors
import os,time
import ThreadPool
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from apns import APNs, Payload
from misc import *
from main import send_notification


if __name__=="__main__":
    send_notification("3e1d3b78b5b815cf9e395d94306b8ad278de7550620f387f5e3fe4f6cc334d39",None,"Testing")
    #send_notification("9475b25b8aecf3a9b506563a746213c59df79775e5da5d41e69d5d10b108d445",None,"Testin")