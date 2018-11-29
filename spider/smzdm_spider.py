# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
import json, logging, time, sys, csv, os, uuid, traceback

def load_cookies():
	with open('./spider/.res/smzdm_cookie.json', 'r') as f:
		return json.load(f)

def load_last_timestamp():
	filelist = os.listdir('./spider/.res/output')
	filelist.sort(reverse=True)
	for file in filelist:
		if os.path.isfile(os.path.join('./spider/.res/output', file)):
			tup = os.path.splitext(file)
			if tup[1] == '.csv':
				return int(tup[0])
	return 0

def write_to_file(article_list, ts):
	with open('./spider/.res/output/' + str(ts) + '.csv', 'w', newline='', encoding='utf-8') as w:
		fieldnames = ['time', 'article_id', 'title', 'zhi-buzhi', 'mall', 'descripe', 'href', 'day', 'ts']
		writer = csv.DictWriter(w, fieldnames=fieldnames, dialect='excel')

		writer.writeheader()
		writer.writerows(article_list)
		
def check_punch(logger, driver):
	user_div = driver.find_element(By.CLASS_NAME, 'user-name')
	if user_div.text.find('cosmoswang') != -1:
		# 已登录，检查是否签到
		punch_element = driver.find_element(By.CLASS_NAME, 'J_punch')
		if punch_element.text.find('领积分') != -1:
			punch_element.click()
			punch_element = driver.find_element(By.CLASS_NAME, 'J_punch')
			if punch_element.text.find('已签到') != -1:
				logger.info('签到成功')
			else:
				logger.warning('签到失败')
		else:
			logger.info('已签到')
	else:
		# 未登录或登录失效，记录日志
		driver.get_screenshot_as_file('./spider/.res/screenshot/screenshot.png')
		logger.warning('not log in...need reget cookies file')

def create_logger(ts = None) :
	
	# 创建一个handler，用于写入日志文件
	if ts == None:
		logger = logging.getLogger('smzdm_logger') 
		fh = logging.FileHandler('./spider/.res/log/.log', encoding='utf-8')
	else:	
		logger = logging.getLogger('smzdm_artical_logger') 
		fh = logging.FileHandler('./spider/.res/log/{0}.log'.format(str(ts)), encoding='utf-8')

	logger.setLevel(logging.INFO)

	# 再创建一个handler，用于输出到控制台
	ch = logging.StreamHandler()
	# 定义handler的输出格式
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelno)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)

	# 给logger添加handler
	logger.addHandler(fh)
	logger.addHandler(ch)
	return logger

def grab_data(logger, driver):
	driver.set_window_size(1920, 1080)
	# driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
	# time.sleep(3)

	logger.info('start fetching')
	page = 1
	last_time_stamp = load_last_timestamp()	# 上一次爬取的时间戳
	newest_time_stamp = sys.maxsize * 100	# 本次爬取的时间戳，从下面爬取时的第一条获取
	current_time_stamp = sys.maxsize * 100	# 当前正在爬取的记录的时间戳
	flag = True	# 记录是否是第一条

	article_list = []
	content_logger = None
	while page < 20 and current_time_stamp > last_time_stamp:
		driver.get('https://www.smzdm.com/p' + str(page))
		if flag:
			check_punch(logger, driver)

		main_list = driver.find_element(By.ID, 'feed-main-list')
		row_wide_list = main_list.find_elements(By.CLASS_NAME, 'feed-row-wide')	

		article_count = 0
		discard_count = 0
		for row_wide in row_wide_list:
			article_id = row_wide.get_attribute('articleid')
			timesort_str = row_wide.get_attribute('timesort')
			if (timesort_str is None) or article_id is None:
				discard_count += 1
				continue
			else:
				ts = int(timesort_str)
			current_time_stamp = ts
			
			if flag:
				flag = False
				newest_time_stamp = ts
				logger.info('fetch new data, see log file "{0}.log" for details'.format(str(newest_time_stamp)))
				content_logger = create_logger(newest_time_stamp)

			day_str = time.strftime("%Y%m%d", time.localtime(ts / 100))
			time_str = time.strftime("%H%M%S", time.localtime(ts / 100))

			if article_id[0] != '3':
				discard_count += 1
				continue
			
			article = {}
			article['time'] = time_str
			article['day'] = day_str
			article['article_id'] = article_id
			article['ts'] = ts

			title_element = row_wide.find_element(By.CLASS_NAME, 'feed-block-title')
			title_href_element = title_element.find_element(By.TAG_NAME, 'a')
			title_href = title_href_element.get_attribute('href')
			title = title_href_element.text
			article['title'] = title
			article['href'] = title_href
			
			content_logger.debug('fetch an article : {0}, {1}, {2}'.format(article_id, current_time_stamp, title))

			content_element = row_wide.find_element(By.CLASS_NAME, 'feed-block')
			descripe_element = content_element.find_element(By.CLASS_NAME, 'feed-block-descripe')
			article['descripe'] = descripe_element.text

			zhi_element = content_element.find_element(By.XPATH, './div[@class="z-feed-content"]/div[@class="z-feed-foot"]/div[@class="z-feed-foot-l"]/span/a[1]/span/span')
			buzhi_element = content_element.find_element(By.XPATH, './div[@class="z-feed-content"]/div[@class="z-feed-foot"]/div[@class="z-feed-foot-l"]/span/a[2]/span/span')
			article['zhi-buzhi'] = zhi_element.text + '/' + buzhi_element.text

			mall_element = content_element.find_element(By.XPATH, './div[@class="z-feed-content"]/div[@class="z-feed-foot"]/div[@class="z-feed-foot-r"]/span/a')
			article['mall'] = mall_element.text
			
			# print(article)
			article_list.append(article)
			article_count += 1

		content_logger.info('page {0} finished, grab {1} articles totally, discade {2} articles records.'.format(page, article_count, discard_count))
		page += 1
		# next_page_button = driver.find_element(By.CLASS_NAME, 'next-page')
		# next_page_button.click()
		# time.sleep(3)
	
	return article_list, newest_time_stamp

def main():
	logger = create_logger()
	logger.info('-'*20)
	logger.info('start chrome')

	option = webdriver.ChromeOptions()
	option.add_argument('headless')
	driver = webdriver.Chrome(service_log_path='./spider/.res/log/chrome.log', options=option)
	# driver = webdriver.Edge()
	# driver = webdriver.Firefox()
	driver.get("https://www.smzdm.com/")

	logger.info('delete all cookies')
	driver.delete_all_cookies()

	logger.info('set cookies')
	cookies = load_cookies()
	for cookie in cookies:
		try:
			driver.add_cookie(cookie)
		except BaseException as e:
			logger.error('unable to set cookie : {0} cause {1}'.format(cookie, e))
			raise e
	logger.info('set cookies finished')
	
	try:
		article_list, newest_time_stamp = grab_data(logger, driver)

		logger.info('fetch data finished, grab {0} articles totally'.format(len(article_list)))
		logger.info('writing to file')

		write_to_file(article_list, newest_time_stamp)
		logger.info('write file finished')
	except BaseException as be:
		error_image_name = str(uuid.uuid1())
		driver.get_screenshot_as_file('./spider/.res/screenshot/{}.png'.format(error_image_name))
		logger.error('grab data error, see file:///./spider/.res/screenshot/{}.png for screenshot'.format(error_image_name))
		logger.error(str(be))
		logger.exception(be)

	driver.close()

if __name__ == "__main__":
	main()
