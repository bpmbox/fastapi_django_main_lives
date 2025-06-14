import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file,no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb
import gradio as gr
import psycopg2
from dataclasses import dataclass, field
from typing import List, Optional
from mysite.interpreter.process import no_process_file,process_file
#from controllers.gra_04_database.rides import test_set_lide
import requests

val = """
# 社員がプロフィールを登録・公開し、お互いに参照できるシステム

## 機能

## LINEのクレーム対応システムの作成
- クレームがあった用語をAPIでナレッジに登録するシステム
- APIキー agentキーをいれ
- 否定語に対する　文言に隊しての設定をする

### ユーザー登録

- ユーザー登録画面で、ユーザー名とパスワードを入力して登録ボタンを押すことにより、新規ユーザーを登録することができる。
- ユーザー名は、既存のユーザーと重複してはいけない。
- ユーザー登録に成功したら、ログイン済み状態として、ユーザー一覧画面へ遷移する。

### ログイン

- ログイン画面で、ユーザー名とパスワードを入力してログインボタンを押すことにより、ログインすることができる。
- ログインに成功したら、ユーザー一覧画面へ遷移する。

### チーム一覧・作成

- チームの一覧が、チームの作成日時降順で表示される。
- チーム名を入力して作成ボタンを押すと、チームが作成される。
- チームの作成後、本画面が再表示される。

### プロフィール編集

- 自身の`所属チーム`・`プロフィール`・`タグ`を編集できる。
- 所属チームは、既存チームからの選択式とする。
- プロフィールは自由入力とする。
- タグは自由入力で、複数入力できるようにする。

### ユーザー一覧・検索

- デフォルトでは全てのユーザーが一覧表示される。
- 検索条件を入力して検索ボタンを押すと、検索条件がプロフィールに部分一致するユーザーのみにフィルタリングできる。
- 一覧は、ユーザー登録日時の降順で表示される。
- 表示内容は、`ユーザー名`・`プロフィール`で、`プロフィール`は先頭10文字と三点リーダーを表示する。
- ユーザー名をクリックすると、そのユーザーのユーザー詳細画面へ遷移する。
- `チーム一覧へ`をクリックすると、チーム一覧画面へ遷移する。

### ユーザー詳細画面

- 特定のユーザーの、`ユーザー名`・`所属チーム`・`プロフィール`・`タグ`が表示される。
- プロフィールの表示はマークダウンに対応させる。
- `一覧へ`リンクをクリックすると、ユーザー一覧画面へ遷移する。

## あなたが作成するもの

バックエンドのプログラム一式を作成してください。
フロントエンドのプログラムは不要です。

- `/api`ディレクトリ以下に作成。
- Python/FastAPI/SQLAlchemyを使う。
- DBはSQLiteを使う。
- 必要に応じて外部ライブラリを使う。
- クラウドや外部サービス(外部API)は使わない。
- .gitignoreを含めること。
- バックエンド
@app.post("
def lumbda_function():

gradio_interface でメイン関数から読み込めるようにして

googleappsscript
ラインの画像検索システム

ファイルは１ファイルで作成して。
１ファイル１機能で難しくしたくない

1,lineからデータがくる
2,doPostで取得
3.typeがイメージの場合はドライブに保存
4,保存したデータをS3にアップロード
5.データはシークレットから取得
6,plantumlでフローの作成
7,システムドキュメントの作成

gradio は gradio_interface というBlock名で作成
fastapiはrouter の作成

"""

def send_to_google_chat(message: str):
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAANwDF_KE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=qSigSPSbTINJITgO30iGKnyeY48emcUJd9LST7FBLLY'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {'text': message}
    response = requests.post(webhook_url, headers=headers, json=data)
    response.raise_for_status()

def process_file_and_notify(*args, **kwargs):
    result = process_file(*args, **kwargs)
    send_to_google_chat(result)
    return result

gradio_interface = gr.Interface(
    fn=process_file_and_notify,
    inputs=[
        "file",
        gr.Textbox(label="Additional Notes", lines=10,value=val),
        gr.Textbox(label="Folder Name",value="test_folders"),
        gr.Textbox(label="github token",value="***********************"),
    ],
    outputs="text",
)