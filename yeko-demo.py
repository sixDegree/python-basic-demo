import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os,time
import asyncio
import aiohttp
import functools
import re
import pymongo

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

	async def refresh(self,progress):
		self.progress += progress
		self.status="......"
		end_str='\r'
		if self.total>0 and self.progress>=self.total:
			end_str='\n'
			self.status='completed'
		print(self.__info(),end=end_str)


###########################################		
# download using `asyncio`+`aiohttp`
###########################################

# do multiple downloads - asyncio
async def do_multiple_downloads_async(url_list,targetDir,callback_func=print):
	 async with aiohttp.ClientSession() as session:
	 	# tasks=[do_aiohttp_download(session,url,targetDir) for url in url_list]
	 	# await asyncio.gather(*tasks)
	 	
	 	tasks=[]
	 	for i,url in enumerate(url_list):
	 		task=asyncio.create_task(do_aiohttp_download(session,i,url,targetDir))
	 		# task.add_done_callback(callback_func)
	 		task.add_done_callback(functools.partial(callback_func,i))
	 		tasks.append(task)
	 		await asyncio.gather(*tasks)

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


###########################################
# information crawler using `requests`
###########################################

def do_crawler(url,params=None,headers=None):
	try:
		response=requests.get(url,params=params,headers=headers)
		response.raise_for_status()
	except requests.Timeout as e:
		print("GET %s Timeout: %s" % (url,e))
	except requests.HTTPError as e:
		print("GET %s HTTPError: %s" % (url,e))
	except Exception as e:
		print("Get %s Exception:" % (url,e))
	else:
		print(response.status_code,response.reason)
	return response

###########################################
# parse record
###########################################

def do_record_parser(record,mode='All',mapping={},skip=[],addition={}):
	result={}
	if mode=='All':
		for k, v in mapping.items():		# {srcKey:destKey}
			result[v]=record[k]
	elif mode=='Mix':
		for k,v in record.items():
			if k in mapping:
				result[mapping[k]]=v
			else:
				result[k]=v	
	for s in skip:
		if s in result:
			result.pop(s)
	for k,v in addition.items():
		result[k]=v
	return result

###########################################
# parse to valid filename
###########################################

