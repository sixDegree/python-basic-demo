from threading import Thread
import threading
import os,time,random

# test1: 异步,多线程交错打印
# result sample:
# Thread-1 print 1
# Thread-2 print 1
# Thread-1 print 2
# Thread-1 print 3
# Thread-1 done!
# Thread-2 print 2
# Thread-2 print 3
# Thread-2 done!
def test_multi_tasks_async():
    def async_task():
        for i in range(1,4):
            print("%s print %d " % (threading.current_thread().name,i))
            time.sleep(random.random())
        print("%s done!" % threading.current_thread().name)

    t1=Thread(target=async_task)
    t2=Thread(target=async_task)
    t1.start()
    t2.start()

# test2: 同步,多线程顺序打印
# result sample:
# Thread-1 print 1
# Thread-1 print 2
# Thread-1 print 3
# Thread-1 done!
# Thread-2 print 1
# Thread-2 print 2
# Thread-2 print 3
# Thread-2 done!
def test_multi_tasks_sync():
    mutex=threading.Lock()

    def sync_task():
        if mutex.acquire():
            for i in range(1,4):
                print("%s print %d " % (threading.current_thread().name,i))
                time.sleep(random.random())
            print("%s done!" % threading.current_thread().name)
            mutex.release()

    t1=Thread(target=sync_task)
    t2=Thread(target=sync_task)
    t1.start()
    t2.start()


# test3: 操作共享资源，不加锁，结果不正确,shoud be 0
# result sample:
# Done Thread-1 do add,num = 208671
# Done Thread-2 do sub,num = -102681
def test_multi_tasks_global_val():
    num=0
    def add_task():
        global num
        for i in range(0,1000000):
            num+=1
        print("Done %s do add,num = %d " % (threading.current_thread().name,num))

    def sub_task():
        global num
        for i in range(0,1000000):
            num-=1
        print("Done %s do sub,num = %d " % (threading.current_thread().name,num))
       
    t1=Thread(target=add_task)
    t2=Thread(target=sub_task)
    t1.start()
    t2.start()

# test4: 操作共享资源，加锁，得正确结果,be 0
# result sample:
# Done Thread-2 do sub,num = -36334
# Done Thread-1 do add,num = 0
def test_multi_tasks_global_val_mutex():
    lock=threading.Lock()
    num=0
    def add_task():
        nonlocal num
        for i in range(0,1000000):
            lock.acquire()
            num+=1
            lock.release()
        print("Done %s do add,num = %d " % (threading.current_thread().name,num))

    def sub_task():
        nonlocal num
        for i in range(0,1000000):
            lock.acquire()
            num-=1
            lock.release()
        print("Done %s do sub,num = %d " % (threading.current_thread().name,num))
    
    t1=Thread(target=add_task)
    t2=Thread(target=sub_task)
    t1.start()
    t2.start()   

# test5: Queue
# result sample:
# Consumer [0] Begin
# Consumer [0] handle item: 5.77
# Consumer [1] Begin
# Consumer [2] Begin
# Waiting for all threads done...
# Consumer [2] handle item: 4.51
# Consumer [1] handle item: 3.87
# Consumer [0] handle item: 1.61
# Consumer [1] handle item: 6.42
# Consumer [2] handle item: 0.17
# Consumer [1] handle item: 9.36
# Consumer [0] handle item: 4.88
# Consumer [1] handle item: 8.63
# Consumer [1] handle item: 0.27
# Consumer [2] Done
# Consumer [0] Done
# Consumer [1] Done
# All threads done.

def test_thread_queue():
    import queue

    def queue_consumer(index,q):
        print("Consumer [%s] Begin" % index)
        while not q.empty():
            item = q.get()
            if not item:
                time.sleep(1)
                continue
            do_task(index,item)
        print('Consumer [%s] Done' % index)

    def do_task(index,item):
        print("Consumer [%s] handle item: %s" % (index,item))
        time.sleep(random.random())

    q=queue.Queue()
    [q.put("%.2f" % (random.random()*10)) for i in range(10)]

    t_list=[]
    for i in range(3):
        t=threading.Thread(target=queue_consumer,args=(i,q,))
        t.start()
        t_list.append(t)
    
    print('Waiting for all threads done...')
    for t in t_list:
        t.join()
    print('All threads done.')

# test6: ThreadLocal
# result sample:
# Done Thread-1 task: step=0
# Done Thread-5 task: step=40
# Done Thread-2 task: step=10
# Done Thread-3 task: step=20
# Done Thread-4 task: step=30

def test_thread_dict():
    thread_dict = {}

    def task(step):
        thread_dict[threading.current_thread()]=step
        do_task()

    def do_task():
        currentThread=threading.current_thread()
        step=thread_dict[currentThread]
        time.sleep(random.random())
        print("Done %s task: step=%s" % (currentThread.name,step))

    for i in range(5):
        t=Thread(target=task,args=(i*10,))
        t.start()


def test_thread_local():
    
    #thread_dict = {}
    thread_local = threading.local()
    
    def task(step):
        #thread_dict[threading.current_thread()]=step
        thread_local.step=step
        do_task()

    def do_task():
        currentThread=threading.current_thread()
        #step=thread_dict[currentThread]
        step=thread_local.step
        time.sleep(random.random())
        print("Done %s task: step=%s" % (currentThread.name,step))

    for i in range(5):
        t=Thread(target=task,args=(i*10,))
        t.start()


if __name__=='__main__':
    print('Start')
    
    # 1. 异步：多线程交错打印
    # test_multi_tasks_async()

    # 2. 同步：多线程顺序打印
    # test_multi_tasks_sync()

    # 3. 共享资源：多线程操作，最终结果不正确
    # test_multi_tasks_global_val()

    # 4. 共享资源：多线程操作，重要部分加锁，最终结果正确
    # test_multi_tasks_global_val_mutex()

    # 5. Queue
    # test_thread_queue()

    # 6. ThreadLocal
    # test_thread_dict()
    # test_thread_local()
   

