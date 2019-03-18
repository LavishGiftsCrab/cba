import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import pandas as pd
from tqdm import *
baseUrl = "https://cba.hupu.com/players"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0','Referer':'https://nba.hupu.com/teams'}

def getTeamUrl():
    req=requests.get(baseUrl,headers=headers,timeout=10)
    soup=BeautifulSoup(req.content,'html5lib')
    teamAll = soup.select('div.overtop tr[valign="top"] a')
    teamLink = []
    for i in teamAll:
        teamLink.append('https://cba.hupu.com/players/'+i.get('href'))
    return teamLink

def getPlayerLink(url):
    try:
        req=requests.get(url,headers,timeout=10)
    except Exception as e:
        print(e)
    soup = BeautifulSoup(req.content,'html5lib')
    teamAll1 = soup.select('div.players_content_padding tr[style="color:#990000"] a')
    teamAll2=soup.select('div.players_content_padding tr[style="color: #990000"] a')
    playerLink1 = []
    playerLink3 = []
    playerLink2 = []
    playerLink=[]
    for i in teamAll1:
        playerLink1.append(i.get('href'))
    for j in teamAll2:
        playerLink2.append(j.get('href'))
    playerLink3=playerLink1+playerLink2;
    for k in playerLink3:
        playerLink.append('https://cba.hupu.com'+k)
    #playerLink=list(map(lambda tag:tag.get('herf'),soup.select('div.players_content_padding')))
    return playerLink

def getData(url):
    try:
        req = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(e)
    Dict=OrderedDict()
    soup=BeautifulSoup(req.content,'html5lib')
    Dict['nam']=soup.select('div.players_content_padding strong')[0].get_text()[0:]
    Dict['pos']=soup.select('div.players_content_padding a')[0].get_text()[0:]
    Dict['hei']=soup.select('div.players_content_padding td[width="26%"]')[0].get_text().split("\n")[1].strip("\t")[4:]
    Dict['wei']=soup.select('div.players_content_padding td[width="26%"]')[0].get_text().split("\n")[2].strip("\t")[4:]
    normal=[]
    score=[]
    for i in range(15,32):
        normal.append(soup.select('div.overtop tr[bgcolor="#999999"] td')[i].get_text())
        score.append(soup.select('div.overtop tr[bgcolor="#f4f4f4"] td')[i+30].get_text())
    detail=dict(zip(normal,score))
    Dict=dict(Dict)
    Dict.update(detail)
    df=pd.DataFrame([Dict])
    return df

def saveData(df):
    # utf_8_sig 防止乱码中文
    df.to_csv('CBA.csv',index=0,encoding="utf_8_sig")

if __name__=="__main__":

    df=pd.DataFrame()
    link=getTeamUrl()
    playerLink=[]
    for tag in link:
        playerLink+=getPlayerLink(tag)
    print(len(playerLink))
    for p in tqdm(playerLink):
        df = df.append(getData(p),ignore_index=True)
        #print(df.size)
    print(df)
    saveData(df)


