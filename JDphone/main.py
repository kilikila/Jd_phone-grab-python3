#获取京东页面上的手机
from urllib.request import urlopen,urlretrieve
from os import _exit
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import  webdriver

main_href="https://search.jd.com/"
seed_href="https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=l25ui5ui.a0bxkd"

head_href="https:"
phantomjs_path=r"D:\mySoftware\phantomjs-2.1.1-windows\bin\phantomjs.exe"

img_dirs=r"E:\Data\imgMain"

phone_hrefs=[] #各个品牌链接集合
shop_hrefs=[]  #各个店铺链接集合

driver=None

def main():
    '''主函数'''
    #
    print(driver.find_element_by_class_name("J_selectorLine").find_element_by_class_name("sl-e-more").click())
    time.sleep(3)
   # print(driver.page_source)

  #  html = urlopen(driver.page_source)
    bsObj = BeautifulSoup(driver.page_source, "html.parser")

    #获取品牌头
   # print(bsObj.find("div",class_="sl-v-logos").contents[1])
    phone_lis = bsObj.find("div",class_="sl-v-logos").ul.find_all('li')
    print(len(phone_lis))
    for child_li in phone_lis:
        try:
            #-品牌挖掘不全------------------------------------
            #print(child_li)
            #print(child_li.a['title'])
            phone_a=child_li.a

            phone_title=phone_a['title']   #品牌名------------------------------------
            print(phone_title)
            phone_hrefs.append(phone_a['href'])  #品牌链接
            imgurl=child_li.img   #品牌图片

            if(imgurl):
                urlretrieve(head_href+imgurl.attrs['src'],img_dirs+'\\%s.jpg' % phone_title) #--------------------

        except AttributeError as a_error:
            print("child_li error")
   # print(phone_hrefs)
    scrap_first() #开启下一步操作


def scrap_first():
    '''抓取第一层'''
    for phone_ in phone_hrefs:
        #链接判断验证----------------------------------------------------
        print(main_href+phone_)
        get_shop_single(main_href+phone_)


def get_shop_single(single_url):
    '''获取单个页面的所有店铺链接'''
    html = urlopen(single_url)
    bsObj = BeautifulSoup(html, "html.parser")
    shop_lis = bsObj.find(id='J_goodsList').ul.find_all('li',{"data-sku":True})
    #for 判断下一页
    for child_li in shop_lis:
        #缺少活动的图片------------------------------------
        try:
            #print(child_li)
            shop_hrefs.append(child_li.find('div',{"class":{"p-name"}}).a['href'])
            #print("----  "+child_li.find('div',{"class":{"p-name"}}).a['href'])
        except AttributeError as at:
            print("get shop error")
            continue

    while len(shop_hrefs):
        shop_=shop_hrefs.pop()
        scrap_second(shop_ if shop_[0]!="/" else (head_href+shop_))

def scrap_second(shopt_url):
    '''抓取第二层'''
    html = urlopen(shopt_url)
    bsObj = BeautifulSoup(html, "html.parser")
    print("开始抓取具体数据")
    #具体数据挖掘--店名-各个样式-参数--等等----------------------------------------


if __name__== '__main__':

    driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    driver.get(seed_href)
    try:
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "J_main")))
    except:
        # print(driver.find_element_by_id("content").text)
        driver.close()
        _exit()
    else:
        print("获取网页")

    main()
    pass