import pymongo
import json
from datetime import datetime

# 1. 建立连接
mongoConnStr="mongodb://cj:123456@localhost:27017/?authSource=admin"
client=pymongo.MongoClient(mongoConnStr)    
print("list dbs:",client.list_database_names())                         # 列出dbs

db=client['mg_test']
print("list collections of mg_test db:",db.list_collection_names())     # 列出collections(类似表)

collection=db['movies']
print("get collection:movies count:",collection.estimated_document_count())

# 2. clear:
# ret=collection.delete_many({})           
# print(ret.deleted_count,ret.acknowledged,ret.raw_result)

# 3. update_one -- update or insert record
contents=json.load(open('test.json','r'))           # load: file -> string -> python obj

print('update or insert records:')
for record in contents:
    id=record.pop('id')
    t=datetime.now()
    print("to store record...id=%s,title=%s" % (id,record['title']))

    record['last_update_time']=t
    ret=collection.update_one({'_id':id}
            ,{'$setOnInsert':{'create_time':t},'$set':record}
            ,upsert=True)

    print(ret.matched_count,ret.modified_count,ret.upserted_id,ret.acknowledged,ret.raw_result)

# 4. find -- list records
print('list stored records:')

results=collection.find({},{'_id':1,'title':1,'rate':1})
for result in results:
    print(result)
# results sample:
# {'_id': '27109879', 'rate': '6.5', 'title': '硬核'}
# {'_id': '26707088', 'rate': '7.1', 'title': '奎迪：英雄再起'}
# {'_id': '30334122', 'rate': '6.1', 'title': '芳龄十六'}
# {'_id': '1945750', 'rate': '7.7', 'title': '污垢'}
# {'_id': '26611891', 'rate': '6.8', 'title': '欢乐满人间2'}

print('list rate>=7 records:')
results=collection.find({'rate':{'$gte':"7"}},{'_id':1,'title':1,'rate':1}).limit(5)
for record in results:
    print(record)

# results sample:
# {'_id': '26707088', 'rate': '7.1', 'title': '奎迪：英雄再起'}
# {'_id': '1945750', 'rate': '7.7', 'title': '污垢'}

# 5. aggregate -- summary records
print('list summary by rate level')
# $cond:{if:{$gte:['$rating',8]},then:1,else:0} 
# $addFields:{'rate_number':{$convert:{input:"$rate",to:"int"}}} 
# use $project also could add fields
results=collection.aggregate([
    {'$addFields':{
        'rate_number':{'$convert':{'input':"$rate",'to':"double"}}
        ,'rate_level':{'$cond':[
            {'$lt':['$rate','7.5']}
            ,{'$cond':[{'$gte':['$rate','6.5']},'Middle','Low']}
            ,'High'
        ]}
    }}
    # ,{'$project':{
    #     '_id':1
    #     ,'rate':1
    #     ,'title':1
    #     # ,'rate_level':{'$cond':[
    #     #     {'$lt':['$rate','7.5']}
    #     #     ,{'$cond':[{'$gte':['$rate','6.5']},'Middle','Low']}
    #     #     ,'High'
    #     # ]}
    # }}
    ,{'$group':{
        '_id':"$rate_level"
        ,'count':{'$sum':1}
        ,'avg_rate':{'$avg':'$rate_number'}
        #,'rate_list':{'$push':'$rate_number'}
        ,'rate_list':{'$push':{'$concat':['$title',':','$rate']}}
    }}
    ,{'$sort':{'count':-1}}
    #,{'$limit':10}
])
for record in results:
    print(record)

# results sample:
# {'_id': 'Middle', 'count': 3, 'avg_rate': 6.8, 'rate_list': ['硬核:6.5', '奎迪：英雄再起:7.1', '欢乐满人间2:6.8']}
# {'_id': 'Low', 'count': 1, 'avg_rate': 6.1, 'rate_list': ['芳龄十六:6.1']}
# {'_id': 'High', 'count': 1, 'avg_rate': 7.7, 'rate_list': ['污垢:7.7']}


print("Done!")




