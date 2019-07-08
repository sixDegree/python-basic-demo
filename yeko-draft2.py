
# request
import requests
def request_information(url,headers):
	try:
		response=requests.get(url,headers=headers)
		response.raise_for_status()
	except exceptions.Timeout as e:
		print("GET %s Timeout: %s" % (url,e.message))
	except exceptions.HTTPError as e:
		print("GET %s HTTPError: %s" % (url,e.message))
	else:
		print(response.status_code,response.reason)
		return response

def request_file(url,headers,proxy=None):
	try:
		response=requests.get(url,headers=headers,proxies=proxy,stream=True)
		response.raise_for_status()
	except exceptions.Timeout as e:
		print("GET %s Timeout: %s" % (url,e.message))
	except exceptions.HTTPError as e:
		print("GET %s HTTPError: %s" % (url,e.message))
	else:
		print(response.status_code,response.reason)
		return response

import os
def download_file(response,filepath,filename):
	contentType=response.headers["Content-Type"]
	contentLength=int(response.headers.get("Content-Length",0))
	print(contentType,contentLength)
	
	if contentType.startswith('text'):
		print("Skip")
		return False;
	else:
		# processBar
		chunk_size = 1024
		progress = ProgressBar(filename, total=contentLength,unit="KB", chunk_size=chunk_size, run_status="downloading", fin_status="download completed")
		# write
		with open(os.path.join(filepath,filename),'wb') as fd:
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					fd.write(chunk);
					progress.refresh(count=len(chunk))
		return True;
		
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
		
		
# parse
from bs4 import BeautifulSoup			
def parse_courses(response,selector,courseCollection):		
	soup=BeautifulSoup(response.content,'html.parser')
	results=soup.select(selector)
	for result in results:
		print(result)
		course_id=result.get('value')
		if course_id ==0:
			continue
		store_records(courseCollection,course_id,result.text,None,None,None,"/"+course_id)
		
def parse_categories(course,results,categoryCollection):
	for result in results:
		print(result)
		store_records(categoryCollection,result.get('id'),result.get('cname'),None,course.get('_id'),course.get('name'),"/"+result.get('id'))
		
def parse_meterials(category,results,meterialCollection):
	for result in results:
		print(result)
		filename=result.get('mt_name')+"."+result.get('pdf').split('.')[-1]
		store_records(meterialCollection,result.get('id'),result.get('mt_name'),filename,category.get('_id'),category.get('name'),"/"+result.get('pdf'))

# store
import pymongo	
from datetime import datetime	
def store_records(collection,id,name,filename=None,parent_id=None,parent_name=None,data_url=None):
	result=collection.find_one({'_id':id})
	if result:
		print("Already Exist:",result)
		return result
	if not filename:
		filename=name
	data={'_id':id,'name':name,'filename':util_parse_to_valid_filename(filename),'status':'New','parent_id':parent_id,'parent_name':parent_name,'data_url':data_url,'last_update_time':datetime.now()}
	result=collection.insert_one(data)
	print(result)
	return result

