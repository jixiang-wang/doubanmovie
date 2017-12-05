class TransCookie():
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

"""
if __name__ == "__main__":
    cookie = 'll="118282"; bid=gW82DXCly0w; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1505057433%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __yadk_uid=mILZdrvyv011DqEyFn9cbek4btuNpreV; _vwo_uuid_v2=17D8992592E4381EE39A5B9857C7276A|4e92f0e70dc7e463198a514416ef5851; __utma=30149280.867240807.1505057433.1505057433.1505057433.1; __utmb=30149280.0.10.1505057433; __utmc=30149280; __utmz=30149280.1505057433.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1627397909.1505057433.1505057433.1505057433.1; __utmb=223695111.0.10.1505057433; __utmc=223695111; __utmz=223695111.1505057433.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=6ebe03a3f42969f2.1505057433.1.1505057452.1505057433.; _pk_ses.100001.4cf6=*'
    trans = TransCookie(cookie)
    print(trans.stringToDict())
"""