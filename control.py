# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:27:09 2022

@author: ss872
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import pyimgur


def getSoup(url,headers=None):   
    '''
    取得soup物件
    ''' 
    soup=None
    try:
        if headers!=None:
            resp=requests.get(url,headers=headers)
        else:
            resp=requests.get(url)
        
        
        if resp.status_code==200:
            resp.encoding='utf-8'
            soup=BeautifulSoup(resp.text,'lxml')    
    except:
        print('取得soup物件失敗...')
    
    return soup


def get_news():
    text=''
    try:
        url='https://tw.news.yahoo.com/'
        r=requests.get(url)
        soup=BeautifulSoup(r.text, 'lxml')
        cfs=soup.find_all('div',class_="Cf")
        domain_url='https://tw.news.yahoo.com/'
        datas=[]
        datas=[[cf.find('h3').text.strip(),cf.find('div',class_="C(#959595) Fz(13px) C($c-fuji-grey-f)! D(ib) Mb(6px)").text.strip(),domain_url+cf.find('a').get('href')] for cf in cfs]
        df=pd.DataFrame(datas,columns=['標題','來源','連結'])
        for i in range(5):
            text+=df['標題'][i]+'\n'+'來源:'+df['來源'][i]+'\n'+df['連結'][i]+'\n'
            text+='------------------------------------\n'
    except:
        text+='功能維護中'
        
    return text

def stop_work():
    try:
        url='https://www.dgpa.gov.tw/typh/daily/nds.html'
        r = requests.get(url)
        r.encoding='utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        trs=soup.find(id="Table").find_all('tr')
        data=''
        for tr in trs[:-1]:
            for td in tr.find_all('td'):
                data+=(td.text.strip())
                data+='\n'
            data+='---------------------------------\n'
    except:
        data+='功能維護中'
    return data

def stock(code,day):
        data=''
        df=pdr.DataReader(code,'yahoo',day)
        plt.figure(figsize=(12,4))
        plt.plot(df.index,df['Close'],label=code)
        plt.legend(fontsize=16)
        plt.grid(True)
        plt.title(code,fontsize=20,pad=20)
        plt.xlabel('Date',fontsize=20,labelpad=20)
        plt.ylabel('Share price',fontsize=20,labelpad=10)
        plt.tight_layout()
        plt.savefig('send.png')
        CLIENT_ID = "2f8541ae362bf06"
        PATH = "send.png"
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(PATH, title="temporary")
        df2=df['Close'][::-1].head()
        for i in range(len(df2)):
            data+='日期:'
            data+=str(df2.index[i])[0:10]
            data+='\n'
            data+='股價:'
            data+=str(round(df2.values[i],3))
            data+='\n'
        return [uploaded_image.link,data]


def Movie():
    url='https://movies.yahoo.com.tw/chart.html'
    soup=getSoup(url)
    datas=soup.find('ul',class_="ranking_list_r")
    text=''
    for data in datas.find_all('a'):
        text+=data.text.split('\n')[3]
        text+='\n'
        text+=data.get('href')
        text+='\n'
        text+='---------------------------------\n'
    return text











