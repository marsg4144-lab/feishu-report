import requests
import os
from datetime import datetime

WEBHOOK_URL = os.environ["FEISHU_WEBHOOK"]

payload = {
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "🚚 Report Unit Dalam Perjalanan"
      },
      "template": "blue"
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": f"**Tanggal:** {datetime.now().strftime('%d/%m/%Y')}"
        }
      },
      {
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**Rute:** BGR → SOG → BGR"}
      },
      {
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**Driver:** Ramdoni"}
      },
      {
        "tag": "div",
        "text": {"tag": "lark_md", "content": "**ETD:** 20:30"}
      },
      {"tag": "hr"},
      {
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": "Status: Dalam Perjalanan"}]
      }
    ]
  }
}

r = requests.post(WEBHOOK_URL, json=payload)
print(r.status_code, r.text)
