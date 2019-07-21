# print
print('--- Print --- ')
print('100+200='+str(100+200))
print('100+200=',100+200)

# input
print('--- Inport --- ')
name=input('input name:')
print('Hello '+name)

# function
print('--- Function --- ')
def say(word):
	print('say:',word)
	
say("Hello")

# module
print('--- Module --- ')
import sys
def test():
	args=sys.argv
	if(len(args)==1):
		print('Hello,world')
	elif(len(args)==2):
		print('Hello,%s' % args[1])
	else:
		print('Too many args')

if __name__=='__main__':
	test()
	
# class
print('--- Class --- ')
class Student(object):
	def __init__(self,name,score):
		self.name=name
		self.score=score
		
	def printScore(self):
		print('%s:%s' % (self.name,self.score))
		
stuA=Student('StuA',59)
stuB=Student('StuB',70)
stuA.printScore()
stuB.printScore()

# log
print('--- Log --- ')
import logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO,filename="parse.log")
logging.info('This is log!')

# json
print('--- Json --- ')
import json
p=dict(name="Tom",age=22,score=80)
print(json.dumps(p))
b_str= '{ "name": "Bob","age": 20, "score": 88}'
b=json.loads(b_str)
print(b)

def student2dict(stu):
	return {"name":stu.name,"score":stu.score}

def dict2student(d):
	return Student(d["name"],d["score"])

stuC=Student("Lili",90)	
stuC_str=json.dumps(stuC,default=student2dict)
print("stuC:"+stuC_str)
stuD_str='{"name":"Susan","score":80}'
stuD=json.loads(stuD_str,object_hook=dict2student)
print(stuD)
print("name:%s,score:%s" % (stuD.name,stuD.score))

print(json.dumps(stuC, default=lambda obj: obj.__dict__))

# requests
print('--- Requests(params) --- ')
import requests

api_endpoint='https://api.github.com'

resp=requests.get(api_endpoint+"/users", params={'since': 45})	
print(resp)
print(resp.request.headers)
print(resp.json())

print('--- Requests(auth) ---')
resp=requests.get(api_endpoint+"/user",auth=('imoocdemo','imoocdemo123'))
print(resp)
print(resp.request.headers)
print(resp.json())

print('--- Requests(patch) ---')
resp=requests.get(api_endpoint+"/user/emails",auth=('imoocdemo','imoocdemo123'))
print(resp.json())
resp=requests.patch(api_endpoint+"/user",auth=('imoocdemo','imoocdemo123'),json={'location':'China'})
print(resp)
print(resp.request.headers)
print(resp.json())
print("Updated Location: ",resp.json()["location"])
print("Updated Email: ",resp.json()["email"])

print('--- Requests(post) ---')
repository={
  "name": "Hello-World",
  "description": "This is your first repository",
  "homepage": "https://github.com",
  "private": True,
  "has_issues": True,
  "has_projects": True,
  "has_wiki": True
}
resp=requests.post(api_endpoint+"/user/repos",auth=('imoocdemo','imoocdemo123'),json=repository)
print(resp)
print(resp.request.headers)
print(resp.json())

# hooks
print('--- Request(hooks) --- ')
def get_key_info(response,*args,**kwargs):
	print(response.headers['Content-Type'])
	
resp=requests.get(api_endpoint,hooks={"response":get_key_info})

# auth
print('--- OAUTH ---')
resp=requests.get(api_endpoint+"/authorizations",auth=('imoocdemo','imoocdemo123'));
print(resp)
print(resp.request.headers)
print(resp.json())

# 'Authorization': 'Basic aW1vb2NkZW1vOmltb29jZGVtbzEyMw=='
from requests.auth import AuthBase
class GithubAuth(AuthBase):
	def __init__(self,token):
		self.token=token
	def __call__(self,req):
		req.headers["Authorization"]=' '.join(['Basic',self.token])
		return req

auth=GithubAuth("aW1vb2NkZW1vOmltb29jZGVtbzEyMw")
resp=requests.get(api_endpoint+"/user/emails",auth=auth)
print(resp)
print(resp.request.headers)
print(resp.json())

# download
print('--- Download ---')
def download_image(url):
    headers={'User-Agent':'Mozilla/5.0'}
    response=requests.get(url,stream=True)
    print(response.status_code,response.reason)
    print(response.headers)
    # print response.content
    with open('demo1.jpg','wb') as fd:
       fd.write(response.content)
	   
download_file('https://static.googleusercontent.com/media/www.google.com/en//googleblogs/pdfs/google_predicting_the_present.pdf')



from datetime import datetime
now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))
print(now.strftime('%Y-%m-%d %H:%M:%S'))


print('--- Log --- ')
import logging

# logging.basicConfig(level=logging.INFO,filename="parse.log")
now=datetime.now()
logfile=os.path.join(Dir_Location,"parse-"+now.strftime('%Y%m%d%H%M%S')+".log")
logging.basicConfig(level=logging.INFO,filename=logfile,format='%(message)s')	# format='%(name)s - %(levelname)s - %(message)s'
logging.info('This is log!')


