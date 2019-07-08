import requests
from bs4 import BeautifulSoup
import os
import re
import logging
from datetime import datetime
	
def download_file(url,filename):
	pass
	
def parse_to_valid_filename(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  			# '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  		# 替换为下划线
    return new_title

def check_exist(filepath,filename):
	target=os.path.join(filepath,filename)
	if os.path.exists(target) and os.path.size(target)
		return True
	return False
	
def download_file(url,filepath,filename):
	proxy={
		"http":"http://cn-proxy.jp.oracle.com:80",
		"https":"http://cn-proxy.jp.oracle.com:80"
	}
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
	}
	try
		response=requests.get(url,headers=headers,proxies=proxy,stream=True)
		response.raise_for_status()
		
		contentType=response.headers["Content-Type"]
		print("request file: ",response.status_code,response.reason,contentType,response.headers.get("Content-Length",None))
		if contentType.startswith('text'):
			# print("Request Headers:",response.request.headers)
			# print("Response Headers:",response.headers)
			# print(response.content)
			print("Skip")
			logging.error("Skip Download [%s/%s] %s",filepath,filename,url)
		else:
			# processBar
			chunk_size = 1024 													# 单次请求最大值
			content_size = int(response.headers.get('Content-Length',0))		# 内容体总大小
			progress = ProgressBar(filename, total=content_size,unit="KB", chunk_size=chunk_size, run_status="downloading", fin_status="download completed")
			# write
			with open(os.path.join(filepath,filename),'wb') as fd:
				for chunk in response.iter_content(chunk_size=1024):
					if chunk:
						fd.write(chunk);
						progress.refresh(count=len(chunk))
	except exceptions.Timeout as e:
        print(e.message)
		logging.error("Download [%s] %s Timeout",filename,url)
    except exceptions.HTTPError as e:
        print(e.message)
		logging.error("Download [%s] %s HTTPError",filename,url)
	except: 
		logging.error("Download [%s] %s UnknowError",filename,url)

				
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
		

# test
# print(parse_to_valid_filename(" dd 【习语】Can you believe it? Level 1"))
# download_file('http://class.121talk.cn/Public/Uploads/Materials/509a656916585.pdf','.','demo.pdf')

		
##########################################################################

def main():
	
	Endpoint='https://class.121talk.cn'
	Teacher_URI='/business/Teachers/detail/id/3554'				
	Course_URI='/business/Students/getMtCatsByCsId/cs_id/'		# https://class.121talk.cn/business/Students/getMtCatsByCsId/cs_id/1080
	Category_URI='/business/Students/getMtsByMtCat/mt_cat/'		# https://class.121talk.cn/business/Students/getMtsByMtCat/mt_cat/10245
	Resource_URI='/Public/Uploads/Materials/'					# http://class.121talk.cn/Public/Uploads/Materials/509a656916585.pdf
	Cookie={'PHPSESSID':'m742kdp8v445pt6ebm3r5r1lm0'}
	
	Dir_Location='D:\\Space\\python\\yeko'				# D:\Space\python\yeko
	if not os.path.exists(Dir_Location):
		os.mkdir(Dir_Location)
	
	now=datetime.now()
	logfile=os.path.join(Dir_Location,"yeko-"+now.strftime('%Y%m%d%H%M%S')+".log")
	logging.basicConfig(level=logging.INFO,filename=logfile,format='%(message)s')	# format='%(name)s - %(levelname)s - %(message)s'
	
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
		,'Cookie':'PHPSESSID=m742kdp8v445pt6ebm3r5r1lm0'
	}
	response=requests.get(Endpoint+Teacher_URI,headers=headers)
	print(response.status_code,response.reason)
	soup=BeautifulSoup(response.content,'html.parser')
	courses=soup.select('select[name="cid"] > option')
	logging.info("Courses: \n %s \n ---------------------------------------------",courses)
	# print(courses)
	for course in courses:
		print('---------------------------------------------')
		print(course.get('value'),course.text)
		course_id=int(course.get('value'))
		if course_id == 0 :
			continue
		course_dir=os.path.join(Dir_Location,parse_to_valid_filename(course.text))
		if not os.path.exists(course_dir):
			os.mkdir(course_dir)
		print('course: ',course_dir)
		print('---------------------------------------------')
		
		# get categories
		logging.info("Categories")
		logging.info("GET %s",Endpoint+Course_URI+str(course_id))
		response=requests.get(Endpoint+Course_URI+str(course_id),headers=headers)
		print("get categories: ",response.status_code,response.reason)
		categories=response.json()
		logging.info("%s \n ---------------------------------------------",categories)
		# print(categories)
		for category in categories:
			print('++++++++++++++++++++++++++++++++++++++++++')
			print(category.get('id'),category.get('cname'))
			category_id=category.get('id')
			category_dir=os.path.join(course_dir,parse_to_valid_filename(category.get('cname')))
			if not os.path.exists(category_dir):
				os.mkdir(category_dir)
			print('category: ',category_dir)
			print('++++++++++++++++++++++++++++++++++++++++++')
			
			# get meterials
			logging.info("GET %s",Endpoint+Category_URI+str(category_id))
			response=requests.get(Endpoint+Category_URI+str(category_id),headers=headers)
			print("get meterials: ",response.status_code,response.reason)
			meterials=response.json()
			logging.info(meterials)
			for meterial in meterials:
				print(meterial.get("id"),meterial.get('pdf'),meterial.get('mt_name'))
				# download meterial
				filename=meterial.get('mt_name')+"."+meterial.get('pdf').split('.')[-1]
				print(filename)
				download_file(Endpoint+Resource_URI+meterial.get('pdf'),category_dir,parse_to_valid_filename(filename))
			print("finish category:",category.get('cname'))
		print("finish course:",course.text)
	print("Complete !")
	
	end_time=datetime.now()
	logging.info(end_time.strftime('%Y-%m-%d %H:%M:%S'))
	
# run 	
main()


