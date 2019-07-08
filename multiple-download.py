import requests
from bs4 import BeautifulSoup
import multiprocessing
from multiprocessing import Pool
import threading
import os,time
import asyncio
import aiohttp
import functools
import re

###########################################
# ProcessBar class
###########################################

class ProgressBar(object):
	def __init__(self,title,total,chunk_size=1024,unit='KB'):
		self.title=title
		self.total=total
		self.chunk_size=chunk_size
		self.unit=unit
		self.progress=0.0

	def __info(self):
		return "【%s】%s %.2f%s / %.2f%s" % (self.title,self.status,self.progress/self.chunk_size,self.unit,self.total/self.chunk_size,self.unit)

	def refresh(self,progress):
		self.progress += progress
		self.status="......"
		end_str='\r'
		if self.total>0 and self.progress>=self.total:
			end_str='\n'
			self.status='completed'
		print(self.__info(),end=end_str)


###########################################
# download using `multiprocessing`/`threading`+`requests`
###########################################

# do multiple downloads - multiprocessing
def do_multiple_download_multiprocessing(url_list,targetDir):
	cpu_cnt=multiprocessing.cpu_count()
	print("系统进程数: %s, Parent Pid: %s" % (cpu_cnt,os.getpid()))

	p = Pool(cpu_cnt)
	results=[]
	for i,url in enumerate(url_list):
		result=p.apply_async(do_download,args=(i,url,targetDir,False,),callback=print_return)
		results.append(result)
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	for result in results:
	 	print(os.getpid(),result.get())
	print('All subprocesses done.')

# callback
def print_return(result):
	print(os.getpid(),result)

# do multiple downloads - threading
def do_multiple_downloads_threads(url_list,targetDir):
	thread_list=[]
	for i,url in enumerate(url_list):
		thread=threading.Thread(target=do_download,args=(i,url,targetDir,True,))
		thread.start()
		thread_list.append(thread)
	print('Waiting for all threads done...')
	for thread in thread_list:
		thread.join()
	print('All threads done.')

# do download using `requests`
def do_download(i,url,targetDir,isPrint=False):
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
	}
	try:
		response=requests.get(url,headers=headers,stream=True,verify=False)
		response.raise_for_status()
	except Exception as e:
		print("Occur Exception:",e)
	else:
		content_length = int(response.headers.get('Content-Length',0))
		filename=str(i)+"."+url.split('/')[-1]
		print(response.status_code,response.reason,content_length,filename)
		progressBar=ProgressBar(filename, total=content_length,chunk_size=1024,unit="KB")
		with open(os.path.join(targetDir,filename),'wb') as fd:
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					fd.write(chunk)
					progressBar.refresh(len(chunk))
		if isPrint:
			print(os.getpid(),threading.current_thread().name,filename,"Done!")
		return '%s %s %s Done' % (os.getpid(),threading.current_thread().name,filename)


###########################################		
# download using `asyncio`+`aiohttp`
###########################################

# do multiple downloads - asyncio
async def do_multiple_downloads_async(url_list,targetDir):
	 async with aiohttp.ClientSession() as session:
	 	# tasks=[do_aiohttp_download(session,url,targetDir) for url in url_list]
	 	# await asyncio.gather(*tasks)
	 	
	 	tasks=[]
	 	for i,url in enumerate(url_list):
	 		task=asyncio.create_task(do_aiohttp_download(session,i,url,targetDir))
	 		# task.add_done_callback(print_async_return)
	 		task.add_done_callback(functools.partial(print_async_return2,i))
	 		tasks.append(task)
	 		await asyncio.gather(*tasks)

# do one download
async def do_async_download(i,url,targetDir):
	async with aiohttp.ClientSession() as session:
		return await do_aiohttp_download(session,i,url,targetDir)

# do download using `aiohttp`
async def do_aiohttp_download(session,i,url,targetDir):
	async with session.get(url) as response:
		content_length = int(response.headers.get('Content-Length',0))
		filename=str(i)+"."+url.split('/')[-1]
		print(response.status,response.reason,content_length,filename)
		progressBar=ProgressBar(filename, total=content_length,chunk_size=1024,unit="KB")
		with open(os.path.join(targetDir,filename),'wb') as fd:
			while True:
				chunk=await response.content.read(1024)
				if not chunk:
					break;
				fd.write(chunk)
				progressBar.refresh(len(chunk))
		await response.release()
	# print(filename,"Done!")
	return filename

# callback
def print_async_return(task):
	print(task.result(),"Done")

def print_async_return2(i,task):
	print(i,":",task.result(),"Done")


###########################################
# Prepare download urls
###########################################

def url_list_crawler():
	url="http://m.ngchina.com.cn/travel/photo_galleries/5793.html"
	response=requests.get(url)
	print(response.status_code,response.reason,response.encoding,response.apparent_encoding)
	response.encoding=response.apparent_encoding
	soup=BeautifulSoup(response.text,'html.parser')
	#results=soup.select('div#slideBox ul a img')
	#results=soup.find_all('img')
	results=soup.select("div.sub_center img[src^='http']")
	url_list=[ r["src"] for r in results]
	print("url_list:",len(url_list))
	print(url_list)
	return url_list

###########################################

# main
if __name__=='__main__':
	print('start')
	
	targetDir="/Users/cj/space/python/download"
	url="http://image.ngchina.com.cn/2019/0325/20190325110244384.jpg"
	url_list=url_list_crawler()

	start=time.time()

	#######################################
	# 1. download one file
	#######################################

	# 1.1 using `requests`
	# do_download("A",url,targetDir)
	# end = time.time()
	# print('Total cost %0.2f seconds.' %  (end-start))
	# start=end

	# 1.2 using `aiohttp`
	# loop=asyncio.get_event_loop()
	# loop.run_until_complete(do_async_download("A",url,targetDir))
	# loop.close()
	# end = time.time()
	# print('Total cost %0.2f seconds.' %  (end-start))
	# start=end

	#######################################
	# 2. download many files
	#######################################

	# # 2.1 using multiple processings
	# do_multiple_download_multiprocessing(url_list,targetDir)
	# end = time.time()
	# print('Total cost %0.2f seconds.' %  (end-start))
	# start=end

	# # 2.2 using multiple threads
	# do_multiple_downloads_threads(url_list,targetDir)
	# end = time.time()
	# print('Total cost %0.2f seconds.' %  (end-start))
	# start=end

	# # 2.3 using asyncio
	# loop=asyncio.get_event_loop()
	# loop.run_until_complete(do_multiple_downloads_async(url_list,targetDir))
	# loop.close()
	# end = time.time()
	# print('Total cost %0.2f seconds.' %  (end-start))
	# start=end
	
	print('end')

###########################################
