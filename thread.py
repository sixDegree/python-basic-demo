import pymongo
import requests
import multiprocessing
import threading
import os, time, random
import re
from multiprocessing import Pool

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

def do_request(process,article):
	start = time.time()
	print('Run task %s [%s] %s' % (process, os.getpid(),article["title"]))
	response=requests.get('http://www.baidu.com')
	print(process,response.status_code,response.reason)
	time.sleep(random.random() * 3)
	end = time.time()
	print('Task %s [%s] :%s runs %0.2f seconds.' % (process,os.getpid(),article["title"], (end - start)))

def do_download(process,meterial,headers):
	print(process,os.getpid(),meterial["name"])
	try:
		filename=meterial["filename"]
		response=requests.get('http://class.121talk.cn/Public/Uploads/Materials/'+meterial['pdf']
			,headers=headers,stream=True)
		response.raise_for_status()
	except exceptions.Timeout as e:
		print("Download [%s] %s Timeout: %s" % (filename,url,e.message))
	except exceptions.HTTPError as e:
		print("Download [%s] %s HTTPError: %s" % (filename,url,e.message))
	else: 
		chunk_size = 1024 													# 单次请求最大值
		content_size = int(response.headers.get('Content-Length',0))		# 内容体总大小
		print(process,response.status_code,response.reason,content_size)
		progress = ProgressBar(filename, total=content_size,unit="KB", chunk_size=chunk_size, run_status="downloading", fin_status="download completed")
		# write
		with open(os.path.join("/Users/cj/space/python/download",filename),'wb') as fd:
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					fd.write(chunk);
					progress.refresh(count=len(chunk))
		print(process,os.getpid(),meterial["name"],"Done")
	# 	db["meterials"].update_one({"_id":meterial["_id"]},{"$set":{"status":"Done"}})
		return meterial["_id"]

def do_thread_download(process,meterial,headers):
	t=threading.Thread(target=do_download,args=(process,meterial,headers,))
	t.start()
	t.join()

def parse_to_valid_filename(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  			# '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  		# 替换为下划线
    return new_title

def update_status(result):
	print("callback:",result)
	db["meterials"].update_one({"_id":result},{"$set":{"status":"Done"}})

class ProgressBar(object):
	def __init__(self, title,total=100.0,unit='',chunk_size=1.0,run_status=None,fin_status=None, count=0.0, sep='/'):
		super(ProgressBar, self).__init__()
		self.info = "【%s】%s %.2f %s %s %.2f %s"
		self.title = title
		self.total = total
		self.count = count
		self.chunk_size = chunk_size
		self.status = run_status or ""
		self.fin_status = fin_status or " " * len(self.status)
		self.unit = unit
		self.seq = sep

	def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
		_info = self.info % (self.title, self.status,self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
		return _info

	def refresh(self, count=1, status=None):
		self.count += count
		# if status is not None:
		self.status = status or self.status
		end_str = "\r"
		if self.total>0 and self.count >= self.total:
			end_str = '\n'
			self.status = status or self.fin_status
		print(self.__get_info(), end=end_str)


if __name__=='__main__':
	start = time.time()
	print('CPU Count:',multiprocessing.cpu_count())
	print('Parent process %s.' % os.getpid())
	p = Pool(4)

	# test1
	# for i in range(5):
	#    p.apply_async(long_time_task, args=(i,))

	# test2
	client=pymongo.MongoClient("mongodb://cj:123456@localhost:27017/demo?authSource=admin")
	db=client["demo"]
	# i=0
	# for article in db["articles"].find():
	# 	p.apply_async(do_request,(i%5,article))
	# 	i=i+1

	# test3
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
		,'Cookie':'PHPSESSID=shddsu72m4fdde2qfpac9b91k2'	#'PHPSESSID=m742kdp8v445pt6ebm3r5r1lm0'
	}
	# response=requests.get('https://class.121talk.cn/business/Students/getMtsByMtCat/mt_cat/10245'
	# 	,headers=headers)
	# print(response)
	# for meterial in response.json():
	# 	filename=parse_to_valid_filename(meterial["mt_name"]+"."+meterial["pdf"].split('.')[-1])
	# 	print(filename)
	# 	if db["meterials"].find_one({"_id":meterial["id"]}):
	# 		continue
	# 	result=db["meterials"].insert_one({"_id":meterial["id"]
	# 		,"name":meterial["mt_name"],"pdf":meterial["pdf"],"filename":filename})
	# 	# print(result)

	# test4
	i=0
	results=[]
	for meterial in db["meterials"].find({'status':None}):
		#print(meterial)
		# result=do_download(i%5,meterial,headers)
		# db["meterials"].update_one({"_id":result},{"$set":{"status":"Done"}})
		result=p.apply_async(do_download,(i%5,meterial,headers,),callback=update_status)
		results.append(result)
		i=i+1

	# test5
	# i=0
	# for meterial in db["meterials"].find({'status':None}):
	# 	print(meterial)
	# 	p.apply_async(do_thread_download,(i%5,meterial,headers,))
	# 	i=i+1

	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	print('All subprocesses done.')

	# for result in results:
	# 	#meterial_id=result;
	# 	meterial_id=result.get()
	# 	print("meterial_id:",meterial_id)
	# 	if meterial_id:
	# 		db["meterials"].update_one({"_id":meterial_id},{"$set":{"status":"Done"}})

	end = time.time()
	print('Total cost %0.2f seconds.' %  (end-start)) #48.71



