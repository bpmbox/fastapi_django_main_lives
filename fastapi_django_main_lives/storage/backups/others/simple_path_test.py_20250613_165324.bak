import os

# 現在のディレクトリと環境を確認
print("=== Environment Check ===")
print(f"Current working directory: {os.getcwd()}")
print(f"INTERPRETER_BASE_PATH: {os.getenv('INTERPRETER_BASE_PATH', 'Not set')}")

# get_base_path関数のテスト
def get_base_path():
    """
    環境に応じて動的にベースパスを取得
    """
    try:
        # 環境変数から取得を試行
        env_base_path = os.getenv("INTERPRETER_BASE_PATH")
        if env_base_path and os.path.exists(os.path.dirname(env_base_path)):
            return env_base_path
        
        # 現在の作業ディレクトリから推測
        current_dir = os.getcwd()
        
        # Codespaces環境の検出
        if "/workspaces/" in current_dir:
            path = os.path.join(current_dir, "app", "Http", "controller")
            return path + "/"
        
        # Docker環境の検出
        if "/home/user/app/" in current_dir or os.path.exists("/home/user/app/"):
            return "/home/user/app/app/Http/controller/"
        
        # ローカル開発環境
        if "fastapi_django_main_live" in current_dir:
            path = os.path.join(current_dir, "app", "Http", "controller")
            return path + "/"
        
        # フォールバック: カレントディレクトリ下にcontrollerディレクトリを作成
        fallback_path = os.path.join(current_dir, "temp_controller")
        return fallback_path + "/"
        
    except Exception as e:
        print(f"Error in get_base_path: {str(e)}")
        # 絶対フォールバック
        return os.path.join(os.getcwd(), "temp_controller") + "/"

# テスト実行
base_path = get_base_path()
print(f"\nDetected base path: {base_path}")

# パスの作成テスト
try:
    os.makedirs(base_path, exist_ok=True)
    print(f"✅ Path created successfully: {base_path}")
    print(f"Path exists: {os.path.exists(base_path)}")
    
    # 書き込みテスト
    test_file = os.path.join(base_path, "test.txt")
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print("✅ Path is writable")
    
except Exception as e:
    print(f"❌ Error with path: {e}")

print("\n=== Test completed ===")
