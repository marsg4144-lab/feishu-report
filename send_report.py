import requests
import os
import json
from datetime import datetime
from typing import Dict, Any

class UnitTracker:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session = requests.Session()
    
    def send_update(self, route: str, driver: str, etd: str, status: str, 
                   status_color: str = "🟢") -> Dict[str, Any]:
        """Send live tracking update to Feishu"""
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # Status mapping for colors
        status_colors = {
            "DALAM PERJALANAN": "🟢",
            "MENUNGGU": "🟡", 
            "SELESAI": "🟢",
            "TERLAMBAT": "🔴",
            "DIBATALKAN": "⚫"
        }
        
        color = status_colors.get(status.upper(), status_colors["DALAM PERJALANAN"])
        
        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
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
                            "content": f"🛣️ **ROUTE**\n**{route}**"
                        }
                    },
                    
                    # DRIVER
                    {
                        "tag": "div", 
                        "text": {
                            "tag": "lark_md",
                            "content": f"👤 **DRIVER**\n**{driver}**"
                        }
                    },
                    
                    # ETD
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md", 
                            "content": f"⏰ **ETD**\n**{etd}**"
                        }
                    },
                    
                    {"tag": "hr"},
                    
                    # STATUS (most prominent)
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"{color} **STATUS: {status.upper()}**"
                        }
                    },
                    
                    # Action buttons
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "📞 Call Driver"
                                },
                                "type": "primary",
                                "value": {"action": "call_driver"}
                            },
                            {
                                "tag": "button", 
                                "text": {
                                    "tag": "plain_text",
                                    "content": "📍 Live Map"
                                },
                                "type": "default",
                                "value": {"action": "show_map"}
                            }
                        ]
                    },
                    
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": "👥 Monitoring by Transport Team"
                            }
                        ]
                    }
                ]
            }
        }
        
        try:
            response = self.session.post(
                self.webhook_url, 
                json=payload,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            result = {
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'response': response.text,
                'timestamp': datetime.now().isoformat()
            }
            
            if not result['success']:
                print(f"❌ Failed to send update: {response.status_code} - {response.text}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_result = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ Request error: {error_result}")
            return error_result

def main():
    # Get webhook URL from environment
    webhook_url = os.environ.get("FEISHU_WEBHOOK")
    if not webhook_url:
        print("❌ FEISHU_WEBHOOK environment variable not set!")
        return
    
    tracker = UnitTracker(webhook_url)
    
    # Example usage
    result = tracker.send_update(
        route="BGR → SOG → BGR",
        driver="Ramdoni", 
        etd="20:30",
        status="DALAM PERJALANAN"
    )
    
    print(f"✅ Update sent: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
