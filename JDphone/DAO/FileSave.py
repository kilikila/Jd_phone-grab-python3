import os
import urllib.request
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
            #self.downLoader(url,self.home+path_s+img_type)
        except FileNotFoundError as fnf:
            print("存储错误："+path_s+" "+fnf.strerror)
            return False
        except Exception as e:
            print("下载失败：" + path_s + " " + repr(e))
            return False
        return True

        #判断文件、目录是否已存在----------------------
    #"common","name","dLoadUrl"
    def downLoader(self,url,savepath):
        user_agent = "Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 55.0.2883.87Safari / 537.36"
        try:
            req = urllib.request.Request(url)
            req.add_header('User-agent', user_agent)
            f = urllib.request.urlopen(req,timeout=3)
            data = f.read()
            with open(savepath, 'wb') as code:
                code.write(data)
        except:
            print(url+"  --失败--")


if __name__ == '__main__':
    pass