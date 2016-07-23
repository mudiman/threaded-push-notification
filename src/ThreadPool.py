from threading import Thread
import time
import Queue
import config
from datetime import datetime
from misc import logger
from notify import sendEmail




class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, func, args, kargs):
        Thread.__init__(self)
        self.tasks = (func, args, kargs)
        #self.daemon = True
        self.running = "NOT STARTED"


    def run(self):
        self.running = "RUNNING"
        try:
            func, args, kargs = self.tasks
            callback = kargs.get('callback')
            temp = 0
            if callback:
                temp = func(*args, **kargs)
            else:
                func(*args, **kargs)
        except Exception, e:
            self.running = "FAILED"
            
            print e
        finally:
            if self.running != "FAILED":
                self.running = "DONE"
            if callback:
                callback(temp)


        
class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.threadlist = []
        self.threads_running()
        

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        thr = Worker(func, args, kargs)
        self.threadlist.append(thr)

            
        
    def threads_running(self):
        count = 0
        self.notstartedcount = 0
        self.donecount = 0
        notrunningthread = []
        for thr in self.threadlist:
            if thr.running == "RUNNING":
                count += 1
            if thr.running == "DONE" or thr.running == "FAILED":
                self.donecount += 1 
            if thr.running == "NOT STARTED" or thr.running == "FAILED":
                notrunningthread.append(thr)
                self.notstartedcount += 1
        left = self.num_threads - count
        if left > 0 and len(notrunningthread) > 0:
            limit = min(len(notrunningthread), left)
            for i in range(0, limit):
                try:
                    notrunningthread[i].start()
                    count += 1
                    self.notstartedcount -= 1
                except Exception:
                    pass
        return count
    
    def writeprogress(self):
        filename=config.PROGRESS_LOG#+str(datetime.now())
        with open(filename,'w') as f:
            f.write("%d,%d" % (config.TOTAL_COMPLETED+self.donecount,config.TOTAL_COMPLETED+(self.threads_running()+self.notstartedcount+self.donecount)))
        logger.info("%d,%d" % (config.TOTAL_COMPLETED+self.donecount,config.TOTAL_COMPLETED+(self.threads_running()+self.notstartedcount+self.donecount))+"  " + str(datetime.now()))

            
            
    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        i=0
        while True:
            if self.threads_running() == 0:
                self.writeprogress()
                sendEmail(self.donecount,self.notstartedcount+self.donecount)
                break
            #print "Threads running %d and not started threads %d and total threads completed %d" % (self.threads_running(), self.notstartedcount, self.donecount)
            self.writeprogress()
            time.sleep(3)
            i=i+3
            if i>=500:
                    sendEmail(self.donecount,self.notstartedcount+self.donecount)
                    i=0
        


if __name__ == '__main__':
    pass
