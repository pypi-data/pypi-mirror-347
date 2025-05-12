import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self, auth_key: str, base_url: str):
        logger.info("Initializing ApiClient, base_url: %s", base_url)
        self.auth_key = auth_key
        self.base_url = base_url
        self.headers = {
            "sec-ch-ua-platform": "Windows",
            "Authorization": f"Bearer {self.auth_key}",
            "Referer": "https://tcinvest.tcbs.com.vn/",
            "Accept-language": "vi",
            "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "origin": "https://tcinvest.tcbs.com.vn",
            "priority": "u=1, i",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            # The following headers are dynamic in curl, you may want to set them optionally or allow as parameters
            # "traceparent": "00-2d9bb3d061abc491f92784aeeda6141e-c096b740011d7c5f-01",
            # "tracestate": "es=s:1",
        }

    def get(self, endpoint: str, params: dict = None):
        logger.info(f"GET request to {self.base_url}/{endpoint} with params: {params}")
        response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers, params=params)
        if response.status_code == 200:
            logger.info(f"GET request successful, response: {response.json()}")
            return response.json()
        else:
            logger.error(f"GET request failed with status code: {response.status_code}, response: {response.text}") 
            response.raise_for_status()

    def post(self, endpoint: str, data: dict = None):
        logger.info(f"POST request to {self.base_url}/{endpoint} with data: {data}")
        response = requests.post(f"{self.base_url}/{endpoint}", headers=self.headers, json=data)
        if response.status_code == 200:
            logger.info(f"POST request successful, response: {response.json()}")
            return response.json()
        else:
            logger.error(f"POST request failed with status code: {response.status_code}, response: {response.text}")
            response.raise_for_status()
