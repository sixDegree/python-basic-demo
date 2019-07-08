from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

'''
https://www.cnblogs.com/zhaof/p/6953241.html
https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions
https://www.cnblogs.com/LOVEYU/p/8392269.html

- 安装`selenium`
	```
	$ pip install selenium
	# check:
	$ python3
	>>> from selenium import webdriver
	>>> help(webdriver)
	```
- 安装browser驱动程序,eg: chrome的`chromedrive`
	+ [download](http://chromedriver.chromium.org/)
	+ copy to path,eg: mac `/usr/local/bin`
	+ check: `chromedriver -v`

- 查找元素: 
	+ `find_element_by_xxx(...)`,`find_element(By.xxx,xxx)`: 返回匹配的第一个元素（`WebElement`类型对象），找不到则抛出异常
	+ `find_elements_by_xxx(...)`,`find_elements(By.xxx,xxx)`: 返回所有匹配的元素列表，找不到则返回空列表
	+ eg: `find_elements(By.CSS_SELECTOR,'.service-bd li')` = `find_elements_by_css_selector(".service-bd li")`
	+ `WebElement`类型对象：
		* `.text` 获取文本值（它与它的所有子孙节点的文字的组合，无则返回空字符串）
		* `.id`
		* `.tag_name`
		* `.location`
		* `.size`
		* `.get_attribute(attrName)` 获取属性值（无则返回None）
		* `find_element_by_xxx / find_elements_by_xxx(...)`
		* `find_element / find_elements(By.xxx,xxx)`
	+ 使用:
		* XPath
			+ `find_element_by_xpath / find_elements_by_xpath(xpath)`
			+ eg: `find_element_by_xpath("//div[@class='detail']/a")`
		* CSS Selector
			+ `find_element_by_css_selector / find_elements_by_css_selector(css)`
			+ eg: `find_element_by_css_selector("div[class='detail'] > div span")`
		* Tag
			+ `find_element_by_id(id)`: 一个或异常
			+ `find_element_by_tag_name / find_elements_by_tag_name(tagName)`
			+ `find_element_by_class_name / find_elements_by_class_name(classValue)`: 使用元素的class值查找元素
			+ `find_element_by_name / find_elements_by_name(name)`: 通过`name`属性查找
			+ `find_element_by_link_text / find_elements_by_link_text(linkText)`: 文本值为linkText的超级链接元素`<a>`
			+ `find_element_by_partial_link_text / find_elements_by_partial_link_text(linkText)`: 文本值包含linkText的超级链接元素`<a>`
			+ eg: `find_element_by_class_name("p1")` = `find_elements_by_xpath("//*[@class='p1']")` = `find_elements_by_css_selector("*[class='p1']")`

- 交互操作([Refer to Action Chains](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains))
	* click,click_and_hold,double_click,context_click
	* drag_and_drop,drag_and_drop_by_offset
	* key_down,key_up
	* move_by_offset,move_to_element,move_to_element_with_offset
	* pause,perform,release,reset_actions
	* send_keys,send_keys_to_element
	* eg: action
		```python
		browser=webdriver.Chrome()
		input= browser.find_element_by_id('kw')
		input.send_keys("MakBook")
		searchBtn = browser.find_element_by_id('su')
		searchBtn.click()
		time.sleep(2)
		input.clear()
		input.send_keys("ipad")
		```
	* eg: action_chains
		```python
		from selenium.webdriver import ActionChains
		
		browser=webdriver.Chrome()
		browser.get("http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable")
		time.sleep(1)

		browser.switch_to.frame('iframeResult')
		source = browser.find_element_by_css_selector('#draggable')
		target = browser.find_element_by_css_selector('#droppable')

		actions = ActionChains(browser)
		actions.drag_and_drop(source, target)
		actions.perform()
		time.sleep(1)
		```

- 执行Javascript: `execute_script(script)`
	```python
	browser=webdriver.Chrome()
	browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
	browser.execute_script('alert("To Bottom")')
	```

- 切换 
	+ `switch_to.xxx`
		* `window(windowName)`
		* `frame(frameName)`
		* `parent_frame()`
		* `active_element()`
		* `default_content()`
		* `alert()`
	+ `back()`,`forward()`

- 异常处理 `selenium.common.exceptions`
	```python
	from selenium import webdriver
	from selenium.common.exceptions import TimeoutException, NoSuchElementException
	
	browser=webdriver.Chrome()
	try:
		browser.get('http://www.baidu.com')
		input= browser.find_element_by_id('kw')
		input.send_keys("MakBook")
		searchBtn = browser.find_element_by_id('su')
		searchBtn.click()
		print("clicked!")
		span=browser.find_element_by_xpath("//div[@id='container']//div[@class='nums']/span[@class='nums_text']")
		print("result:",span.text)
	except (TimeoutException,NoSuchElementException) as e:
		print("Occur Exception:",e)
	except Exception as e:
		print("Unknow Exception:",type(e),e)
	finally:
		print("close!")
		browser.close()
	```

- Cookie
	+ `get_cookie(name)`
	+ `add_cookie(dict)`: required keys “name” and “value”
	+ `delete_cookie(name)`
	+ `get_cookies()`
	+ `delete_all_cookes()`

- 等待元素
	+ 强制等待 `time.sleep(seconds)`
	+ 隐式等待 `browser.implicitly_wait(seconds)`
	+ 显示等待
		```python
		from selenium.webdriver.support.wait import WebDriverWait
		from selenium.webdriver.support import expected_conditions as EC

		wait=WebDriverWait(driver,10, 0.5)
		optionLocator = (By.XPATH, "//select/option")
		btnLocator=(By.CSS_SELECTOR, '.btn-search')

		option=wait.until(EC.presence_of_element_located(optionLocator))
		print(option)

		btn=wait.until(EC.element_to_be_clickable(btnLocator))
		print(btn)
		```
		* EC 常用的判断条件：
			+ `title_is` : 标题是某内容
			+ `title_contains` : 标题包含某内容
			+ `visibility_of` : 可见，传入元素对象
			+ `staleness_of` : 判断一个元素是否仍在DOM，可判断页面是否已经刷新
			+ `alert_is_present` : 是否出现Alert
			+ `frame_to_be_available_and_switch_to_it` : frame加载并切换
			+ `element_selection_state_to_be` : 传入元素对象以及状态，相等返回True，否则返回False
			+ `element_located_selection_state_to_be` : 传入定位元组以及状态，相等返回True，否则返回False
			
			presence_of_element_located(locator) : 指定元素出现，传入定位元组，如(By.ID, 'p')
			presence_of_all_elements_located(locator)

			invisibility/visibility_of_element_located(locator) : 指定元素不可见／可见

			element_to_be_clickable(locator) : 指定元素可点击
			element_located_to_be_selected(locator) : 指定元素可选择
			element_to_be_selected(element)
			text_to_be_present_in_element(locator,text) : 指定元素的文本包含指定文本
			text_to_be_present_in_element_value(locator,text) : 指定元素值包含某文字

		
'''

