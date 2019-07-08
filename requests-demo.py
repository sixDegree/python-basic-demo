import requests
from requests import Request, Session
import json
import base64
import time
import os

###########################################
# 1. Response
###########################################

# 1.1 Response: status/encoding/headers
def test_response():
	print('Test: Response(status,headers)')
	resp=requests.get('http://www.baidu.com')
	print("type(resp):",type(resp))							# <class 'requests.models.Response'>
	print("status:",resp.status_code,resp.reason)			# 200 OK
	print("encoding:",resp.encoding,resp.apparent_encoding)	# ISO-8859-1 utf-8
	print("request headers:",resp.request.headers)
	# {'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
	print("response headers:",resp.headers)
	# {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'Keep-Alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Tue, 19 Mar 2019 15:46:48 GMT', 'Last-Modified': 'Mon, 23 Jan 2017 13:28:24 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18', 'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}
	print('--------------------------')

# 1.2 Response: content / text / text using apparent_encoding
def test_response_cnontent_text():
	print('Test: Response(content,text,apparent_encoding text)')
	resp=requests.get('http://www.baidu.com')
	print("content:",resp.content[200:400])
	# b'l=stylesheet type=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>\xe7\x99\xbe\xe5\xba\xa6\xe4\xb8\x80\xe4\xb8\x8b\xef\xbc\x8c\xe4\xbd\xa0\xe5\xb0\xb1\xe7\x9f\xa5\xe9\x81\x93</title></head> <body link=#0000cc> <div id=wrapper> <div id=head> <div class=h'
	print("text:",resp.text[200:400])
	# l=stylesheet type=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>ç¾åº¦ä¸ä¸ï¼ä½ å°±ç¥é</title></head> <body link=#0000cc> <div id=wrapper> <div id=head> <div class=h
	resp.encoding=resp.apparent_encoding
	print("text using apparent_encoding:",resp.text[200:400])
	# l=stylesheet type=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>百度一下，你就知道</title></head> <body link=#0000cc> <div id=wrapper> <div id=head> <div class=head_wrapper> <div
	print('--------------------------')

# 1.3 Response: raw
def test_response_raw():
	print('Test: Response(raw)')
	resp=requests.get('http://www.baidu.com',stream=True)
	print(resp.raw)
	print(resp.raw.read(200))
	# for chunk in resp.iter_content(100):
	# 	print(str(chunk))

###########################################
# 2. Exception
###########################################

def test_exception():
	print("Test: Exception")
	def do_request(url):
	  try:
	    r=requests.get(url,timeout=0.1)
	    r.raise_for_status()
	    r.encoding=r.apparent_encoding
	  except requests.Timeout or requests.HTTPError as e:
	        print(e)
	  except Exception as e:
	    print("Request Error:",e)
	  else:
	        print(r.text)
	        print(r.status_code)
	        return r.text

	result=do_request("http://www.baidu.com")
	print(result[200:400])
	print('--------------------------')

###########################################
# 3. Requests method
###########################################
Endpoint="http://httpbin.org"

# 3.1 reqeusts.get
def test_requests_get():
	print('Test: requests.get')
	r=requests.get(Endpoint+'/get')
	print(r.json())
	# {
	#   "args": {},
	#   "headers": {
	#     "Accept": "*/*",
	#     "Accept-Encoding": "gzip, deflate",
	#     "Host": "httpbin.org",
	#     "User-Agent": "python-requests/2.21.0"
	#   },
	#   "origin": "58.209.61.113, 58.209.61.113",
	#   "url": "https://httpbin.org/get"
	# }
	print('--------------------------')

# 3.2 requests.head
def test_requests_head():
	print('Test: requests.head')
	r=requests.head(Endpoint+'/get')
	print(r.text)
	# ''
	print(r.headers)
	# {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': '*', 'Content-Encoding': 'gzip', 'Content-Type': 'application/json', 'Date': 'Tue, 19 Mar 2019 13:16:24 GMT', 'Server': 'nginx', 'Connection': 'keep-alive'}
	print('--------------------------')

# 3.3 requests.post -- data:json
def test_requests_post_json():
	print('Test: requests.post -- data:json')
	# 向URL POST一个字典,自动编码为form(表单)
	record={'key1':'value1','key2':'value2'}
	r=requests.post(Endpoint+'/post',data=record)
	print(r.json())
	# {'args': {}, 'data': '', 'files': {}, 'form': {'key1': 'value1', 'key2': 'value2'}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '23', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.21.0'}, 'json': None, 'origin': '58.209.61.113, 58.209.61.113', 'url': 'https://httpbin.org/post'}

