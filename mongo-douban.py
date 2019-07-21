import pymongo
import requests
from datetime import datetime

def do_crawler(url,params=None):
	try:
		response=requests.get(url,params=params)
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

def connect_mongo(conn_str):
	client=pymongo.MongoClient(conn_str)
	print(client.list_database_names())
	return client

def get_connected_db(conn_str,db_name):
	client=pymongo.MongoClient(conn_str)
	return client[db_name]

def store_one_record(collection,record,parser):
	result=parser(record)
	now=datetime.now()
	result['last_update_time']=now
	response=collection.update_one({'_id':result['_id']}
		,{'$setOnInsert':{'create_time':now},'$set':result}
		,upsert=True)
	# print(response.matched_count,response.modified_count,response.upserted_id,response.acknowledged,response.raw_result)

def store_records(collection,records,parser):
	if not records:
		return
	for record in records:
		store_one_record(collection,record,parser)
		
def list_collection_records(collection):
	results=collection.find()
	for result in results:
		print(result)

def clear_collection_records(collection):
	result=collection.delete_many({})
	print(result.deleted_count,result.acknowledged,result.raw_result)

class RecordParser(object):
	def __init__(self,mapping,mode,skip=[],extra={}):
		self.mapping=mapping		# {srcKey:destKey}
		self.mode=mode
		self.skip=skip
		self.extra=extra

	def set_mapping(self,mapping):
		self.mapping=mapping

	def set_mode(self,mode):
		self.mode=mode

	def set_extra(self,extra):
		self.extra=extra

	def set_skip(self,skip):
		self.skip=skip

	def do_parse(self,record):
		result={}
		if self.mode=='All':
			for k, v in self.mapping.items():
				result[v]=record[k]
		elif self.mode=='Mix':
			for k,v in record.items():
				if k in self.mapping:
					result[self.mapping[k]]=v
				else:
					result[k]=v	

		for s in self.skip:
			if s in result:
				result.pop(s)

		for k,v in self.extra.items():
			result[k]=v

		return result

	def parse_records(self,records):
		results=[]
		for record in records:
			results.append(self.do_parse(record))
		return results


##############################################

def test_parser(records):
	# 1 test1: mode='All'
	mode='All'
	mapping={'id':'_id','title':'title','rate':'rate','url':'url','cover':'image','is_new':'is_new','playable':'playable'}
	recordParser=RecordParser(mapping,mode)
	results=recordParser.parse_records(records)
	print(results)

	# 2 test2: mode='Mix'
	mode='Mix'
	mapping={'id':'_id'}
	recordParser=RecordParser(mapping,mode)
	results=recordParser.parse_records(records)
	print(results)


def annual_2018_list(db):
	# collection:
	# 	annual_2018
	# 	annual_2018_kinds
	# 	annual_2018_subjects

	# 1. list collection: annual_2018:
	print('annual_2018:')
	records=db['annual_2018'].find({},{'_id':1,'title':1}).limit(5)
	for record in records:
		print(record)
	print('----------------------')

	# 2. list collection: annual_2018_kinds
	print('annual_2018_kinds:')
	kindRecords=db['annual_2018_kinds'].find({}
		,{'_id':1,"kind_cn":1,"kind_str":1,"payload.title":1}).limit(5)
	for record in kindRecords:
		print(record)
	print('----------------------')

	# 3. list collection: annual_2018_subjects:
	print('annual_2018_subjects:')
	subjectRecords=db['annual_2018_subjects'].find({}
		,{'_id':1,'title':1,'type':1,'rating':1,'rating_count':1,'parent_id':1}
		).sort('rating',pymongo.DESCENDING).limit(5)		#.sort({'rating':-1})
	for record in subjectRecords:
		print(record)
	print('----------------------')

def annual_2018_subjects_aggregate(db):
	print('annual_2018_subjects & groupby:parent_id & join annual_2018:')
	# $cond:{if:{$gte:['$rating',8]},then:1,else:0}		
	results=db.annual_2018_subjects.aggregate([
		{'$group':{
			'_id':{'parent_id':'$parent_id','status':'$status'}
			,'count':{'$sum':1}
			,'avg_rating':{'$avg':'$rating'}
			,'high_cnt':{
				'$sum':{
					'$cond':[{'$gte':['$rating',8]},1,0]
				}
			}
			,'middle_cnt':{
				'$sum':{
					'$cond':[
						{'$lt':['$rating',8]}
						,{'$cond':[{'$gte':['$rating',6]},1,0]}
						,0]
				}
			}
			,'low_cnt':{
				'$sum':{
					'$cond':[{'$lt':['$rating',6]},1,0]
				}
			}
			,'rating_list':{'$push':'$rating'}
		}}
		,{'$lookup':{
			'from':'annual_2018'
			,'localField':'_id.parent_id'
			,'foreignField':'_id'
			,'as':'parent'
		}}
		,{'$project':{
			'_id':1
			,'count':1
			,'avg_rating':1
			,'high_cnt':1
			,'middle_cnt':1
			,'low_cnt':1
			,'rating_list':1
			,'title':{'$arrayElemAt':['$parent.title',0]}
			,'title2':'$parent.title'
		}}
		,{'$sort':{'count':-1}}
		,{'$limit':10}
	])
	for record in results:
		print(record)
	print('----------------------')

