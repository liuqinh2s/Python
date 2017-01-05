#!/usr/bin/env python3
# coding=utf-8

__author__ = 'liuqin'

import urllib.request
import re
import threading
import queue

IDdict = {}
#百度贴吧爬取用户ID，以minecraft吧为例
class BaiDuTieBa():
    def __init__(self, kw, pn):
        self.baseurl = "http://tieba.baidu.com/f/like/manage/list?"
        self.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
        self.headers = {'User-Agent': self.userAgent}
        self.kw = kw
        self.pn = pn
        self.IDdict = IDdict

    def getHTML(self):
        url = self.baseurl + 'kw=' + self.kw + '&' + 'pn=' + str(self.pn)
        request = urllib.request.urlopen(url)
        # 注意这里网页源码编码是：GBK，用decode解码时要选择gbk
        pageHTML = request.read().decode('gbk')
        return pageHTML

    def getUserID(self):
        regex = re.compile('.*?username="(.*?)".*?')
        pageHTML = self.getHTML()
        UserID = re.findall(regex, pageHTML)
        return UserID

    def writeIDinDict(self):
        UserID = self.getUserID()
        count = 0
        for id in UserID:
            count += 1
            self.IDdict[count + self.pn * 20] = id

    def start(self):
        self.getUserID()
        self.writeIDinDict()
        print(u'写入第%d页用户ID' % (self.pn))


def writeInFile():
    file = open(u'./百度贴吧minecraft吧用户ID.txt', 'a+', encoding='UTF-8')
    # print(file.encoding)
    for i in IDdict:
        file.write(IDdict[i]+'\n')
    file.close()


#具体要做的任务
def do_job(kw, pn):
    spider = BaiDuTieBa(kw, pn)
    spider.start()

def do_job1(kw, pn):
    spider = BaiDuTieBa(kw, pn)
    return spider

# 单线程爬虫
def NoThreads(kw, pn):
    for i in range(1, pn+1):
        do_job(kw, i)


# 即时创建即时销毁多线程
class Thread_spider(threading.Thread):

    def __init__(self, kw, pn):
        threading.Thread.__init__(self)
        self.pn = pn
        self.kw = kw

    def run(self):
        do_job(self.kw, self.pn)
def MultiThreads(kw, pn):
    threads1 = [Thread_spider(kw, i) for i in range(1, pn+1)]
    for i in threads1:
        i.start()
    for i in threads1:
        if i.is_alive: i.join()

# 用线程池和任务队列
class WorkManager(object):# 这是一个线程管理器
    def __init__(self, kw, work_num, thread_num):
        self.task_queue = queue.Queue()
        self.threads = []
        self.kw = kw
        self.__init_task_queue(work_num)
        self.__init_thread_pool(thread_num)
        self.start_task()

    """
        添加一项工作入队
    """
    def add_job(self, func):
        self.task_queue.put(func)  # 任务入队，Queue内部实现了同步机制

    """
        初始化任务队列
    """
    def __init_task_queue(self, jobs_num):
        for i in range(1, jobs_num + 1):
            self.add_job(do_job1(self.kw, i))

    """
        初始化线程池
    """
    def __init_thread_pool(self,thread_num):
        for i in range(1,thread_num+1):
            self.threads.append(Work(self.task_queue))

    """
        开始执行任务
    """
    def start_task(self):
        for i in self.threads:
            i.setDaemon(1)
            i.start()

    """
        等待所有线程运行完毕
    """
    def wait_allcomplete(self):
        for item in self.threads:
            item.join(1)

class Work(threading.Thread):# 这是线程类

    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue

    def run(self):
        while not self.task_queue.empty():
            self.task_queue.get().start()# 任务异步出队，Queue内部实现了同步机制
            self.task_queue.task_done()  # 通知系统任务完成


if __name__ == '__main__':
    kw = 'minecraft'  # 贴吧名称
    pn = 1000 # 页面数
    # 不用多线程模式
    # NoThreads(kw, pn)

    # 即时创建即时销毁，多线程模式
    # MultiThreads(kw, pn)

    # 任务队列线程池模式：（任务数：100，线程：10）
    threads_num = 100
    work_manager =  WorkManager(kw, pn, threads_num)
    work_manager.wait_allcomplete()

    print("hello world")
    writeInFile()
