import os
import shutil
import hmac
import hashlib
import base64
import subprocess
import time
import async_timeout
import asyncio
import requests
import json

# Conditional imports to avoid circular dependencies
try:
    from mysite.logger import logger, log_error
except ImportError:
    # Fallback logger for standalone usage
    import logging
    logger = logging.getLogger(__name__)
    log_error = logger.error

try:
    import mysite.interpreter.interpreter_config
except ImportError:
    pass

try:
    from models.ride import test_set_lide
except ImportError:
    def test_set_lide(prompt, url):
        logger.warning("test_set_lide not available")
        pass

try:
    from mysite.libs.github import github
except ImportError:
    def github(token, foldername):
        logger.warning("github function not available")
        return "https://github.com/placeholder"

GENERATION_TIMEOUT_SEC=60

def get_base_path():
    """
    環境に応じて動的にベースパスを取得
    """
    try:
        # 環境変数から取得を試行
        env_base_path = os.getenv("INTERPRETER_BASE_PATH")
        if env_base_path:
            # パスの正規化と存在確認
            normalized_path = os.path.normpath(env_base_path)
            if not normalized_path.endswith('/'):
                normalized_path += '/'
            
            # 親ディレクトリの存在確認
            parent_dir = os.path.dirname(normalized_path.rstrip('/'))
            if os.path.exists(parent_dir):
                return normalized_path
            
            logger.warning(f"Environment path parent not found: {parent_dir}")
        
        # 現在の作業ディレクトリから推測
        current_dir = os.getcwd()
        logger.info(f"Current directory: {current_dir}")
        
        # Codespaces環境の検出
        if "/workspaces/" in current_dir:
            path = os.path.join(current_dir, "app", "Http", "controller")
            return os.path.normpath(path) + "/"
        
        # Docker環境の検出
        if "/home/user/app/" in current_dir or os.path.exists("/home/user/app/"):
            return "/home/user/app/app/Http/controller/"
        
        # ローカル開発環境
        if "fastapi_django_main_live" in current_dir:
            path = os.path.join(current_dir, "app", "Http", "controller")
            return os.path.normpath(path) + "/"
        
        # フォールバック: カレントディレクトリ下にcontrollerディレクトリを作成
        fallback_path = os.path.join(current_dir, "temp_controller")
        return os.path.normpath(fallback_path) + "/"
        
    except Exception as e:
        logger.error(f"Error in get_base_path: {str(e)}")
        # 絶対フォールバック
        return os.path.join(os.getcwd(), "temp_controller") + "/"

# 動的にベースパスを設定 - 遅延初期化
BASE_PATH = None

def get_base_path_safe():
    """
    安全なベースパス取得（遅延初期化）
    """
    global BASE_PATH
    if BASE_PATH is None:
        BASE_PATH = get_base_path()
    return BASE_PATH

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

# Conditional import for google_chat functions
try:
    from mysite.interpreter.google_chat import send_google_chat_card, send_google_chat_card_thread
except ImportError:
    def send_google_chat_card(*args, **kwargs):
        logger.warning("send_google_chat_card not available")
        pass
    def send_google_chat_card_thread(*args, **kwargs):
        logger.warning("send_google_chat_card_thread not available")
        pass

#プロセスの実行
def ensure_base_path_exists():
    """
    ベースパスが存在することを確認し、必要に応じて作成
    """
    global BASE_PATH
    # 遅延初期化
    if BASE_PATH is None:
        BASE_PATH = get_base_path()
    
    try:
        os.makedirs(BASE_PATH, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create base path {BASE_PATH}: {str(e)}")
        # フォールバックパスを試行
        fallback_path = os.path.join(os.getcwd(), "temp_controller/")
        try:
            os.makedirs(fallback_path, exist_ok=True)
            BASE_PATH = fallback_path
            logger.info(f"Using fallback path: {BASE_PATH}")
            return True
        except Exception as fallback_error:
            logger.error(f"Failed to create fallback path: {str(fallback_error)}")
            return False

def no_process_file(prompt, foldername,thread_name=None):
    set_environment_variables()
    
    # ベースパスの存在確認
    if not ensure_base_path_exists():
        return "Error: Could not create or access base directory"
    
    target_dir = f"{BASE_PATH}{foldername}"
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        return f"Error creating directory {target_dir}: {str(e)}"

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
    
    # ベースパスの存在確認
    if not ensure_base_path_exists():
        return "Error: Could not create or access base directory"
    
    target_dir = f"{BASE_PATH}{foldername}"
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        return f"Error creating directory {target_dir}: {str(e)}"

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
    
    # ベースパスの存在確認
    if not ensure_base_path_exists():
        return "Error: Could not create or access base directory"
    
    target_dir = f"{BASE_PATH}{foldername}"
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        return f"Error creating directory {target_dir}: {str(e)}"
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

