
from os import _exit

from JDphone.DAO.DB_mysql import DB_Mysql


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
