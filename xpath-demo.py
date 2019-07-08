from lxml import etree

def do_xpath(root,path):
	result=root.xpath(path)
	print("%s : \n%s" % (path,result))
	return result

def do_xpath_detail(root,path):
	result=root.xpath(path)
	print(path,":")
	if type(result)==list and len(result)>0:
		for i,r in enumerate(result):
			if type(r)==etree._Element:
				print(i,":",etree.tounicode(r))
			else:
				print(i,":",r)
	else:
		print(result)
	return result

def test_path_any(root):
	print("--- `//` ----")
	do_xpath(root,'p')
	# []
	do_xpath(root,'//p')
	# [<Element p at 0x109f34148>, <Element p at 0x109f34188>, <Element p at 0x109f34248>, <Element p at 0x109f34288>]
	do_xpath(root,'//p/a/text()')
	# ['Elsie', 'Lacie', 'Tillie', 'Miss']
	do_xpath(root,'//p//a/text()')
	# ['Elsie', 'Lacie', 'Tillie', ' World ', 'Miss']
	do_xpath(root,'.//a/text()')
	# ['Elsie', 'Lacie', 'Tillie', ' World ', 'Miss']

	print('--- `xpath` ---')
	print(root.xpath("//p/b//a"))
	# [<Element a at 0x10b555f08>]
	print(root.xpath("//p/b")[1].xpath("//a"))
	# [<Element a at 0x10b555f08>, <Element a at 0x10b5770c8>, <Element a at 0x10b577108>, <Element a at 0x10b577048>, <Element a at 0x10b577088>]
	print(root.xpath("//p/b")[1].xpath("./a"))
	# [<Element a at 0x10c719f48>]
	print(root.xpath("//p/b")[1].xpath("../text()"))
	# [' hello ...', ' ']
	print(root.xpath('//p/b/..//a')[0].text)
	# World
	print('------------------------')

def test_path_direct(root):
	print("--- `/` ----")
	do_xpath(root,'/div')
	# []
	do_xpath(root,'/html')
	# [<Element html at 0x10cd7a388>]
	do_xpath(root,'/html/body/div/p')
	# [<Element p at 0x10fdcc908>, <Element p at 0x1104f8388>, <Element p at 0x1104f8308>, <Element p at 0x1104f82c8>]
	do_xpath(root,'//p/a')
	# [<Element a at 0x104550488>, <Element a at 0x1045504c8>, <Element a at 0x104550588>, <Element a at 0x1045505c8>]
	print('------------------------')

def test_path_element(root):
	print("--- `lxml.etree._Element` ----")
	result=root.xpath("//p/b")
	for i,r in enumerate(result):
		print(i,type(r),":",r.tag,r.attrib,r.get('class'),r.text,r.xpath('string(.)'))
	# 0 <class 'lxml.etree._Element'> : b {'class': 'bstyle'} bstyle The Dormouse's story The Dormouse's story
	# 1 <class 'lxml.etree._Element'> : b {} None None  World
	print('------------------------')

def test_path_attr(root):
	print("--- `@` ----")
	do_xpath(root,'/@class')
	# []
	do_xpath(root,'//@class')
	# ['title', 'bstyle', 'story', 'sister', 'sister', 'sister', 'story', 'outAstyle']
	
	do_xpath(root,'//p[@class]')
	# [<Element p at 0x10e4c3888>, <Element p at 0x10e4c36c8>, <Element p at 0x10e4c3708>]
	do_xpath(root,"//p[@class='story']")
	# [<Element p at 0x110ba8708>, <Element p at 0x110ba8548>]

	do_xpath(root,"//p/@class")
	# ['title', 'story', 'story']
	do_xpath(root,"//p[@class='story']/@class")
	# ['story', 'story']
	do_xpath(root,"//p[@class='story']//@class")
	# ['story', 'sister', 'sister', 'sister', 'story', 'outAstyle']
	print('------------------------')

