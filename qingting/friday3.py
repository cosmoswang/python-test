# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import time, requests, sys, logging, os, random

def main(start, end):
    sleep_time = 60 * 15   # 每次下载的间隔时间

    logger = logging.getLogger('friday')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('friday-{}.log'.format(int(time.time())))
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelno)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    url_pattern = 'http://www.audio69.com/book/415/{}.html'

    if not os.path.exists('./.res/friday'):
        os.makedirs('./.res/friday')

    for page in range(start, end + 1):
        if page == 0:
            continue

        file = './.res/friday/{}.m4a'.format(page)
        if os.path.isfile(file):
            size = os.path.getsize(file)
            if size > 1024 * 1024:
                logger.debug('文件{}已存在，不重复下载'.format(file))
                continue
            else:
                logger.debug('文件{}已存在，但文件小于1M，重复下载文件'.format(file))

        content = download_single(page, url_pattern, logger)

        if len(content) < 1024 * 1024:
            # repeat once
            logger.warning('下载的文件小于1M，可能有问题，延时后重试一次')
            st = sleep_time + random.randint(-10, 60)
            logger.debug('延时{}秒'.format(st))
            time.sleep(st)
            content = download_single(page, url_pattern, logger)

            if len(content) < 1024 * 1024:
                logger.warning('下载的文件重试后依然小于1M，已保存至{}，继续后面的下载'.format(file))

        with open(file, 'wb') as writer:
            writer.write(content)

        st = sleep_time + random.randint(-10, 60)
        logger.debug('延时{}秒'.format(st))
        time.sleep(st)

def download_single(page, url_pattern, logger):
    url = url_pattern.format(page)
    logger.info('开始下载第{}章，url:{}'.format(page, url))
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    html = requests.get(url=url, headers={'User-Agent': user_agent}).text
    html_parser = BeautifulSoup(html, 'html.parser')

    src = html_parser.find('audio').find('source').attrs['src']

    Referer = url
    time.sleep(random.randint(3, 10))
    r = requests.get(url=src, headers={'User-Agent': user_agent, 'Referer': Referer})
    logger.info('第{}章下载完毕'.format(page))
    return r.content



if __name__ == "__main__":
    main(230, 660)

