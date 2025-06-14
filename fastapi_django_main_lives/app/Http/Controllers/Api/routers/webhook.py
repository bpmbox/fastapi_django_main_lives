
import os
import sys
import subprocess
import logging
from fastapi import FastAPI, Request, HTTPException,APIRouter
import requests
import json
from datetime import datetime
import importlib
import pkgutil
from mysite.libs.utilities import validate_signature, no_process_file
#from mysite.database.database import ride,create_ride
from routers.gra_04_database.rides import test_set_lide
from mysite.interpreter.prompt import prompt_genalate,test_prompt
from mysite.interpreter.google_chat import send_google_chat_card,send_google_chat_card_thread,send_google_chat_wav
#from mysite.interpreter.interpreter import chat_with_interpreter
from routers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter_no_stream
from mysite.appsheet.appsheet import get_senario
import asyncio
from prompts.promps import prompt_for_create_system,prompt,get_prompt
from command.line_get_user_profile import get_user_profile
from command.n8n import post_data,post_data_line
import time
import traceback
from pathlib import Path
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

logger = logging.getLogger(__name__)
##
#router = APIRouter()
router = APIRouter()
#@router.get("/route/webhooks")

@router.post("/webhook")
async def webhook(request: Request):
    import os
    DEBUG=0
    #return
    #logger.info("[Start] ====== LINE webhook ======")
    body = await request.body()
    received_headers = dict(request.headers)
    body_str = body.decode("utf-8")
    logger.info("Received Body: %s", body_str)
    body_json = json.loads(body_str)
    events = body_json.get("events", [])

    webhook_url = os.getenv("chat_url")
    token = os.getenv("token")
    ChannelAccessToken = os.getenv('ChannelAccessToken')
    n8nurl = os.getenv("n8nhook")

    print(webhook_url)
    print(ChannelAccessToken)
    #exit

    thread_name=""
    ###return
    #url = github(token,foldername)
    try:

        for event in events:
            if event["type"] == "message" and event["message"]["type"] == "text":
                user_id = event["source"]["userId"]
                text = event["message"]["text"]
                event_type = event.get('type')
                webhook_event_id = event.get('webhookEventId')
                delivery_context = event.get('deliveryContext', {})
                timestamp = event.get('timestamp')
                mode = event.get('mode')

                # メッセージ情報を取得
                message = event.get('message', {})
                message_type = message.get('type')
                message_id = message.get('id')
                message_text = message.get('text')
                quote_token = message.get('quoteToken')
                chat_id = event.get('source', {}).get('chatId')
                # ソース情報を取得
                source = event.get('source', {})
                source_type = source.get('type')
                user_id = source.get('userId')
                
                # 応答トークンを取得
                reply_token = event.get('replyToken')

                user_name,thmbnail = get_user_profile(user_id,ChannelAccessToken)

                logger.info("Received Headers: %s", user_name)
                logger.info("Received Headers: %s", thmbnail)

                #logger.info("------------------------------------------")
                first_line = text.split('\n')[0]
                #logger.info(f"User ID: {user_id}, Text: {text}")
                #########################################################################
                # 査定用のプロンプト
                #promps,prompt_res = prompt_genalate("返信は日本語で答えて下さい "+text,get_prompt(text))

                #test_set_lide(text,"a1")
                #no_process_file(text, "ai")
                #\r\m
                #########################################################################
                #user_name,thmbnail#
                title = f""" {user_name}様から下記の質問があります"""
                
                subtitle = f"""<b>ユーザーID</b> {user_id}\r\n <b>質問内容</b>\r\n{message_id} {text}"""

                ##
                subtitle = f"""
                <b>ユーザーID:</b>
                    {user_id}
                <b>質問内容:</b> 
                    {text}
                
                """    
                #<b>Webhook Event ID:</b> {webhook_event_id}<br>
                #<b>Delivery Context:</b> {json.dumps(delivery_context)}<br>
                #<b>Timestamp:</b> {timestamp}<br>
                #<b>Mode:</b> {mode}<br>
                #<b>Message Type:</b> {message_type}<br>
                #<b>Message ID:</b> {message_id}<br>
                #<b>Message Text:</b> {message_text}<br>
                #<b>Quote Token:</b> {quote_token}<br>
                #<b>Source Type:</b> {source_type}<br>
                #<b>Reply Token:</b> {reply_token}<br>            
                link_text = "\r\n<b>チャットボット設定用シート</b>\r\n シート用のアプリはチャットから\r\n @リファペディア\r\n と打ち込むと開きます"
                link_url = "https://docs.google.com/spreadsheets/d/13pqP-Ywo5eRlZBsYX2m3ChARG38EoIYOowFd3cWij1c/edit?gid=283940886#gid=283940886"
                #test_set_lide(subtitle, text)
                #thread_name = send_google_chat_card(webhook_url, title, subtitle, link_text, link_url,thmbnail)



                #########################################################################
                ### n8n WorkFlowStart
                #########################################################################
                line_signature = received_headers.get("x-line-signature")
                ####$for debug
                headers = {
                    "Content-Type": "application/json",
                    "X-Line-Signature": line_signature,
                    "Authorization": f"Bearer vzn2zssSEtHb/IVgMbgY1KxLQUfmUXRuiQiQkZLRVsHOeQBp9KsU5/M0i/2XKtw1K+eXN4PyjHQKcG5Vj5l+4e5CGAOQa/veKWdn83UPJQJU17FC9ONucjc84gvNFcRAy4IZcFcMky2PTzazf0KGiFGUYhWQfeY8sLGRXgo3xvw=",
                    "user_id":user_id,
                }
                #/webhook-test/d2d0af6e-5c42-45b6-a923-3bd2d8520e3f
                #d2d0af6e-5c42-45b6-a923-3bd2d8520e3d
                
                
                
                #thread_name = send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name)
                #return
                #test case
                #########################################################################
                print("mesage is ------------------------------"+message_text)
                #if any(keyword in message for keyword in ["買取方法", "取扱商品", "本日の金価格"]):
                if "金価格" in message_text or "買取方法" in message_text:
                    print("start reply -----------------------------------------------"+reply_token)
                    first_line = text.split('\n')[0]
                    # test_prompt
                    line_bot_api = LineBotApi(ChannelAccessToken)
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text=message_text+"買取方法、取扱商品、または本日の金価格に関連するメッセージです 固定メッセージです クレジットは消費しません")
                    )
                    print("End replay -----------------------------------------------")
                    exit
        if not line_signature:
            raise HTTPException(status_code=400, detail="X-Line-Signature header is missing.")

        if not validate_signature(body.decode("utf-8"), line_signature, os.getenv("ChannelSecret")):
            raise HTTPException(status_code=400, detail="Invalid signature.")

        if not os.getenv("WEBHOOK_URL") or not os.getenv("WEBHOOK_URL").startswith("https://"):
            raise HTTPException(status_code=400, detail="Invalid webhook URL")

        headers = {
            "Content-Type": "application/json",
            "X-Line-Signature": line_signature,
            "Authorization": f"Bearer {os.getenv('ChannelAccessToken')}",
        }
        #
        logger.info("Forwarding to URL: %s", os.getenv("WEBHOOK_URL"))
        logger.info("Forwarding Headers: %s", headers)
        logger.info("Forwarding Body: %s", body.decode("utf-8"))
        print("-------------------------------------------------------------------")
        response = requests.post("https://api-mebo.dev/line/events/397cca5b-1a1c-4cee-b207-3b2b4fe642ab191ab9d06f32b7/3491d43d-f3e3-4c90-be9e-70fd61783a1b1919394918b1ac", headers=headers, data=body)
        #responses = requests.post(os.getenv("WEBHOOK_GAS"), headers=headers, data=body)
        logger.info("Response Code: %s", response.status_code)
        logger.info("Response Content: %s", response.text)
        logger.info("Response Headers: %s", response.headers)
        print("-------------------------------------------------------------------")
        
        return {"status": "success", "response_content": response.text}#, response.status_code

    except Exception as e:
        print(e)
        error_file = os.path.basename(__file__)  # ファイル名を取得
        error_line = sys._getframe(1).f_lineno  # 行番号を取得
        print(f"Error occurred at file {error_file} on line {error_line}: {str(e)}")
        #raise するとシステムとまるのでアンコメント
        #raise HTTPException(status_code=500, detail=str(e))
        return {"status": "success", "response_content": str(e)}#, response.status_code
