# 腾讯疫情实时地图

import requests
import pandas as pd
import json

url='https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
html=requests.get(url)
content=json.loads(html.text)
df=pd.DataFrame(columns=['国家和地区','确诊人数','死亡人数','治愈病例'])
for i in range(len(content['data'])):
     df.loc[i+1]=[content['data'][i]['name'],content['data'][i]['confirm'],
                  content['data'][i]['dead'],content['data'][i]['heal']]
df.to_csv('E://data_2.csv',index=0,encoding='utf_8_sig')
print('数据保存成功')

