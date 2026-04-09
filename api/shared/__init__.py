import os
import json
import hashlib
import hmac
import time
import azure.functions as func

SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-before-deploying').encode()
USERS = {
    os.environ.get('APP_USERNAME', 'admin'): os.environ.get('APP_PASSWORD', 'admin')
}
CONFIG = {
    'client_id':     os.environ.get('PBI_CLIENT_ID',     'bf4e6c9c-2fe5-4eb2-9e05-2785f8c2c42a'),
    'client_secret': os.environ.get('PBI_CLIENT_SECRET', ''),
    'tenant_id':     os.environ.get('PBI_TENANT_ID',     'c94e2732-29d6-41d6-89d9-08c9798a6601'),
    'workspace_id':  os.environ.get('PBI_WORKSPACE_ID',  '7e8075a9-3b1f-430a-827e-b7f65d591c69'),
    'report_id':     os.environ.get('PBI_REPORT_ID',     '6d7bf2e6-e8b1-4d92-814d-1120d38053fb'),
}

TOKEN_EXPIRY_SECONDS = 3600


def create_token(username: str) -> str:
    expiry = str(int(time.time()) + TOKEN_EXPIRY_SECONDS)
    payload = f"{username}|{expiry}"
    sig = hmac.new(SECRET_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}|{sig}"


def verify_token(token: str) -> bool:
    parts = token.split('|')
    if len(parts) != 3:
        return False
    username, expiry, sig = parts
    expected = hmac.new(SECRET_KEY, f"{username}|{expiry}".encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return False
    try:
        if int(expiry) < int(time.time()):
            return False
    except ValueError:
        return False
    return True


def json_response(body: dict, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body),
        status_code=status_code,
        mimetype="application/json"
    )
