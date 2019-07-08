import multiprocessing
from multiprocessing import Pool
import threading
import os,time
import queue
import asyncio


###########################################
# long time task
# blocking
# unblocking
###########################################

def do_task(index,item_name,item_time,isPrint=False):
	print('[start]\t %s:%s\t %s %s...%s' % (index, os.getpid(),threading.current_thread().name,item_name,item_time))
	start=time.time()
	time.sleep(item_time)
	end=time.time()
	result ='[end]\t %s:%s\t %s %s...%.2f' % (index, os.getpid(),threading.current_thread().name,item_name,(end-start))
	if isPrint:
		print(result)
	return result

def print_task_result(result):
	print(os.getpid(),threading.current_thread().name,result)

async def do_async_task(index,item_name,item_time,isPrint=False):
	print('[start]\t %s:%s\t %s...%s' % (index, os.getpid(),item_name,item_time))
	start=time.time()
	# time.sleep(item_time)
	await asyncio.sleep(item_time)
	end=time.time()
	result ='[end]\t %s:%s\t %s...%.2f' % (index, os.getpid(),item_name,(end-start))
	if isPrint:
		print(result)
	return result

def print_async_task_result(task):
	print(task.result())

###########################################
# 0. serial 串行
###########################################

def test_serial(items):
	print("--- Test: serial ---")
	for index,(item_name,item_time) in enumerate(items):
		#print(index,item_name,item_time)
		do_task(index,item_name,item_time,isPrint=True)
	print('All tasks done')

###########################################
# 1. multi-process
# sync
# async
###########################################

# 串行
def test_multi_process_sync(items):
	print("--- Test: multi_process_sync ---")
	cpu_cnt=multiprocessing.cpu_count()
	print("系统进程数: %s, Parent Pid: %s" % (cpu_cnt,os.getpid()))
	
	p = Pool(cpu_cnt)
	results=[]
	for i,(item_name,item_time) in enumerate(items):
		index= i%(cpu_cnt)
		result=p.apply(do_task,args=(index,item_name,item_time,))
		# results.append(result)
		print(result)
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	# print('Print results...')
	# for result in results:
	#  	print(result)
	print('All subprocesses done.')

# 并行
def test_multi_process_async(items):
	print("--- Test: multi_process_async ---")
	cpu_cnt=multiprocessing.cpu_count()
	print("系统进程数: %s, Parent Pid: %s" % (cpu_cnt,os.getpid()))
	
	handler=ResultHandler(items)

	p = Pool(cpu_cnt)
	results=[]
	for i,(item_name,item_time) in enumerate(items):
		index= i%(cpu_cnt)
		result=p.apply_async(do_task,args=(index,item_name,item_time,),callback=print_task_result)
		# result=p.apply_async(do_task,args=(index,item_name,item_time,),callback=handler.update_status)
		# result=p.apply_async(do_task,args=(index,item_name,item_time,))
		# results.append(result)
		print(result)
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	# print('Print results...')
	# for result in results:
	#  	print(result.get())
	print('All subprocesses done.')

class ResultHandler:
	def __init__(self,config=None):
		self.config=config
	def update_status(self,result):
		print("callback:",result)

###########################################
# 2. multi-thread
###########################################

def test_multi_thread(items):
	print("--- Test: multi_thread ---")
	thread_list=[]
	for i,(item_name,item_time) in enumerate(items):
		thread=threading.Thread(target=do_task,args=(i,item_name,item_time,True,))
		thread.start()
		thread_list.append(thread)
	print('Waiting for all threads done...')
	for thread in thread_list:
		thread.join()
	print('All threads done.')

###########################################
# 3. multi-thread queue
###########################################	

def test_multi_thread_queue(items):
	print("--- Test: thread queue ---")
	
	q=queue.Queue()
	[q.put(item) for item in items]

	thread_list=[]
	for index in range(3):
		thread=threading.Thread(target=queue_consumer,args=(index,q,))
		thread.start()
		thread_list.append(thread)
	
	print('Waiting for all threads done...')
	for thread in thread_list:
		thread.join()
	print('All threads done.')

