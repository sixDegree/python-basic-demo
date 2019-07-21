from threading import Thread
import threading
import os,time,random

def task(name):
    print("%s do task %s start" % (threading.current_thread().name,name))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print("%s do task %s end (%.2f)" % (threading.current_thread().name,name,end-start))


class MyThread(Thread):
    def __init__(self,taskName):
        Thread.__init__(self)
        self.taskName=taskName

    def run(self):
        print("%s do task %s start" % (self.name,self.taskName)) # name属性中保存的是当前线程的名字
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print("%s do task %s end (%.2f)" % (self.name,self.taskName,end-start))


def thread_inst_test():
    t=Thread(target=task,args=('test',))
    t.start()

def thread_class_test():
    t=MyThread('test')
    t.start()


if __name__=='__main__':
    print("%s thread start" % threading.current_thread().name)
    
    # thread_inst_test()

    thread_class_test()
    
    print("%s thread end" % threading.current_thread().name)