import bson
def annual_2018_subjects_mapreduce(db):
	# Note: `group` method will be deprecated and removed in pymongo 4.0
	print('annual_2018_subjects_map_reduce:')
	# db.annual_2018_subjects.mapReduce(
	# 	function(){
	# 		emit(this.parent_id,{rating:this.rating,total:this.rating||0,count:1});
	# 	},function(key,values){
	# 		reduceVal={total:0,count:0,high_cnt:0,middle_cnt:0,low_cnt:0};
	# 		values.forEach(function(item){
	# 			reduceVal.total+=item.total;
	# 			reduceVal.count+=item.count;
	# 			if(item.rating>=8)
	# 				reduceVal.high_cnt++;
	# 			else if(item.rating<8 && item.rating>=6)
	# 				reduceVal.middle_cnt++;
	# 			else
	# 				reduceVal.low_cnt++
	# 		})
	# 		return {avg:reduceVal.total/reduceVal.count
	# 			,high_cnt:reduceVal.high_cnt
	# 			,middle_cnt:reduceVal.middle_cnt
	# 			,low_cnt:reduceVal.low_cnt};
	# 	},{out:'subjects_mapreduce'}
	# )

	result=db.annual_2018_subjects.inline_map_reduce(
		bson.Code('''
			function(){
				emit(this.parent_id,{rating:this.rating,total:this.rating||0,count:1});
			}
		''')
		,bson.Code('''
			function(key,values){
				reduceVal={total:0,count:0,high_cnt:0,middle_cnt:0,low_cnt:0};
				values.forEach(function(item){
					reduceVal.total+=item.total;
					reduceVal.count+=item.count;
					if(item.rating>=8)
						reduceVal.high_cnt++;
					else if(item.rating<8 && item.rating>=6)
						reduceVal.middle_cnt++;
					else
						reduceVal.low_cnt++
				})
				return {avg:reduceVal.total/reduceVal.count
					,high_cnt:reduceVal.high_cnt
					,middle_cnt:reduceVal.middle_cnt
					,low_cnt:reduceVal.low_cnt};
			}
		''')
		,'subjects_mapreduce'
	)
	for record in result.get("results",[]):
		print(record)
	print('----------------------')

def annual_2018_aggregate(db):
	print("annual_2018 join annual_2018_subjects: ")
	results=db.annual_2018.aggregate([
		{'$lookup':{
			'from':'annual_2018_subjects'
			,'localField':'_id'
			,'foreignField':'parent_id'
			,'as':"subjects"
		}}
		,{'$project':{
			"_id":1
			,"title":1
			,"subjects.title":1
			,"subjects.rating":1
		}}
		,{'$sort':{'_id':1}}
		,{'$limit':10}
	])
	for record in results:
		print(record)
	print('----------------------')

def annual_2018_kinds_aggregate(db):
	print("annual_2018_kinds join annual_2018_subjects: ")
	results=db.annual_2018_kinds.aggregate([
		{'$lookup':{
			'from':'annual_2018_subjects'
			,'localField':'_id'
			,'foreignField':'parent_id'
			,'as':"subjects"
			}
		}
		,{'$project':{
			"_id":1
			,"kind_cn":1
			,"kind_str":1
			,"payload.title":1
			,"payload.subject_ids":1
			,"subjects._id":1
			,"subjects.title":1
			,'subjects.rating':1
			}
		}
		,{'$sort':{'_id':1}}
		,{'$limit':10}
	])
	for record in results:
		print(record)
	print('----------------------')


#########################################

# main

