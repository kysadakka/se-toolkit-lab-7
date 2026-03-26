"""LMS API client for backend integration."""
import sys
from pathlib import Path

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
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            response = requests.request(method, url, headers=self.headers, timeout=5, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise Exception(f"Connection error: cannot reach {self.base_url}")
        except requests.exceptions.Timeout:
            raise Exception(f"Timeout: backend at {self.base_url}")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP {response.status_code}: {response.reason}")
        except Exception as e:
            raise Exception(f"API error: {str(e)}")

    def get_items(self):
        return self._request("GET", "/items/")

    def get_learners(self):
        return self._request("GET", "/learners/")

    def get_scores(self, lab: str):
        return self._request("GET", f"/analytics/scores?lab={lab}")

    def get_pass_rates(self, lab: str):
        return self._request("GET", f"/analytics/pass-rates?lab={lab}")

    def get_timeline(self, lab: str):
        return self._request("GET", f"/analytics/timeline?lab={lab}")

    def get_groups(self, lab: str):
        return self._request("GET", f"/analytics/groups?lab={lab}")

    def get_top_learners(self, lab: str, limit: int = 5):
        return self._request("GET", f"/analytics/top-learners?lab={lab}&limit={limit}")

    def get_completion_rate(self, lab: str):
        return self._request("GET", f"/analytics/completion-rate?lab={lab}")

    def trigger_sync(self):
        return self._request("POST", "/pipeline/sync", json={})

client = LMSClient()
