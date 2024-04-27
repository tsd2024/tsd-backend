from fastapi import Request
from google.oauth2 import id_token
from google.auth.transport import requests

from src.contract.exceptions import InvalidTokenException, MissingTokenException

CLIENT_ID = "50333286952-cn2jg51pihob9a8t22scs03a3gvtkpn3.apps.googleusercontent.com"


def verify_token(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token == "":
        raise MissingTokenException("Token is missing")
    try:
        user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        return user_info
    except ValueError:
        raise InvalidTokenException("Invalid token")

