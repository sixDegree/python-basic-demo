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
	if type(result)==element.Tag or type(result)==element.NavigableString or (not isinstance(result, Iterator)and len(result)==0):
		print(result)
		return
	for i,r in enumerate(result):
		print(i,":",r.name)
	print('-------------------------')

#############################################
# 1. Tag `name`,`attrs`
#############################################

def test_tag_name_and_attrs(soup):
	print('--- Demo: Tag <p> ---')

	print("soup.p:",soup.p)
	# <p class="highlight" id="test1">
	#                 Hello <a>Tom</a>
	#                 Nice to meet you <!-- This is a comment -->
	# </p>
	print("soup.p.name:",soup.p.name)
	# p
	print("soup.p.attrs:",soup.p.attrs)
	# {'id': 'test1', 'class': ['highlight']}
	print("soup.p.attr['class']:",soup.p.attrs["class"])
	# ['highlight']
	print("soup.p.attrs['id']:",soup.p.attrs["id"])
	#  test1
	print("soup.p['class']:",soup.p["class"])
	#['highlight']
	print("-----------------------------------")

#############################################
# 2. Tag `text`/`string`
#############################################

def test_tag_p_text(soup):
	print('--- Demo: Tag <p> text ---')
	print("soup.p.text:",soup.p.text)
	#
	#                Hello Tom
	#                Nice to meet you
	#
					
	print("soup.p.get_text():",soup.p.get_text())
	#
	#                Hello Tom
	#                Nice to meet you
	#
		
	print("type(soup.p.get_text()):",type(soup.p.get_text()))	# <class 'str'>
	print("-----------------------------------")

def test_tag_p_string(soup):
	print('--- Demo: Tag <p> string ---')
	print("soup.p.string:",soup.p.string)				# None
	print("type(soup.p.string)",type(soup.p.string))	# <class 'NoneType'>
	print("soup.p.strings:",soup.p.strings)				# <generator object Tag._all_strings at 0x00000000028FDD68>
	for i,s in enumerate(soup.p.strings):
	    print(i,":",s)
	print("-----------------------------------")    
	# 0 :
	#                 Hello
	# 1 : Tom
	# 2 :
	#                 Nice to meet you
	# 3 :

def test_tag_text_and_string(soup):
	print('--- Demo: Tag <a> text/string ---')
	print("soup.a.text:",soup.a.text)						# Chat with sb
	print("soup.a.string:",soup.a.string)					# Chat with sb
	print("type(soup.a.string):",type(soup.a.string))		# <class 'bs4.element.NavigableString'>
	print("-----------------------------------")

	print('--- Demo: Tag <b> text/string ---')
	print("soup.b.text:",soup.b.text)						# This is title
	print("soup.b.string:",soup.b.string)					# None
	print("type(soup.b.string):",type(soup.b.string))		# <class 'NoneType'>
	print("-----------------------------------")

	print('--- Demo: Tag <i> text/string ---')
	print("soup.i.text:",soup.i.text)						#
	print("soup.i.string:",soup.i.string)					# This is comment
	print("type(soup.i.string):",type(soup.i.string))		# <class 'bs4.element.Comment'>
	print("-----------------------------------")

#############################################
# 3. going down: `contents`,`children`,`decendants`
#############################################

def test_tag_p_contents(soup):
	print('--- Demo: Tag <p> contents ---')
	print(type(soup.p.contents))	#  <class 'list'>
	print_result(soup.p.contents)
	# 0 :
	#                 Hello
	# 1 : <a>Tom</a>
	# 2 :
	#                 Nice to meet you
	# 3 :  This is a comment
	# 4 :

def test_tag_p_children(soup):
	print('--- Demo: Tag <p> children ---')
	print(soup.p.children)			# <list_iterator object at 0x0000000001E742E8>
	print_result(soup.p.children)
	# 0 :
	#                 Hello
	# 1 : <a>Tom</a>
	# 2 :
	#                 Nice to meet you
	# 3 :  This is a comment
	# 4 :

def test_tag_p_descendants(soup):
	print('--- Demo: Tag <p> descendants ---')
	print(soup.p.descendants)		# <generator object Tag.descendants at 0x00000000028ADD68>
	print_result(soup.p.descendants)
	# 0 :
	#                 Hello
	# 1 : <a>Tom</a>
	# 2 : Tom
	# 3 :
	#                 Nice to meet you
	# 4 :  This is a comment
	# 5 :

#############################################
# 4. going up: `parent`,`parents`
#############################################

