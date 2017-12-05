from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from ..items import Doubanmovie250Item
from scrapy.http import Request
#from ..get_cookies import TransCookie
from scrapy.conf import settings #从settings文件中导入Cookie，这里也可以from scrapy.conf import settings.COOKIE
import random
import string
import re
import traceback


class MovieSpider(CrawlSpider):
    name = "douban_movie250_spider"
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    cookie = settings['COOKIE']  # 带着Cookie向网页发请求
    """
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        }
    """
    cookies = "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    #cookies = "ll='118282'; bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    #trans_cookies = TransCookie(cookies).stringToDict()
    #print(trans_cookies)

    def parse(self, response):

        urls = ["https://movie.douban.com/top250?start={}&filter=".format(str(25*i)) for i in range(0, 10)]
        for i, url in enumerate(urls):
            #'dont_merge_cookies': True
            yield Request(url, meta={'cookiejar': i,'dont_merge_cookies': True}, callback=self.parse_list)

    def parse_list(self, response):
        selector = Selector(response)
        infos = selector.xpath('//ol[@class="grid_view"]/li')
        #获取每页电影的部分数据，包括detail_url
        for info in infos:
            detail_url = info.xpath('div/div[2]/div[@class="hd"]/a/@href').extract()[0]
            name = info.xpath('div/div[2]/div[@class="hd"]/a/span[1]/text()').extract()[0]
            quote = info.xpath('div/div[2]/div[@class="bd"]/p/span[@class="inq"]/text()').extract()[0] if info.xpath('div/div[2]/div[@class="bd"]/p/span[@class="inq"]/text()') else "无"
            score = float(info.xpath('//span[@property="v:average"]/text()').extract()[0])
            yield Request(detail_url, meta={'cookiejar': response.meta['cookiejar'],'name': name,'detail_url': detail_url,'quote': quote,'score': score},callback=self.parse_item)

    def parse_item(self, response):
        item = Doubanmovie250Item()
        item['name'] = response.meta['name']
        item['detail_url'] = response.meta['detail_url']
        item['top'] = int(response.xpath('//span[@class="top250-no"]/text()').extract()[0][3:])
        item['score'] = response.meta['score']
        item['quote'] = response.meta['quote']
        item['year'] = int(response.xpath('//div[@id="content"]/h1/span[2]/text()').extract()[0][1:-1])
        item['director'] = response.xpath('//a[@rel="v:directedBy"]/text()').extract()
        item['scriptwriter'] = response.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()').extract()
        item['actor'] = response.xpath('//a[@rel="v:starring"]/text()').extract()
        item['classification'] = response.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract()
        item['showtime'] = response.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract()
        item['film_time'] = response.xpath('//div[@id="info"]/span[@property="v:runtime"]/text()').extract()
        item['alias'] = response.xpath('//div[@id="info"]').re(r'</span> (.+)<br>\n')[-2]
        item['IMDb_url'] = response.xpath('//div[@id="info"]/a/@href').extract()[0]
        item['votes'] = int(response.xpath('//span[@property="v:votes"]/text()').extract()[0])
        item['describe'] = response.xpath('//div[@id="link-report"]/span/text()').re(r'\S+')[0]
        check_item = response.xpath('//div[@id="info"]').re(r'</span> (.+)<br>\n')[1]
        result = self.check_contain_chinese(check_item)
        # 有些电影详情页信息包含有官方网站，比如：https://movie.douban.com/subject/1291552/
        if result:
            item['made_country'] = response.xpath('//*[@id="info"]').re(r'</span> (.+)<br>\n')[1]
            item['language'] = response.xpath('//*[@id="info"]').re(r'</span> (.+)<br>\n')[2]
        else:
            item['made_country'] = response.xpath('//*[@id="info"]').re(r'</span> (.*)<br>\n')[2]
            item['language'] = response.xpath('//*[@id="info"]').re(r'</span> (.*)<br>\n')[3]
        yield item
    #判断字符串是否含有汉字
    def check_contain_chinese(self, check_str):
        #for ch in check_str.decode('utf-8'):
        Pattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = Pattern.search(check_str)
        if match:
            return True
        else:
            return False

