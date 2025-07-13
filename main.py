import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header, HTTPException
from app.handlers import ping, issues, pull_requests
import hmac
import hashlib
from datetime import datetime

load_dotenv()

app = FastAPI()
GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

def verify_signature(body: bytes, signature: str) -> bool:
    if not GITHUB_SECRET:
        return True
    mac = hmac.new(GITHUB_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@app.post("/webhook")
async def webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None)
):
    body = await request.body()

    if not verify_signature(body, x_hub_signature_256 or ""):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    log_event(x_github_event, payload)

    if x_github_event == "ping":
        return ping.handle(payload)
    elif x_github_event == "issues":
        return await issues.handle(payload)
    elif x_github_event == "pull_request":
        return await pull_requests.handle(payload)

    return {"msg": "Unhandled event"}

def log_event(event_type: str, payload: dict):
    with open("webhook.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {event_type} | {payload}\n")
