import azure.functions as func
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared import USERS, create_token, json_response


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return json_response({"error": "Invalid JSON"}, 400)

    username = body.get("username", "")
    password = body.get("password", "")

    if USERS.get(username) == password:
        token = create_token(username)
        return json_response({"token": token})

    return json_response({"error": "Invalid username or password."}, 401)
