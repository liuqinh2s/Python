# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2, json
import urllib
import re
import random
import hashlib
import cookielib
from urllib import urlencode
from lxml import etree
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "weixin9047"  # 这里改写你在微信公众平台里输入的token
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # sha1加密算法
        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        content = xml.find("Content").text  # 获得用户所输入的内容
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        if (content == u"天气"):
            url = "http://m.ip138.com/21/nanjing/tianqi/"
            headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
            req = urllib2.Request(url, headers=headers)
            opener = urllib2.urlopen(req)
            html = opener.read()
            rex = r'(?<=img src="/image/s[0-9].gif" alt=").{1,6}(?=" />)'
            rexx = r'(?<=div class="temperature">).{5,15}(?=</div>)'
            n = re.findall(rex, html)
            m = re.findall(rexx, html)
            str_wether = ""
            for (i, j) in zip(m, n):
                str_wether = str_wether + j + "     " + i + "\n"
            return self.render.reply_text(fromUser, toUser, int(time.time()), "最近五天天气:\n" + str_wether)
        elif (content[0:2] == u"电影"):
            keyword = urllib.quote(content[2:].encode("utf-8"))
            url = "http://www.wangpansou.cn/s.php?q=" + keyword
            headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
            req = urllib2.Request(url, headers=headers)
            opener = urllib2.urlopen(req)
            html = opener.read()
            rex = r'https?://pan.baidu.com.*\?uk=[0-9]{10}.*[\d+?]"'
            m = re.findall(rex, html)
            string = u""
            for i in m:
                string = string + i + "\n"
            return self.render.reply_text(fromUser, toUser, int(time.time()), u"以下是电影链接：\n" + string)
        elif (u"段子" in content):
            url_8 = "http://www.qiushibaike.com/"
            url_24 = "http://www.qiushibaike.com/hot/"
            headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
            req_8 = urllib2.Request(url_8, headers=headers)
            req_24 = urllib2.Request(url_24, headers=headers)
            opener_8 = urllib2.urlopen(req_8)
            opener_24 = urllib2.urlopen(req_24)
            html_8 = opener_8.read()
            html_24 = opener_24.read()
            rex = r'(?<=div class="content">).*?(?=<!--)'
            m_8 = re.findall(rex, html_8, re.S)
            m_24 = re.findall(rex, html_24, re.S)
            m_8.extend(m_24)
            random.shuffle(m_8)
            return self.render.reply_text(fromUser, toUser, int(time.time()), m_8[0].replace('<br/>', ''))
        elif (content[0:2] == u"开源"):
            url = "https://www.oschina.net/action/user/hash_login"
            urll = "http://www.oschina.net/action/tweet/pub"
            username = "904727147@qq.com"
            passw = ""  # 密码肯定不会给你们的
            password = hashlib.sha1(passw).hexdigest()
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
            urllib2.install_opener(opener)
            data = {'email': username, 'pwd': password}
            data_post = urllib.urlencode(data)
            opener.open(url, data_post)
            user = "2391943"
            msg = content[2:].encode("utf-8")
            user_code = "lPFz26r3ZIa1e3KyIWlzPNpJlaEmZqyh6dAWAotd"
            post = {'user_code': user_code, 'user': user, 'msg': msg}
            msg_post = urllib.urlencode(post)
            html = urllib2.urlopen(urll, msg_post).read()
            return self.render.reply_text(fromUser, toUser, int(time.time()), u"发送到开源中国动弹成功！")
        elif (content[0:2] == u"快递"):
            keyword = content[2:]
            url = "http://www.kuaidi100.com/autonumber/autoComNum?text=" + keyword
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
            urllib2.install_opener(opener)
            html = urllib2.urlopen(url).read()
            jo = json.loads(html)
            typ = jo["auto"][0]['comCode']
            if (typ is None):
                return self.render.reply_text(fromUser, toUser, int(time.time()), u"请检查你的定单号！")
            urll = "http://www.kuaidi100.com/query?type=" + typ + "&postid=" + keyword
            html_end = urllib2.urlopen(urll).read()
            jo_end = json.loads(html_end)
            if (jo_end["status"] == "201"):
                return self.render.reply_text(fromUser, toUser, int(time.time()), u"订单号输入有误，请重新输入！")
            text = jo_end["data"]
            string = u""
            for i in text:
                string = string + i["time"] + i["context"] + "\n"
            return self.render.reply_text(fromUser, toUser, int(time.time()), string)
        elif (content == u"微博热点"):
            url = "http://weibo.cn/pub/?tf=5_005"
            headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
            req = urllib2.Request(url, headers=headers)
            opener = urllib2.urlopen(req)
            html = opener.read().decode("utf-8")
            rex = r'(?<=div class="c"><a href=").{60,79}(?=</a>)'
            ss = re.findall(rex, html)
            string = u""
            for i in ss:
                string = string + i.replace('>', '\n') + "\n"
            return self.render.reply_text(fromUser, toUser, int(time.time()), string.replace('"', ''))
        elif (content == u"知乎信息"):
            username = '18362983803'
            password = ''  # 这是以前的密码别尝试了
            _xsrf = '558c1b60725377c5810ae2484b26781e'
            url = r'https://www.zhihu.com/login/phone_num'
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
            data = urllib.urlencode({"phone_num": username, "password": password, '_xsrf': _xsrf})
            opener.open(url, data)
            html = opener.open('https://www.zhihu.com/noti7/new?r=1454793308655').read()
            jo = json.loads(html)
            data = jo[1]
            string = "增长了：" + str(data[0]) + "个评论" + str(data[1]) + "个粉丝" + str(data[2]) + "个赞同"
            return self.render.reply_text(fromUser, toUser, int(time.time()), string)
        elif (content[0:2] == u"闹钟"):
            string = str(time.strftime("%H:%M", time.localtime()))
            if (string == content[2:]):
                mail_info = {
                    "from": "904727147@qq.com",
                    "to": "904727147@qq.com",
                    "hostname": "smtp.qq.com",
                    "username": "904727147@qq.com",
                    "password": "himnbtwxa",
                    "mail_subject": "懒猪起床！",
                    "mail_text": "起床了，猪",
                    "mail_encoding": "utf-8"
                }
                smtp = SMTP_SSL(mail_info["hostname"])
                smtp.set_debuglevel(1)

                smtp.ehlo(mail_info["hostname"])
                smtp.login(mail_info["username"], mail_info["password"])

                msg = MIMEText(mail_info["mail_text"], "plain", mail_info["mail_encoding"])
                msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
                msg["from"] = mail_info["from"]
                msg["to"] = mail_info["to"]
                i = 0
                while (i < 20):
                    j = 0
                    while (j < 2):
                        smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
                        j = j + 1
                    i = i + 1
                    time.sleep(10)

                smtp.quit()

                return self.render.reply_text(fromUser, toUser, int(time.time()), string)
            return self.render.reply_text(fromUser, toUser, int(time.time()), string + u"879")
        elif (u"钟志远" in content):
            return self.render.reply_text(fromUser, toUser, int(time.time()),
                                          u"你想找全世界最帅的人干嘛？如果你是妹子，请加微信18362983803！汉子绕道！")
        elif (u"使用" in content):
            return self.render.reply_text(fromUser, toUser, int(time.time()),
                                          u"搜电影:电影+电影名,最近天气：天气，微博热门：微博热点，知乎信息：知乎信息，快递查询：快递+单号，看笑话：段子，发送动弹到开源中国：开源+内容")
        else:
            url = r'http://www.xiaohuangji.com/ajax.php'
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0')]
            string = urllib.quote(content.encode("utf-8"))
            try:
                data = urllib.urlencode({"para": string})
                html = opener.open(url, data).read()
                string = html + "\n----[回复[使用]]"
                return self.render.reply_text(fromUser, toUser, int(time.time()), string)
            except Exception, ex:
                return self.render.reply_text(fromUser, toUser, int(time.time()), u"我不想理你了～")


