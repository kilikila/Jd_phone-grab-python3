import threading
from os import _exit

from bs4 import BeautifulSoup

from JDphone.CrawlDrivers.pyDriver import *
from JDphone.CrawlDrivers.BrowerDriver import PhDriver
from JDphone.DAO.DB_mysql import DB_Mysql
from JDphone.DAO.FileSave import SaveFile

config = {
    'host':'localhost',#'192.168.1.116',
    'port': 3306,
    'user': 'musicUser',#'newPC',
    'password': '123456',
    'db': 'liulimusic',
    'charset': 'utf8'
}

main_href="http://www.hacg.fi/wp/"
seed_href="http://www.hacg.fi/wp/page/"

phantomjs_path=r"D:\mySoftware\phantomjs-2.1.1-windows\bin\phantomjs.exe"

img_dirs=r"E:\Data\Liuli_Music"


#抓取数据存储到数据库中，建立两张表->常规表--音乐表
#歌曲名-下载链接-来源链接-标签名(音乐)-描述语言
#音乐标签->进入

phone_hrefs=[] #各个品牌链接集合
shop_hrefs=[]  #各个店铺链接集合

db=DB_Mysql(config)  #数据库
if not db:
    print("db对象声明失败，程序退出")
    _exit(0)



imgSave= SaveFile(img_dirs)

#db.creatTable("common",{"BrandName":"varchar(40)","imgUrl":"varchar(60)"})
#db.creatTable("musicLab",{"BrandName":"varchar(40)","imgUrl":"varchar(60)"})
'''
    while bgIndex!=edIndex:
        i_lock.acquire()
        bgIndex += 1
        index_t =bgIndex
        i_lock.release()
        if not driver.getPage(orgHref+str(bgIndex),"main"): continue#应当报错
        bsObj = BeautifulSoup(driver.getPgSrc(), "html.parser")

    while bgIndex!=edIndex:
        i_lock.acquire()
        bgIndex += 1
        index_t =bgIndex
        i_lock.release()
        pageSrc =getHtml(orgHref+str(index_t))
        if not pageSrc: continue#应当报错
        bsObj = BeautifulSoup(pageSrc, "html.parser")
    '''
def commonCrawl(edIndex,orgHref,i_lock):
    '''扒取常规外挂音乐数据'''
    global bgIndex

    #driver = PhDriver(phantomjs_path, orgHref+str(bgIndex), "content")  # 浏览器驱动器-开始到s扒取主页面

    '''
 while bgIndex != edIndex:
        i_lock.acquire()
        bgIndex += 1
        index_t =bgIndex
        i_lock.release()
        if not driver.getPage(orgHref + str(index_t), "main"): continue  # 应当报错
        bsObj = BeautifulSoup(driver.getPgSrc(), "html.parser")

    '''

    while bgIndex!=edIndex:
       # i_lock.acquire()
        bgIndex += 1
        index_t =bgIndex
      #  i_lock.release()
        pageSrc =getHtml(orgHref+str(index_t))
        if not pageSrc: continue#应当报错
        bsObj = BeautifulSoup(pageSrc, "html.parser")
        audioList = bsObj.find_all('audio') # 获取audio标签列表

        # 获取父元素->获取分类标签->判断是否音乐元素->放弃
        for audioTag in audioList:
            name = dloadUrl = title = text = ""
            try:   #get用于多数据集合findAll().get("xx")->list
                dloadUrl = audioTag.get('src') or audioTag.source.get('src') or " "#audioTag['src'] or audioTag.source['src'] #音乐下载地址**
                div=audioTag.find_parent("div",class_="entry-content") #父div元素
                article=div and div.find_parent("article") #article父元素
                title=article.h1.a.get_text("|", strip=True) or " " #文章标题**
                p=div.p #描述语言标签
                text=p and p.get_text("|") or " "  #描述文字**
                wordlist=[words for words in text.split("|") if words[0]=="\n" and 1<len(words)<40] #字符集合
                #t=getAttr(wordlist,-1)
                #name=wordlist and wordlist[-1]
                name=(wordlist[-1] if len(wordlist) else " ").strip()#歌曲名**
                #if not name:name="" #待修改——————
                #name=text.split()[-1]  #歌曲名
            except Exception as e:
                print("抓取错误%d--"%index_t+repr(e))
            finally:#"text: "+text+  +"\n----"+str(index_t)
                print("\nname:"+name+"\ndloadUrl:"+dloadUrl)
                print("============== " + str(index_t) + " ============== " + threading.currentThread().getName() + " \n\n")
                db.insertData("common",[{"name":name,"dLoadUrl":dloadUrl,"srcUrl":orgHref+str(index_t),"title":title,"description":text}])#存入数据库
    #driver.close()
    pass


def musicLabCrawl():
    '''扒取音乐标签数据'''
    pass

def bgCrawl(Num):
    #创建数据库
    db.creatTable("common", {"name": "varchar(40)", "dLoadUrl": "varchar(1000)", "srcUrl": "varchar(1000)",
                             "title": "varchar(60)", "description": "varchar(1000)"})

    index_lock = threading.RLock()
    global bgIndex
    bgIndex=0
    for i in range(Num):
        t = threading.Thread(name=str(i),target=commonCrawl, args=(179,seed_href,index_lock))
        t.start()
    pass


if __name__=="__main__":
    #在HTTP请求上设置好超时时间，最好设定sockect的超时，这样更底层一些。
    #在上层做一个检测机制，定时轮询线程是否正常，如果遇到不响应的直接kill掉。
    #1、超时跳出
    #2、线程状态检测
    bgCrawl(1)
    pass