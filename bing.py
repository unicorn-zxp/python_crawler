#爬取必应壁纸
# 注意指定爬取内容的存储目录和爬取的页面数量
import os
import re
import urllib.request
import requests
 
def get_one_page(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    response = requests.get(url,headers = headers)
    if(response.status_code == 200):
        return response.text
    return None
 
def download(url,filename):
    filepath = 'D:/桌面背景//  '+ filename + '.jpg'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    if os.path.exists(filepath):
        return
    with open(filepath,'wb')as f:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        f.write(response.read())

def parse(html):
    pattern  = re.compile('data-progressive="(.*?)".*?<h3>(.*?)</h3>')
    items = re.findall(pattern,html)
    for item in items:
        try:
            url = item[0].replace('800','1920').replace('480','1080')
            imagename = item[1].strip()
            rule = re.compile(r'[a-zA-z1-9()-/]')#[]用来表示一组字符【abc】匹配a,b,或c
            imagename = rule.sub('', imagename)
            download(url,imagename.strip())
            print(imagename,"正在下载")
        except Exception:
            continue
 
 
 
 
if __name__ == '__main__':
    for page in range(1,4):
        url = 'https://bing.ioliu.cn/?p='+str(page)
        print("正在抓取第", page, "页" ,url)
        html = get_one_page(url)
        parse(html)
