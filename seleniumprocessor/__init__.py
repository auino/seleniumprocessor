import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# initiates the selenium connection, by using the `webdriverfile` path, the `url` to open, the timeout `to` to wait for page load, and, optionally, waiting for the login of the user
def initiate_connection(webdriverfile, url, to, loginrequired=True, headless=False):
	# starting browser
	chrome_options = Options()
	if headless: chrome_options.add_argument('--headless')
	brw = webdriver.Chrome(executable_path=webdriverfile, options=chrome_options)
	# opening the home page
	brw.get(url)
	# waiting the page to be loaded
	time.sleep(to)
	# waiting for user login
	if loginrequired: input('Please login to your account and then enter y to continue: ')
	# returning the browser controller
	return brw

def navigatepath(brw, n, p, to):
	if type(p) is str: p = p.split('>')
	for e in brw.find_elements_by_class_name(n):
		if e.text.lower() == p[0].lower():
			try: e.click()
			except: brw.execute_script("arguments[0].click();", e)
			time.sleep(to)
			if len(p) <= 1: break
			try: navigatepath(brw, n, p[1:], to)
			except:
				try: e.click()
				except: brw.execute_script("arguments[0].click();", e)
				time.sleep(to)
				navigatepath(brw, n, p[1:], to)

def run_action_on_object(brw, res, e, obj, checkfilterpassed_callback=None):
	if not checkfilterpassed_callback is None:
		if e.get('filter') != None and not checkfilterpassed_callback(e.get('filter')): return res
	if e.get('action') == 'click':
		try: obj.click()
		except: brw.execute_script("arguments[0].click();", obj)
	if e.get('action') == 'navigate': navigatepath(brw, e.get('class_name'), e.get('action_parameters'), e.get('sleep'))
	if e.get('action') == 'empty_value':
		while obj.get_attribute('value') != '': obj.send_keys(Keys.BACKSPACE)
	if e.get('action') == 'send_keys': obj.send_keys(e.get('action_parameters'))
	if e.get('action') == 'store_text': res[e.get('action_parameters')] = obj.text
	if e.get('action') == 'scroll_to': ActionChains(brw).move_to_element(obj).perform()
	if e.get('action') == 'foreach':
		res['list'] = []
		if not e.get('class_name') is None: sub_brws = brw.find_elements_by_class_name(e.get('class_name'))
		if not e.get('name') is None: sub_brws = brw.find_elements_by_name(e.get('name'))
		for sub_brw in sub_brws:
			sub_res = {}
			for s in e.get('action_parameters'):
				brw_obj = sub_brw
				if s.get('context') == 'whole_page': brw_obj = brw
				if not s.get('class_name') is None: sub_obj = brw_obj.find_element_by_class_name(s.get('class_name'))
				if not s.get('name') is None: sub_obj = brw_obj.find_element_by_name(s.get('name'))
				sub_res = run_action_on_object(brw_obj, sub_res, s, sub_obj)
			res['list'].append(sub_res)
	return res

def run_process(brw, url_home, to, p, backtohome_begin=True, backtohome_end=True, checkfilterpassed_callback=None):
	res = {}
	if backtohome_begin:
		brw.get(url_home)
		time.sleep(to)
	for e in p:
		obj = None
		if e.get('filter') != None and not checkfilterpassed_callback(e.get('filter')): continue
		if e.get('index') is None:
			if not e.get('class_name') is None: obj = brw.find_element_by_class_name(e.get('class_name'))
			if not e.get('name') is None: obj = brw.find_element_by_name(e.get('name'))
		else:
			if not e.get('class_name') is None: obj = brw.find_elements_by_class_name(e.get('class_name'))[e.get('index')]
			if not e.get('name') is None: obj = brw.find_elements_by_name(e.get('name'))[e.get('index')]
		res = run_action_on_object(brw, res, e, obj, checkfilterpassed_callback)
		if not e.get('sleep') is None: time.sleep(e.get('sleep'))
	if backtohome_end:
		brw.get(url_home)
		time.sleep(to)
	return res
