import os
from urllib.request import urlretrieve

class SaveFile(object):
    def __init__(self,homePath):
        self.home=homePath+"/"
        pass

    def creatDirs(self,num,midPath=""):
        path_t = self.home + midPath
        if midPath!="":path_t+="/"
        if isinstance(num, int) and num>=0:
            for i in range(num):
                try:
                    os.makedirs(path_t + str(i))
                except FileExistsError as fee:
                    print(fee.strerror)
        else:
            try:
                os.makedirs(path_t+str(num))
            except FileExistsError as fee:
                print(fee.strerror)
        #os.path.exists(path_t+)

    def saveImg(self,url,path_s,img_type=""):
        '''url  path  img_type'''
        if url[:4]!="http":
            url="https:"+url
        try:
            urlretrieve(url,self.home+path_s+img_type)
        except FileNotFoundError as fnf:
            print("存储错误："+path_s+" "+fnf.strerror)
            return False
        except Exception as e:
            print("下载失败：" + path_s + " " + repr(e))
            return False
        return True

        #判断文件、目录是否已存在----------------------


if __name__ == '__main__':
    pass