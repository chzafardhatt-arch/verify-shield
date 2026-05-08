from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from database import validate_api_key, increment_usage, log_usage, create_client, get_all_clients

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ABSTRACT_EMAIL_KEY = "3c3af0009e8d498a8b23cd4503d08ea8"
ABSTRACT_PHONE_KEY = "d9de96a644f54bd49f707d95dc3c6e13"
ABSTRACT_IP_KEY = "45d097a4b9e544ed8ed3f46432ae8e7a"
ADMIN_SECRET = "ahmad_admin_2026"

def run_email_check(email: str):
    try:
        url = f"https://emailreputation.abstractapi.com/v1/?api_key={ABSTRACT_EMAIL_KEY}&email={email}"
        response = requests.get(url, timeout=10)
        data = response.json()
        score = data.get("email_quality", {}).get("score", 0)
        risk = data.get("email_risk", {}).get("address_risk_status", "unknown")
        is_disposable = data.get("email_quality", {}).get("is_disposable", False)
        if risk == "low" and not is_disposable:
            status = "Safe"
        elif risk == "high" or is_disposable:
            status = "Flagged"
        else:
            status = "Review"
        return round(score * 100), status, risk, is_disposable
    except:
        disposable_domains = ["mailinator.com", "tempmail.com", "guerrillamail.com", "10minutemail.com"]
        domain = email.split("@")[-1] if "@" in email else ""
        is_disposable = domain in disposable_domains
        if is_disposable:
            return 85, "Flagged", "high", True
        return 20, "Safe", "low", False

def run_phone_check(phone: str):
    try:
        url = f"https://phonevalidation.abstractapi.com/v1/?api_key={ABSTRACT_PHONE_KEY}&phone={phone}"
        response = requests.get(url, timeout=10)
        data = response.json()
        valid = data.get("valid", False)
        line_type = data.get("type", "unknown")
        country = data.get("country", {}).get("name", "Unknown")
        carrier = data.get("carrier", "Unknown")
        risky_types = ["voip", "tollfree", "unknown"]
        if not valid:
            status = "Flagged"
            risk = "high"
        elif line_type.lower() in risky_types:
            status = "Review"
            risk = "medium"
        else:
            status = "Safe"
            risk = "low"
        return status, risk, valid, line_type, country, carrier
    except:
        return "Review", "unknown", False, "unknown", "Unknown", "Unknown"

def run_ip_check(ip: str):
    try:
        url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={ABSTRACT_IP_KEY}&ip_address={ip}"
        response = requests.get(url, timeout=10)
        data = response.json()
        country = data.get("country", "Unknown")
        city = data.get("city", "Unknown")
        is_vpn = data.get("security", {}).get("is_vpn", False)
        is_tor = data.get("security", {}).get("is_tor", False)
        is_proxy = data.get("security", {}).get("is_proxy", False)
        is_bot = data.get("security", {}).get("is_bot", False)
        threat_score = 0
        if is_vpn: threat_score += 30
        if is_tor: threat_score += 50
        if is_proxy: threat_score += 30
        if is_bot: threat_score += 40
        threat_score = min(100, threat_score)
        if threat_score >= 50:
            status = "Flagged"
        elif threat_score >= 20:
            status = "Review"
        else:
            status = "Safe"
        return status, threat_score, country, city, is_vpn, is_tor, is_proxy, is_bot
    except:
        return "Review", 0, "Unknown", "Unknown", False, False, False, False

@app.get("/")
def root():
    return {"message": "VerifyShield API by Ahmad", "version": "3.0", "status": "online"}

@app.get("/check")
def check_email(email: str, api_key: str = "demo"):
    if api_key != "demo":
        client = validate_api_key(api_key)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid or inactive API key")
        if client[5] >= client[6]:
            raise HTTPException(status_code=429, detail="Monthly request limit reached")
        increment_usage(api_key)

    risk_score, status, risk, is_disposable = run_email_check(email)
    if api_key != "demo":
        log_usage(api_key, email, status, risk_score)

    return {
        "email": email,
        "score": risk_score,
        "status": status,
        "risk": risk,
        "is_disposable": is_disposable,
        "requests_remaining": "demo" if api_key == "demo" else "unlimited"
    }

@app.get("/check-phone")
def check_phone(phone: str, api_key: str = "demo"):
    if api_key != "demo":
        client = validate_api_key(api_key)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid or inactive API key")
        if client[5] >= client[6]:
            raise HTTPException(status_code=429, detail="Monthly request limit reached")
        increment_usage(api_key)

    status, risk, valid, line_type, country, carrier = run_phone_check(phone)
    return {
        "phone": phone,
        "status": status,
        "risk": risk,
        "valid": valid,
        "line_type": line_type,
        "country": country,
        "carrier": carrier
    }

@app.get("/check-ip")
def check_ip(ip: str, api_key: str = "demo"):
    if api_key != "demo":
        client = validate_api_key(api_key)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid or inactive API key")
        if client[5] >= client[6]:
            raise HTTPException(status_code=429, detail="Monthly request limit reached")
        increment_usage(api_key)

    status, threat_score, country, city, is_vpn, is_tor, is_proxy, is_bot = run_ip_check(ip)
    return {
        "ip": ip,
        "status": status,
        "threat_score": threat_score,
        "country": country,
        "city": city,
        "is_vpn": is_vpn,
        "is_tor": is_tor,
        "is_proxy": is_proxy,
        "is_bot": is_bot
    }

@app.get("/admin/create-client")
def create_client_endpoint(name: str, email: str, plan: str = "starter", admin_key: str = ""):
    if admin_key != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    api_key = create_client(name, email, plan)
    return {"message": "Client created!", "api_key": api_key, "name": name, "plan": plan}

@app.get("/admin/clients")
def list_clients(admin_key: str):
    if admin_key != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    clients = get_all_clients()
    return {"clients": [
        {
            "id": c[0], "name": c[1], "email": c[2],
            "api_key": c[3], "plan": c[4],
            "requests_used": c[5], "requests_limit": c[6],
            "created_at": c[7], "is_active": c[8]
        } for c in clients
    ]}