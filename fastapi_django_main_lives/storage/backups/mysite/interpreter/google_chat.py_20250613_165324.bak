import requests
import json

def convert_newlines_to_google_chat_format(text):
    # 改行文字を <br> タグに置き換える
    return text.replace('\\n', '\\\n')
#

def send_google_chat_wav(webhook_url, title, subtitle, link_text, link_url,image_url=None):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    #subtitle = convert_newlines_to_google_chat_format(subtitle)

    card_message = {
        "cards": [
            {
                "header": {
                    "title": title,
                     "imageUrl": image_url,
                     "imageStyle": "IMAGE" 
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": "音声ファイル"
                                }
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "音声を開く",
                                            "onClick": {
                                                "openLink": {
                                                    "url": subtitle
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
        #
    response_data = response.json()
    thread_name = response_data['thread']['name']
    return thread_name



def send_google_chat_card(webhook_url, title, subtitle, link_text, link_url,image_url=None,wav_url=None):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    subtitle = convert_newlines_to_google_chat_format(subtitle)

    card_message = {
        "cards": [
            {
                "header": {
                    "title": title,
                     "imageUrl": image_url,
                     "imageStyle": "IMAGE" 
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
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "ラインチャットを開く",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-php.hf.space/main_list.php?page=mainpage"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },  
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "答えを確認する(GSS)",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://docs.google.com/spreadsheets/d/13pqP-Ywo5eRlZBsYX2m3ChARG38EoIYOowFd3cWij1c/edit?gid=546803454#gid=546803454"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },        
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "音声ファイルを開く",
                                            "onClick": {
                                                "openLink": {
                                                    "url": wav_url
                                                }
                                            }
                                        }
                                    }
                                ]
                            }, 
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "Youtubで質問",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://youtube.com/live/F0NuvKMzuBY?feature=share"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "業務シナリオボット",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://miibo.jp/chat/3621b152-82fe-4ffd-9696-1daa0934e37a19087ba9d801fc?name=%E3%83%"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },                           
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "ナレッジを追加する",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://miibo.dev/admin/datastore"
                                                }
                                            }
                                        }
                                    }
                                ]
                            }, 
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "ナレッジを追加する EVA業務一覧",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://docs.google.com/spreadsheets/d/1ZdD7hVUsXeu4cO7Bys5WkyTplSkhZIi2KhDhBmfenKs/edit?gid=925846218#gid=925846218"
                                                }
                                            }
                                        }
                                    }
                                ]
                            }, 
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "ナレッジの作り方",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://chill-shoemaker-341.notion.site/dd577fb90fa7446bb3d25ce1c832da30"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },  
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "予定管理をする",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://urlounge.atlassian.net/browse/KAN-41"
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
        #
    response_data = response.json()
    thread_name = response_data['thread']['name']
    return thread_name

def send_google_chat_card_thread(webhook_url, title, subtitle, link_text, link_url,thread_name):
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
                        ]
                    }
                ]
            }
        ],
        "thread": {
            "name":thread_name
        } 
    }

    #https://chat.googleapis.com/v1/spaces/AAAAv_S3Bco/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=D635e0eoj7MdO8HV6Ufs1HUZdNiDdz-Eo3Td3OqAFKI&messageReplyOption=REPLY_MESSAGE_OR_FAIL
    response = requests.post(webhook_url+"&messageReplyOption=REPLY_MESSAGE_OR_FAIL", headers=headers, data=json.dumps(card_message))

    if response.status_code == 200:
        print("Message posted successfully.")
    else:
        print(f"Failed to post message: {response.status_code}, {response.text}")
    
    response_data = response.json()
    thread_name = response_data['thread']['name']
    return thread_name