import requests
import os
from datetime import datetime

WEBHOOK_URL = os.environ["FEISHU_WEBHOOK"]

now = datetime.now().strftime('%d/%m/%Y %H:%M')

payload = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "🚚 LIVE UNIT TRACKING"
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"📅 **Update:** {now}"
                }
            },

            {"tag": "hr"},

            # ROUTE
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "🛣️ **RUTE**\nBGR → SOG → BGR"
                }
            },

            # DRIVER
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "👤 **DRIVER**\nRamdoni"
                }
            },

            # ETD
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "⏰ **ETD**\n20:30"
                }
            },

            {"tag": "hr"},

            # STATUS (lebih menonjol)
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "🟢 **STATUS: DALAM PERJALANAN**"
                }
            },

            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": "Monitoring by Transport Team"
                    }
                ]
            }
        ]
    }
}

r = requests.post(WEBHOOK_URL, json=payload)
print(r.status_code, r.text)
