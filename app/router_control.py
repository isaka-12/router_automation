import requests
from app.config import ROUTER_URL

def add_mac_to_whitelist(mac):
    try:
        # send fake request for now (you will customize later)
        response = requests.post(f"{ROUTER_URL}/whitelist", data={"mac": mac})
        return response.status_code == 200
    except Exception as e:
        print(f"Router communication failed: {e}")
        return False
