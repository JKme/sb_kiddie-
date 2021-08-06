# 爬取火绒控制中心已安装软件，并且保存到csv
import requests
import json
import openpyxl
import csv

URL = "<>"
s = requests.Session()
payload = {"username": "admin", "password": "<sha1 of password>"}
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "<>"
}


def spider():
    s.post(URL, data=json.dumps(payload), headers=headers)
    # print(r.status_code, r.text, r.request.body)

    d1 = {"groupby": "software", "filter": {"software": ""}, "view": {"begin": 0, "count": 4518}, "order": []}
    data = s.post("<sd>/mgr/swinfo/_search", data=json.dumps(d1), headers=headers).text
    with open("huorong.csv", "w") as f:
        c = csv.writer(f)
        c.writerow(["软件名称", "发布者", "版本号", "已安装", "安装率"])
        for l in json.loads(data)["data"]["list"]:
            c.writerow([l["name"], l["publisher"], l["version"], l["installed"], str(l["rate"])+"%"])


if __name__ == "__main__":
    spider()

    
    
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time


def spider():
    # option = webdriver.ChromeOptions()
    # option.add_experimental_option("--headless")
    # option.add_experimental_option("detach", True)

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    web = Chrome(options=chrome_options)

    web.get('https://ngabbs.com/read.php?tid=27586426&authorid=61078637&page=3')

    time.sleep(3)  # 睡眠2秒
    html = web.find_element_by_xpath("//*").get_attribute("outerHTML")
    print(html)
    getContents(html)
    # web.find_element_by_xpath('//*[@id="pagebtop"]/table/tbody/tr/td[4]/a').click()


def getContents(html):
    pattern = re.compile(r"<span id=\"postcontent(\d+)\" class=\"postcontent ubbcode\">(.*?)<img.*?src=\"(.*?)\"")
    match = re.findall(pattern, html)
    if match:
        print(match)


if __name__ == "__main__":
    spider()

    
    
