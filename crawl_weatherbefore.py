#直接爬取表格，以一年的数据为例子

import requests
import re
import pandas as pd

def get_page(year):
    page_list=[]
    for i in range(1,10):
        page_list.append('http://tianqihoubao.com/lishi/feidong/month/%d0%d.html'%(year,i))
    page_list.append('http://tianqihoubao.com/lishi/feidong/month/%d10.html'%year)
    page_list.append('http://tianqihoubao.com/lishi/feidong/month/%d11.html'%year)
    page_list.append('http://tianqihoubao.com/lishi/feidong/month/%d12.html'%year)
    return page_list

def get_html(url):
    return requests.get(url).text

def parse_html(html):
    pattern=re.compile(r'<td>(.*?)</td>',re.S)
    content=re.findall(pattern,html)
    rule1=re.compile(r'[<b>\n\r<a> ]')
    rule2=re.compile(r'href=.*?天气预报"',re.S)
    for i in range(len(content)):
        content[i]=re.sub(rule2,'',content[i])
        content[i]=re.sub(rule1,'',content[i])
    return content

def save_file(path,content):
    df=pd.DataFrame(columns=['日期','天气状况','气温','风力风向'])
    for i in range(int(len(content)/4-1)):
        index=4*(i+1)
        df.loc[i+1]=[content[index][:-1],
                    content[index+1],
                    content[index+2],
                    content[index+3]]
    df.to_csv(path,index=0,encoding='utf_8_sig')
    
if __name__=='__main__':
    page_list=get_page(2019)
    for page in page_list:
        html=get_html(page)
        content=parse_html(html)
        save_file('E://天气后报//%s.csv'%page[-11:-5],content)
    print('文件保存成功')
    
    
