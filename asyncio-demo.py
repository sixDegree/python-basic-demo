import asyncio
import time,random
import queue

async def do_async_task(index,item):
    print('[start]\t %s:\t %s' % (index,item))
    start=time.time()
    await asyncio.sleep(random.random())
    end=time.time()
    result ='[end]\t %s:\t %s (spent:%.2f)' % (index,item,(end-start))
    return result


# Waiting for all sub-proc done...
# [start]  1:  8.50
# [start]  3:  6.14
# [start]  7:  9.91
# [start]  0:  7.31
# [start]  4:  2.26
# [start]  8:  3.13
# [start]  5:  3.44
# [start]  6:  5.45
# [start]  9:  3.83
# [start]  2:  9.07
# get result: [end]    4:  2.26 (spent:0.54)
# get result: [end]    3:  6.14 (spent:0.35)
# get result: [end]    6:  5.45 (spent:0.75)
# get result: [end]    8:  3.13 (spent:0.03)
# get result: [end]    7:  9.91 (spent:0.31)
# get result: [end]    9:  3.83 (spent:0.61)
# get result: [end]    5:  3.44 (spent:0.48)
# get result: [end]    0:  7.31 (spent:0.39)
# get result: [end]    1:  8.50 (spent:0.69)
# get result: [end]    2:  9.07 (spent:0.18)
# All sub-procs done.
# <coroutine object do_async_task at 0x1108098c8>
# <coroutine object do_async_task at 0x110809848>
# <coroutine object do_async_task at 0x1108099c8>
# <coroutine object do_async_task at 0x110809a48>
# <coroutine object do_async_task at 0x110809ac8>
# <coroutine object do_async_task at 0x110809b48>
# <coroutine object do_async_task at 0x110809bc8>
# <coroutine object do_async_task at 0x110809c48>
# <coroutine object do_async_task at 0x110809cc8>
# <coroutine object do_async_task at 0x110809dc8>

def test_asyncio_coroutine():
    loop = asyncio.get_event_loop()
    
    task_list=[]
    for i in range(10):
        item="%.2f" % (random.random()*10)
        t=do_async_task(i,item)                 # t is coroutine
        task_list.append(t)
    
    print('Waiting for all sub-proc done...')
    
    # method1: use asyncio.wait
    done,pending=loop.run_until_complete(asyncio.wait(task_list))
    print(done,pending)
    for r in done:
        print("get result:",r.result())

    # method2: use asyncio.gather
    # results=loop.run_until_complete(asyncio.gather(*task_list))
    # print(results)
    # for r in result:
    #     print("get result:",r)

    loop.close()
    print('All sub-procs done.')
    
    for task in task_list:
        # task:
        # type: coroutine
        # sample: <coroutine object do_async_task at 0x10f24c8c8>
        print(task)
    
# Waiting for all sub-proc done...
# [start]  0:  6.28
# [start]  1:  6.02
# [start]  2:  5.86
# [start]  3:  1.32
# [start]  4:  8.29
# [start]  5:  6.30
# [start]  6:  2.07
# [start]  7:  3.41
# [start]  8:  8.47
# [start]  9:  3.76
# callback: [end]  4:  8.29 (spent:0.11)
# callback: [end]  0:  6.28 (spent:0.18)
# callback: [end]  3:  1.32 (spent:0.20)
# callback: [end]  6:  2.07 (spent:0.31)
# callback: [end]  1:  6.02 (spent:0.51)
# callback: [end]  9:  3.76 (spent:0.51)
# callback: [end]  7:  3.41 (spent:0.75)
# callback: [end]  8:  8.47 (spent:0.78)
# callback: [end]  5:  6.30 (spent:0.79)
# callback: [end]  2:  5.86 (spent:1.00)
# get result: [end]    5:  6.30 (spent:0.79)
# get result: [end]    2:  5.86 (spent:1.00)
# get result: [end]    8:  8.47 (spent:0.78)
# get result: [end]    6:  2.07 (spent:0.31)
# get result: [end]    3:  1.32 (spent:0.20)
# get result: [end]    0:  6.28 (spent:0.18)
# get result: [end]    9:  3.76 (spent:0.51)
# get result: [end]    7:  3.41 (spent:0.75)
# get result: [end]    4:  8.29 (spent:0.11)
# get result: [end]    1:  6.02 (spent:0.51)
# All sub-procs done.
# get task result: [end]   0:  6.28 (spent:0.18)
# get task result: [end]   1:  6.02 (spent:0.51)
# get task result: [end]   2:  5.86 (spent:1.00)
# get task result: [end]   3:  1.32 (spent:0.20)
# get task result: [end]   4:  8.29 (spent:0.11)
# get task result: [end]   5:  6.30 (spent:0.79)
# get task result: [end]   6:  2.07 (spent:0.31)
# get task result: [end]   7:  3.41 (spent:0.75)
# get task result: [end]   8:  8.47 (spent:0.78)
# get task result: [end]   9:  3.76 (spent:0.51)

