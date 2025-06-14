import requests
import json

# Webhook URL
webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAAA/messages?key=YOUR_WEBHOOK_KEY&token=YOUR_WEBHOOK_TOKEN&messageReplyOption=REPLY_MESSAGE_OR_FAIL'  # ここを実際のWebhook URLに置き換えてください

# スレッドキーを設定（任意の一意な値）
thread_key = 'example-thread-key'

# 初回メッセージを送信
initial_message = {
    'text': 'Hello from the Google Chat Webhook!',
    'threadKey': thread_key
}

response = requests.post(webhook_url, data=json.dumps(initial_message), headers={'Content-Type': 'application/json'})

print('Initial message response:', response.json())

# スレッド内に返信メッセージを送信
follow_up_message = {
    'text': 'This is a follow-up message in the same thread.',
    'threadKey': thread_key
}

response = requests.post(webhook_url, data=json.dumps(follow_up_message), headers={'Content-Type': 'application/json'})

print('Follow-up message response:', response.json())
