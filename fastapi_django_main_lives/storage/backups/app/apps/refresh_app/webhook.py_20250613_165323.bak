
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
                promps,prompt_res = prompt_genalate("返信は日本語で答えて下さい "+text,get_prompt(text))

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

                import requests
                import os

                # テキストを定義
                # texts = (text)

                # テキストをファイルに保存
                text_file_path = 'text.txt'
                with open(text_file_path, 'w', encoding='utf-8') as file:
                    file.write(text)

                # 音声合成のクエリを取得
                with open(text_file_path, 'r', encoding='utf-8') as file:
                    response = requests.post(
                        "https://kenken999-voicebox.hf.space/audio_query?speaker=1",
                        params={'text': file.read()}
                    )

                query_json = response.json()

                # 音声合成の実行
                response = requests.post(
                    "https://kenken999-voicebox.hf.space/synthesis?speaker=2",
                    headers={"Content-Type": "application/json"},
                    json=query_json
                )

                # staticフォルダに音声ファイルを保存
                os.makedirs('staticfiles', exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                audio_file_name = f"audio_{timestamp}.wav"
                audio_file_path = os.path.join('staticfiles', audio_file_name)
                with open(audio_file_path, 'wb') as file:
                    file.write(response.content)
                ##audio send add
                print(f"Audio saved as {audio_file_path}")
                wavurl = "https://kenken999-fastapi-django-main.hf.space/static/"+audio_file_name
                #thread_name = send_google_chat_wav(webhook_url, "youtube audiofile", wavurl, link_text, link_url,thmbnail)#thread_name)
                thread_name = send_google_chat_card(webhook_url, title, subtitle, link_text, link_url,thmbnail,wavurl)



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
                post_data("https://kenken999-nodex-n8n.hf.space/webhook-test/d2d0af6e-5c42-45b6-a923-3bd2d8520e3f",text,thread_name,headers)
                #http://localhost:7860/webhook-test/d2d0af6e-5c42-45b6-a923-3bd2d8520e3f
                post_data_line("https://kenken999-nodex-n8n.hf.space/webhook-test/d2d0af6e-5c42-45b6-a923-3bd2d8520e3d",body,headers)
                #http://localhost:7860/webhook/d2d0af6e-5c42-45b6-a923-3bd2d8520e3d
                post_data_line("https://kenken999-nodex-n8n.hf.space/webhook/d2d0af6e-5c42-45b6-a923-3bd2d8520e3d",body,headers)
                #post_data_line("https://kenken999-nodex-n8n.hf.space/webhook/d2d0af6e-5c42-45b6-a923-3bd2d8520e3f",body,headers)
                
                #return

                
                post_data(n8nurl,text,thread_name,headers)
                time.sleep(10)
                #########################################################################
                title = f""" プロンプト作成 {promps}"""
                subtitle = f"""userid {user_id}\r\n chatid {thread_name}\r\n{prompt_res}"""
                link_text = "データを確認する"
                link_url = "https://kenken999-php.hf.space/diamondprice_list.php"
                #test_set_lide(subtitle, text)
                if DEBUG==1:
                    thread_name = send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name)
                
                #thread_name = send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name)
                #return
                #test case
                #########################################################################
                first_line = text.split('\n')[0]
                #test_prompt
                res = test_prompt("返信は必ず日本語でして下さい \r\n"+prompt_res,text)
                
                if DEBUG==1:
                    thread_name = send_google_chat_card_thread(webhook_url, "プロンプトテスト "+first_line, str(res), link_text, link_url,thread_name)
                
                #thread_name = send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name)
                now = datetime.now()
                yyyymmddhis = now.strftime('%Y%m%d%H%M%S')

    
                ######################################################################### 
                ## excute create program
                if DEBUG==1:
                    res_no_process = no_process_file(prompt_for_create_system+res, "gpt_enginner"+ yyyymmddhis,thread_name)
                # execute open interpreter
                #########################################################################
                if DEBUG==1:
                    full_response,history = chat_with_interpreter_no_stream(prompt_for_create_system+"\r\n"+res)
                if DEBUG==1:
                    thread_name = send_google_chat_card_thread(webhook_url, f"自動設定開始 {res}", str(full_response), link_text, link_url,thread_name)
                ####################################################################
                #ダイヤ金額計算
                from babyagi.classesa.diamond import calculate
                if DEBUG==1:
                    title = f""" ダイヤ予測計算の実行 類似５件表示 {text} 
                    id,price,carat, cut, color, clarity, depth, diamondprice.table, x, y, z 類似度"""
                    #ベクトルインデックス
                    res_calculate = calculate(text)
                    subtitle = res_calculate
                    link_text = "データを確認する"
                    link_url = "https://kenken999-php.hf.space/diamondprice_list.php"
                    #########################################################################
                    #test_set_lide(subtitle, text)
                
                    #if DEBUG==0:
                    thread_name = send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name)
                #########################################################################
                from babyagi.babyagi import completion
                #import tempfile
                text = text.replace("\r\n","")
                # コマンドを構築
                command = f"""make runbabyagi "{text}に対して、より良いチャットボットでのQAプランデータ設定の提案を日本語で作成してください" {thread_name}"""
                if DEBUG==1:
                    with open('/home/user/app/babyagi/prompt.txt', 'w') as file:
                        file.write(f"""{text}の質問 についてチャットボットでよりよく対応するプランを日本語で作成して""")
                    
                ######################################################################
                if DEBUG==1:
                    proc = subprocess.Popen(
                        ["make", "runbabyagi", thread_name],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )                  
 
        logger.info("Received Headers: %s", received_headers)
        logger.info("Received Body: %s", body.decode("utf-8"))
        ###############################################################################
        #send to appsheet 
        get_senario("user_id",str(body))
        #apps script send
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("Received Body: %s", "send data to appsheet ")
        #response = requests.post(os.getenv("WEBHOOK_URL"), headers=headers, data=body)
        # check signature
        line_signature = received_headers.get("x-line-signature")
        logger.info("Received Body: %s", "start send messages ")
        #headers = {
        #                "Content-Type": "application/json",
        #                "X-Line-Signature": line_signature,
        #                "Authorization": f"Bearer {os.getenv('ChannelAccessToken')}",
        #             }
        #r#esponse = requests.post(os.getenv("WEBHOOK_URL"), headers=headers, data=body)
        
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

        logger.info("Forwarding to URL: %s", os.getenv("WEBHOOK_URL"))
        logger.info("Forwarding Headers: %s", headers)
        logger.info("Forwarding Body: %s", body.decode("utf-8"))

        response = requests.post(os.getenv("WEBHOOK_URL"), headers=headers, data=body)
        responses = requests.post(os.getenv("WEBHOOK_GAS"), headers=headers, data=body)
        logger.info("Response Code: %s", response.status_code)
        logger.info("Response Content: %s", response.text)
        logger.info("Response Headers: %s", response.headers)

        return {"status": "success", "response_content": response.text}#, response.status_code

    except Exception as e:
        error_file = os.path.basename(__file__)  # ファイル名を取得
        error_line = sys._getframe(1).f_lineno  # 行番号を取得
        print(f"Error occurred at file {error_file} on line {error_line}: {str(e)}")
        # スタックトレースの詳細を取得
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_info = traceback.extract_tb(exc_tb)[-1]  # 最後のトレースバック情報を取得
        error_file = tb_info.filename  # エラーが発生したファイル
        error_line = tb_info.lineno    # エラーが発生した行
        error_trace = traceback.format_exc()  # スタックトレース全体を取得       
        #エラー内容の分析
        promps,res = prompt_genalate(str(e))
        #test_set_lide(text,"a1")
        #no_process_file(text, "ai")
        custormer_supportpage = "\r\n カスタマーサポートはこちらから \r\n https://bpmboxesscom-46463613.hubspotpagebuilder.com/ja \r\n "
        title = f"""Error occurred at file {error_file} on line {error_line}: {str(e)}\n{error_trace}エラーが起こりました  -+errer file is {error_file}  error line is {error_line} {str(e)} 自動修復の開始 """
        subtitle = custormer_supportpage+res
        link_text = "test"
        link_url = "url"
        #test_set_lide(subtitle, text)
        logger.error(res)
        #send error to google chat
        ###
        #send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name)            
        
        logger.error("Error: %s", str(e))
        #raise するとシステムとまるのでアンコメント
        #raise HTTPException(status_code=500, detail=str(e))
        return {"status": "success", "response_content": str(e)}#, response.status_code
