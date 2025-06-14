import os
import sys
import subprocess
import logging
from fastapi import FastAPI, Request, HTTPException
import requests
import json
from datetime import datetime
import importlib
import pkgutil
from mysite.libs.utilities import validate_signature, no_process_file
#from mysite.database.database import ride,create_ride
from controllers.gra_04_database.rides import test_set_lide
from mysite.interpreter.prompt import prompt_genalate,test_prompt
from mysite.interpreter.google_chat import send_google_chat_card,send_google_chat_card_thread
#from mysite.interpreter.interpreter import chat_with_interpreter
#from routers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter_no_stream
from mysite.appsheet.appsheet import get_senario
import asyncio
logger = logging.getLogger(__name__)


"""
router 
"""
def include_routers(app):
    package_dir = "routers"
    if not os.path.exists(package_dir):
        logger.error(f"Package directory {package_dir} does not exist.")
        return

    for module_info in pkgutil.iter_modules([package_dir]):
        try:
            if module_info.ispkg:
                sub_package_dir = os.path.join(package_dir, module_info.name)
                for sub_module_info in pkgutil.iter_modules([sub_package_dir]):
                    module_name = (
                        f"routers.{module_info.name}.{sub_module_info.name}"
                        if sub_module_info.ispkg
                        else f"routers.{module_info.name}.{sub_module_info.name}"
                    )
                    module = importlib.import_module(module_name)
                    if hasattr(module, "router"):
                        app.include_router(module.router)
            else:
                module_name = f"routers.{module_info.name}"
                module = importlib.import_module(module_name)
                if hasattr(module, "router"):
                    app.include_router(module.router)
        except ModuleNotFoundError as e:
            logger.error(f"Module not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
from datetime import datetime


def get_user_profile(user_id, access_token):
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        profile = response.json()
        user_name = profile.get('displayName')
        user_thumbnail = profile.get('pictureUrl')
        return user_name, user_thumbnail
    else:
        print(f"Failed to get user profile: {response.status_code}, {response.text}")
        return None, None


#from routers.webhooks import router
def setup_webhook_routes(app: FastAPI):
    from polls.routers import register_routers

    register_routers(app) 
    from routers.webhook import router
    app.include_router(router)