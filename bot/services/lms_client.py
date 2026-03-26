"""LMS API client for backend integration."""
import httpx
from config import LMS_API_URL, LMS_API_KEY

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
            with httpx.Client() as client:
                response = client.request(method, url, headers=self.headers, timeout=5.0, **kwargs)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception(f"Backend error: connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise Exception(f"Backend error: timeout ({self.base_url}). The service may be overloaded.")
        except httpx.HTTPStatusError as e:
            raise Exception(f"Backend error: HTTP {e.response.status_code} {e.response.reason_phrase}. The backend service may be down.")
        except httpx.HTTPError as e:
            raise Exception(f"Backend error: {str(e)}")

    def get_items(self):
        """GET /items/ — all labs and tasks."""
        return self._request("GET", "/items/")

    def get_pass_rates(self, lab: str):
        """GET /analytics/pass-rates?lab={lab}"""
        return self._request("GET", f"/analytics/pass-rates?lab={lab}")

client = LMSClient()