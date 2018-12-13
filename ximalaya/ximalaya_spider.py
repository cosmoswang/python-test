# -*- coding: utf-8 -*-
import os, sys, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   #这里是把顶层目录加入到python的环境变量中。
sys.path.append(BASE_DIR)

from qingting import downloader, Edge_dev
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import configparser

def main(channel, page):
	driver = webdriver.Edge()
	driver.get('https://www.ximalaya.com/')

	login_img = driver.find_element(By.CLASS_NAME, 'img')
	login_img.click()

	time.sleep(1)

	config = configparser.ConfigParser()
	config.read('./.res/.conf')

	account_name_input = driver.find_element(By.NAME, 'accountName')
	account_pwd_input = driver.find_element(By.NAME, 'accountPWD')
	login_button = driver.find_element(By.CLASS_NAME, 'login-pop__form').find_element(By.XPATH, 'div[3]/button')
	account_name_input.send_keys(config.get('info', 'user'))
	account_pwd_input.send_keys(config.get('info', 'pass'))
	login_button.click()

	time.sleep(1)
	driver.get('https://www.ximalaya.com/jiaoyu/{}'.format(channel))
	time.sleep(1)
	title_element = driver.find_element(By.XPATH, '//*[@id="root"]/main/section/div/div[2]/div[1]/div[1]/div[2]/div[2]/h1')
	title = title_element.text

	dev = Edge_dev.Edge_dev()
	dev.prepare()

	print(title)
	dl = downloader.Downloader(title)
	dl.start()

	nav_element = None
	try:
		nav_element = driver.find_element(By.CSS_SELECTOR, 'nav.pagination')
	except BaseException as e:
		print(e)
	
	total_page = 1
	if nav_element != None:
		last_page_elment = nav_element.find_element(By.XPATH, 'ul/li[last()-1]')
		total_page = int(last_page_elment.text)
	current_page = page

	# $('div.sound-list ul li div.icon-wrapper div.all-icon')
	# var lis = document.getElementsByClassName('all-icon default rC5T'); var length = lis.length; for (var i = 0; i < length; i++) {lis[0].className = 'all-icon play rC5T'}
	while current_page <= total_page:
		driver.get('https://www.ximalaya.com/{}/p{}'.format(channel, current_page))
		driver.switch_to.default_content()
		time.sleep(5)
		driver.execute_script("window.scrollBy(0, 700)")
		# driver.execute_script("var lis = document.getElementsByClassName('all-icon default rC5T'); var length = lis.length; for (var i = 0; i < length; i++) {lis[0].className = 'all-icon play rC5T'}")
		sound_element = driver.find_element(By.CLASS_NAME, 'sound-list')
		ul_element = sound_element.find_element(By.TAG_NAME, 'ul')
		# print(nav_element.location_once_scrolled_into_view)
		# nav_element._execute
		li_list = ul_element.find_elements(By.TAG_NAME, 'li')
		href_list = []
		for li in li_list:
			a = li.find_element(By.XPATH, 'div[2]/a')
			artical = a.text
			if dl.check_exists(artical):
				continue
			
			h = a.get_attribute('href')
			href_list.append(h)

		for h in href_list:
			driver.get(h)
			time.sleep(1)
			driver.switch_to_default_content()

			icon_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, 'icon play-icon XH7H'))
			# icon_element = driver.find_element(By.CLASS_NAME, 'icon play-icon XH7H')
			artical_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, 'title-wrapper XH7H'))
			artical = artical_element.text
			time_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, 'total-time time MO'))
			total_time = time_element.text
			icon_element.click()
			
			_url = dev.getUrl()

			url = {}
			url['url'] = _url
			url['title'] = artical
			url['timelong'] = total_time.replace(':', '-')

			dl.download(url)
			

		current_page += 1

	dl.end()

if __name__ == "__main__":
	# jiaoyu/4345263
	channel = 'youshengshu/8301461'
	page = 1
	if len(sys.argv) > 1:
		channel = sys.argv[1]

	if len(sys.argv) > 2:
		page = int(sys.argv[2])

	main(channel, page)