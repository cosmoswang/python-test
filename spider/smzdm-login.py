# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, json

def login(driver, button):
	button.click()
	time.sleep(5)
	driver.switch_to.frame("J_login_iframe")
	input_user = driver.find_element(By.ID, "username")
	input_user.send_keys("")
	input_pass = driver.find_element(By.ID, "password")
	input_pass.send_keys("")
	# button_submit = driver.find_element(By.ID, "login_submit")
	# button_submit.click()

driver = webdriver.Chrome()
driver.get("https://www.smzdm.com/")
punch_button = driver.find_element(By.CLASS_NAME, "J_punch")

if (punch_button.text == "签到得积分"):
	print("准备登录")
	login(driver, punch_button)
	# 登录
else:
	print("已登录")

time.sleep(10)
driver.switch_to.default_content()
punch_button = driver.find_element(By.CLASS_NAME, "J_punch")
print(punch_button.text)

with open('./spider/.res/smzdm_cookie.json', 'w') as f:
	json.dump(driver.get_cookies(), f)

# driver.close()


