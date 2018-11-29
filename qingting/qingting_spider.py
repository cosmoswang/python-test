from selenium import webdriver
import json

def load_cookies():
	with open('./qingting/qingting_cookie.json', 'r') as f:
		return json.load(f)

driver = webdriver.Chrome()
driver.get('https://www.qingting.fm')
driver.delete_all_cookies()

cookies = load_cookies()
for cookie in cookies:
	try:
		driver.add_cookie(cookie)
	except BaseException as e:
		# logger.error('unable to set cookie : {0} cause {1}'.format(cookie, e))
		raise e

driver.get('https://www.qingting.fm/channels/239012')