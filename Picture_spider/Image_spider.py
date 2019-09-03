# -*- coding: utf-8 -*-
# author :HXM


import os
import sys
import time
import random
import requests
from multiprocessing import Pool


class Image():

    def __init__(self, query, start_page):
        '''
        初始化变量
        :param query:
        '''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'cookie': 'cookie: ugid=bc3daf0cf0358953543823f494d646e65181880; lux_uid=155456416425039679; _sp_ses.0295=*; _ga=GA1.2.927584132.1554564164; _gid=GA1.2.2067052407.1554564164; _gat=1; uuid=d3e54660-587f-11e9-b876-258be7230c3c; xpos=%7B%7D; _sp_id.0295=c6a0b006-76df-45f7-9040-e0eb225a2e49.1554564164.1.1554564202.1554564164.afdc0c70-8900-4a66-80a2-b96e46015489'
        }

        self.url = 'https://unsplash.com/napi/search/photos'

        self.query = query
        self.start_page = start_page

    def get_page(self, page):
        '''
        1.默认创建images文件夹
        2.传入参数,将数据格式化
        :param page:
        :return:
        '''

        if not os.path.exists('images'):
            os.makedirs('images')

        params = {
            'query': self.query,
            'xp': '',
            'per_page': 20,
            'page': page
        }

   
        response = session.get(url=self.url, params=params, headers=self.headers)

        try:
            if response.status_code == 200:
                # print(response.content.decode('utf-8'))
                return response.json()
            else:
                return None
        #     排除异常
        except Exception as e:

            print("error is %s" % e)

    pass

    def page_parse(self, htmls):
        '''
        1.数据解析提取
        2.清洗返回字典
        :param htmls:
        :return:
        '''
        jsons = htmls.get('results')

        for json in jsons:
            url = json.get('urls').get('full')

            yield {
                'url': url
            }

    pass

    def save(self, items):
        '''
        1.字典的遍历
        2.保存图片在images文件中
        :param items:
        :return:
        '''
        try:
            for item in items:
                responses = requests.get(url=(item.get('url')), headers=self.headers)
                if responses.status_code == 200:
                    # 随机命名图片
                    name = random.randint(1000, 9999)
                    # 设置开始时间
                    start_time = time.time()
                    # 保存图片
                    with open('images/{}.jpg'.format(name), 'wb')as f:

                        f.write(responses.content)
                        # 模拟进度条
                        for i in range(100):
                            k = i + 1

                            str = '>' * (i // 2) + '' * ((100 - k) // 2)

                            sys.stdout.write('\r' + str + '[%s%%]' % (i + 1))

                            sys.stdout.flush()

                            time.sleep(0.01)
                    #         结束时间
                    end_time = time.time()

                    print("Download %s.jpg success! It cost %.2f s" % (name, (end_time - start_time)))
                else:
                    print("Download fail!")

        except Exception as e:

            print("Download %s" % e)

    pass

    def total_size(self, path):
        '''
        递归计算文件夹大小
        增加文件计算代码优化
        :param path:
        :return:
        '''
        size_sum = 0
        file_list = os.listdir(path)
        for name_list in file_list:

            abs_path = os.path.join(path, name_list)
            if os.path.isdir(abs_path):

                size = self.total_size(abs_path)
                size_sum += size
            else:
                size_sum += os.path.getsize(abs_path)
        return size_sum

    def run(self):
        '''
        启动函数,并开始抓取
        :return:
        '''
        pages = int(self.start_page) + 2
        for page in range(2, pages, 1):
            htmls = self.get_page(page=page)

            items = self.page_parse(htmls=htmls)

            self.save(items)

            time.sleep(1)

            sizes = float(self.total_size('images'))

            real_size = sizes / 1024 / 1024

            print("抓取第%s页成功,目前文件夹总大小 %.2f MB" % (page, real_size))
        pass


GROUP_START = 0
GROUP_END = 8

if __name__ == '__main__':
    '''
    交互界面
    开启多线程池
    '''
    query = input("请输入关键字(例如 animal):")
    page = input("请输入抓取的页数:")

    pool = Pool()

    groups = ([x * 15 for x in range(GROUP_START, GROUP_END + 1)])

    spider = Image(query=query, start_page=page)

    pool.map(spider.run(), groups)

    pool.join()

    pool.close()
