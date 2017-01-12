# coding:utf-8
import urllib.request
import urllib.parse
import urllib.response
import http.cookiejar

filename = "cookie.txt"
cookie = http.cookiejar.MozillaCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open("http://www.baidu.com")
cookie.save(ignore_discard=True, ignore_expires=True)
# ignore_discard的意思是即使cookie将被丢弃也将它保存下来
# ignore_expires的意思是如果已经存在cookie文件，就覆盖保存cookie文件
cookie.load("./cookie.txt", ignore_discard=True, ignore_expires=True)
postdata = urllib.parse.urlencode({})

