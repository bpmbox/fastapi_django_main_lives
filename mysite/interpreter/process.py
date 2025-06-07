import os
import shutil
import hmac
import hashlib
import base64
import subprocess
import time
from mysite.logger import logger
import async_timeout
import asyncio
import mysite.interpreter.interpreter_config 
from models.ride import test_set_lide
from mysite.libs.github import github
import requests
import json
from mysite.logger import log_error
import os
GENERATION_TIMEOUT_SEC=60
BASE_PATH = "/home/user/app/app/Http/controller/"

def set_environment_variables():
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    os.environ["OPENAI_API_KEY"] = os.getenv("api_key")
    os.environ["MODEL_NAME"] = "llama3-8b-8192"
    os.environ["LOCAL_MODEL"] = "true"

def convert_newlines_to_google_chat_format(text):
    # 改行文字を <br> タグに置き換える
    return text.replace('\\n', '\\\n')

def send_google_chat_card(webhook_url, title, subtitle, link_text, link_url):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    subtitle = convert_newlines_to_google_chat_format(subtitle)

    card_message = {
        "cards": [
            {
                "header": {
                    "title": title,
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": subtitle
                                }
                            },
                            {
                                "textParagraph": {
                                    "text": "<b>{}</b>".format(link_text)
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Open Link",
                                            "onClick": {
                                                "openLink": {
                                                    "url": link_url
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                "textParagraph": {
                                    "text": "<b>{}</b>".format("ステップ２　テスト　google apps script(その場で誰でもさくっと動くレベルがいい)")
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Open Link",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://script.google.com/d/1YJCQDrzGnrJiRcJcRjX9RuKR3gGrIj84p5kp4ZMiY-ls9UafjhDEUXIk/edit?usp=sharing"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                "textParagraph": {
                                    "text": "<b>{}</b>".format("ステップ３　テスト　google colab(その場で誰でもさくっと動くレベルがいい)")
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Open Link",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://colab.research.google.com/drive/1LNR_Y9sk9DGYnWTxHP09s9x4JLe3GmqS?hl=ja"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                "textParagraph": {
                                    "text": "<b>{}</b>".format("ステップ４　workflow　に組み込み(うまくいった　小さなものを組み合わせる)")
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Open Link",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://bpmboxesscom-46463613.hubspotpagebuilder.com/ja/"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                "textParagraph": {
                                    "text": "<b>{}</b>".format("ステップ５　カスタマーサービス内部で相談")
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Open Link",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://bpmboxesscom-46463613.hubspotpagebuilder.com/ja/"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                             {
                                "textParagraph": {
                                    "text": "<b>{}</b>".format("ステップ６　過去のテンプレートを元に思ったものを作ってみる　コピーペースト 繰り返し")
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Open Link",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-php.hf.space/main_list.php"
                                                }
                                            }
                                        }
                                    }
                                ]
                            }, 
                             {
                                "textParagraph": {
                                    "text": "<b>{}</b>".format("リファスタチャットボット確認")
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Open Link",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://www.coze.com/store/bot/7372534558954176520?panel=1&bid=6cqv73j0k7g0i"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },                                                                                                                

                        ]
                    }
                ]
            }
        ]
    }


    response = requests.post(webhook_url, headers=headers, data=json.dumps(card_message))

    if response.status_code == 200:
        print("Message posted successfully.")
    else:
        print(f"Failed to post message: {response.status_code}, {response.text}")



def validate_signature(body: str, signature: str, secret: str) -> bool:
    if secret is None:
        logger.error("Secret is None")
        return False

    hash = hmac.new(
        secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash).decode("utf-8")
    return hmac.compare_digest(expected_signature, signature)
from mysite.interpreter.google_chat import send_google_chat_card,send_google_chat_card_thread
#プロセスの実行
def no_process_file(prompt, foldername,thread_name=None):
    set_environment_variables()
    try:
        proc = subprocess.Popen(["mkdir", f"{BASE_PATH}{foldername}"])
    except subprocess.CalledProcessError as e:
        return f"Processed Content:\n{e.stdout}\n\nMake Command Error:\n{e.stderr}"

    no_extension_path = f"{BASE_PATH}{foldername}/prompt"
    time.sleep(1)
    with open(no_extension_path, "a") as f:
        f.write(prompt)
    time.sleep(1)
    try:
        prompt_file_path = no_extension_path
        with open(prompt_file_path, "a") as prompt_file:
            prompt_file.write(prompt)
    except Exception as e:
        return f"Error writing prompt to file: {str(e)}"
    time.sleep(1)

    try:
        proc = subprocess.Popen(
            ["make", "run", foldername],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(input="n\ny\ny\n")
        webhook_url = os.getenv("chat_url")
        token = os.getenv("token")
        #githubでのソース作成
        #log_error("github でエラーが起きました")
        try:
            url = github(token,foldername)
        except Exception as e:
            log_error(e)

        title = """ラインで作るオープンシステム
        お客様の質問内容の
        プログラムを作成しました"""
        subtitle = prompt
        link_text = "ステップ１　githubで　プログラムを確認する githubだと相談者が沢山いるのでわからなければ聞いてみる "
        link_url = url

        #send_google_chat_card,send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name)
        
        #insert data to db
        #test_set_lide(prompt,url)
        print(f"Processed Content:success ")
        return f"Processed Content:success "#\n{stdout}\n\nMake Command Output:\n{stdout}\n\nMake Command Error:\n{stderr}"
    except subprocess.CalledProcessError as e:
        print(f"Processed Content:false ")
        return f"Processed Content:error"# {str(e)}"#\n{e.stdout}\n\nMake Command Error:\n{e.stderr}"

def process_nofile(prompt, foldername, token=None):
    set_environment_variables()
    try:
        os.makedirs(f"{BASE_PATH}{foldername}", exist_ok=True)
    except Exception as e:
        return f"Error creating directory: {str(e)}"

    time.sleep(1)

    # promptファイルの作成
    prompt_file_path = f"{BASE_PATH}{foldername}/prompt"
    try:
        with open(prompt_file_path, "w") as prompt_file:
            prompt_file.write(prompt)
    except Exception as e:
        return f"Error writing prompt to file: {str(e)}"

    time.sleep(1)

    # foldernameの登録
    test_set_lide(prompt, foldername)

    try:
        proc = subprocess.Popen(
            ["make", "run", foldername],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(input="n\ny\ny\n")

        token = os.getenv("github_token")
        try:
            url = github(token, foldername)
        except Exception as e:
            log_error(e)
            url = "Error creating GitHub repo"

        test_set_lide(prompt, url)

        return f"Processed open github url: {url}\nContent:\n{stdout}\n\nMake Command Output:\n{stdout}\n\nMake Command Error:\n{stderr}"
    except subprocess.CalledProcessError as e:
        return f"Processed url: {url}\nMake Command Error:\n{e.stderr}"


def process_file(fileobj, prompt, foldername,token=None):
    set_environment_variables()
    try:
        proc = subprocess.Popen(["mkdir", f"{BASE_PATH}{foldername}"])
    except subprocess.CalledProcessError as e:
        return f"Processed Content:\n{e.stdout}\n\nMake Command Error:\n{e.stderr}"
    time.sleep(2)
    path = f"{BASE_PATH}{foldername}/" + os.path.basename(fileobj)
    shutil.copyfile(fileobj.name, path)
    base_name = os.path.splitext(os.path.basename(fileobj))[0]
    no_extension_path = f"{BASE_PATH}{foldername}/{base_name}"
    shutil.copyfile(fileobj, no_extension_path)
    with open(no_extension_path, "a") as f:
        f.write(prompt)
    try:
        prompt_file_path = no_extension_path
        with open(prompt_file_path, "w") as prompt_file:
            prompt_file.write(prompt)
    except Exception as e:
        return f"Error writing prompt to file: {str(e)}"
    time.sleep(1)
    #foldernameの登録
    test_set_lide(prompt,foldername)
    try:
        proc = subprocess.Popen(
            ["make", "run", foldername],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = proc.communicate(input="n\ny\ny\n")

        token = os.getenv("github_token")
        #githubでのソース作成
        #log_error("github でエラーが起きました")
        try:
            url = github(token,foldername)
        except Exception as e:
            log_error(e)
        #url = "test"
        test_set_lide(prompt,url)
        return f"Processed open github url:{url}\nContent:\n{stdout}\n\nMake Command Output:\n{stdout}\n\nMake Command Error:\n{stderr}"
    except subprocess.CalledProcessError as e:
        return f"Processed url:{url}\nContent:\n{stdout}\n\nMake Command Error:\n{e.stderr}"