if __name__ == '__main__':
	print('start')
	
	# conn mongodb:
	# mongoConnStr='mongodb://mongoadmin:123456@192.168.99.100:27017/demo?authSource=admin'
	mongoConnStr="mongodb://cj:123456@localhost:27017/?authSource=admin"
	client=connect_mongo(mongoConnStr)

	#########################################
	# 1. douban - movies
	#########################################

	# url='https://movie.douban.com/j/search_subjects'
	# params={'type':'movie','tag':'热门','sort':'recommend','page_limit':20,'page_start':0}
	
	# db=client['douban']
	# collection=db['movies']
	# print(db.list_collection_names())

	# # 1.1 clear
	# clear_collection_records(db['movies'])
	
	# # 1.2 crawler
	# response=do_crawler(url,params)
	# records=response.json()
	# print(records.get("subjects",[]))
	# # test parse 
	# # test_parser(records.get("subjects",[]))
	
	# # 1.3 store
	# recordParser=RecordParser({'id':'_id'},'Mix')
	# store_records(db['movies'],records.get("subjects",[]),recordParser.do_parse)

	# # 1.4. check
	# list_collection_records(db['movies'])

	#########################################
	# 2. douban - annual 2018
	#########################################

	db=client['douban']
	endpoint='https://movie.douban.com/ithil_j/activity/movie_annual2018'

	# 2.1 catch categories
	# url=endpoint
	# response=do_crawler(url)
	# records=response.json().get("res").get("widget_infos")

	# collection=db['annual_2018']
	# recordParser=RecordParser({'id':'_id'},'Mix')
	# store_records(collection,records,recordParser.do_parse)
	# list_collection_records(collection)

	# 2.2 catch details
	# kindCollection=db['annual_2018_kinds']
	# kindParser=RecordParser({'id':'_id'},'Mix',skip=["subject","subjects"])

	# subjectCollection=db['annual_2018_subjects']
	# subjectParser=RecordParser({'id':'_id'},'Mix'
	# 	,skip=["color_scheme","interest","rating_stats","orig_title"])
	
	# results=db['annual_2018'].find()
	# for i,result in enumerate(results):
	# 	widget_url=endpoint+'/widget/'+str(i)
	# 	print(widget_url)
	# 	response=do_crawler(widget_url)
	# 	records=response.json()
	# 	# store kind
	# 	kind=records.get("res")
	# 	store_one_record(kindCollection,kind,kindParser.do_parse)
	# 	# store subjects
	# 	subjects=kind.get("subjects") or []
	# 	extra={'parent_id':kind["id"]}
	# 	print('kind_id:',kind["id"])
	# 	print('subject_ids:',kind.get('payload').get('subject_ids'))
	# 	print('subject len:',len(subjects))
	# 	subjectParser.set_extra(extra)
	# 	store_records(subjectCollection,subjects,subjectParser.do_parse)

	# 2.3 query from mongodb
	# annual_2018_list(db)
	# annual_2018_subjects_aggregate(db)
	# annual_2018_subjects_mapreduce(db)
	# annual_2018_aggregate(db)
	# annual_2018_kinds_aggregate(db)


	print('end')



##############################################
# douban - movies
# https://movie.douban.com/explore#!type=movie&tag=热门&sort=recommend&page_limit=20&page_start=100
##############################################
# url(json):	https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=100
# response sample:
		# {,…}
		# subjects: [{rate: "7.1", cover_x: 1974, title: "一个小忙", url: "https://movie.douban.com/subject/27072988/",…},…]
		# 0: {rate: "7.1", cover_x: 1974, title: "一个小忙", url: "https://movie.douban.com/subject/27072988/",…}
		# 1: {rate: "6.1", cover_x: 1943, title: "宁静", url: "https://movie.douban.com/subject/26970964/",…}
		# 2: {rate: "7.2", cover_x: 2025, title: "五尺天涯", url: "https://movie.douban.com/subject/30135110/",…}
		# 3: {rate: "7.4", cover_x: 2024, title: "被抹去的男孩", url: "https://movie.douban.com/subject/27066184/",…}
		# 4: {rate: "6.8", cover_x: 4234, title: "门锁", url: "https://movie.douban.com/subject/27617348/",…}
		# 5: {rate: "7.1", cover_x: 1488, title: "篮球冠军", url: "https://movie.douban.com/subject/30205168/",…}
		# 6: {rate: "6.5", cover_x: 1656, title: "假若比尔街能说话", url: "https://movie.douban.com/subject/27087130/",…}
		# 7: {rate: "7.1", cover_x: 1500, title: "蒙上你的眼", url: "https://movie.douban.com/subject/27092648/",…}
		# 8: {rate: "6.9", cover_x: 1800, title: "极线杀手", url: "https://movie.douban.com/subject/27180599/",…}
		# 9: {rate: "7.2", cover_x: 950, title: "你的婚礼", url: "https://movie.douban.com/subject/26411377/",…}
		# 10: {rate: "6.7", cover_x: 504, title: "侏罗纪世界2", url: "https://movie.douban.com/subject/26416062/",…}
		# 11: {rate: "7.3", cover_x: 2000, title: "寄宿学校", url: "https://movie.douban.com/subject/30201003/",…}
		# 12: {rate: "8.7", cover_x: 1200, title: "命运之夜——天之杯2：失去之蝶",…}
		# 13: {rate: "5.9", cover_x: 1024, title: "后来的我们", url: "https://movie.douban.com/subject/26683723/",…}
		# 14: {rate: "5.0", cover_x: 1080, title: "黄金兄弟", url: "https://movie.douban.com/subject/27069427/",…}
		# 15: {rate: "6.3", cover_x: 1038, title: "我的间谍前男友", url: "https://movie.douban.com/subject/26999424/",…}
		# 16: {rate: "7.8", cover_x: 2570, title: "冷战", url: "https://movie.douban.com/subject/26894602/",…}
		# 17: {rate: "7.2", cover_x: 675, title: "本回家了", url: "https://movie.douban.com/subject/27179199/",…}
		# 18: {rate: "8.6", cover_x: 700, title: "利兹与青鸟", url: "https://movie.douban.com/subject/27062637/",…}
		# 19: {rate: "6.7", cover_x: 678, title: "坏种", url: "https://movie.douban.com/subject/30317630/",…}
