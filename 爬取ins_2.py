# -*- coding = utf-8 -*-
# _author_ = 'Unicorn'
# time :2021/5/14 0:38
# 'keep calm and carry on'

# 需要更改user_name就好，也需要找到第一个请求地址line21
# 但这种是有序的(按照发ins的顺序逆序爬取)
# 链接里的三个参数，id,first,after，可以不动

import re
import requests
import os


class Ins_Spider:
    def __init__(self, user_name, save_path, save_number):
        # 前十二张图片存储的地址
        self.url = 'https://www.instagram.com/{}/'.format(user_name)
        self.path = save_path
        self.number = save_number
        # 记录当前爬取图片的数目
        self.count = 0
        # 先确保能登录，然后记录下网站存储的cookie信息
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'cookie': 'mid=YJ1MBgALAAHbXzm9dZjijEu9y3q8; ig_did=72534081-1995-4C32-BA7D-DDEC136FB71A; ig_nrcb=1; csrftoken=V61Y3SjW8U6HeiCf1VTW7dPa3PfZu2Jh; ds_user_id=3881242613; sessionid=3881242613%3Ag77iFu2slgyshw%3A3; shbid=18069; shbts=1620921441.4445887; rur=VLL'}

        # 将动态加载的部分，有规律的部分用{}表示，便于后面的转义
        self.uri = 'https://www.instagram.com/graphql/query/?query_hash=32b14723a678bd4628d70c1f877b94c9&variables=%7B%22id%22%3A%221474952074%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%3D%3D%22%7D'
        # 第一个转义的字符串
        self.cursor_list = [
            'QVFDUDlpSVFrX2ppcUdPUGc0d05VYXE3MjRyQXR2cTdSbkc5d1dlX2hIb255YlF3WTRhdlFwclhPWkZnVjFWWGhjdTlNbFpaRTd5dHRuUkR5ZmV3bHBhaw']

    # 解析前十二张图片
    def parse_html_1(self):
        html_1 = requests.get(self.url, headers=self.headers).text
        pattern = re.compile(r'"display_url":"(.*?)","edge_media_to_tagged_user')
        first_img_url = re.findall(pattern, html_1)
        self.download(first_img_url)
        print('******************第一阶段的图片爬取完毕******************')

    # 解析剩下的图片
    def parse_html_2(self):
        while len(self.cursor_list) > 0:
            if self.count >= self.number:
                break
            html_url = self.uri.format(cursor=self.cursor_list[0])
            html = requests.get(html_url, headers=self.headers).text
            pattern1 = re.compile(r'"has_next_page":true,"end_cursor":"(.*?)=="}')
            # 为下一次跳转提供转义字符串
            # self.cursor_list.extend(re.findall(pattern1,html))
            pattern2 = re.compile(r'"display_url":"(.*?)","display_resources"')
            # 获取图片链接列表，但是这个链接中有转义字符\u0026，需要变成&，放在download函数中处理
            img_url_list = re.findall(pattern2, html)
            self.download(img_url_list)
            self.cursor_list = re.findall(pattern1, html)

    # 下载，只考虑图片，不考虑视频
    def download(self, img_list):
        if len(img_list) == 0:
            exit()
            # img_list = list(set(img_list))  # 直接去重会乱序
        vis = set()
        for img in img_list:
            # 标准化图片下载链接
            if img in vis:
                continue
            vis.add(img)
            img = img.replace('\\u0026', '&')
            r = requests.get(img, headers=self.headers)
            if r.status_code != 200:
                print('图片链接无法访问')
                continue
            with open(self.path + '/' + '%d.jpg' % self.count, 'wb') as f:
                f.write(r.content)
                print('图片保存成功')
                f.close()
            self.count += 1
            #  保存的图片达到预设，退出程序
            if self.count >= self.number:
                break


if __name__ == '__main__':
    # name = 'meyoco'
    name = 'seinonana'
    path = 'E:/pic/%s' % name
    if not os.path.exists(path):
        os.makedirs(path)
    number = 100
    demo = Ins_Spider(user_name=name, save_path=path, save_number=number)
    demo.parse_html_1()
    demo.parse_html_2()
    print('******************图片爬取完毕******************')