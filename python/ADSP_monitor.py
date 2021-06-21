# coding: utf-8
import requests
import sqlite3
from lxml import etree
import re
import json
conn = sqlite3.connect('release_history.db')
cursor = conn.cursor()

URL = "https://www.manageengine.com/products/self-service-password/release-notes.html"


def init_db():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS release(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            release_note VARCHAR (255),
            build VARCHAR (255),
            issue_fix VARCHAR (65535),
            createdate DATETIME DEFAULT (DATETIME('now','localtime'))
            )
        """
    )


def ddrobots(release_notes, issues):
    """
    """
    token = ""
    ddrobot = f"https://oapi.dingtalk.com/robot/send?access_token={token}"
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    json_text = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"Demo ",
            "text": f"#### ADSP升级提醒:\n升级版本: {release_notes}\n\n 升级内容：\n{issues}\n [链接]({URL})"
        },
        "at": {
            "atMobiles": [],
            "isAtAll": "false"
        }
    }

    requests.post(ddrobot, data=json.dumps(json_text), headers=headers)


def getHtml():
    r = requests.get(URL).text
    h = etree.HTML(r)
    release_notes = h.xpath('//*[@id="scroll"]/div[2]/h2')[0].text
    fix_issues = h.xpath('//*[@id="scroll"]/div[2]/ul[2]/li')
    v = re.findall(r"build (\d+)", release_notes)[0]

    issues = ""
    for i in fix_issues:
        issues += "* " + i.text + "\n"

    old_version = ""
    rows = cursor.execute("select * from release order by createdate desc limit 1")
    # print(rows[0][2])
    for row in rows:
        old_version = row[2]

    if v != old_version:
        ddrobots(release_notes, issues)
        cursor.execute("INSERT INTO release(release_note, build, issue_fix) VALUES (?,?,?)", (release_notes,v, issues))
        conn.commit()


if __name__ == "__main__":
    init_db()
    getHtml()
