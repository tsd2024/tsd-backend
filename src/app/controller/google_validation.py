from fastapi import HTTPException, Depends, Request, APIRouter

from google.oauth2 import id_token
from google.auth.transport import requests

app = APIRouter()


CLIENT_ID = "50333286952-cn2jg51pihob9a8t22scs03a3gvtkpn3.apps.googleusercontent.com" 


async def verify_token(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    print("Received token:", token)
    if token == "":
        raise HTTPException(status_code=401, detail="Token is missing")
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        print(idinfo)
        return idinfo
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/secure-route")
async def secure_route(user_info: dict = Depends(verify_token)):
    return {"message": "This is a secure route", "user": user_info}