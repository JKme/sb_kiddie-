# coding: utf-8
import requests
import json


EMAIL = ""
AUTH = ""
URL = "https://api.cloudflare.com/client/v4/graphql/"
ZONE = ""

Headers = {
    "X-Auth-Email": EMAIL,
    "X-Auth-Key": AUTH,
    "Content-Type": "application/json"
}

payload = f'''{{
  viewer {{
    zones(filter: {{zoneTag: "{ZONE}"}}) {{
      firewallEventsAdaptiveGroups(filter: {{datetime_geq: "2021-03-21T00:00:00Z", datetime_leq: "2021-03-23T16:40:00Z", ruleId: "", action:"block"}}, limit: 5000) {{ 
        count
        dimensions {{
          datetime
          clientIP
          clientRequestPath
          ruleId
          action
          clientRefererHost
        }}
      }}
    }}
  }}
}}'''

ret = requests.post(URL, headers=Headers, data=json.dumps({"query": payload})).content
print(json.loads(ret)["data"]["viewer"]["zones"])
