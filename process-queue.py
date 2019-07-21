from multiprocessing import Process, Queue
from multiprocessing import Manager,Pool
import os, time, random

def produce_task(q):
    while True:
        if not q.full():
            t=random.random()
            q.put(t)
            print('produce:%.2f' % t)
            time.sleep(t)
        else:
            print('stop produce!')
            break

def consume_task(q):
    while True:
        if not q.empty():
            t=q.get()
            print('consume:%.2f' % t)
            time.sleep(t)
        else:
            print('stop consume!')
            break

def process_test():
    q=Queue(5)
    p_produce=Process(target=produce_task,args=(q,))
    p_consume=Process(target=consume_task,args=(q,))
    p_produce.start()
    p_consume.start()
    p_produce.join()
    p_consume.join()
    print("Done!")

def pool_test():
    q=Manager().Queue(5)
    p=Pool(2)
    p.apply_async(produce_task,(q,))
    p.apply_async(consume_task,(q,))
    p.close()
    p.join()
    print("Done!")

if __name__=='__main__':
    # process_test()
    pool_test()
   