from urllib import request
import re
import os
import requests
url0='https://www.socwall.com'
urls=[]
urls.append(url0)
for i in range(2,4):
    urls.append(url0+'/wallpapers/'+'page:%d'%i)


    
for url in urls:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    response = requests.get(url,headers = headers) 
    response.encoding=response.apparent_encoding
    html=response.text
    pattern=re.compile(r'<a.*? href="(.*?)".*?/>')
    imglist=re.findall(pattern,html)#里面包含很多杂七杂八的字符串
    truelist=[]

    for item in imglist:
        if re.match(r'^/desktop.*?wallpaper-by-unknown-artist/',item):
            truelist.append(item)

x=1
for wallpaperpage in truelist:
    url1=url0+wallpaperpage[:-19]
    response1=requests.get(url1) 
    html1=response1.text
    pattern1=re.compile(r'<a href="(.*?)" class="download">')
    url2=re.findall(pattern1,html1)
    pic_urls=url0+url2[0]
    print('正在爬取第 '+'%d'%x+' 张图片：'+ pic_urls)
    root="D://pics//"
    path=root+'%d.jpg'%x
    #path=root+pic_urls.split('/')[-1]
    with open(path,"wb")as f:
        r=requests.get(pic_urls)
        f.write(r.content)
        f.close()
        print("文件保存成功")
    x+=1
    
    