# 3.4 requests.post -- data:string
def test_requests_post_string():
	print('Test: requests.post -- data:string')
	# 向URL POST一个字符串,自动编码为data
	record="ABC123"
	r=requests.post(Endpoint+'/post',data=record)
	print(r.json())
	# {'args': {}, 'data': 'ABC123', 'files': {}, 'form': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '6', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.21.0'}, 'json': None, 'origin': '58.209.61.113, 58.209.61.113', 'url': 'https://httpbin.org/post'}


###########################################
# 4. Requests args
###########################################

def print_json_better(json_str):
    return print(json.dumps(json.loads(json_str),indent=4))
	
# 4.1 args: params
def test_args_params():
	print('Test: params')
	r = requests.request('GET', Endpoint+'/get', params={'p1': 'v1', 'p2': 'p2'}) 
	print("url(+params):",r.url)	# http://httpbin.org/get?p1=v1&p2=p2
	print("request headers:",r.request.headers)
	print("response headers:",r.headers)
	print_json_better(r.text)
	print('--------------------------')

# 4.2 args: data - 表单参数
def test_args_data():
	print('Test: data 表单参数')
	# content-type: application/x-www-form-urlencoded
	# 内容： key1=value1&key2=value2
	r=requests.request('POST',Endpoint+'/post',data={'key1':'value1','key2':'value2'})
	print("content-type:",r.request.headers['content-type'])	
	print_json_better(r.text)
	print('--------------------------')

# 4.3 args: json - JSON参数
def test_args_json():
	print('Test: json JSON参数')
	# content-type: application/json
	# 内容："{'key1':'value1','key2':'value2'}"
	r=requests.request('POST',Endpoint+'/post',json={'key1':'value1','key2':'value2'})
	print("content-type:",r.request.headers['Content-Type'])
	print_json_better(r.text)
	print('--------------------------')

# 4.4 args: headers
def test_args_headers():
	print('Test: headers')
	Header={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
	}
	r=requests.request('GET',Endpoint+'/get',headers=Header)
	print('User-Agent:',r.request.headers['User-Agent'])
	print('--------------------------')

# 4.5 args: auth - basic auth
def test_args_auth_basic():
	print('Test: auth - basic auth')
	r=requests.request('GET',Endpoint+'/basic-auth/Tom/Tom111')
	print(r.status_code,r.reason)
	# 401 UNAUTHORIZED

	r=requests.request('GET',Endpoint+'/basic-auth/Tom/Tom111',auth=('Tom','Tom123'))
	print(r.status_code,r.reason)
	# 401 UNAUTHORIZED

	r=requests.request('GET',Endpoint+'/basic-auth/Tom/Tom123',auth=('Tom','Tom123'))
	print(r.status_code,r.reason)
	print(r.request.headers)
	print(r.text)
	# 200 OK
	# {'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Authorization': 'Basic VG9tOlRvbTEyMw=='}
	# {
	#   "authenticated": true,
	#   "user": "Tom"
	# }
	print(base64.b64decode('VG9tOlRvbTEyMw=='))
	print('--------------------------')

# 4.6 args: auth - oauth
def test_args_auth_oauth():
	print('Test: auth - oauth')
	r=requests.request('GET',Endpoint+'/bearer')
	print(r.status_code,r.reason)			# 401 UNAUTHORIZED
	print(r.headers)						# Note: 'WWW-Authenticate': 'Bearer'

	r=requests.request('GET',Endpoint+'/bearer',headers={'Authorization':'Bearer 1234567'})
	print(r.status_code,r.reason)			# 200 OK
	print(r.headers)
	print('--------------------------')

# 4.7 args: auth - advance:自定义身份验证（继承requests.auth.AuthBase）
def test_args_auth_advance():
	print('Test: auth - advance:自定义身份验证（继承requests.auth.AuthBase）')
	from requests.auth import AuthBase
	class MyAuth(AuthBase):
		def __init__(self,authType,token):
			self.authType=authType
			self.token=token
		def __call__(self,req):
			req.headers['Authorization']=' '.join([self.authType,self.token])
			return req
	r=requests.request('GET',Endpoint+'/bearer',auth=MyAuth('Bearer','123456'))
	print(r.status_code,r.reason)					# 200 OK
	print("Request Headers:",r.request.headers)
	print("Response Headers:",r.headers)
	print("Response Text:",r.text)

