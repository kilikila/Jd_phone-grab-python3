# ---- Condition
# ---- 捉迷藏的游戏
import threading, time
from os import _exit
import urllib.request
from urllib.request import urlretrieve

from JDphone.DAO.FileSave import SaveFile
from JDphone.DAO.DB_mysql import DB_Mysql

img_dirs=r"E:\Data\Music_LL"


config = {
    'host':'localhost',#'192.168.1.116',
    'port': 3306,
    'user': 'musicUser',#'newPC',
    'password': '123456',
    'db': 'liulimusic',
    'charset': 'utf8'
}

db=DB_Mysql(config)  #数据库
if not db:
    print("db对象声明失败，程序退出")
    _exit(0)

dataSet = db.getData("common","name","dLoadUrl")

def downLaodMusic():
    imgSave = SaveFile(img_dirs)
    imgSave.creatDirs("")
    i=0
    for res in dataSet:
        #imgSave.saveImg(res["dLoadUrl"],res["name"])

        user_agent = "Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 55.0.2883.87Safari / 537.36"
        try:
            req = urllib.request.Request(res["dLoadUrl"])
            req.add_header('User-agent', user_agent)
            f = urllib.request.urlopen(req,timeout=3)
            data = f.read()
            with open(r"E:\Data\Music_LL/" + res["name"]+".mp3", 'wb') as code:
                code.write(data)
        except:
            print(res["dLoadUrl"])
        finally:
            i+=1
            print("----"+str(i*100/len(dataSet))+"%----")

if __name__ =="__main__":
   # urlretrieve('http://www.moxpan.cc/data/2017013116222351049480.mp3', r"E:\Data\Music_LL\1")
   downLaodMusic()
#---------重试-------------错误链接保存----------------------
  # f=open(r"E:\Data\Music_LL\test.mp3", 'wb')
  # f.close()
   '''
   user_agent = "Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 55.0.2883.87Safari / 537.36"
   req = urllib.request.Request('http://www.moxpan.cc/data/2017013116222351049480.mp3')
   req.add_header('User-agent', user_agent)
   f = urllib.request.urlopen(req)
   data = f.read()
   with open(r"E:\Data\Music_LL/", 'wb') as code:
       code.write(data)
 '''
   pass