def test_asyncio_future():
    
    def handle_result(future):
        print("callback:",future.result())

    loop = asyncio.get_event_loop()
    task_list=[]
    for i in range(10):
        item="%.2f" % (random.random()*10)
        t=do_async_task(i,item)                 # t is coroutine
        f=loop.create_task(t)                   # f is future
        f.add_done_callback(handle_result)
        task_list.append(f)
    
    print('Waiting for all sub-proc done...')
    
    # method1: use asyncio.wait
    done,pending=loop.run_until_complete(asyncio.wait(task_list))
    print(done,pending)
    for r in done:
        print("get result:",r.result())

    # method2: use asyncio.gather
    # results=loop.run_until_complete(asyncio.gather(*task_list))
    # print(results)
    # for r in result:
    #     print("get result:",r)


    for task in task_list: 
        # task:
        # type: _asyncio.Task,subtype of `Future`
        # sample: <Task finished 
        # coro=<do_async_task() done, defined at asyncio-demo.py:5> 
        # result='[end]\t 7:\t... (spent:0.36)'>
        print("get task result:",task.result())



# --- Test: asyncio queue ---
# Waiting for all sub-proc done...
# Consumer[1] Begin
# Consumer[0] Begin
# Consumer[2] Begin
# do task 0: Consumer[1] 5.87
# do task 1: Consumer[0] 7.46
# do task 2: Consumer[2] 7.20
# do task 1: Consumer[0] 7.46 (spent:0.05)
# do task 3: Consumer[0] 7.28
# do task 2: Consumer[2] 7.20 (spent:0.61)
# do task 4: Consumer[2] 7.07
# do task 0: Consumer[1] 5.87 (spent:0.72)
# do task 5: Consumer[1] 9.09
# do task 3: Consumer[0] 7.28 (spent:0.67)
# do task 6: Consumer[0] 9.65
# do task 4: Consumer[2] 7.07 (spent:0.33)
# do task 7: Consumer[2] 6.64
# do task 6: Consumer[0] 9.65 (spent:0.89)
# do task 8: Consumer[0] 3.21
# do task 7: Consumer[2] 6.64 (spent:0.74)
# do task 9: Consumer[2] 1.78
# do task 5: Consumer[1] 9.09 (spent:0.98)
# Consumer[1] Done
# do task 9: Consumer[2] 1.78 (spent:0.13)
# Consumer[2] Done
# do task 8: Consumer[0] 3.21 (spent:0.62)
# Consumer[0] Done
# All sub-procs done.
def test_asyncio_queue():

    async def do_async_task(index,item):
        print('do task %s: Consumer[%s] %s' % (item[0],index,item[1]))
        start=time.time()
        await asyncio.sleep(random.random())
        end=time.time()
        result ='do task %s: Consumer[%s] %s (spent:%.2f)' % (item[0],index,item[1],(end-start))
        return result

    def handle_result(future):
        print(future.result())

    async def async_queue_consumer(index,q):
        print("Consumer[%s] Begin" % index)
        while not q.empty():
            item = await q.get()
            if not item:
                await asyncio.sleep(1)
                continue
            task=asyncio.create_task(do_async_task(index,item))
            task.add_done_callback(handle_result)
            await asyncio.gather(task)
        print('Consumer[%s] Done' % index)

   
    print("--- Test: asyncio queue ---")
    q=asyncio.Queue()
    [q.put_nowait((i,"%.2f" % (random.random()*10))) for i in range(10)]
    
    tasks = [async_queue_consumer(i,q) for i in range(3)]
    loop = asyncio.get_event_loop()
    
    print('Waiting for all sub-proc done...')
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print('All sub-procs done.')
        
    
if __name__ =='__main__':
    # test_asyncio_coroutine()
    test_asyncio_future()
    # test_asyncio_queue()