def queue_consumer(index,q):
	print("Consumer [%s] Begin" % index)
	while not q.empty():
		item = q.get()
		if not item:
			time.sleep(1)
			continue
		do_task(index,item[0],item[1],isPrint=True)
	print('Consumer [%s] Done' % index)

###########################################	
# 4. asyncio
###########################################

def test_asyncio(items):
	print("--- Test: asyncio ---")
	loop = asyncio.get_event_loop()
	tasks=[]
	for i,(item_name,item_time) in enumerate(items):
		t=loop.create_task(do_async_task(i,item_name,item_time))
		t.add_done_callback(print_async_task_result)
		tasks.append(t)
		# tasks.append(do_async_task(i,item_name,item_time))
	print('Waiting for all sub-proc done...')
	# results=loop.run_until_complete(asyncio.wait(tasks))
	# print(type(results))
	# for r in results[0]:
	#	print(r.result())
	done,pending=loop.run_until_complete(asyncio.wait(tasks))
	# for r in done:
	# 	print(r.result())
	# for task in tasks:
	# 	print(task.result())
	loop.close()
	print('All sub-procs done.')

###########################################
# 5. asyncio queue
###########################################

def test_asyncio_queue(items):
	print("--- Test: asyncio queue ---")
	
	q=asyncio.Queue()
	[q.put_nowait(item) for item in items]
	tasks = [async_queue_consumer(index,q) for index in range(3)]
	loop = asyncio.get_event_loop()
	
	print('Waiting for all sub-proc done...')
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()
	print('All sub-procs done.')
	
async def async_queue_consumer(index,q):
	print("Consumer [%s] Begin" % index)
	while not q.empty():
		item = await q.get()
		if not item:
			await asyncio.sleep(1)
			continue
		task=asyncio.create_task(do_async_task(index,item[0],item[1]))
		task.add_done_callback(print_async_task_result)
		await asyncio.gather(task)
		# start=time.time()
		# print('[Start] %s ... %s' % (item[0],item[1]))
		# await asyncio.sleep(item[1])
		# q.task_done()
		# end=time.time()
		# print('End %s ... %.2f' % (item[0],(end-start)))
	print('Consumer [%s] Done' % index)


###########################################

# main
if __name__ == '__main__':
	print('start')
	start = time.time()
	
	items=[
		('task_1',1)
		,('task_2',2)
		,('task_3',3)
		,('task_4',1)
		,('task_5',2)
		,('task_6',3)
	]

	###########################################
	# 0. serial
	###########################################
	# test_serial(items)
	# end=time.time()
	# print('Runs %0.2f seconds.' % (end - start))
	# start=end

	###########################################
	# 1. multiple processings
	###########################################

	# 1.1 sync
	# test_multi_process_sync(items)
	# end=time.time()
	# print('Runs %0.2f seconds.' % (end - start))
	# start=end
	
	# 1.2 async
	# test_multi_process_async(items)
	# end=time.time()
	# print('Runs %0.2f seconds.' % (end - start))
	# start=end
	
	###########################################
	# 2. multiple threads
	###########################################

	# 2.1 multiple threads
	# test_multi_thread(items)
	# end=time.time()
	# print('Runs %0.2f seconds.' % (end - start))
	# start=end

	# 2.2 multiple theads + queue
	# test_multi_thread_queue(items)
	# end=time.time()
	# print('Runs %0.2f seconds.' % (end - start))
	# start=end

	###########################################
	# 3. asyncio
	###########################################

	# 3.1 asyncio
	# test_asyncio(items)
	# end=time.time()
	# print('Runs %0.2f seconds.' % (end - start))
	# start=end
	
	# 3.2 asyncio + queue
	# test_asyncio_queue(items)
	# end=time.time()
	# print('Runs %0.2f seconds.' % (end - start))
	# start=end
	
	print('end')

###########################################

	