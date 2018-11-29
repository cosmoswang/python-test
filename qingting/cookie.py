from selenium import webdriver
import json

driver = webdriver.Edge()
driver.get('https://www.qingting.fm/channels/239012')

with open('./qingting/qingting_cookie.json', 'w') as f:
	json.dump(driver.get_cookies(), f)

