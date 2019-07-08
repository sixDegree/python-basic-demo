import jsonpath
import json

def test_json(content):
	# 1. loads: string -> python obj
	print('---- loads: --------------')
	result=json.loads(content)
	print(type(result))								# <class 'dict'>
	print(result)

	# 2. dumps: python obj -> string
	print('---- dumps: --------------')
	subjects=result.get('subjects')
	result=json.dumps(subjects,ensure_ascii=False)	# 禁用ascii编码，按utf-8编码	
	print(type(result))								# <class 'str'>
	print(result)

	# 3. dump: python obj -> string -> file
	print('---- dump: --------------')
	json.dump(subjects,open('test.json','w'),ensure_ascii=False)
	with open('test.json','r') as f:
		print(f.read())

	# 4. load: file -> string -> python obj
	print('---- load: --------------')
	result=json.load(open('test.json','r'))
	print(type(result))								# <class 'list'>
	print(result)

	print('-------------------------')


def test_jsonpath(content):
	# 0. 加载
	obj=json.loads(content)

	# 1. `[?()]`
	results=jsonpath.jsonpath(obj,'$.subjects[?(float(@.rate)>=7)]')
	print(type(results))
	# <class 'list'>	
	print(results)
	#[{'rate': '7.1', 'cover_x': 2000, 'title': '奎迪：英雄再起', 'url': 'https://movie.douban.com/subject/26707088/', 'playable': False, 'cover': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2544510053.webp', 'id': '26707088', 'cover_y': 2800, 'is_new': False}
	# , {'rate': '7.7', 'cover_x': 1500, 'title': '污垢', 'url': 'https://movie.douban.com/subject/1945750/', 'playable': False, 'cover': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2548709468.webp', 'id': '1945750', 'cover_y': 2222, 'is_new': False}
	# ]

	# 2. `.xxx`
	results=jsonpath.jsonpath(obj,'$.subjects[?(float(@.rate)>=7)].title')
	print(results)
	# ['奎迪：英雄再起', '污垢']

	# 3. `[index1,index2]`
	results=jsonpath.jsonpath(obj,'$.subjects[0,2,3].cover_x')
	print(results)
	# [1000, 800, 1500]

	# 4. `[start:end]`
	results=jsonpath.jsonpath(obj,'$.subjects[0:3].cover_x')
	print(results)
	# [1000, 2000, 800]

	# 5. `[start:end:step]`
	results=jsonpath.jsonpath(obj,'$.subjects[0:3:2].cover_x')
	print(results)
	# [1000, 800]

	# 6. `?( && )`,`?(,)`
	# cover_x	cover_y
	# 1000		1414
	# 2000		2800
	# 800		1185
	# 1500		2222
	# 1179		1746
	results=jsonpath.jsonpath(obj,'$.subjects[?(@.cover_x>=1000 && @.cover_y<1500)]')
	print(len(results))
	# 1
	results=jsonpath.jsonpath(obj,'$.subjects[?(@.cover_x>=1000,@.cover_y<1500)]')
	print(len(results))
	# 5

	print('-------------------------')

if __name__=='__main__':
	print('start')

	# https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=5&page_start=100
	content='''
	{"subjects":[
		{"rate":"6.5","cover_x":1000,"title":"硬核","url":"https://movie.douban.com/subject/27109879/","playable":false,"cover":"https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2532653002.webp","id":"27109879","cover_y":1414,"is_new":false}
		,{"rate":"7.1","cover_x":2000,"title":"奎迪：英雄再起","url":"https://movie.douban.com/subject/26707088/","playable":false,"cover":"https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2544510053.webp","id":"26707088","cover_y":2800,"is_new":false}
		,{"rate":"6.1","cover_x":800,"title":"芳龄十六","url":"https://movie.douban.com/subject/30334122/","playable":false,"cover":"https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2549923514.webp","id":"30334122","cover_y":1185,"is_new":false}
		,{"rate":"7.7","cover_x":1500,"title":"污垢","url":"https://movie.douban.com/subject/1945750/","playable":false,"cover":"https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2548709468.webp","id":"1945750","cover_y":2222,"is_new":false}
		,{"rate":"6.8","cover_x":1179,"title":"欢乐满人间2","url":"https://movie.douban.com/subject/26611891/","playable":false,"cover":"https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2515404175.webp","id":"26611891","cover_y":1746,"is_new":false}
	]}
	'''

	##############################
	# json: 
	#	loads,load: jsonString -> pythonObj
	#	dumps,dump: pythonObj -> jsonString
	##############################
	# | Json     	| Python 	|
	# |:------------|:----------|
	# | object 		| dict   	|
	# | array 		| list   	|
	# | string 		| unicode	|
	# | number(int) | int,long  |
	# | number(real)| float   	|
	# | true 		| True   	|
	# | false 		| False   	|
	# | null 		| None		|
	##############################

	# test_json(content)

	##############################
	# jsonpath
	# - `$`: 根节点
	# - `@`: 当前节点
	# - `*`: 通配符，匹配所有
	# - `..`: 递归搜索
	# - `.` : 子节点
	# - `[]`: 取子节点,迭代器标示(可在里面做简单的迭代操作，如数组下标，根据内容选值等) 
	# 	+ `[start:end]`,`[start:end:step]`
	# 	+ `[,]` 支持迭代器中做多选
	# 	+ `[(,)]`
	# - `()`: 支持表达式计算
	# 	+ `?()`: 过滤操作，表达式结果必须是boolean类型
	##############################

	# test_jsonpath(content)

	print('end')