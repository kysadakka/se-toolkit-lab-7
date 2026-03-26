"""LMS API client for backend integration."""
import sys
from pathlib import Path

# Add bot directory to path for imports
bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

import requests
from config import load_config

config = load_config()
LMS_API_URL = config.get("LMS_API_URL", "http://localhost:42002")
LMS_API_KEY = config.get("LMS_API_KEY", "")

class LMSClient:
    def __init__(self):
        self.base_url = LMS_API_URL
        self.headers = {
            "Authorization": f"Bearer {LMS_API_KEY}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, path: str, **kwargs):
        """Make HTTP request to LMS backend."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            response = requests.request(method, url, headers=self.headers, timeout=5, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise Exception(f"Connection error: cannot reach {self.base_url}. Check that backend is running.")
        except requests.exceptions.Timeout:
            raise Exception(f"Timeout: backend at {self.base_url} did not respond in time.")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP {response.status_code}: {response.reason}")
        except Exception as e:
            raise Exception(f"API error: {str(e)}")

    def get_items(self):
        """GET /items/ — all labs and tasks."""
        return self._request("GET", "/items/")

    def get_pass_rates(self, lab: str):
        """GET /analytics/pass-rates?lab={lab}"""
        return self._request("GET", f"/analytics/pass-rates?lab={lab}")

client = LMSClient()