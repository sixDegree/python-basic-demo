#coding=utf-8

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
# 1. 基础选择
# `#id`
# `tagName`
# `.styleClass`
#############################################

# 1.1 selector by tag `id`
def test_select_with_id(soup):
	print('--- Demo: `select("#link1")` ---')
	result=soup.select("#link1")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

	print('--- Demo: `select("a#link1")` ---')
	result=soup.select("a#link2")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

# 1.2 selector by tag `name`
def test_select_with_name(soup):
	print('--- Demo: `select("title")` ---')
	result=soup.select("title")
	print_result(result)
	# 0 : <title>The Dormouse's story</title>

# 1.3 selector by tag `class`
def test_select_with_class(soup):
	print('--- Demo: `select(".sister")` ---')
	result=soup.select(".sister")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>


#############################################
# 2. 属性过滤
# `[attribute]`
# `[attribute=value]`
# `[attribute!=value]`
# `[attribute^=value]`
# `[attribute$=value]`
# `[attribute*=value]`
# `[selector1][selector2][selectorN]`
#############################################

def test_select_with_attr(soup):
	print('--- Demo: `select("a[href]")` ---')
	result=soup.select('a[href]')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: `select("a[href^="http://example.com/"]")` ---')
	result=soup.select('a[href^="http://example.com/"]')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: `select("a[href$="tillie"])` ---')
	result=soup.select('a[href$="tillie"]')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: `select("a[href*=".com/el"]")` ---')
	result=soup.select('a[href*=".com/el"]')
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

	print('--- Demo: `select("[class=sister]")` ---')
	result=soup.select("[class=sister]")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print("--- Demo: `[class=sister][id=link2]` --- ")
	print_result(soup.select("[class=sister][id=link2]"))
	# 0 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>


#############################################
# 3. 层级选择
# `ancestor descendent`
# `parent > child`
# `prev + next` ：next sibling tag
# `prev ~ siblings` ：next all sibling tags
#############################################

def test_select_down(soup):	
	print('--- Demo: `select("body a")` ---')
	result=soup.select("body a")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: `select("body > a") ---')
	result=soup.select("body > a")
	print_result(result)
	# []

	print('--- Demo: `select("p > a") ---')
	result=soup.select("p > a")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: `select("p > a:nth-of-type(2)")` ---')
	result=soup.select("p > a:nth-of-type(2)")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

	print('--- Demo: `select("p > #link1")` ---')
	result=soup.select("p > #link1")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

def test_select_sibling(soup):
	print('--- Demo: `select("#link1 ~ .sister")` ---')
	result=soup.select("#link1 ~ .sister")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 1 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

	print('--- Demo: `select("#link1 + .sister")` ---')
	result=soup.select("#link1 + .sister")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

#############################################
# 4. 元素过滤
# `:not(selector)`
# `:nth-of-type(index)`
# `:nth-child(index)`
# `:first-child`
# `:last-child`
# `:only-child`
#############################################

def test_select_with_element_filter(soup):
	print("--- Demo: `:not(.story)` --- ")
	print_result(soup.select("p:not(.story)"))
	# 0 : <p class="title"><b>The Dormouse's story</b></p>

	print('--- Demo: `select("p:nth-of-type(3)")` ---')
	result=soup.select("p:nth-of-type(3)")
	print_result(result)
	# 0 : <p class="story">...</p>

	print("--- Demo: `p > :first-child` --- ")
	print_result(soup.select("p > :first-child"))
	# 0 : <b>The Dormouse's story</b>
	# 1 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

	print("--- Demo: `p > :nth-child(1)` --- ")
	print_result(soup.select("p > :nth-child(1)"))
	# 0 : <b>The Dormouse's story</b>
	# 1 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

	print("--- Demo: `p > :last-child` --- ")
	print_result(soup.select("p > :last-child"))
	# 0 : <b>The Dormouse's story</b>
	# 1 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

	print("--- Demo: `p > :only-child` --- ")
	print_result(soup.select("p > :only-child"))
	# 0 : <b>The Dormouse's story</b>

