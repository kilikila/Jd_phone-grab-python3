from os import _exit

from bs4 import BeautifulSoup

from BrowerDriver import  PhDriver
from DAO.DB_mysql import DB_Mysql
from DAO.FileSave import SaveFile

config = {
    'host':'localhost',
    'port': 3306,
    'user': 't1',
    'password': '123456',
    'db': 'test1',
    'charset': 'utf8'
}

main_href="https://search.jd.com/"
seed_href="https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=8cekgbui.a0bxkd"

phantomjs_path=r"D:\mySoftware\phantomjs-2.1.1-windows\bin\phantomjs.exe"

img_dirs=r"E:\Data\JD_PhoneImg"

phone_hrefs=[] #各个品牌链接集合
shop_hrefs=[]  #各个店铺链接集合

db=DB_Mysql(config)  #数据库
if not db:
    print("db对象声明失败，程序退出")
    _exit(0)

driver=PhDriver(phantomjs_path,seed_href,"J_main")  #浏览器驱动器-开始到s扒取主页面

imgSave= SaveFile(img_dirs)

def getBrand():
    db.creatTable("Brand",{"BrandName":"varchar(40)","imgUrl":"varchar(60)"})
    driver.triggerElements("J_selectorLine/sl-e-more","click",lambda dri:BeautifulSoup(dri.page_source, "html.parser").find("li",id="brand-32315"))

    bsObj=BeautifulSoup(driver.getPgSrc(), "html.parser")
    driver.close()

    #获取品牌头
    # print(bsObj.find("div",class_="sl-v-logos").contents[1])
    phone_lis = bsObj.find("div",class_="sl-v-logos").ul.find_all('li')

    brand_arrs=[]
    index=0
    imgSave.creatDirs(-1)

    for child_li in phone_lis:
        try:
            brand={}
            phone_a=child_li.a
            brand["BrandName"]=phone_a['title']   #品牌名s
            print(brand["BrandName"])

            phone_hrefs.append(phone_a['href'])  #品牌链接
            imgurl=child_li.img   #品牌图片

            brand["imgUrl"]=""

            if(imgurl):
                brand["imgUrl"]="-1/"+str(index)+".jpg"   #.jpg-"\\\////"--------------------
                imgSave.saveImg(imgurl.attrs['src'],brand["imgUrl"])


            index += 1
        except AttributeError as a_error:
            print("child_li error")
        else:
            brand_arrs.append(brand)
    db.insertData("Brand",brand_arrs)

    getShops(phone_hrefs[0],0)#开始获取每家店铺

def idExist(dri,id_str):
    try:
        dri.find_element_by_id(id_str)
    except:
        print("%s 元素已消失"%id_str)
        return True
    else:
        return False

def getShops(url,index):
    url_phone=main_href + url
    driver_th = PhDriver(phantomjs_path, url_phone, "J_main")  # 浏览器驱动器--线程用--移动到某品牌主页面

    #bsObj=BeautifulSoup(driver_th.getPgSrc(), "html.parser")
    bsObj=None
    shop_hrefs=[]  #店铺url列表

    while True:
        page_t = driver_th.triggerElements("", "scroll_RB",lambda dri_p: idExist(dri_p,"J_scroll_loading"))
        if not page_t:
            print("--%s--  进入下一页失败" % str(index))  # 进入下一页失败退出当前线程循环
            break
        else:
            bsObj = BeautifulSoup(driver_th.getPgSrc(), "html.parser")

        shop_lis=bsObj.find("div",id="J_goodsList").find_all('li',{"data-sku":True})
        for li_t in shop_lis:
            try:
                shop_hrefs.append(li_t.find('div',{"class":{"p-name"}}).a['href'])
            except AttributeError as at:
                print("get shop error")
                continue

        print("---t---"+str(len(shop_hrefs)))
        print(bsObj.find("a",class_="pn-next")["class"])
        if len(bsObj.find("a",class_="pn-next")["class"])>=2 :
            break
        else:
            # 待修改，暂停修改为判断是否主线程然后进行线程暂停
            page_i=bsObj.find("div",id="J_bottomPage").find("a",class_="curr").get_text()
            print("-----text-----"+page_i)
            result_t=driver_th.triggerElements("pn-next", "click",lambda dri : dri.find_element_by_id("J_bottomPage")\
                         .find_element_by_class_name("curr").text!=page_i)#--------------------
            if not result_t:
                print("--%s--  进入下一页失败"%str(index)) #进入下一页失败退出当前线程循环
                break
            else:
                bsObj = BeautifulSoup(driver_th.getPgSrc(), "html.parser")

    driver_th.close()

    print(shop_hrefs)
    # 获取当前shop数-遍历获取url
    #判断并并触发下一页--获取新bsObj
    # 获取当前shop数-遍历获取url
    getGoodsInfo(shop_hrefs[0],index,0)

def getGoodsInfo(url,index_brand,index_shop):
    '''进行页面信息的详细扒取，参数，款式，图片，评价，评论数'''
    '''需要进行商品参数的规范化存储'''
    url_shop = "http:" + url

    driver_th = PhDriver(phantomjs_path, url_shop, "spec-img")  # 浏览器驱动器--线程用--移动到某品牌主页面
    page_t = driver_th.triggerElements("", "scroll_RB", 3)
    bsObj = BeautifulSoup(page_t, "html.parser")

    #判断是否为智能机-------

    #获取基本介绍信息
    intro_div = bsObj.find("div", class_="product-intro")  #"product-intro"
    #总名称
    full_name=intro_div.find("div",class_="itemInfo-wrap").find("div",class_="sku-name").get_text()
    print(full_name)
    #价格
    base_price=intro_div.find("div",class_="summary").find("span",class_="price").get_text()
    print(base_price)
    #获取款式-重定位链接获取图片-------------
    #
    #
    #

    #移动到介绍栏--------------

    #移动到规格栏-------------

    #移动到评价栏-----------------

    pass



if __name__=="__main__":
    getBrand()