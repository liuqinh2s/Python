#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'a spider for 嗅事百科'

__author__ = 'liuqin'

import urllib.request
import urllib.response
import re

# 糗事百科爬虫类
class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'mozilla/5.0 (macintosh; intel mac os x 10_12_2) applewebkit/537.36 (khtml, like gecko) chrome/55.0.2883.95 safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        #存放段子的变量，每个元素是一页段子
        self.stories = []
        #程序是否继续运行的变量
        self.enable = False

    def getpage(self, pageIndex):
        url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
        #用urlopen()获取页面源码
        request = urllib.request.urlopen(url)
        #用decode()转码
        pageCode = request.read().decode('utf-8')
        return pageCode

    def getPageItem(self, pageIndex):
        pageCode = self.getpage(pageIndex)
        if not pageCode :
            print("页面加载失败。。。")
            return None
        pattern = re.compile('author.*?alt="(.*?)".*?content">.*?<span>(.*?)</span>(.*?)number">(.*?)<.*?>', re.S)
        items = re.findall(pattern, pageCode)
        #用来存储每页的段子
        pageStories = []
        for item in items:
            # 如果有图则抛弃这条段子
            haveImg = re.search("img", item[2])
            if(haveImg):
                continue
            else:
                # 把<br/>替换成'\n'
                replaceBR = re.compile(r'(<br\s*/>)')
                text = re.sub(replaceBR, '\n', item[1])
                # item[0]是作者，text是段子内容，item[3]是点赞的数量
                pageStories.append([item[0], text, item[3]])

        return pageStories

    #加载并提取页面内容，加入到stories中
    def loadPage(self):
        # 如果当前页面少于2页，则新加载一页
        if self.enable == True:
            if len(self.stories)<2:
                # 获取新的一页
                pageStories = self.getPageItem(self.pageIndex)
                # 存储这页段子
                if pageStories:
                    self.stories.append(pageStories)
                    # 页面索引加一
                    self.pageIndex += 1

    # 调用该方法，每次回车打印输出一条段子
    def getOneStory(self, pageStories, page):
        # 遍历一页段子
        for story in pageStories:
            # 等待输入回车
            input = input()
            # 每次输入回车，先判断是否需要加载页面
            self.loadPage()
            # 如果输入Q，则结束程序
            if input == 'Q':
                self.enable = False
                return
            print(u"第%d页\t发布人:%s\t赞:%s\n%s" %(page,story[0],story[2],story[1]))

    # 开始方法
    def start(self):
        print(u"正在读取糗事百科，回车查看新段子，输入Q退出程序")
        # enable变为True，程序可正常运行
        self.enable = True
        # 先加载一页
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()