def parse_to_valid_filename(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  			# '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  		# 替换为下划线
    return new_title

###########################################
# persist to mongodb using `pymongo`
###########################################

def get_connected_db(conn_str,db_name):
	client=pymongo.MongoClient(mongoConnStr)
	# print(client.list_database_names())
	# print(client[db_name].list_collection_names())
	return client[db_name]

def do_record_store(collection,record):
	now=datetime.now()
	record['last_update_time']=now
	response=collection.update_one({'_id':record['_id']}
		,{'$setOnInsert':{'create_time':now},'$set':record}
		,upsert=True)
	# print(response.matched_count,response.modified_count,response.upserted_id,response.acknowledged,response.raw_result)
	return response

def do_record_update(collection,id,record):
	record['last_update_time']=datetime.now()
	response=collection.update_one({'_id':id},{'$set':record})
	return response

def list_collection_records(collection):
	results=collection.find()
	for result in results:
		print(result)


###########################################

def inforamtion_crawler(endpoint,crawler,db,header):
	# 1. course
	response=do_crawler(endpoint+crawler['courses']['uri'],headers=header)
	soup=BeautifulSoup(response.content,'html.parser')
	records=soup.select(crawler['courses']['target'])
	print(records)
	for record in records:
		print("course:",record)
		course_result={
			'_id':record.get('value')
			,'title':record.text
			,'filename':parse_to_valid_filename(record.text)
		}
		r=do_record_store(db['courses'],course_result)
		print(r.raw_result)
	print('course crawler done')
	
	# 2. unit
	for course in db['courses'].find():
		unit_url=endpoint+crawler['units']['uri'].replace('{course_id}',course['_id'])
		unit_resp=do_crawler(unit_url,headers=header)
		for record in unit_resp.json():
			print("unit:",record)
			unit_result={
				'_id':record['id']
				,'title':record['cname']
				,'filename':parse_to_valid_filename(record['cname'])
				,'parent_id':course['_id']
			}
			r=do_record_store(db['units'],unit_result)
			print(r.raw_result)
		# course x done
		print('course %s done' % course['_id'])
		do_record_update(db['courses'],course['_id'],{'status':'Ready'})
	print('unit crawler done')

	# 3. lesson
	for unit in db['units'].find():
		lesson_url=endpoint+crawler['lessons']['uri'].replace('{unit_id}',unit['_id'])
		lesson_resp=do_crawler(lesson_url,headers=header)
		for record in lesson_resp.json():
			print("lesson:",record)
			lesson_result={'_id':record['id']
				,'title':record['mt_name']
				,'doc':record['pdf']
				,'filename':parse_to_valid_filename(record['mt_name'])+"."+record['pdf'].split('.')[-1]
				,'parent_id':unit['_id']
			}
			r=do_record_store(db['lessons'],lesson_result)
			print(r.raw_result)
		# unit x done
		print('unit %s done' % unit['_id'])
		do_record_update(db['units'],unit['_id'],{'status':'Ready'})
	print('lesson crawler done')


def prepare_targetDir(db,targetDir):
	# 0. targetDir
	if not os.path.exists(targetDir):
		os.mkdir(targetDir)
	print('preapred dir:',targetDir)

	# 1. course dirs
	for course in db['courses'].find():
		course_dir=os.path.join(targetDir,course['filename'])
		if not os.path.exists(course_dir):
			os.mkdir(course_dir)
		# 2. unit dirs
		for unit in db['units'].find({'parent_id':course['_id']}):
			unit_dir=os.path.join(course_dir,unit['filename'])
			if not os.path.exists(unit_dir):
				os.mkdir(unit_dir)
		print('prepare course dir %s done' % course['filename'])

def download_meterials(db,targetDir,url,limit_size=0):
	lesson_handler=ResultHandler(db['lessons'])
	unit_handler=ResultHandler(db['units'])
	tasks=[]
	loop=asyncio.get_event_loop()
	for (unit,items) in gen_download_list(db,targetDir,url,limit_size):
		print('add download unit task:',unit['title'],len(items))
		t=loop.create_task(do_multiple_downloads_async(unit,items
			,callback_func=functools.partial(lesson_handler.handle,'lesson')))
		t.add_done_callback(functools.partial(unit_handler.handle,'unit'))
		tasks.append(t)
	print('Waiting for all sub-proc done...')
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()
	print('All sub-proc done...')

def gen_download_list(db,targetDir,url,limit_size=0):
	for course in db['courses'].find({'status':'Ready'}).limit(limit_size):
		print('course:',course['title'])
		for unit in db['units'].find({'status':'Ready','parent_id':course['_id']}).limit(limit_size):
			targetFileDir=os.path.join(targetDir,course['filename'],unit['filename'])
			results=[]
			for lesson in db['lessons'].find({'status':{'$ne':'Done'},'parent_id':unit['_id']}):
				targetUrl=url.replace('{filename}',lesson['doc'])
				targetFilename=lesson['filename']
				results.append({
					'_id':lesson['_id']
					,'url':targetUrl
					,'dir':targetFileDir
					,'filename':targetFilename
				})
			# print('unit:',unit['title'],len(results))
			yield (unit,results)
	return 'done !'

def do_summary(db):
	results=db.units.aggregate([
		{'$group':{
			'_id':'$parent_id'
			,'total':{'$sum':1}	
			,'done_cnt':{
				'$sum':{'$cond':[{'$eq':['$status','Done']},1,0]}
			}
			,'ready_cnt':{
				'$sum':{'$cond':[{'$eq':['$status','Ready']},1,0]}
			}
		}}
		,{'$match':{
			'done_cnt':{'$gt':0}
		}}
		,{'$lookup':{
			'from':'courses'
			,'localField':'_id'
			,'foreignField':'_id'
			,'as':'course'
		}}
		,{'$project':{
			'total':1
			,'done_cnt':1
			,'ready_cnt':1
			,'title':{'$arrayElemAt':['$course.title',0]}
		}}
	])
	for result in results:
		print(result)
		if result['total']==result['done_cnt']:
			response=do_record_update(db['courses'],result['_id'],{'status':'Done'})
			print(response.raw_result)


###########################################		
# download using `asyncio`+`aiohttp`
###########################################

# do multiple downloads - asyncio
async def do_multiple_downloads_async(unit,items,callback_func=print):
	async with aiohttp.ClientSession() as session:
	 	# tasks=[do_aiohttp_download(session,url,targetDir) for url in url_list]
	 	# await asyncio.gather(*tasks)
	 	tasks=[]
	 	for item in items:
	 		task=asyncio.create_task(do_aiohttp_download(session,item))
	 		task.add_done_callback(callback_func)
	 		tasks.append(task)
	 		await asyncio.gather(*tasks)
	return unit

# do download using `aiohttp`
async def do_aiohttp_download(session,item):
	async with session.get(item['url']) as response:
		content_length = int(response.headers.get('Content-Length',0))
		print(response.status,response.reason,content_length,item['filename'])
		progressBar=ProgressBar(item['filename'], total=content_length,chunk_size=1024,unit="KB")
		with open(os.path.join(item['dir'],item['filename']),'wb') as fd:
			while True:
				chunk=await response.content.read(1024)
				if not chunk:
					break;
				fd.write(chunk)
				await progressBar.refresh(len(chunk))
		await response.release()
	# print(filename,"Done!")
	return item


# callback
class ResultHandler(object):
	def __init__(self,collection):
		self.collection=collection

	def handle(self,title,task):
		item=task.result();
		response=do_record_update(self.collection,item['_id'],{'status':'Done'})
		print(response.raw_result)
		print("< %s : %s  %s Done >" % (title,item['_id'],item['filename']))

###########################################
# demo2: comments crawler
###########################################

def comments_crawler(endpoint,crawler,db,header):
	next_page="1"
	while True:
		print("page:",next_page)
		comment_url=endpoint+crawler['comments']['uri'].replace("{page}",next_page)
		response=do_crawler(comment_url,headers=header)
		if response.status_code!=200:
			print('fail')
			break
		soup=BeautifulSoup(response.content,'html.parser')
		# get comments
		records=soup.select(crawler['comments']['target'])
		parse_store_comments(records)
		# get next page
		next_link=soup.select_one(crawler['comments']['next_link'])
		if not next_link or not next_link.has_attr('href'):
			break
		next_page=next_link['href'].split('/')[-1]
	print('comments crawler done')


def parse_store_comments(records):
	# print(records)
	for record in records:
		# print("comment:",record)
		tds=record.find_all('td')
		if not tds[7].a:
			continue
		comment_result={
			'_id':tds[7].a['href'].split('/')[-1]
			,'time':tds[0].text
			,'teacher':tds[1].span.a.text
			,'course':tds[2].dt.find_all('p')[0].text
			,'unit':tds[2].dt.find_all('p')[1].text
			,'lesson':tds[2].dt.find_all('p')[2].text
			,'meterial_doc':tds[2].dd.p.a['href'].split('/')[-1]
			,'status':'Ready'
		}
		print(comment_result)
		r=do_record_store(db['comments'],comment_result)
		print(r.raw_result)	
	

def comments_content_crawler(endpoint,crawler,db,header):
	for comment in db['comments'].find({'status':'Ready'}):
		print(comment)
		url=endpoint+crawler['comments']['content_uri'].replace('{comment_id}',comment['_id'])
		response=do_crawler(url,headers=header)
		soup=BeautifulSoup(response.content,'html.parser')
		results=soup.select(crawler['comments']['content_target'])
		content=results[1].text.strip()
		print(content)
		r=do_record_update(db['comments'],comment['_id'],{'content':content,'status':'Done'})
		print(r.raw_result)
	print('comments content crawler done')

###########################################

if __name__ == '__main__':
	print('start')

	endpoint='https://class.121talk.cn'
	crawler={
		'courses':{
			'uri':'/business/Teachers/detail/id/3313'
			,'return':'html'
			,'target':'select[name="cid"] > option'
			,'mapping':{'value':'_id','text':'name'}	# {srcKey:destKey}
		}
		,'units':{
			'uri': '/business/Students/getMtCatsByCsId/cs_id/{course_id}'
			,'return':'json'
			,'mapping':{'id':'_id','cname':'title'}
		}
		,'lessons':{
			'uri':'/business/Students/getMtsByMtCat/mt_cat/{unit_id}'
			,'return':'json'
			,'mapping':{'id':'_id','mt_name':'title','pdf':'doc'}
		}
		,'comments':{
			'uri':'/business/Students/classRecords/p/{page}'
			,'return':'html'
			,'target':'table.list_table > tbody > tr'
			,'mapping':{'0.text':'time','1.span.a':'teacher','2.dl.dt.p':'lesson','2.dl.dd.p.a':'meterial_url','7.a':'content'}
			,'next_link':'div.page a.page_next'
			,'content_uri':'/business/Students/getMemo/id/{comment_id}'
			,'content_target':'table.fill_table textarea.big_textara'
		}
	}
	meterial_download_uri='/Public/Uploads/Materials/{filename}'
	header={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
		,'Cookie':'PHPSESSID=t911nl1ivpd0q36fgq0c6d8gr6'
	}
	targetDir='/Users/cj/space/python/download/yeko'
	# mongoConnStr='mongodb://mongoadmin:123456@192.168.99.100:27017/demo?authSource=admin'
	mongoConnStr="mongodb://cj:123456@localhost:27017/?authSource=admin"
	db_name='yeko'
	db=get_connected_db(mongoConnStr,db_name)

	# 1. crawler - courses,units,lessons
	# inforamtion_crawler(endpoint,crawler,db,header)

	# 2. prepare
	# prepare_targetDir(db,targetDir)

	# 3. check download list
	# for (unit,items) in gen_download_list(db,targetDir,endpoint+meterial_download_uri,limit_size=3):
	# 	print('add download unit task:',unit['title'],len(items))

	# 4. download
	# start=time.time()
	# download_meterials(db,targetDir,endpoint+meterial_download_uri,limit_size=2)
	# print('Total cost %0.2f seconds.' %  (end-start))

	# 5. summary
	# do_summary(db)

	# 6. crawler - comments
	# comments_crawler(endpoint,crawler,db,header)
	
	# 7. crawler - comments content
	# comments_content_crawler(endpoint,crawler,db,header)

	

	print('end')






