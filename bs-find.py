from bs4 import BeautifulSoup
from bs4 import element
import re
from collections import Iterator

def print_result(result):
	if type(result)==element.Tag or (not isinstance(result, Iterator) and len(result)==0):
		print(result)
		return
	for i,r in enumerate(result):
		print(i,":",r)
	print('-------------------------')

def print_result_name(result):
	if type(result)==element.Tag or (not isinstance(result, Iterator) and len(result)==0):
		print(result)
		return
	for i,r in enumerate(result):
		print(i,":",r.name)
	print('-------------------------')

#############################################
# 1.1 searching down: by `name`
#############################################

def test_find_all_with_tagname(soup):
	print('--- Demo: `find_all("a")` ---')
	result=soup.find_all('a')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: `find_all(["a","title"])` ---')
	result=soup.find_all(['a','title'])
	print_result(result)
	# 0 : <title>The Dormouse's story</title>
	# 1 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 2 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 3 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

def test_find_all_with_True(soup):
	print('--- Demo: `find_all(True)` ---')
	result=soup.find_all(True)
	print_result(result)
	# 0 : <html><head><title>The Dormouse's story</title></head> <body>
	# <p class="title"><b>The Dormouse's story</b></p>
	# <p class="story">
	# Once upon a time there were three little sisters; and their names were
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# </p>
	# <p class="story">...</p>
	# </body>
	# </html>
	# 1 : <head><title>The Dormouse's story</title></head>
	# 2 : <title>The Dormouse's story</title>
	# 3 : <body>
	# <p class="title"><b>The Dormouse's story</b></p>
	# <p class="story">
	# Once upon a time there were three little sisters; and their names were
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# </p>
	# <p class="story">...</p>
	# </body>
	# 4 : <p class="title"><b>The Dormouse's story</b></p>
	# 5 : <b>The Dormouse's story</b>
	# 6 : <p class="story">
	# Once upon a time there were three little sisters; and their names were
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# </p>
	# 7 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 8 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 9 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
	# 10 : <p class="story">...</p>

def test_find_all_with_re_compile(soup):
	print('--- Demo: `find_all(re.compile("b")` ---')
	result=soup.find_all(re.compile('b'))
	print_result(result)
	# 0 : <body>
	# <p class="title"><b>The Dormouse's story</b></p>
	# <p class="story">
	# Once upon a time there were three little sisters; and their names were
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# </p>
	# <p class="story">...</p>
	# </body>
	# 1 : <b>The Dormouse's story</b>

#############################################
# 1.2 searching down: by 'attrs'
#############################################

def test_find_all_with_attrs(soup):
	print('--- Demo: find_all("p","story") ---')
	result=soup.find_all('p','story')
	print_result(result)
	# 0 : <p class="story">
	# Once upon a time there were three little sisters; and their names were
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# </p>
	# 1 : <p class="story">...</p>

	print('--- Demo: find_all(id="link1") ---')
	result=soup.find_all(id='link1')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

	print('--- Demo: find_all(class_="sister") ---')
	result=soup.find_all(class_='sister')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: find_all(id=re.compile("link")) ---')
	result=soup.find_all(id=re.compile('link'))
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: find_all(attrs={"class":"story"}) ---')
	result=soup.find_all(attrs={'class':'story'})
	print_result(result)
	# 0 : <p class="story">
	# Once upon a time there were three little sisters; and their names were
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# </p>
	# 1 : <p class="story">...</p>

#############################################
# 1.3 searching down: by `recursive`
#############################################

def test_find_all_with_recursive(soup):
	print('--- Demo: find_all("a") ---')
	result=soup.find_all('a')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: find_all("a",recursive=False) ---')
	result=soup.find_all('a',recursive=False)
	print_result(result)
	# []

#############################################
# 1.4 searching down: by `string/text`
#############################################

def test_find_all_with_string(soup):
	print('--- Demo: find_all(string="three") ---')
	result=soup.find_all(string='three')
	print_result(result)
	# []

	print('--- Demo: find_all(string=re.compile("e")) ---')
	result=soup.find_all(string=re.compile('e'))
	print_result(result)
	# 0 : The Dormouse's story
	# 1 : The Dormouse's story
	# 2 :
	# Once upon a time there were three little sisters; and their names were
	#
	# 3 : Elsie
	# 4 : Lacie
	# 5 : Tillie
	# 6 : ; and they lived at the bottom of a well.

#############################################
# 1.5 searching down : by `limit` -- find()也就是当limit=1时的find_all()
#############################################

def test_find_all_with_limit(soup):
	print('--- Demo: find_all("a",limit=2) ---')
	result=soup.find_all('a',limit=2)
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

#############################################
# 1.6 searching down : by `self def function`
#############################################

def test_find_all_with_filter(soup):
	print('--- Demo: using `self def function` ---')
	def my_filter(tag):
		return tag.has_attr('id') and re.match('link',tag.get("id"))

	result=soup.find_all(my_filter)
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

#############################################
# 2. searching up: `find_parents`
#############################################

def test_find_parents(soup):
	print('--- Demo: link2.`find_parents()` ---')
	result=soup.find(id="link2").find_parents()
	print_result_name(result)
	# 0 : p
	# 1 : body
	# 2 : html
	# 3 : [document]

def test_find_parents(soup):
	print('--- Demo: link2.`find_parents("p")` ---')
	result=soup.find(id="link2").find_parents('p')
	print_result(result)
	# 0 : <p class="story">
	# Once upon a time there were three little sisters; and their names were
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
	# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# </p>

#############################################
# 3. searching sideway: `find_next_siblings`
#############################################

def test_find_next_siblings(soup):
	print('--- Demo: `find_next_siblings()` ---')
	result=soup.find(id="link1").find_next_siblings()
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 1 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

#############################################
# 4. searching forth and back: `find_all_next`
#############################################

def test_find_all_next(soup):
	print('--- Demo: `find_all_next()` ---')
	result=soup.find(id="link1").find_all_next()
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 1 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
	# 2 : <p class="story">...</p>

#############################################

if __name__=='__main__':
	content='''
	<html><head><title>The Dormouse's story</title></head> <body>
	<p class="title"><b>The Dormouse's story</b></p>
	<p class="story">
	Once upon a time there were three little sisters; and their names were
	<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.
	</p>
	<p class="story">...</p>
	</body>
	</html>
	'''
	soup=BeautifulSoup(content,'html.parser')
	print(soup.prettify())

	# 1.1 searching down: by `name`
	test_find_all_with_tagname(soup)
	test_find_all_with_True(soup)
	test_find_all_with_re_compile(soup)

	# 1.2 searching down: by 'attrs'
	test_find_all_with_attrs(soup)

	# 1.3 searching down: by `recursive`
	test_find_all_with_recursive(soup)
	
	# 1.4 searching down: by `string/text`
	test_find_all_with_string(soup)
	
	# 1.5 searching down : by `limit` -- find()也就是当limit=1时的find_all()
	test_find_all_with_limit(soup)
	
	# 1.6 searching down : by `self def function`
	test_find_all_with_filter(soup)
	
	# 2. searching up: `find_parents`
	test_find_parents(soup)
	test_find_parents(soup)
	
	# 3. searching sideway: `find_next_siblings`
	test_find_next_siblings(soup)
	
	# 4. searching forth and back: `find_all_next`
	test_find_all_next(soup)

	print('end!')

#############################################