# utils
import re
def util_parse_to_valid_filename(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  			# '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  		# 替换为下划线
    return new_title

	
#######################################################################################################
	
# main
# Status: New,Ready,Created,Done

# 0. Reset

def clear(db,collections):
	for col in collections:
		db[col].drop()
	print('Clear complete!')

def reset(db,collections,status):
	for col in collections:
		db[col].update_many({},{'$set':{'status':status,'last_update_time':datetime.now()}})
	print('Reset complete!')
	
	
# 1. Catch data to db:
def catch_and_store(Config,db):
	courseCollection=db['courses']
	categoryCollection=db['categories']
	meterialCollection=db['meterials']
	
	# courses
	courseResponse=request_information(Config["Endpoint"]+Config["URI"]["Course"],Config["Headers"])
	parse_courses(courseResponse,'select[name="cid"] > option',courseCollection)
	print('Catech courses to db complete!')
	
	# categories
	for course in courseCollection.find({'status':'New'}):
		categoryResponse=request_information(Config["Endpoint"]+Config["URI"]["Category"]+course.get('data_url'),Config["Headers"])
		parse_categories(course,categoryResponse.json(),categoryCollection)
		# prepare_dir(Config["RootDir"],course,courseCollection)
	print('Catech categories to db complete!')
	
	# meterials
	for category in categoryCollection.find({'status':'New'}):
		meterialResponse=request_information(Config["Endpoint"]+Config["URI"]["Meterial"]+category.get('data_url'),Config["Headers"])
		parse_meterials(category,meterialResponse.json(),meterialCollection)
		# prepare_dir(Config["RootDir"],category,categoryCollection)
	print('Catech meterial to db complete!')
	
# 2. Prepare Dir:
def prepare_dirs(rootDir,db):
	courseCollection=db['courses']
	categoryCollection=db['categories']
	meterialCollection=db['meterials']
	
	for course in courseCollection.find({'status':'New'}):
		dir=os.path.join(rootDir,course.get('filename'))
		if not os.path.exists(dir):
			os.mkdir(dir)
		result=courseCollection.update_one({'_id':course.get('_id')},{'$set':{'status':'Ready','location':rootDir,'last_update_time':datetime.now()}})
		print(result)
	print('Prepare course dirs complete!')

	for category in categoryCollection.find({'status':'New'}):
		course=courseCollection.find_one({"_id":category.get('parent_id')})
		courseDir=os.path.join(course.get('location'),course.get('filename'))
		dir=os.path.join(course.get('location'),course.get('filename'),category.get('filename'))
		if not os.path.exists(dir):
			os.mkdir(dir)
		result=categoryCollection.update_one({'_id':category.get('_id')},{'$set':{'status':'Ready','location':courseDir,'last_update_time':datetime.now()}})
		print(result)
		result=meterialCollection.update_many({'parent_id':category.get('_id')},{'$set':{'status':'Ready','location':dir,'last_update_time':datetime.now()}})
		print(result)
	print('Prepare category dirs complete!')
		
# 3. Download meterials:
def download_meterials(Config,db):
	meterialCollection=db['meterials']
	for meterial in meterialCollection.find({'status':'Ready'}):
		file=os.path.join(meterial.get('location'),meterial.get('filename'))
		print('file:',file)
		
		response=request_file(Config["Endpoint"]+Config["URI"]["Resource"]+meterial.get('data_url'),Config["Headers"],Config["Proxy"])
		if not response:
			continue;	
		if os.path.exists(file):
			existFileSize=os.path.getsize(file);
			contentLength=int(response.headers.get('Content-Length',0))
			msg='Exist:'+str(existFileSize)+"/"+str(contentLength)
			print(msg)
			if existFileSize == contentLength:
				print("Skip")
				meterialCollection.update_one({'_id':meterial.get('_id')},{'$set':{'status':'Done','details':'Existed','last_update_time':datetime.now()}})
				continue
		result=download_file(response,meterial.get('location'),meterial.get('filename'))
		print(result)
		if result:
			meterialCollection.update_one({'_id':meterial.get('_id')},{'$set':{'status':'Done','last_update_time':datetime.now()}})
	print('Download meterials complete!')

def do_download(process,Config,meterial):
	file=os.path.join(meterial.get('location'),meterial.get('filename'))
	print(process,meterial["name"])
	response=request_file(Config["Endpoint"]+Config["URI"]["Resource"]+meterial.get('data_url'),Config["Headers"],Config["Proxy"])
	if not response:
		return	
	if os.path.exists(file):
		existFileSize=os.path.getsize(file);
		contentLength=int(response.headers.get('Content-Length',0))
		msg='Exist:'+str(existFileSize)+"/"+str(contentLength)
		print(msg)
		if existFileSize == contentLength:
			print("Skip")
			# db['meterials'].update_one({'_id':meterial.get('_id')},{'$set':{'status':'Done','details':'Existed','last_update_time':datetime.now()}})
			return meterial.get('_id');
	result=download_file(response,meterial.get('location'),meterial.get('filename'))
	print(result)
	if result:
		#db['meterials'].update_one({'_id':meterial.get('_id')},{'$set':{'status':'Done','last_update_time':datetime.now()}})
		return meterial.get('_id')

class ResultHandler:
	def __init__(self,db):
		self.db=db
	def update_status(self,result):
		print("callback:",result)
		if result:
			self.db['meterials'].update_one({'_id':result},{'$set':{'status':'Done','last_update_time':datetime.now()}})
	
# def update_status(id):
# 	print("callback:",id)
# 	#db['meterials'].update_one({'_id':id},{'$set':{'status':'Done','last_update_time':datetime.now()}})
# 	meterial=db['meterials'].find_one({'_id':id})
# 	print(meterial["name"])
		
import multiprocessing
from multiprocessing import Pool
import os, time, random
		
def multi_download_meterials(Config,db):
	print("系统进程数：",multiprocessing.cpu_count())
	print('Parent process %s.' % os.getpid())
	p = Pool(4)
	i=1
	results=[]
	handler=ResultHandler(db)
	start = time.time()
	for meterial in db['meterials'].find({'status':'Ready'}):
		result=p.apply_async(do_download,args=(i%5,Config,meterial,),callback=handler.update_status)
		i=i+1
		results.append(result)
		
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	print('All subprocesses done.')
	
	end = time.time()
	print('Runs %0.2f seconds.' % (end - start))
	
# summary
def summary(db):
	# db.categories.aggregate([ {$group:{_id:{parent_id:'$parent_id',parent_name:'$parent_name',status:'$status'},count:{$sum:1}}},{$sort:{"count":1}},{$out:"course_summary"} ])
	# db.meterials.aggregate([ {$group:{_id:{parent_id:'$parent_id',parent_name:'$parent_name',status:'$status'},count:{$sum:1}}},{$sort:{"count":1}},{$out:"category_summary"} ])
	# for category in categoryCollection.aggregate([{'$group':{'_id':{'parent_id':'$parent_id','parent_name':'$parent_name','status':'$status'},'count':{'$sum':1}}}]):
	#	print(category["_id"],category["count"])
	
	#iter=db.meterials.aggregate([
	#	{'$group':
	#		{
	#			'_id':{'parent_id':'$parent_id','parent_name':'$parent_name'}
	#			,'total':{'$sum':1}
	#			,'ready_cnt':{
	#				'$sum':{
	#					'$cond':[{'$eq':['$status','Ready']},1,0]		# $cond:{if:{$eq:['$status','Ready']},then:1,else:0}
	#				}
	#			}
	#			,'done_cnt':{
	#				'$sum':{
	#					'$cond':[{'$eq':['$status','Done']},1,0]
	#				}
	#			}
	#		}
	#	}
	#] )
	#for meterialGrp in iter:
	#	# print(meterialGrp["_id"],meterialGrp["total"],meterialGrp["ready_cnt"],meterialGrp["done_cnt"])
	#	if meterialGrp["total"] == meterialGrp["done_cnt"]:
	#		print("Done:",meterialGrp["_id"])
	#		#db.categories.update_one({"_id":meterialGrp["_id"]["parent_id"]},{'$set':{"status":'Done'}})
	#		
	
	# The `group` method will be deprecated and removed in pymongo 4.0
	#import bson
	#for category in db.categories.find({'status':'Ready'}):
	#	iter=db.meterials.group(
	#		key={'parent_id':1,'parent_name':1,'status':1}
	#		,condition={}
	#		,initial={'total':0,'ready_cnt':0,'done_cnt':0}
	#		,reduce=bson.Code('''function(curr,result){
	#			result.total++;
	#			if(curr.status=='Ready')
	#				result.ready_cnt++;
	#			else if (curr.status=='Done')
	#				result.done_cnt++;
	#		}''') 
	#	)
	#	for meterialGrp in iter:
	#		print(meterialGrp["parent_id"],meterialGrp["total"],meterialGrp["ready_cnt"],meterialGrp["done_cnt"])
	#	

	for category in db.categories.find({'status':'Ready'}):
		#print(category["_id"],category["name"])
		total=db.meterials.count_documents({'parent_id':category["_id"]})
		done_cnt=db.meterials.count_documents({'parent_id':category["_id"],"status":'Done'})
		if total==done_cnt:
			print("Done(%s):%s %s" % (total,category["_id"],category["name"]))
			db.categories.update_one({"_id":category["_id"]},{'$set':{"status":"Done"}})
		else:
			print("Process(%s/%s):%s %s" % (done_cnt,total,category["_id"],category["name"]))
	print("Summary categories completed!")
	
	for course in db.courses.find({'status':'Ready'}):
		total=db.categories.count_documents({'parent_id':course["_id"]})
		done_cnt=db.categories.count_documents({'parent_id':course["_id"],"status":'Done'})
		if total==done_cnt:
			print("Done(%s):%s %s" % (total,course["_id"],course["name"]))
			db.courses.update_one({"_id":course["_id"]},{'$set':{"status":"Done"}})
		else:
			print("Process(%s/%s):%s %s" % (done_cnt,total,course["_id"],course["name"]))
	print("Summary courses completed!")	
	#pass
	
	
	
def main():
	# config
	Config={
		'RootDir':'D:\\Space\\python\\yeko2'								# D:\Space\python\yeko
		,'Endpoint':'https://class.121talk.cn'
		,'URI':{
			'Course':'/business/Teachers/detail/id/3554'
			,'Category':'/business/Students/getMtCatsByCsId/cs_id/'			# https://class.121talk.cn/business/Students/getMtCatsByCsId/cs_id/1080
			,'Meterial':'/business/Students/getMtsByMtCat/mt_cat/'			# https://class.121talk.cn/business/Students/getMtsByMtCat/mt_cat/10245
			,'Resource':'/Public/Uploads/Materials/'						# http://class.121talk.cn/Public/Uploads/Materials/509a656916585.pdf
		}
		,'Headers':{
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
			,'Cookie':'PHPSESSID=m742kdp8v445pt6ebm3r5r1lm0'
		}
		#,'Cookie':{'PHPSESSID':'m742kdp8v445pt6ebm3r5r1lm0'}
		,"Proxy":{
			"http":"http://cn-proxy.jp.oracle.com:80",
			"https":"http://cn-proxy.jp.oracle.com:80"
		}
		,'MongoConnection':'mongodb://mongoadmin:123456@192.168.99.100:27017/demo?authSource=admin'
		,'StoreDB':'yeko'
	}
	
	client=pymongo.MongoClient('mongodb://mongoadmin:123456@192.168.99.100:27017/demo?authSource=admin')
	db=client['yeko']
	
	# 0. clear,reset
	#clear(db,["categories","meterials"])
	#reset(db,["courses"],"New")
	#reset(db,["meterials"],"Ready")
	
	# 1. Catch data to db:
	#catch_and_store(Config,db)
	
	# 2. create dir
	#prepare_dirs(Config["RootDir"],db)
	
	# 3. Download meterials:
	# download_meterials(Config,db)
	# multi_download_meterials(Config,db)
	
	# 4. Summary
	summary(db)

# run
#main()

if __name__ == '__main__':
	main()


###################################################################################

# db.categories.aggregate([{$lookup:{from:'meterials',localField:'_id',foreignField:'parent_id',as:"meterials"}},{$project:{"_id":0,"name":1,"meterials.name":1,"meterials.status":1}}])
# { "name" : "香港朗文版小学英语 1A", "meterials" : [ { "name" : "Welcome to English 1A Chapter 1", "status" : "Done" }, { "name" : "Welcome to English 1A Chapter 2", "status" : "Done" }, { "name" : "Welcome to English 1A Chapter 3", "status" : "Done" }, { "name" : "Welcome to English 1A Chapter 4", "status" : "Done" }, { "name" : "Welcome to English 1A Chapter 5", "status" : "Done" }, { "name" : "Welcome to English 1A Chapter 6", "status" : "Done" } ] }
# { "name" : "香港朗文版小学英语 1B", "meterials" : [ { "name" : "Welcome to English 1B Chapter 1", "status" : "Done" }, { "name" : "Welcome to English 1B Chapter 2", "status" : "Done" }, { "name" : "Welcome to English 1B Chapter 3", "status" : "Done" }, { "name" : "Welcome to English 1B Chapter 4", "status" : "Done" }, { "name" : "Welcome to English 1B Chapter 5", "status" : "Done" }, { "name" : "Welcome to English 1B Chapter 6", "status" : "Done" } ] }

#  db.meterials.group({ 
# 	key:{parent_id:1,parent_name:1,status:1}
# 	,initial:{total:0,ready_cnt:0,done_cnt:0}
# 	,reduce:function(curr,result){
# 		result.total++;
# 		if(curr.status=='Ready')
# 			result.ready_cnt++;
# 		else if (curr.status=='Done')
# 			result.done_cnt++;
# 	} 
# })
 
# db.meterials.group({ key:{parent_id:1,parent_name:1,status:1}, initial:{total:0}, reduce:function(curr,result){result.total++} })
# [
#         {
#                 "parent_id" : "11205",
#                 "parent_name" : "香港朗文版小学英语 1A",
#                 "status" : "Done",
#                 "total" : 6
#         },
#         {
#                 "parent_id" : "11206",
#                 "parent_name" : "香港朗文版小学英语 1B",
#                 "status" : "Done",
#                 "total" : 6
#         },
#         {
#                 "parent_id" : "11207",
#                 "parent_name" : "香港朗文版小学英语 2A",
#                 "status" : "Done",
#                 "total" : 6
#         },
# 		...
# ]

# db.meterials.aggregate([ {$group:{_id:{parent_id:'$parent_id',parent_name:'$parent_name',status:'$status'},count:{$sum:1}}} ])
# db.meterials.aggregate([ {$group:{_id:{parent_id:'$parent_id',parent_name:'$parent_name',status:'$status'},count:{$sum:1}}},{$sort:{"count":1}} ])
# db.meterials.aggregate([ {$group:{_id:{parent_id:'$parent_id',parent_name:'$parent_name',status:'$status'},count:{$sum:1}}},{$sort:{"count":1}},{$out:"category_summary"} ])
# { "_id" : { "parent_id" : "11997", "parent_name" : "生日会", "status" : "Done" }, "count" : 1 }
# { "_id" : { "parent_id" : "12287", "parent_name" : "Pei  Ni", "status" : "Done" }, "count" : 1 }
# { "_id" : { "parent_id" : "11543", "parent_name" : "雅思口语水平测试教材", "status" : "Ready" }, "count" : 5 }
# { "_id" : { "parent_id" : "11482", "parent_name" : "男士话题", "status" : "Done" }, "count" : 5 }

# db.meterials.aggregate([ 
# 	{$group:
# 		{
# 			_id:{parent_id:'$parent_id',parent_name:'$parent_name'}
# 			,count:{$sum:1}
# 			,ready_cnt:{
# 				$sum:{
# 					$cond:[{$eq:['$status','Ready']},1,0]		# $cond:{if:{$eq:['$status','Ready']},then:1,else:0}
# 				}
# 			}
# 			,done_cnt:{
# 				$sum:{
# 					$cond:[{$eq:['$status','Done']},1,0]
# 				}
# 			}
# 		}
# 	}
# ] )
#
# { "_id" : { "parent_id" : "67", "parent_name" : "新托福口语-初级" }, "count" : 30, "ready_cnt" : 30, "done_cnt" : 0 }
# { "_id" : { "parent_id" : "10435", "parent_name" : "新托福考试中级阅读专项进阶" }, "count" : 11, "ready_cnt" : 11, "done_cnt" : 0 }