def get_browser(slience=False):
	if not slience:
		return webdriver.Chrome()							# 会弹出一个 chrome 浏览器
	else:
		chrome_options=Options()
		chrome_options.add_argument('--headless') 
		chrome_options.add_argument('--disable-gpu')
		browser=webdriver.Chrome(options=chrome_options)	# 创建的chrome浏览器是不可见的
		return browser

##################################
# 1. browser
##################################
def test_browser():
	browser=get_browser()
	browser.get('http://www.baidu.com')
	print(browser.page_source)
	browser.close()

def test_browser_options():
	browser=get_browser(slience=True)
	browser.get('http://www.baidu.com')
	print(browser.page_source)
	browser.close()

##################################
# 2. 查找元素
##################################

def test_element():
	browser=get_browser(slience=True)
	browser.get('http://www.baidu.com')

	print('--- input ---')
	input= browser.find_element_by_id('kw')
	print_element(input)

	print('--- searchBtn ---')
	#searchBtn = browser.find_element_by_id('su')
	searchBtn=browser.find_element(By.ID,'su')
	print_element(searchBtn)

def print_element(ele):
	print("id:",ele.id)
	print("tag_name:",ele.tag_name)
	print("location:",ele.location)
	print("size:",ele.size)
	print("text:",ele.text)
	print("class:",ele.get_attribute("class"))
	print("name:",ele.get_attribute("name"))
	print("type:",ele.get_attribute("type"))
	print("value:",ele.get_attribute("value"))
	print("id:",ele.get_attribute("id"))

##################################
# 3. 交互操作
##################################

# 交互
def test_action():
	browser=webdriver.Chrome()
	browser.get('http://www.baidu.com')

	input= browser.find_element_by_id('kw')
	input.send_keys("MakBook")

	searchBtn = browser.find_element_by_id('su')
	searchBtn.click()
	
	time.sleep(2)
	input.clear()
	input.send_keys("ipad")

	time.sleep(2)
	browser.close()

