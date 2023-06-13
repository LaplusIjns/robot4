# -*- coding: utf8 -*-
"""
{"pttuser": 
    [
        {"pttid": "a000000000", 
         "latest_push": ": \u5f9e\u80fd\u767b\u8b8a\u65e9\u898b", 
         "latest_title": "[\u6c34\u661f] \u8607\u5abd\u7684\u7d50\u5c40\u8981\u600e\u9ebc\u624d\u4e0d\u6703\u721b\u6389\uff1f"
         } 
    ]
}
"""
import json
from bs4 import BeautifulSoup
# import time
import urllib.request as req
user=['a000000000','plzza0cats']
ban_word = [": 那是假ee真cs刷題仔",": 有錢人家吃你懶覺 沒錢你吃雞腿就好",": 有錢人家吃你懶覺  沒錢你吃雞腿就好",": 還不是代工",": c52.exe是崩不應求",": 我看見一切  我看見永恆  我看見奇蹟  我看見解救的神"]
global flag1
global notsavefile
# nowtime_day = time.localtime(time.time()).tm_yday
def findpush():
    # 載入舊資料
    with open('push.json','r', encoding='utf-8') as f:
        json_object=json.load(f)
        f.close
    # 預備用於寫入新資料
    with open('push.json','r', encoding='utf-8') as ff:
        json_object_new=json.load(ff)
        ff.close
    # print(json_object)
    userAgent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'
    }
    for usercount in range(len(json_object['pttuser'])):
        print("=============="+user[usercount]+"============")
        # flag1判斷是否跳離迴圈
        # savefile 判斷紀錄最新推文
        flag1 = 0
        notsavefile = True
        # print(json_object['pttuser'][usercount]['latest_push'])
        url='https://www.pttweb.cc/user/'+user[usercount]+'?t=message&page=0'

        request = req.Request(url,headers=userAgent)
        with req.urlopen(request) as resopnse:
            data = resopnse.read().decode("utf-8")
        root = BeautifulSoup(data,"html.parser")
        pusha1 = root.find_all("div",class_="thread-item")
        print("尋找上次紀錄文章: "+json_object['pttuser'][usercount]['latest_title'])
        print("尋找上次推文:"+json_object['pttuser'][usercount]['latest_push'])
        # 單頁全部文章
        for thread in range(len(pusha1)):
            print("當前文章位置: "+str(thread))    
            # print(pusha1[thread].text)
            thread_board = pusha1[thread].find("span",class_="thread-list-board").text
            if(thread_board=="[ FireEmblem ]"):
                continue
            thread_title = pusha1[thread].find("span",class_="thread-title").text
            thread_url = pusha1[thread].find("a",href=True)
            total_push = pusha1[thread].find_all("span",class_="yellow--text text--darken-2")
            total_time = pusha1[thread].find_all("span",class_="ml-3 grey--text text--lighten-1")
            # 全部推文內容
            buffer1 = [x.text for x in total_push]
            # 推文時間
            buffer2 = [y.text for y in total_time]
            # 找到結束點離開
            if json_object['pttuser'][usercount]['latest_title'] == thread_title and json_object['pttuser'][usercount]['latest_push'] == buffer1[(len(buffer1)-1)]:
                print("找到目標 停止搜尋")
                flag1=1
                break
            # 當前文章為上次最後文章
            if json_object['pttuser'][usercount]['latest_title']== thread_title :
                print("進入上次最後文章")
                tmp = 0
                for z in range(len(buffer1)):
                    print("總推文:"+str(z))
                    if json_object['pttuser'][usercount]['latest_push'] == buffer1[z]:
                        print("找進入上次最後文章時最後更新推文")
                        tmp=z+1
                        # print(tmp)
                        for i in range(tmp,len(buffer1)):
                            print(user[usercount]+" "+buffer1[i]+"  "+buffer2[i])
                        continue
                    print("找完同篇剩餘推文")
                    flag1=1
            print("renew data") 
            # 更新json檔為最新資料
            if notsavefile:
                    with open('push.json', 'w', encoding='utf-8') as openfile1:
                        json_object_new['pttuser'][usercount]['latest_title'] = thread_title
                        json_object_new['pttuser'][usercount]['latest_push'] = buffer1[(len(buffer1)-1)]
                        json.dump(json_object_new,openfile1)
                        openfile1.close
                        notsavefile = False
                        print("update file!!  111")
            if(flag1==1):
                break;        
            #  當文章有簽名檔跳過文章
            if(flag1 !=1 and any (word in buffer1 for word in ban_word )):
                    continue
            print(thread_board+" "+thread_title)
            # await channel.send("```fix"+"\n"+thread_board+" "+thread_title+"\n"+"```")
            print("https://www.ptt.cc"+thread_url['href']+".html")
            # await channel.send("<https://www.ptt.cc"+thread_url['href']+".html>")
            # 分析單文章內全部推文
            for z in range(len(buffer1)):
                print("推文位置 "+str(z))
                # print("===456===")
                # print("======find"+json_object['pttuser'][usercount]['latest_push'])
                if json_object['pttuser'][usercount]['latest_push'] == buffer1[z]:
                    print("find_latest_push")
                    flag1=1
                if flag1==1:
                    print("結束迴圈")
                    break;    
                if flag1==0:
                    print(user[usercount]+" "+buffer1[z]+"  "+buffer2[z])

findpush()