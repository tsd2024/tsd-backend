from fastapi import WebSocket
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel

from src.contract.exceptions import MissingTokenException, InvalidTokenException
from src.database.repository.user_repository import UserRepository

CLIENT_ID = "50333286952-cn2jg51pihob9a8t22scs03a3gvtkpn3.apps.googleusercontent.com"
class TokenVerifier(BaseModel):
    user_repository: UserRepository
    def verify_token(self, token):
        if token == "":
            raise MissingTokenException("Token is missing")
        try:
            user_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            self.user_repository.ensure_exists(user_info.get("email"), user_info.get("name"))
            return user_info
        except ValueError:
            raise InvalidTokenException("Invalid token")

