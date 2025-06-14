import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 環境変数からサービスアカウントのJSON内容を取得
service_account_info = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')

if service_account_info is None:
    raise ValueError("サービスアカウントのJSON内容が設定されていません。")

# JSON文字列を辞書に変換
service_account_info_dict = json.loads(service_account_info)

# サービスアカウント情報を使用して認証情報を作成
credentials = service_account.Credentials.from_service_account_info(
    service_account_info_dict,
    scopes=['https://www.googleapis.com/auth/chat.bot']  # 必要なスコープを指定
)

# Google Chat APIクライアントを作成
chat_service = build('chat', 'v1', credentials=credentials)

# メッセージを送信するスペースの名前（適切な形式に修正）
space_name = 'spaces/AAAAv_S3Bco'  # ここを実際のスペースIDに置き換えてください

# 初回メッセージを送信
initial_message = {
    'text': 'スレッドへ返信に変更テスト'
}

initial_response = chat_service.spaces().messages().create(
    parent=space_name,
    body=initial_message
).execute()

# スレッドキーを取得
thread_name = initial_response['thread']['name']
print('Initial message sent. Thread name:', thread_name)

return thread_name


# 後続のメッセージをスレッド内に送信するためのURLを構築
url = f'https://chat.googleapis.com/v1/{space_name}/messages?messageReplyOption=REPLY_MESSAGE_OR_FAIL'

# 後続のメッセージをスレッド内に送信
follow_up_message = {
    'text': 'スレッドへ返信.',
    'thread': {
        'name': thread_name
    }
}

# アクセストークンを取得
credentials.refresh(Request())
access_token = credentials.token

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(follow_up_message))

print('Follow-up message sent:', response.json())
