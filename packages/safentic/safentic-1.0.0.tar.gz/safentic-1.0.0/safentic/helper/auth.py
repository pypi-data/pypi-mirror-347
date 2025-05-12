import requests
from ..config import *

def validate_api_key(key: str) -> dict:
    try:
        response = requests.post(BASE_API_PATH + API_KEY_ENDPOINT, json={"api_key": key})
        if response.status_code != 200:
            return {"valid": False}
        data = response.json()
        return {"valid": True, **data}
    except Exception:
        return {"valid": False}