# 4.8 args: cookies
def test_args_cookies():
	print('Test: cookies')
	Cookie={
		'freefrom':'Test123'
	}
	r=requests.request('GET',Endpoint+'/cookies/set',cookies=Cookie)
	print(r.status_code,r.reason)					# 200 OK
	print(r.text)
	# {
	#   "cookies": {
	#     "freefrom": "Test123"
	#   }
	# }
	print('--------------------------')

# 4.9 args: cookies
def test_args_timeout():
	print('Test: timeout')
	def timeout_request(url,timeout):
	    try:
	        resp=requests.get(url,timeout=timeout)
	        resp.raise_for_status()
	    except requests.Timeout or requests.HTTPError as e:
	        print(e)
	    except Exception as e:
	        print("unknow exception:",e)
	    else:
	        print(resp.text)
	        print(resp.status_code)
			
	timeout_request(Endpoint+'/get',0.1)
	# HTTPConnectionPool(host='httpbin.org', port=80): Max retries exceeded with url: /get (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x1025d9400>, 'Connection to httpbin.org timed out. (connect timeout=0.1)'))		
	print('--------------------------')

# 4.10 args: files - upload
def test_args_files_upload():
	print('Test: files - upload')

	# prepare files
	with open('test1.txt','w') as f:
		f.write('Hello world!')
	with open('test2.txt','w') as f:
		f.write('Nice to meet you!')

	# Post one file
	#f={'image': open('test1.txt', 'rb')}
	f={'txt': open('test1.txt', 'rb')}
	r = requests.post(Endpoint+'/post', files=f)
	print(r.status_code,r.reason)
	print(r.headers)
	#print(r.text[100:200])
	print(r.text)

	print('--------------------------')
	# POST Multiple Multipart-Encoded Files
	multiple_files = [
		# ('images', ('黑洞1.jpg', open('黑洞1.jpg', 'rb'), 'image/jpg')),
		# ('images', ('极光1.jpg', open('极光1.jpg', 'rb'), 'image/jpg'))
		('t1', ('test1.txt', open('test1.txt', 'rb'), 'text')),
		('t2', ('test2.txt', open('test2.txt', 'rb'), 'text'))
	]
	r = requests.post(Endpoint+'/post', files=multiple_files)
	print(r.status_code,r.reason)
	print(r.headers)
	#print(r.text[100:200])
	print(r.text)

	# clear
	if os.path.exists('test1.txt'):
		os.remove('test1.txt')
	if os.path.exists('test2.txt'):
		os.remove('test2.txt')
	print('--------------------------')

# 4.11 args: stream=True
def test_args_streams():
	print('Test: stream=True')
	with requests.get(Endpoint+"/stream/3",stream=True) as r:
		print(r.status_code,r.reason)
		contentLength=int(r.headers.get('content-length',0))
		print("content-length:",contentLength)
		# 此时仅有响应头被下载下来了，连接保持打开状态，因此允许我们根据条件获取内容
		if contentLength<100:
			print(r.content)
		else:
			print('read line by line')
			lines=r.iter_lines() # iter_content	一块一块的下载遍历内容
			for line in lines:	
				if line:
					print(line)				
		print('Done')
	print('--------------------------')	

###########################################
# 5. Event Hooks
###########################################

def test_event_hooks():
	print('Test: Event Hooks')
	def get_key_info(response,*args,**kwargs):
		print("callback:content-type",response.headers['Content-Type'])
	r=requests.get(Endpoint+'/get',hooks=dict(response=get_key_info))
	print(r.status_code,r.reason)

	# callback:content-type application/json
	# 200 OK
	print('--------------------------')

###########################################
# 6. Session
###########################################

# 6.1 Session - 跨请求保持某些参数
def test_session_cookie():
	print('Test: Session - 跨请求保持某些参数')
	# 在同一个 Session 实例发出的所有请求之间保持 cookie， 期间使用 urllib3 的 connection pooling 功能
	s = requests.Session()
	r=s.get(Endpoint+'/cookies/set/mycookie/123456')
	print("set cookies",r.status_code,r.reason)		# set cookies 200 OK
	r = s.get(Endpoint+"/cookies")
	print("get cookies",r.status_code,r.reason)		# get cookies 200 OK
	print(r.text)
	# {
	#   "cookies": {
	#     "mycookie": "123456"
	#   }
	# }
	print('--------------------------')

