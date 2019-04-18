# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import time, requests, sys, logging, os, random

def main(start, end):
    sleep_time = 60 * 12   # 每次下载的间隔时间

    logger = logging.getLogger('friday')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('friday-{}.log'.format(int(time.time())))
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelno)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    url_pattern = 'http://m.audio69.com/book/415/{}.html'

    if not os.path.exists('./.res/friday'):
        os.makedirs('./.res/friday')

    download_with_request(start, end, logger, url_pattern, sleep_time)

def download_with_request(start, end, logger, url_pattern, sleep_time):
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

        # if len(content) < 1024 * 1024:
        #     # repeat once
        #     logger.warning('下载的文件小于1M，可能有问题，延时后重试一次')
        #     st = sleep_time + random.randint(-10, 60)
        #     logger.debug('延时{}秒'.format(st))
        #     time.sleep(st)
        #     content = download_single(page, url_pattern, logger)

        if len(content) < 1024 * 1024:
            logger.warning('下载的文件重试后依然小于1M，已保存至{}，继续后面的下载'.format(file))

        with open(file, 'wb') as writer:
            writer.write(content)

        st = sleep_time + random.randint(-60, 60)
        logger.debug('延时{}秒'.format(st))
        time.sleep(st)

def download_single(page, url_pattern, logger):
    url = url_pattern.format(page)
    logger.info('开始下载第{}章，url:{}'.format(page, url))
    user_agent = 'Mozilla/5.0 (Linux; Android 8.1.0; OE106 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.70 Mobile Safari/537.36'
    html = requests.get(url=url, headers={'User-Agent': user_agent}).text
    html_parser = BeautifulSoup(html, 'html.parser')

    src = html_parser.find('audio').find('source').attrs['src']
    logger.debug('识别到文件下载路径:{}'.format(src))

    return download_m4a(src, logger, page, url, user_agent)


def download_m4a(src, logger, page, Referer, user_agent):
    '''
    GET /asdasdasd/415/130/1555409707/62dc24b36491c7183ab1522c905daa56/768303c1a4d553ba53aa4929f44a4ab6.m4a HTTP/1.1
    Host: q2.audio69.com
    Connection: keep-alive
    Accept-Encoding: identity;q=1, *;q=0
    User-Agent: Mozilla/5.0 (Linux; Android 8.1.0; OE106 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.70 Mobile Safari/537.36
    Accept: */*
    Referer: http://m.audio69.com/book/415/130.html
    Accept-Language: zh-CN,zh;q=0.9
    Range: bytes=0-
    '''

    Connection = 'keep-alive'
    Accept_Encoding = 'identity;q=1, *;q=0'
    Accept = '*/*'
    Accept_Language = 'zh-CN,zh;q=0.9'
    Range = 'bytes=0-'

    time.sleep(random.randint(3, 10))
    r = requests.get(url=src, headers={'User-Agent': user_agent, 'Referer': Referer, 'Connection': Connection,
                                       'Accept-Encoding': Accept_Encoding, 'Accept': Accept, 'Accept-Language': Accept_Language, 'Range': Range})
    
    logger.debug('请求获取完毕，状态码：{}'.format(r.status_code))
    while r.status_code == 404:
        time.sleep(1)
        logger.debug('404重试')
        r = requests.get(url=src, headers={'User-Agent': user_agent, 'Referer': Referer, 'Connection': Connection,
                                       'Accept-Encoding': Accept_Encoding, 'Accept': Accept, 'Accept-Language': Accept_Language, 'Range': Range})
        logger.debug('请求获取完毕，状态码：{}'.format(r.status_code))
                                       
    logger.info('第{}章下载完毕'.format(page))
    return r.content


if __name__ == "__main__":
    main(230, 660)

