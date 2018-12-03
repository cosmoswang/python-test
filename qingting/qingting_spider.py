from selenium import webdriver
from selenium.webdriver.common.by import By
import json, time, sys
import Edge_dev
import downloader

def load_cookies():
	with open('./qingting/.res/qingting_cookie.json', 'r') as f:
		return json.load(f)

def main(channel, page):
	driver = webdriver.Edge()
	driver.get('https://www.qingting.fm')
	driver.delete_all_cookies()

	cookies = load_cookies()
	for cookie in cookies:
		try:
			driver.add_cookie(cookie)
		except BaseException as e:
			# logger.error('unable to set cookie : {0} cause {1}'.format(cookie, e))
			raise e

	driver.get('https://www.qingting.fm/channels/{}'.format(channel))

	dev = Edge_dev.Edge_dev()
	dev.prepare()

	app_element = driver.find_element(By.ID, 'app')
	print(app_element.location)
	title_element = app_element.find_element(By.XPATH, 'div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/h1')
	title = title_element.text
	print(title)

	dl = downloader.Downloader(title)
	dl.start()

	page_element = app_element.find_element(By.XPATH, 'div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/ul')
	last_page_elment = page_element.find_element(By.XPATH, 'li[last()-1]')
	

	total_page = int(last_page_elment.text)
	current_page = page
	while current_page <= total_page:
		driver.get('https://www.qingting.fm/channels/{}/{}'.format(channel, current_page))
		driver.switch_to.default_content()
		time.sleep(5)
		app_element = driver.find_element(By.ID, 'app')
		page_element = app_element.find_element(By.XPATH, 'div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/ul')
		# next_page_element = page_element.find_element(By.XPATH, 'li[last()]/a')

		ul_element = app_element.find_element(By.XPATH, 'div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/ul')
		li_list = ul_element.find_elements(By.TAG_NAME, 'li')
		for li in li_list:
			# print(li.text)
			b = li.find_element(By.XPATH, 'span/div/button[1]')
			artical_element = li.find_element(By.XPATH, 'span/a/p')
			artical = artical_element.text
			timelong_element = li.find_element(By.XPATH, 'span[2]')
			timelong = timelong_element.text
			b.click()
			# time.sleep(5)
			_url = dev.getUrl()

			url = {}
			url['url'] = _url
			url['title'] = artical
			url['timelong'] = timelong.replace(':', '-')

			time.sleep(1)
			print(url)
			dl.download(url)
			driver.execute_script("window.scrollBy(0, 50)")

		time.sleep(5)
		current_page += 1
		# next_page_element.click()

	dl.end()
	

if __name__ == "__main__":
	channel = '231663'
	page = 1
	if len(sys.argv) > 1:
		channel = sys.argv[1]

	if len(sys.argv) > 2:
		page = int(sys.argv[2])

	main(channel, page)