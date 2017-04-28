import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
##################返回None的部分需要修改成抛出异常##################
class PhDriver(object):
    def __init__(self,drPath,url,id_str):
        self.driver=webdriver.PhantomJS(executable_path=drPath)
        self.activeTag=False #需要加载页面使得Ph被激活
        if url and id_str:
            self.getPage(url,id_str)


    def getPgSrc(self):
        '''获取当前源页面'''
        if not self.activeTag:return None #r若页面未激活则返回空值
        return self.driver.page_source

    def getPage(self,url,id_str):
        '''获取页面，根据id判断页面是否加载完成'''
        self.driver.get(url)
        try:
            element = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.ID, id_str)))
        except Exception as e:
            # print(driver.find_element_by_id("content").text)
            print("获取页面失败--" + repr(e))
            self.driver.close()
            return None
        else:
            self.activeTag=True
            return self.driver.page_source
            #print("获取网页")

    def triggerElements(self, loc_str, tri_type, method,time_out=10):
        '''根据xxx/xxx/xxx形式的class字符串找寻元素并触发元素返回源页面，redirect_tag为函数或者秒数'''
        '''根据 css 字符串找寻元素并触发元素返回源页面，redirect_tag为函数或者秒数'''
        if not self.activeTag:return None

        ele_ = None

        if loc_str!="":
            ele_ = self.driver
            try:
                ele_ = ele_.find_element_by_css_selector(loc_str)
            except Exception as e:
                print("元素触发错误,寻找触发元素失败，请检查定位css%s--" % loc_str + repr(e))
                return False

        '''
              if loc_str!="":
                  class_loc = loc_str.split("/")
                  ele_=self.driver
                  try:
                      for ele_str in class_loc:
                          ele_=ele_.find_element_by_class_name(ele_str)
                  except:
                      raise "元素触发错误,寻找触发元素失败"
                      return False
      '''


        if tri_type=="click":
            ele_.click()
        elif tri_type == "hover":
            ele_.hover()
        elif tri_type == "scroll_RB":
            js_code="window.scrollTo(%d,%d);"%(10000,10000)#移动到最右下角
            self.driver.execute_script(js_code)
        else:
            raise "请选择触发类型"
            #窗体元素移动

        return self.__waitForRedirect(method,time_out)

    def __waitForRedirect(self,method,time_out=10):
        if not method:
            raise ValueError("参数设置错误或缺少判定函数以及参数")

        if not isinstance(method,int):  # 判断是否需要重定向等待,不需要时则自定义函数判断点击悬停效果是否奏效
            return WebDriverWait(self.driver, time_out).until(method)
        else:
            time.sleep(method)
            return self.driver.page_source

    def getElementByCss(self,loc_str):
        # #id.class #
        ele_=None
        try:
            ele_=self.driver.find_element_by_css_selector(loc_str)
        except Exception as e:
            print("%s 所定位的元素寻找失败，请检查定位css字符串或者其他什么的，哈哈--" % loc_str + repr(e))
            return False
        else:
            return ele_

    def close(self):
        self.activeTag = False
        self.driver.close()


if __name__=='__main__':
    '''测试'''
    pass

'''
    driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    driver.get(seed_href)

'''