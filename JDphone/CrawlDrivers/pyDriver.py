import urllib.request
import socket
import time
import re

#登录用的帐户信息
user_agent = "Mozilla / 5.0(WindowsNT10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 55.0.2883.87Safari / 537.36"

def getHtml(url,delay_time=3):
    '''获取指定页面'''
    #time.sleep(delay_time)
    html=""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-agent', user_agent)
        page = urllib.request.urlopen(req)
        html = page.read().decode('utf-8')
        page.close()
    except Exception as e:
        print("无法请求到页面:%s --" % url + repr(e))

    finally:
        #time.sleep(delay_time)
        return html

if __name__=="__main__":
    pass