# 动作链
from selenium.webdriver import ActionChains
def test_action_chains():
	browser = get_browser()
	browser.get("http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable")
	time.sleep(1)

	browser.switch_to.frame('iframeResult')
	source = browser.find_element_by_css_selector('#draggable')
	target = browser.find_element_by_css_selector('#droppable')

	actions = ActionChains(browser)
	actions.drag_and_drop(source, target)
	actions.perform()

	time.sleep(1)

##################################
# 4. 执行JavaScript
##################################
def test_js():
	browser = get_browser()
	browser.get("http://www.baidu.com")
	browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
	browser.execute_script('alert("To Bottom")')
	time.sleep(2)

##################################
# 5. 切换
##################################

# 1. window tab切换：
# 执行js命令`window.open()`打开选项卡
# 不同的选项卡是存在`browser.window_handles`列表中
# eg: 通过`browser.window_handles[0]`可以操作第一个选项卡
def test_window():
	browser=get_browser()
	browser.get('https://www.baidu.com')
	browser.execute_script('window.open()')
	print(browser.window_handles)

	browser.switch_to.window(browser.window_handles[1])
	browser.get('https://www.douban.com/')
	time.sleep(1)

	browser.switch_to.window(browser.window_handles[0])
	browser.get('https://python.org')
	time.sleep(1)

	# 浏览器的前进和后退: back(),forward()
	browser.back()
	time.sleep(1)
	browser.forward()
	time.sleep(1)

	browser.close()

# 2. frame切换
def test_frame():
	browser=get_browser(slience=True)
	browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
	
	browser.switch_to.frame('iframeResult')
	source = browser.find_element_by_css_selector('div#draggable')
	print(source)
	print(source.text)
	try:
	    logo = browser.find_element_by_class_name('logo')
	except NoSuchElementException:
	    print('NO LOGO')

	browser.switch_to.parent_frame()
	logo = browser.find_element_by_class_name('logo')
	print(logo)
	print(logo.text)

##################################
# 6. 异常处理
##################################
from selenium.common.exceptions import TimeoutException, NoSuchElementException
def test_exception():
	browser=get_browser()
	try:
		browser.get('http://www.baidu.com')
		input= browser.find_element_by_id('kw')
		input.send_keys("MakBook")
		searchBtn = browser.find_element_by_id('su')
		searchBtn.click()
		print("clicked!")
		span=browser.find_element_by_xpath("//div[@id='container']//div[@class='nums']/span[@class='nums_text']")
		print("result:",span.text)
	except (TimeoutException,NoSuchElementException) as e:
		print("Occur Exception:",e)
	except Exception as e:
		print("Unknow Exception:",type(e),e)
	finally:
		print("close!")
		browser.close()

##################################
# 7. 等待
##################################

# 1. 隐式等待
def test_implicit_wait():
	browser=get_browser()
	browser.get('http://www.baidu.com')
	input= browser.find_element_by_id('kw')
	input.send_keys("MakBook")
	searchBtn = browser.find_element_by_id('su')
	searchBtn.click()

	browser.implicitly_wait(3)
	span=browser.find_element_by_xpath("//div[@id='container']//div[@class='nums']/span[@class='nums_text']")
	print(span.text)
	browser.close()

# 2. 显示等待
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def test_explicit_wait():
	browser=get_browser()
	browser.get('http://www.baidu.com')
	input= browser.find_element_by_id('kw')
	input.send_keys("MakBook")
	searchBtn = browser.find_element_by_id('su')
	searchBtn.click()

	wait=WebDriverWait(browser,5, 0.5)
	locator = (By.XPATH, "//div[@id='container']//div[@class='nums']/span[@class='nums_text']")
	span=wait.until(EC.presence_of_element_located(locator))
	
	print(span.text)
	browser.close()

##################################
# 8. cookie操作
##################################

# get_cookie(name)
# add_cookie(dict): required keys “name” and “value”
# delete_cookie(name)
# get_cookies()
# delete_all_cookes()
def test_cookie():
	browser=get_browser(slience=True)
	browser.get('http://www.baidu.com')
	cookies=browser.get_cookies()
	print(cookies)
	browser.add_cookie({'name':'user','value':'Tom'})
	print(browser.get_cookie('user'))

if __name__=='__main__':
	# test_browser()
	# test_browser_options()

	# test_element()
	# test_action()
	# test_action_chains()
	# test_js()
	# test_window()
	# test_frame()

	# test_exception()
	# test_implicit_wait()
	# test_explicit_wait()

	# test_cookie()

	