# 6.2: Session - 为请求方法提供缺省数据
def test_session_default():
	print('Test: Session - 为请求方法提供缺省数据')
	# 通过为会话对象的属性提供数据来实现（注：方法层的参数覆盖会会话的参数）
	s = requests.Session()
	s.auth = ('user', 'pass')
	s.headers.update({'x-test': 'true'})
	# both 'x-test' and 'x-test2' are sent
	r=s.get(Endpoint+'/headers', headers={'x-test2': 'true'})
	print(r.request.headers)
	# {'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'x-test': 'true', 'x-test2': 'true', 'Authorization': 'Basic dXNlcjpwYXNz'}
	print('--------------------------')

# 6.3: Session - 用作前后文管理器
def test_session_context():
	print('Test: Session - 用作前后文管理器')
	with requests.Session() as s:		# 这样能确保 with 区块退出后会话能被关闭，即使发生了异常也一样
		s.get('http://httpbin.org/cookies/set/mycookie/Test123')
		r = s.get(Endpoint+"/cookies")
		print("set cookies",r.status_code,r.reason)
		print(r.text)
		# {
		#   "cookies": {
		#     "mycookie": "Test123"
		#   }
		# }
	print("out with:")
	r = s.get(Endpoint+"/cookies")
	print("get cookies",r.status_code,r.reason)
	print(r.text)
	# {
	#   "cookies": {
	#     "mycookie": "Test123"
	#   }
	# }
	print('--------------------------')

###########################################
# 7. Prepared Request 
# 可在发送请求前，对body／header等做一些额外处理
###########################################

def test_prepared_request():
	print('Test: Prepared Request')
	s=Session()
	req=Request('GET',Endpoint+'/get',headers={'User-Agent':'fake1.0.0'})
	prepared=req.prepare()  # 要获取一个带有状态的 PreparedRequest需使用`s.prepare_request(req)`
	# could do something with prepared.body/prepared.headers here
	resp=s.send(prepared,timeout=3)
	print(resp.status_code,resp.reason)
	print("request headers:",resp.request.headers)
	# {'User-Agent': 'fake1.0.0'}

	print("response headers:",resp.headers)
	# {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json', 'Date': 'Thu, 21 Mar 2019 15:47:30 GMT', 'Server': 'nginx', 'Content-Length': '216', 'Connection': 'keep-alive'}
	
	print(resp.text)
	# {
	#   "args": {},
	#   "headers": {
	#     "Accept-Encoding": "identity",
	#     "Host": "httpbin.org",
	#     "User-Agent": "fake1.0.0"
	#   },
	#   "origin": "117.83.222.100, 117.83.222.100",
	#   "url": "https://httpbin.org/get"
	# }
	print('--------------------------')

###########################################
# 8. Chunk-Encoded Requests
# 分块传输,使用生成器或任意没有具体长度的迭代器
###########################################

def test_chunk_encoded():
	print('8: Chunk-Encoded Requests')
	def gen():
	    yield b'hi '
	    yield b'there! '
	    yield b'How are you?'
	    yield b'This is for test 123567890.....!'
	    yield b'Test ABCDEFG HIGKLMN OPQ RST UVWXYZ.....!'
	r=requests.post(Endpoint+'/post', data=gen())	 # stream=True
	print(r.status_code,r.reason,r.headers['content-length'])
	for chunk in r.iter_content(chunk_size=100):		# chunk_size=None
		if chunk:
			print(chunk)
	print('--------------------------')

###########################################
# 9. download file
###########################################

# 9.1 一次性下载（小文件，stream=False）
def test_download_stream_false(url):
	print('Test: Download file -- 一次性下载（小文件，stream=False）')
	try:
		r=requests.get(url)
		r.raise_for_status()
		print(r.status_code,r.reason)
		contentType=r.headers["Content-Type"]
		contentLength=int(r.headers.get("Content-Length",0))
		print(contentType,contentLength)
	except Exception as e:
		print(e)
	else:
		filename=r.url.split('/')[-1]
		print('filename:',filename)
		target=os.path.join('.',filename)
		if os.path.exists(target) and os.path.getsize(target):
			print('Exist -- Skip download!')
		else:
			with open(target,'wb') as fd:
				fd.write(r.content)
	print('--------------------------')

