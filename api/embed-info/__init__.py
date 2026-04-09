import azure.functions as func
import sys
import os
import json
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def _json_resp(body: dict, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body), status_code=status_code, mimetype="application/json"
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("embed-info function triggered")

    # Import shared module with fallback
    try:
        from shared import CONFIG, verify_token
    except Exception as imp_err:
        logging.error(f"Import error: {imp_err}")
        return _json_resp({"error": f"Server config error: {imp_err}"}, 500)

    token = req.headers.get("X-Auth-Token", "")
    if not token:
        return _json_resp({"error": "Unauthorized - no token"}, 401)

    if not verify_token(token):
        return _json_resp({"error": "Unauthorized - invalid token"}, 401)

    # Import heavy dependencies inside handler
    try:
        import msal
        import requests
    except ImportError as dep_err:
        logging.error(f"Missing dependency: {dep_err}")
        return _json_resp({"error": f"Missing dependency: {dep_err}"}, 500)

    try:
        authority = f"https://login.microsoftonline.com/{CONFIG['tenant_id']}"
        scope = ['https://analysis.windows.net/powerbi/api/.default']

        app_msal = msal.ConfidentialClientApplication(
            CONFIG['client_id'],
            authority=authority,
            client_credential=CONFIG['client_secret']
        )

        result = app_msal.acquire_token_for_client(scopes=scope)

        if 'access_token' not in result:
            error_msg = result.get('error_description', 'Unknown error')
            logging.error(f"MSAL error: {error_msg}")
            return _json_resp({"error": f"Failed to get access token: {error_msg}"}, 500)

        access_token = result['access_token']

        embed_url = (
            f"https://api.powerbi.com/v1.0/myorg/groups/{CONFIG['workspace_id']}"
            f"/reports/{CONFIG['report_id']}/GenerateToken"
        )
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        body = {'accessLevel': 'View', 'allowSaveAs': False}

        response = requests.post(embed_url, json=body, headers=headers, timeout=30)

        if response.status_code != 200:
            logging.error(f"PBI API error {response.status_code}: {response.text}")
            return _json_resp({"error": f"Failed to generate embed token: {response.text}"}, response.status_code)

        embed_data = response.json()

        return _json_resp({
            "embedToken": embed_data["token"],
            "embedUrl": embed_data.get(
                "embedUrl",
                f"https://app.powerbi.com/reportEmbed?reportId={CONFIG['report_id']}&groupId={CONFIG['workspace_id']}"
            ),
            "reportId": CONFIG["report_id"],
            "expiresAt": embed_data.get("expiration")
        })

    except Exception as e:
        logging.error(f"embed-info exception: {e}")
        return _json_resp({"error": str(e)}, 500)
