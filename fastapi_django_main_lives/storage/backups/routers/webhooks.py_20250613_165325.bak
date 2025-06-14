import os
import subprocess
#import logging
from fastapi import FastAPI, Request, HTTPException
import requests
import json
from datetime import datetime
import importlib
import os
import pkgutil
from mysite.libs.utilities import validate_signature, no_process_file
#from mysite.database.database import ride,create_ride
from controllers.gra_04_database.rides import test_set_lide
from typing import List
from fastapi import APIRouter, Depends
from mysite.logger import logger

router = APIRouter(prefix="/process", tags=["messages"])

@router.post("/webhook")
def get_choices(
    messages
):
    logger.info("[Start] ====== LINE webhook ======")
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        user_id_with_timestamp = messages[:10]
        #user_id_with_timestamp = messages#f"{now}_{title}_{user_id}"
        no_process_file(messages, user_id_with_timestamp)
        #db登録
        test_set_lide(messages, user_id_with_timestamp)
    except Exception as e:
        logger.error("Error: %s", str(e))
