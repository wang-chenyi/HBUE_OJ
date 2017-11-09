# coding:utf-8
import cookielib
import urllib
import urllib2

# 第一个参数是需要获得代码的url，第二个是对服务器请求的请求次数，
from bs4 import BeautifulSoup


def download(url, num_retries=2):
    print('Downloading:', url)
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print('Download error: ', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry Sxx HTTP errors
                return download(url, num_retries - 1)
    return html

class HBUE:
    def __init__(self, username, password):
        # 通过登录后获取 cookie
        self.cookie = ''
        # 获得模拟登陆后的url
        self.res_url = ''
        # 设置登录成功后的请求头中的Referer
        self.referer = ''
        # 定义登陆url
        self.login_url = 'http://218.197.80.13/xtgl/login_login.html'
        # 定义cookie
        self.cj = cookielib.CookieJar()
        # 定义用户名和密码
        self.username = username
        self.passwd = password
        # 对登陆数据进行编码
        self.encode_data = urllib.urlencode({
            # 从网页中分析得到的表单的属性  yhm 、mm， 具体代码见下
            'yhm': self.username,
            'mm': self.passwd,
        })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

    # 模拟登录
    def login(self):
        # 构造请求， 在登录时不检查请求头
        request = urllib2.Request(self.login_url, self.encode_data)
        # 得到反馈结果
        response = self.opener.open(request)
        # 一系列后续设置
        self.res_url = response.geturl()
        self.cookie = self.res_url[46:89].upper()
        self.referer = self.res_url.replace(';' + self.cookie, '')

    def getInf(self):
        headers = {
            'Referer': self.referer,
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Cookie': self.cookie,
        }
        data = {
            'dyym': '/xsxxxggl/xsgrxxwh_cxXsgrxx.html',
            'gnmkdm': 'N100801',
            'gnmkdmKey': 'index',
            'gnmkmc': '%E6%9F%A5%E8%AF%A2%E4%B8%AA%E4%BA%BA%E4%BF%A1%E6%81%AF',
            'layout': 'func-layout',
            'sessionUserKey': self.username,
        }
        # 对post的数据进行编码
        encoded_data = urllib.urlencode(data)
        url = 'http://218.197.80.13/xsxxxggl/xsgrxxwh_cxXsgrxx.html'
        req = urllib2.Request(url=url, data=encoded_data, headers=headers)
        response = urllib2.urlopen(req)
        res = response.read()
        soup = BeautifulSoup(res, 'lxml')
        inf_id = {
            'student_id': 'col_xh',
            'real_name': 'col_xm',
            'student_class': 'col_bh_id',
            'email': 'col_dzyx',
        }

        inf = {}
        for key, value in inf_id.items():
            inf[key] = soup.find(id=value).get_text().strip()
        return inf
