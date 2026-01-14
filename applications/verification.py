import requests

def auto_verify(application, aadhaar):
    digi = requests.get(f"http://127.0.0.1:8000/mock/digilocker/fetch/{aadhaar}/").json()
    appli = requests.get(f"http://127.0.0.1:8000/mock/applisarkar/verify/{aadhaar}/").json()

    if "error" in digi or "error" in appli:
        return False, "Government record missing"

    if appli["fraud"]:
        return False, "Fraud flagged by AppliSarkar"

    if appli["domicile"] != "Jammu & Kashmir":
        return False, "Invalid domicile"

    return True, digi