def test_path_predicates(root):
	print("--- `[]` ----")
	do_xpath_detail(root,'//p[1]')
	# 0 : <p class="title"><b class="bstyle">The Dormouse's story</b></p>
	do_xpath_detail(root,'//p[last()]')
	# 0 : <p class="story">...<a class="outAstyle">Miss</a> </p>
	do_xpath_detail(root,'//p[last()-1]')
	# 0 : <p> hello ...<b><a> World </a></b> </p>

	do_xpath_detail(root,'//a[1]')
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a> World </a>
	# 2 : <a class="outAstyle">Miss</a>
	do_xpath_detail(root,'//p/a[1]')
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a class="outAstyle">Miss</a>
	do_xpath_detail(root,'//a[position()<=2]')
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	# 2 : <a> World </a>
	# 3 : <a class="outAstyle">Miss</a>

	do_xpath_detail(root,'//a[@class]')
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	# 2 : <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# 3 : <a class="outAstyle">Miss</a>
	do_xpath_detail(root,'//a[@class="outAstyle"]')
	# 0 : <a class="outAstyle">Miss</a>

	do_xpath_detail(root,'//p[b]')
	# 0 : <p class="title"><b class="bstyle">The Dormouse's story</b></p>
	# 1 : <p> hello ...<b><a> World </a></b> </p>
	do_xpath_detail(root,"//p[b/@class]")
	# 0 : <p class="title"><b class="bstyle">The Dormouse's story</b></p>
	do_xpath_detail(root,"//p[b[@class='bstyle']]")
	# 0 : <p class="title"><b class="bstyle">The Dormouse's story</b></p>
	print('------------------------')

def test_path_wildcard(root):
	print("--- `*` ----")
	do_xpath_detail(root,"//p/*")
	# 0 : <b class="bstyle">The Dormouse's story</b>
	# 1 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 2 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	# 3 : <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# 4 : <b><a> World </a></b>
	# 5 : <a class="outAstyle">Miss</a>

	do_xpath_detail(root,"//p//*")
	# 0 : <b class="bstyle">The Dormouse's story</b>
	# 1 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 2 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	# 3 : <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.
	# 4 : <b><a> World </a></b>
	# 5 : <a> World </a>
	# 6 : <a class="outAstyle">Miss</a>

	do_xpath_detail(root,"//p/*/a")
	# 0 : <a> World </a>

	do_xpath_detail(root,"//b[@*]")
	# 0 : <b class="bstyle">The Dormouse's story</b>

	do_xpath_detail(root,"//*[@class='sister']")
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	# 2 : <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.
	print('------------------------')

def test_path_multi(root):
	print("--- `|` ----")
	do_xpath_detail(root,"//p/a[@class='outAstyle']|//p/b[@class]")
	# 0 : <b class="bstyle">The Dormouse's story</b>
	# 1 : <a class="outAstyle">Miss</a>
	print('------------------------')

def test_path_and_or_not(root):
	print("--- `and` ----")
	do_xpath_detail(root,"//a[@class='sister' and @id='link2']")
	# 0 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	do_xpath_detail(root,"//a[@class='sister'][@id='link2']")
	# 0 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	
	print("--- `or` ----")
	do_xpath_detail(root,"//a[@id='link1' or @class='outAstyle']")
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a class="outAstyle">Miss</a>
	
	print("--- `not` ----")
	do_xpath_detail(root,"//a[not(@class='sister')]")
	# 0 : <a> World </a>
	# 1 : <a class="outAstyle">Miss</a>

	print("--- `and & or & not` ----")
	do_xpath_detail(root,"//a[not(@class='sister') and @class or @id='link1']")
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a class="outAstyle">Miss</a>
	print('------------------------')

def test_path_func(root):
	print("--- `starts-with()` ----")
	do_xpath_detail(root,"//a[starts-with(@href,'http://example.com/')]")
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	# 2 : <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.

	print("--- `contains()` ----")
	do_xpath_detail(root,"//a[contains(text(),'ie') and contains(@id,'link')]")
	# 0 : <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 1 : <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>and
	# 2 : <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.
	do_xpath_detail(root,"//b[contains(text(),'World')]")
	# []

	print("--- `text()` ----")
	do_xpath(root,"//b/text()")
	# ["The Dormouse's story"]
	do_xpath(root,"//b//text()")
	# ["The Dormouse's story", ' World ']

	print("--- `string(.)` ----")
	result=do_xpath(root,"//b")
	for r in result:
		print(r.xpath('string(.)'))
	# The Dormouse's story
 	# World
	print('------------------------')

def test_path_self(root):
	print("--- `self::` ----")
	do_xpath_detail(root,"//self::b")
	# 0 : <b class="bstyle">The Dormouse's story</b>
	# 1 : <b><a> World </a></b>

	print("--- `attribute::` ----")
	do_xpath(root,"//a/attribute::*")
	# ['http://example.com/elsie', 'sister', 'link1', 'http://example.com/lacie', 'sister', 'link2', 'http://example.com/tillie', 'sister', 'link3', 'outAstyle']
	do_xpath(root,"//a/attribute::class")
	# ['sister', 'sister', 'sister', 'outAstyle']
	
	print('------------------------')