def test_tag_p_parent(soup):
	print('--- Demo: Tag <p> parent ---')
	print(type(soup.p.parent))		# <class 'bs4.element.Tag'>
	print_result(soup.p.parent)
	# <div id="div2">
	# <p class="highlight" id="test1">
	#                 Hello <a>Tom</a>
	#                 Nice to meet you <!-- This is a comment -->
	# </p>
	# <p class="story" id="test2">Story1</p>
	# <p class="story" id="test3">Story2</p>
	# </div>

def test_tag_p_parents(soup):
	print('--- Demo: Tag <p> parents ---')
	print(soup.p.parents)			# <generator object PageElement.parents at 0x00000000028FDD68>
	print_result_name(soup.p.parents)
	# 0 : div
	# 1 : div
	# 2 : [document]

#############################################
# 5. going sideway: next_sibling,next_siblings vs. find_next_siblings()
#############################################

def test_tag_p_next_sibling(soup):
	print('--- Demo: Tag <p> next_sibling ---')
	print_result(soup.p.next_sibling)
	# 0 :

def test_tag_p_next_siblings(soup):
	print('--- Demo: Tag <p> next_siblings ---')
	print(soup.p.next_siblings)		# <generator object PageElement.next_siblings at 0x00000000028FDD68>
	print_result(soup.p.next_siblings)
	# 0 :
	# 
	# 1 : <p class="story" id="test2">Story1</p>
	# 2 :
	# 
	# 3 : <p class="story" id="test3">Story2</p>
	# 4 :

def test_tag_p_find_next_siblings(soup):
	print('--- Demo: `find_next_siblings()` ---')
	result=soup.p.find_next_siblings()
	print_result(result)
	# 0 : <p class="story" id="test2">Story1</p>
	# 1 : <p class="story" id="test3">Story2</p>
	
#############################################
# 6. going forth and back: next_element,next_elements vs. find_all_next()
#############################################

def test_tag_p_next_element(soup):
	print('--- Demo: Tag <p> next_element ---')
	print(soup.p.next_element)
	#
	# Hello
	print(type(soup.p.next_element))
	# <class 'bs4.element.NavigableString'>

def test_tag_p_next_elements(soup):
	print('--- Demo: Tag <p> next_elements ---')
	print(soup.p.next_elements)		# <generator object PageElement.next_elements at 0x00000000028FDD68>
	print_result(soup.p.next_elements)
	# 0 :
	#                 Hello
	# 1 : <a>Tom</a>
	# 2 : Tom
	# 3 :
	#                 Nice to meet you
	# 4 :  This is a comment
	# 5 :
	# 
	# 6 :
	# 
	# 7 : <p class="story" id="test2">Story1</p>
	# 8 : Story1
	# 9 :
	# 
	# 10 : <p class="story" id="test3">Story2</p>
	# 11 : Story2
	# 12 :
	# 
	# 13 :
	# 
	# 14 :

def test_tag_p_find_all_next(soup):
	print('--- Demo: `find_all_next()` ---')
	result=soup.p.find_all_next()
	print_result(result)
	# 0 : <a>Tom</a>
	# 1 : <p class="story" id="test2">Story1</p>
	# 2 : <p class="story" id="test3">Story2</p>

#############################################

# main
if __name__=='__main__':
	content='''
	<a>Chat with sb</a>
	<b> This is title  <!-- Guess --> </b>
	<i><!--This is comment--></i>
	<div id="div1">
	    <div id="div2">
	        <p id="test1" class="highlight">
	        	Hello <a>Tom</a>
	        	Nice to meet you <!-- This is a comment -->
	        </p>
			<p id="test2" class="story">Story1</p>
			<p id="test3" class="story">Story2</p>
	    </div>
	</div>
	'''

	soup=BeautifulSoup(content,'html.parser')
	print(soup.prettify())

	# 1. Tag `name`,`attrs`
	test_tag_name_and_attrs(soup)

	# 2. Tag `text`/`string`
	test_tag_p_text(soup)
	# test_tag_p_string(soup)
	# test_tag_text_and_string(soup)

	# # 3. going down: `contents`,`children`,`decendants`
	# test_tag_p_contents(soup)
	# test_tag_p_children(soup)
	# test_tag_p_descendants(soup)

	# # 4. going up: `parent`,`parents`
	# test_tag_p_parent(soup)
	# test_tag_p_parents(soup)

	# # 5. going sideway: next_sibling,next_siblings vs. find_next_siblings()
	# test_tag_p_next_sibling(soup)
	# test_tag_p_next_siblings(soup)
	# test_tag_p_find_next_siblings(soup)

	# # 6. going forth and back: next_element,next_elements vs. find_all_next()
	# test_tag_p_next_element(soup)
	# test_tag_p_next_elements(soup)
	# test_tag_p_find_all_next(soup)

	print('end!')

#############################################

