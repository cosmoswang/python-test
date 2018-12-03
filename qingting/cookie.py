from selenium import webdriver
import json, time

driver = webdriver.Chrome()
driver.get('https://www.qingting.fm/channels/239012')

time.sleep(30)

with open('./qingting/.res/qingting_cookie.json', 'w') as f:
	json.dump(driver.get_cookies(), f)