def test_path_up(root):
	print("--- `parent::` ----")
	do_xpath(root,"//a/ancestor::p")
	# [<Element p at 0x102291c88>, <Element p at 0x102291cc8>, <Element p at 0x102291d88>]
	
	print("--- `parent::` ----")
	do_xpath(root,"//a/parent::p")
	# [<Element p at 0x102291c88>, <Element p at 0x102291cc8>]
	print('------------------------')

def test_path_down(root):
	print("--- `descendant::` ----")
	do_xpath(root,"//p/descendant::a[not(@class)]")
	# [<Element a at 0x102786e48>]

	print("--- `child::` ----")
	do_xpath(root,"//p/child::a[not(@class)]")
	# []
	print('------------------------')

def test_path_sideway(root):
	print("--- `following::`,`following-sibling::` ----")
	do_xpath(root,"//p[last()-1]/following::*")
	# [<Element p at 0x1040fcf08>, <Element a at 0x1040fcfc8>]
	do_xpath(root,"//p[last()-1]/following-sibling::*")
	# [<Element p at 0x1040fcf08>]

	print("--- `preceding::`,`preceding-sibling::` ----")
	do_xpath(root,"//p[2]/preceding::*")
	# [<Element p at 0x109089d08>, <Element b at 0x109089dc8>]
	do_xpath(root,"//p[2]/preceding-sibling::*")
	# [<Element p at 0x109089dc8>]
	print('------------------------')


if __name__=='__main__':
	print('start')
	content='''
	<div>
		<p class="title"><b class='bstyle'>The Dormouse's story</b></p>
		<p class="story">
			Once upon a time there were three little sisters; and their names were
			<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
			<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
			and <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
			; and they lived at the bottom of a well.
			<p> hello ...<b><a> World </a></b> </p>
		</p>
		<p class="story">...<a class="outAstyle">Miss</a> </p>
	</div>
	'''

	# html = etree.parse('./test.html',etree.HTMLParser())
	html = etree.HTML(content)
	print(html)
	# <Element html at 0x1019312c8>

	# result = etree.tostring(html)		# 会补全缺胳膊少腿的标签
	# print(result.decode("utf-8"))
	print(etree.tounicode(html))		# 会补全缺胳膊少腿的标签
	# <html><body><div>
	# 	<p class="title"><b class="bstyle">The Dormouse's story</b></p>
	# 	<p class="story">
	# 		Once upon a time there were three little sisters; and their names were
	# 		<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	# 		<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
	# 		and <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
	# 		; and they lived at the bottom of a well.
	# 		</p><p> hello ...<b><a> World </a></b> </p>
	# 	<p class="story">...<a class="outAstyle">Miss</a> </p>
	# </div>
	# </body></html>
	
	# test_path_any(html)
	# test_path_direct(html)
	# test_path_element(html)

	# test_path_attr(html)
	# test_path_predicates(html)
	
	# test_path_wildcard(html)

	# test_path_multi(html)
	# test_path_and_or_not(html)

	# test_path_func(html)
	
	# test_path_self(html)
	# test_path_up(html)
	# test_path_down(html)
	# test_path_sideway(html)

	########################################
	# xml
	########################################
	content='''
	<collection shelf="New Arrivals">
		<movie title="Enemy Behind">
		   <type>War, Thriller</type>
		   <format>DVD</format>
		   <year>2003</year>
		   <rating>PG</rating>
		   <stars>10</stars>
		   <description>Talk about a US-Japan war</description>
		</movie>
		<movie title="Transformers">
		   <type>Anime, Science Fiction</type>
		   <format>DVD</format>
		   <year>1989</year>
		   <rating>R</rating>
		   <stars>8</stars>
		   <description>A schientific fiction</description>
		</movie>
	</collection>
	'''
	root=etree.XML(content)
	print(root)
	print(etree.tounicode(root))

	result=root.xpath('//movie')
	for i,r in enumerate(result):
		print(i,r,":",r.tag,r.attrib,r.get('title'))
		print("text:",r.text)
		print("string:",r.xpath('string(./description)'))
		print('rating:',r.xpath('./rating/text()'))

	print('end')