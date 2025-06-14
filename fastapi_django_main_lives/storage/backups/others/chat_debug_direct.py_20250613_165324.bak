#!/usr/bin/env python3
"""
chat_with_interpreter関数を直接デバッグするスクリプト
VS Codeでブレークポイントを設定して、関数の動作を詳細に調べる
"""

import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 環境変数を読み込み
from dotenv import load_dotenv
load_dotenv()

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

def main():
    """メイン関数 - ここにブレークポイントを設定"""
    print("🐛 Chat interpreter debug session starting...")
    
    # ここにブレークポイントを設定 (行 29)
    print(f"🔧 API Key exists: {bool(os.getenv('GROQ_API_KEY'))}")
    
    try:
        # chat_with_interpreter関数をインポート
        from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter
        print("✅ chat_with_interpreter function imported successfully")
        
        # ここにブレークポイントを設定してテストメッセージを準備 (行 36)
        test_message = "Hello, what is 2+2?"
        test_password = "12345"
        
        print(f"🚀 Testing with message: '{test_message}'")
        print(f"🔑 Using password: '{test_password}'")
        
        # ここにブレークポイントを設定してchat_with_interpreter関数を呼び出し (行 43)
        print("🔧 Calling chat_with_interpreter function...")
        
        # レスポンスジェネレータを取得
        response_generator = chat_with_interpreter(
            message=test_message,
            history=None,
            passw=test_password,
            temperature=0.7,
            max_new_tokens=512
        )
        
        # ここにブレークポイントを設定してレスポンスを処理 (行 54)
        print("📡 Processing responses...")
        response_count = 0
        
        for response in response_generator:
            response_count += 1
            # ここにブレークポイントを設定して各レスポンスをチェック (行 59)
            print(f"📨 Response {response_count}: {response[:100]}...")
            
            # 長いレスポンスの場合は最初の部分のみ表示
            if len(response) > 200:
                print(f"📝 Full response length: {len(response)} characters")
                break
        
        print(f"✅ Debug session completed. Total responses: {response_count}")
        
    except Exception as e:
        # ここにブレークポイントを設定してエラーを詳細に調査 (行 69)
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        
        # エラーの詳細情報
        print(f"📊 Error type: {type(e).__name__}")
        print(f"📋 Error args: {e.args}")

if __name__ == "__main__":
    main()
