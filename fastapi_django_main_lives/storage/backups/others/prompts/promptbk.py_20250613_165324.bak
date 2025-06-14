prompt_for_create_system = """
下記の質問に対応するコードをdjangoでアプリを作成　プロジェクトはいりません
fastapiでrouter部分を作成　組み込みはメイン部分でします
フロントエンドをgradioで作成
#google apps script frontend
    googleappsscript  doGet でのgradioの表示処理を作成 google.script.runで関数は呼び出し
#google apps script backend
    frontendからの呼び出し用のバックエンドスクリプト
仕様書の作成
PlantUMLでシーケンス図の作成
Markdownでのプログラム殺名
#下記参考にAPIも作成しておいて
action insert list edit update でCRUDがかわる
同じようにGASのAPIも作成しておいて

def create_vector():
    inputs = tokenizer(result, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    # [CLS]トークンの出力を取得
    embeddings = outputs.last_hidden_state[:,0,:].squeeze().detach().cpu().numpy().tolist()   
    print(embeddings)
    import requests

    url = "https://kenken999-php.hf.space/api/v1.php"

    payload = "model_name={embeddings}&vector_text={result}&table=products&action=insert""
    headers = {
    'X-Auth-Token': 'admin',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'runnerSession=muvclb78zpsdjbm7y9c3; pD1lszvk6ratOZhmmgvkp=13767810ebf0782b0b51bf72dedb63b3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)    
    return True

下記の質問 作成対応内容

"""        

prompt = """
1, Q&Aのテーブルを作成してください DBはpostgress pk はPostgresのAutoIncrementの serialでの自動追加
2, 質問が来た際には、まず質問に対しての答えを過去のデータから探します
3, Q&Aから役割を作成します
    質問に対しての答えを出す、シナリオを考える
4, 実際にテストして正しい答えがでるか確認
5, 出ない場合は再度作成しなおします
    1から6を繰り返し、答えが出たプロンプトを登録します
7, 成功した場合それを保存します
8, 同じ質問が来たら質問別にプロンプトを変更します
9, 上記をラインの質問に内部の方が納得いくまで、日々修正していきます
"""
def get_prompt(text):
    prompt2 = f""" 
    # 返信について日本語で必ず答えて下さい
    # 役割
        あなたはリファスタという会社のアシスタントです
        金、ダイヤモンド、商品を売りたい顧客います
        売りに来た顧客の質問内容は {text}
        この質問を買取店の査定人に対して、理解がしやすい わかりやすい質問に変更してください
        質問のカテゴリーも、ファインチューニングに必要な物にして下さい

        リファスタのYOUTUBEから質問に対する　動画のURLを提示してください、２，３個
        https://www.youtube.com/@refastaofficial/search?query=質問内容
        質問内容を質問に変更して　上記のURLを参考にしてください

        質問のカテゴリーも、ファインチューニングに必要な物にして下さい
        質問を元に、Q&Aを５つ作って下さい。フィードバックとデータの精査に使います

        質問内容を元に下記の形で商品検索のURLを作成してください
        https://kenken999-php.hf.space/zendesk__dataszz_list.php?qs=500%E5%86%86

        

        会社にはデータベースがあり質問内容から、商品を検索するSQLを作成してください
        必要なテーブルのCreate文も作成してして下さい
        pk は postgress なので 自動連番のserialにして下さい
        質問の内容をそのテーブルにいれるインサート文も作成してくさい

        ほかに、良い提案があればして下さい。こうしたらもっと、良くなるよなど。
        上記の内容を元に、HTML　LP用のHTMLを作成してください

    ## リファスタの住所
        〒170-0013 東京都豊島区東池袋１丁目２５−１４ アルファビルディング 4F
    ## 買取ダイヤテンプレート
        - price,
        - carat, 
        - cut, 
        - color, 
        - clarity, 
        - depth, 
        - diamondprice.table, 
        - x, 
        - y, 
        - z
    ## 買取ブランドテンプレート
        ・ブランド名：
        ・モデル名：
        ・型番や品番：
        ・購入店：
        ・購入時期：
        ・購入金額：
        ・付属品：
        ・コンディション：
        (10段階評価厳しめ)
        ・貴金属品位：
        ・貴金属重量：
        (キッチンスケールでも(sparkle))
        ・ダイヤや宝石の鑑定書はお写真で！
        ・イニシャル：あり　なし 
    ## リファスタのサイト 
        (monitor)24h対応事前査定
        https://kinkaimasu.jp/estimate/?openExternalBrowser=1&utm_source=LINE

        (open book)買取システムナビ
        https://kinkaimasu.jp/system/?openExternalBrowser=1&utm_source=LINE

        (car)店舗アクセス
        https://goo.gl/veQZ03

        (?)よくある質問
        https://kinkaimasu.jp/faq/?openExternalBrowser=1&utm_source=LINE"
        User,hibiki,2024/06/16,21:53:47,"まだ買取をするか未定ですが、
        一度査定をよろしくお願いします。"
        Account,応答メッセージ,2024/06/16,21:53:47,"(clock)ただ今対応時間外(clock)
        営業時間：11:00～20:00
        ※年中無休 
        翌営業日に順次対応致しますので、お写真や情報はいつでもお送りください(moon wink)


        (monitor)24h対応事前査定
        https://kinkaimasu.jp/estimate/?openExternalBrowser=1&utm_source=LINE

        (open book)買取システムナビ
        https://kinkaimasu.jp/system/?openExternalBrowser=1&utm_source=LINE

        (car)店舗アクセス
        https://goo.gl/veQZ03

        (?)よくある質問
        https://kinkaimasu.jp/faq/?openExternalBrowser=1&utm_source=LINE"
    ## サービス
    ## フリーダイヤル
        お気軽にお電話くださいませ(sparkle)
        10:30〜20:00 年中無休

        オンライン買取も受付中
        https://kinkaimasu.jp/online-promise/?openExternalBrowser=1&utm_source=LINE 

    ## (smartphone) 電話番号
        0120-954-679

    ## (LINE messenger) LINE通話
        https://lin.ee/c6inM4V    

    """
    return prompt2