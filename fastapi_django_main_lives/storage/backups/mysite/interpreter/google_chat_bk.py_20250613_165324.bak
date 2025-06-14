import requests
import json

def convert_newlines_to_google_chat_format(text):
    # 改行文字を <br> タグに置き換える
    return text.replace('\\n', '\\\n')
#
def send_google_chat_card(webhook_url, title, subtitle, link_text, link_url,image_url=None):
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
                                            "text": "チャットボット設定シートを開く ",
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
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "ラインチャットを開く",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://chat.line.biz/U2df77fd63804c72346b4e50c0096572e/chat/Ua13ef47afc077917275658a44019e072"
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
                                            "text": "プロンプト修正",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-php.hf.space/prompts_list.php"
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
                                            "text": "Q&A検証正しい物だけにチェック",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-php.hf.space/zendesk__dataszz_list.php?qs=500%E5%86%86"
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
                                            "text": "データ確認チャット 反映されているか確認",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-nodex-n8n-domain.hf.space/webhook/6264497c-6231-4023-abef-82b86f8e298b/chat"
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
                                            "text": "WEBボットカスタマーサポートテスト",
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
                                            "text": "HUBスポットチャットテスト",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-gradio-fastapi-statichfspace-46277896.hubspotpagebuilder.com/workflow"
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
                                            "text": "ダイヤモンドデータ確認 EVAのデータも登録し予測検索用にベクトル化する",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-php.hf.space/diamondprice_list.php"
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
                                            "text": "ワークフロー修正",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://kenken999-nodex-n8n-domain.hf.space/workflow/hArXsWSx9ZrvUnvT"
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
                                            "text": "全体行程マインドマップ",
                                            "onClick": {
                                                "openLink": {
                                                    "url": "https://www.mindmeister.com/3342966040?e=turtle&new=1#"
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