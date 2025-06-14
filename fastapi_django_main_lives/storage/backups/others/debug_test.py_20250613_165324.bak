"""
デバッグテスト用のサンプルファイル
ブレークポイントを設定してデバッグを試すことができます
"""

import os
import sys
from dotenv import load_dotenv

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 環境変数を読み込み
load_dotenv()

def test_debug_function():
    """
    デバッグテスト用関数
    この関数にブレークポイントを設定してデバッグを試してください
    """
    print("🐛 デバッグテストを開始します")
    
    # ここにブレークポイントを設定してください
    api_key = os.getenv("GROQ_API_KEY")
    print(f"API Key loaded: {bool(api_key)}")
    
    # 変数の値を確認できます
    test_data = {
        "message": "Hello, Debug!",
        "number": 42,
        "list": [1, 2, 3, 4, 5]
    }
    
    # ここにもブレークポイントを設定してtest_dataの中身を確認できます
    for key, value in test_data.items():
        print(f"{key}: {value}")
    
    print("🎉 デバッグテスト完了")
    return test_data

def test_api_connection():
    """
    API接続テスト用関数
    """
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ API key not found")
        return False
    
    try:
        # ここにブレークポイントを設定してGroqクライアントの初期化を確認
        client = Groq(api_key=api_key)
        print("✅ Groq client created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating Groq client: {e}")
        return False

def test_chat_with_interpreter():
    """
    chat_with_interpreter関数のデバッグテスト
    """
    print("🔧 chat_with_interpreter のテストを開始")
    
    try:
        # chat_with_interpreter関数をインポート
        from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter
        
        # ここにブレークポイントを設定
        test_message = "Hello, what is 2+2?"
        test_password = "12345"
        
        print(f"テストメッセージ: {test_message}")
        print(f"パスワード: {test_password}")
        
        # ここにブレークポイントを設定してchat_with_interpreter関数の呼び出しを確認
        response_generator = chat_with_interpreter(
            message=test_message,
            history=None,
            passw=test_password,
            temperature=0.7,
            max_new_tokens=512
        )
        
        # レスポンスを収集
        responses = []
        for response in response_generator:
            responses.append(response)
            print(f"Response chunk: {response}")
            # ここにもブレークポイントを設定してレスポンスを確認
        
        print(f"Total responses: {len(responses)}")
        return responses
        
    except Exception as e:
        print(f"❌ Error testing chat_with_interpreter: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=== デバッグテスト開始 ===")
    
    # ここにブレークポイントを設定してステップ実行してみてください
    result = test_debug_function()
    
    # API接続テスト
    api_success = test_api_connection()
    
    # chat_with_interpreter テスト
    chat_responses = test_chat_with_interpreter()
    
    print("=== デバッグテスト終了 ===")
    print(f"結果: {result}")
    print(f"API接続: {'成功' if api_success else '失敗'}")
    print(f"チャット応答数: {len(chat_responses) if chat_responses else 0}")
