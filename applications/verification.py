import requests
from requests import RequestException


def _safe_fetch_json(url: str, timeout: int = 5):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except (RequestException, ValueError):
        return {"error": "service_unavailable"}

def auto_verify(application, aadhaar):
    digi = _safe_fetch_json(f"http://127.0.0.1:8000/mock/digilocker/fetch/{aadhaar}/")
    appli = _safe_fetch_json(f"http://127.0.0.1:8000/mock/applisarkar/verify/{aadhaar}/")

    if "error" in digi or "error" in appli:
        return False, "Government record missing or verification service unavailable"

    if appli.get("fraud"):
        return False, "Fraud flagged by AppliSarkar"

    return True, digi