# one of `subjects` detail:
		#{
		# cover: "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2527824211.jpg"
		# cover_x: 1974
		# cover_y: 3000
		# id: "27072988"
		# is_new: false
		# playable: false
		# rate: "7.1"
		# title: "一个小忙"
		# url: "https://movie.douban.com/subject/27072988/"
		#}


##############################################
# douban - annual 2018
# https://www.douban.com/
# https://movie.douban.com/annual/2018
##############################################

# 1. categories
# url(json):	https://movie.douban.com/ithil_j/activity/movie_annual2018
# response sample:
	# {
	# r: 0
	# res: {TYPE: "ActivityPage", id: 15, kind: 0, payload: {,…}, pv: "5455655", status: 1, title: "豆瓣",…}
	# TYPE: "ActivityPage"
	# id: 15
	# kind: 0
	# payload: {,…}
	# pv: "5455655"
	# status: 1
	# title: "豆瓣"
	# url: "movie_annual2018"
	# url_name: "movie_annual2018"
	# version: "2018"
	# widget_infos: [{id: 776, show_divider: false, show_divider_txt: "", title: "开篇"},…]
	# status: {code: 200}
	#}
# one of `widget_infos` detail:
	# 0: {id: 776, show_divider: false, show_divider_txt: "", title: "开篇"}
	# id: 776
	# show_divider: false
	# show_divider_txt: ""
	# title: "开篇"

# 2. widget:
# url(json):	https://movie.douban.com/ithil_j/activity/movie_annual2018/widget/0,1,2,...68
# response sample:
	#{
	# r: 0
	# res: {TYPE: "ActivityPageWidget", comment_count: 341, id: 835, kind: 1, kind_cn: "Top 10",…}
	# TYPE: "ActivityPageWidget"
	# comment_count: 341
	# id: 835
	# kind: 1
	# kind_cn: "Top 10"
	# kind_str: "top10"
	# page_id: 15
	# payload: {background_img: "https://img3.doubanio.com/view/activity_page/raw/public/p3190.jpg",…}
	# status: 0
	# subject: {color_scheme: {_avg_color: [0.052083333333333336, 0.4050632911392405, 0.30980392156862746],…},…}
	# subjects: [{color_scheme: {_avg_color: [0.052083333333333336, 0.4050632911392405, 0.30980392156862746],…},…},…]
	# user: {avatar: "https://img1.doubanio.com/icon/u2279829-7.jpg", id: "2279829", name: "张小北",…}
	# status: {code: 200}
	#}
# one of `subjects` detail:
	# color_scheme: {_avg_color: [0.052083333333333336, 0.4050632911392405, 0.30980392156862746],…}
	# cover: "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2519070834.jpg"
	# id: "26752088"
	# interest: {}
	# is_released: true
	# m_url: "https://m.douban.com/movie/subject/26752088/"
	# orig_title: ""
	# playable: true
	# rating: 9
	# rating_count: 1063957
	# rating_stats: [0.003470065049621366, 0.0035029611159097594, 0.04205903058112311, 0.2583948411448959,…]
	# title: "我不是药神"
	# type: "movie"
	# url: "https://movie.douban.com/subject/26752088/"


##############################################
# douban - top250
# url(html): 
#	page1: 		https://movie.douban.com/top250
#	nextPage:	https://movie.douban.com/top250?start=25&filter=
##############################################