#############################################
# 5. 内容过滤
# `:contains(text)`
# `:empty`
# `:has(selector)`
#############################################

def test_select_with_content_filter(soup):
	print("--- Demo: `p:contains(story)` --- ")
	print_result(soup.select("p:contains(story)"))
	# 0 : <p class="title"><b>The Dormouse's story</b></p>

	print("--- Demo: `p:empty` --- ")
	print_result(soup.select("p:empty"))
	# []

	print("--- Demo: `p:has(b)` --- ")
	print_result(soup.select("p:has(b)"))
	# 0 : <p class="title"><b>The Dormouse's story</b></p>

#############################################
# 6 表单属性过滤
# `:enabled`
# `:disabled`
# `:checked`
#############################################

def test_select_with_form_attrs(soup):
	print("--- Demo: `:disabled`` --- ")
	print_result(soup.select(":disabled"))
	# 0 : <input disabled="" type="text" value="input something"/>

#############################################
# 7. selector list/one
# `selector1, selector2, selectorN`
#############################################

def test_select_multi(soup):
	print('--- Demo: `select("#link1,#link2")` ---')
	result=soup.select("#link1,#link2")
	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

def test_select_one(soup):
	print('--- Demo: `select_one(".sister")` ---')
	result=soup.select_one(".sister")
	print_result(result)
	# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

#############################################
# 8. get attribute value
# `.get_text()`,`.attrs['...']`
#############################################

def test_get_attribute_value(soup):
	print('--- Demo: `get attribute value` ---')
	result=soup.select(".sister")

	print_result(result)
	# 0 : <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
	# 1 : <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
	# 2 : <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
	
	print(result[0].get_text())
	#Elsie

	print(result[0].attrs)
	#{'href': 'http://example.com/elsie', 'class': ['sister'], 'id': 'link1'}
	
	print(result[0].attrs['id'])
	#link1

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
	<input type="text" disabled value="input something"></input>
	</body>
	</html>
	'''

	soup=BeautifulSoup(content,'html.parser')
	print(soup.prettify())

	#############################################
	# 1. 基础选择
	# `#id`
	# `tagName`
	# `.styleClass`
	#############################################
	test_select_with_id(soup)
	test_select_with_name(soup)
	test_select_with_class(soup)
	
	#############################################
	# 2. 属性过滤
	# `[attribute]`
	# `[attribute=value]`
	# `[attribute!=value]`
	# `[attribute^=value]`
	# `[attribute$=value]`
	# `[attribute*=value]`
	# `[selector1][selector2][selectorN]`
	#############################################
	test_select_with_attr(soup)

	#############################################
	# 3. 层级选择
	# `ancestor descendent`
	# `parent > child`
	# `prev + next` ：next sibling tag
	# `prev ~ siblings` ：next all sibling tags
	#############################################
	test_select_down(soup)
	test_select_sibling(soup)

	#############################################
	# 4. 元素过滤
	# `:not(selector)`
	# `:nth-of-type(index)`
	# `:nth-child(index)`
	# `:first-child`
	# `:last-child`
	# `:only-child`
	#############################################
	test_select_with_element_filter(soup)

	#############################################
	# 5. 内容过滤
	# `:contains(text)`
	# `:empty`
	# `:has(selector)`
	#############################################
	test_select_with_content_filter(soup)

	#############################################
	# 6 表单属性过滤
	# `:enabled`
	# `:disabled`
	# `:checked`
	#############################################
	test_select_with_form_attrs(soup)

	#############################################
	# 7. selector list/one
	# `selector1, selector2, selectorN`
	#############################################
	test_select_multi(soup)
	test_select_one(soup)

	#############################################
	# 8. get attribute value
	# `.get_text()`,`.attrs['...']`
	#############################################
	test_get_attribute_value(soup)

	print('end!')

#############################################