# 9.2: Download file -- 流式分块下载（大文件，stream=True)
def test_download_stream_true(url):
	print('Test: Download file -- 流式分块下载（大文件，stream=True)')
	try:
		r=requests.get(url,stream=True)
		r.raise_for_status()
		print(r.status_code,r.reason)
		contentType=r.headers["Content-Type"]
		contentLength=int(r.headers.get("Content-Length",0))
		print(contentType,contentLength)		
	except Exception as e:
		print(e)
	else:
		filename=r.url.split('/')[-1]
		print('filename:',filename)
		target=os.path.join('.',filename)
		if os.path.exists(target) and os.path.getsize(target):
			print('Exist -- Skip download!')
		else:
			with open(target,'wb') as fd:
				for chunk in r.iter_content(chunk_size=10240):
					if chunk:
						fd.write(chunk)
						print('download:',len(chunk))
	finally:
		r.close()
		print('close')
	print('--------------------------')

# 9.3 Download file -- 显示进度条
def test_download_with_progress(url):
	print('Test: Download file -- 显示进度条')
	try:
		with requests.get(url,stream=True) as r:
			r.raise_for_status()
			print(r.status_code,r.reason)
			
			contentType=r.headers["Content-Type"]
			contentLength=int(r.headers.get("Content-Length",0))
			print(contentType,contentLength)
			
			filename=r.url.split('/')[-1]
			print('filename:',filename)
			
			target=os.path.join('.',filename)
			if os.path.exists(target) and os.path.getsize(target):
				print('Exist -- Skip download!')
			else:
				chunk_size=1024
				progress=ProgressBar(filename, total=contentLength,chunk_size=chunk_size,unit="KB")
				with open(target,'wb') as fd:
					for chunk in r.iter_content(chunk_size=chunk_size):
						if chunk:
							fd.write(chunk)
							#print('download:',len(chunk))
							progress.refresh(count=len(chunk))
				
	except Exception as e:
		print(e)
	print('--------------------------')
	

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

# main			
if __name__ == '__main__':
	print('start')

	###########################################
	# 1. Response
	# 1.1 Response: status/encoding/headers
	# 1.2 Response: content / text / text using apparent_encoding
	# 1.3 Response: raw
	###########################################
	# test_response()
	# test_response_cnontent_text()
	# test_response_raw()

	###########################################
	# 2. Exception
	###########################################
	# test_exception()

	###########################################
	# 3. Requests method
	# 3.1: requests.get
	# 3.2: requests.head
	# 3.3: requests.post -- data:json
	# 3.4: requests.post -- data:string
	###########################################
	# test_requests_get()
	# test_requests_head()
	# test_requests_post_json()
	# test_requests_post_string()

	###########################################
	# 4 Requests args
	# 4.1: params
	# 4.2: data 表单参数
	# 4.3: json JSON参数
	# 4.4: headers
	# 4.5: auth - basic auth
	# 4.6: auth - oauth
	# 4.6: auth - advance:自定义身份验证（继承requests.auth.AuthBase）
	# 4.7: cookies
	# 4.8: timeout
	# 4.9: files - upload
	# 4.10: stream=True
	###########################################
	# test_args_params()
	# test_args_data()
	# test_args_json()
	# test_args_headers()
	# test_args_auth_basic()
	# test_args_auth_oauth()
	# test_args_auth_advance()
	# test_args_cookies()
	# test_args_timeout()
	# test_args_files_upload()
	# test_args_streams()

	###########################################
	# 5. Event Hooks
	###########################################
	# test_event_hooks()

	###########################################
	# 6. Session
	# 6.1: Session - 跨请求保持某些参数
	# 6.2: Session - 为请求方法提供缺省数据
	# 6.3: Session - 用作前后文管理器
	###########################################
	# test_session_cookie()
	# test_session_default()
	# test_session_context()

	###########################################
	# 7. Prepared Request
	###########################################
	# test_prepared_request()

	###########################################
	# 8. Chunk-Encoded Requests分块传输
	###########################################
	# test_chunk_encoded()

	###########################################
	# 9. Download file
	###########################################
	# url="http://image.ngchina.com.cn/2019/0319/20190319063405284.png"
	# test_download_stream_false(url)
	# test_download_stream_true(url)
	# test_download_with_progress(url)

	print('end')

###########################################


