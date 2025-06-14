import requests
import json
import os
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

from fastapi import APIRouter, HTTPException
from gradio_client import Client

#router = APIRouter()
router = APIRouter(prefix="/gradio", tags=["gradio"])
@router.get("/route/gradio")

def get_senario(id,res):
    table = "LOG"

    client = Client("kenken999/fastapi_django_main_live")
    result = client.predict(
            message="Hello!!",
            request=0.95,
            param_3=512,
            api_name="/chat"
    )
    return result

# main input
#res = get_senario("LOG")
#print(res)
#return res

#print(response.json())
if __name__ == "__main__":
    get_senario("test","test")