import logging
import os
from mysite.interpreter.prompt import prompt_genalate
from mysite.interpreter.google_chat import send_google_chat_card

# Loggerの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(lineno)d")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_error(logs):
    # ログメッセージを記録
    logger.error("エラーが発生しました: %s", logs)
    
    # 環境変数からwebhookのURLを取得し、存在しない場合はエラーメッセージを設定
    webhook_url = os.getenv("chat_url")
    # ログメッセージをプロンプト生成関数に渡してサブタイトルを生成
    promps = prompt_genalate(str(logs),"エラー内容を修正")
    title = "LOG"
    subtitle = promps
    link_text = "test"
    link_url = "url"
    # Googleチャットカードを送信
    send_google_chat_card(webhook_url, title, subtitle, link_text, link_url)
