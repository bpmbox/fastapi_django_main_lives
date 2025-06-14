import requests

def post_data_line(url, body,headers):
    # POSTリクエストのペイロード
    payload = body

    # ヘッダーの設定（必要に応じて）
    #$headers = {
    #    'Content-Type': 'application/json'
    #}
    #
    # POSTリクエストの送信
    #response = requests.post(url, json=payload, headers=headers)
    response = requests.post(url, headers=headers, data=body)
    # レスポンスのステータスコードを表示
    print(f'Status Code: {response.status_code}')

    # レスポンスの内容を表示
    print(f'Response Content: {response.content.decode()}')

    return response

def post_data(url, word, thread,headers):
    # POSTリクエストのペイロード
    payload = {
        'word': word,
        'thread': thread
    }

    # ヘッダーの設定（必要に応じて）
    #$headers = {
    #    'Content-Type': 'application/json'
    #}

    # POSTリクエストの送信
    response = requests.post(url, json=payload, headers=headers)

    # レスポンスのステータスコードを表示
    print(f'Status Code: {response.status_code}')

    # レスポンスの内容を表示
    print(f'Response Content: {response.content.decode()}')

    return response

# 使用例
#url = ''
#word = 'example_word'
#thread = 'example_thread'
#post_data(url, word, thread)
