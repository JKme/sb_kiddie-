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

    
#/var/tmp/stock.txt 40|3
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import requests
import json
import time


def spider():
    old_num, page = read_log()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    web = Chrome(options=chrome_options)

    web.get(f'https://ngabbs.com/read.php?tid=27586426&authorid=61078637&page={page}')

    time.sleep(3)  # 睡眠2秒
    html = web.find_element_by_xpath("//*").get_attribute("outerHTML")

    pattern = re.compile(r"<span id=\"postcontent(\d+)\" class=\"postcontent ubbcode\">(.*?)<img.*?src=\"(.*?)\"",re.DOTALL)
    match = re.findall(pattern, html)
    lastContent = match[-1:][0]
    msg_num = lastContent[0]
    msg_txt = lastContent[1]
    record_log(msg_num, page)
    print(msg_txt, msg_num)
    # robot("Success " + msg_txt)
    if msg_num > old_num:
        robot("Success " + msg_txt)

    if len(match) == 20:
        record_log(msg_num, int(page)+1)


def record_log(msg_num, page):
    with open("/var/tmp/stock.txt", "w+") as f:
        f.write(f"{msg_num}|{page}")


def read_log():
    with open("/var/tmp/stock.txt", "r") as f:
        data = f.readline().strip("\n").split("|")
        return data[0], data[1]


def robot(msg):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    msg = msg.replace("<br>", "\n")
    url = 'https://hooks.slack.com/services/<token>'
    data = {"channel": "#general", "username": "GAN", "text": msg, "type": "mrkdwn"}
    requests.post(url, data={"payload": json.dumps(data)}, headers=headers)


if __name__ == "__main__":
    spider()
    
    
