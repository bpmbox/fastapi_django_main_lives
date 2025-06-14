"""
Robust process.py module with environment-agnostic path handling
"""
import os
import shutil
import hmac
import hashlib
import base64
import subprocess
import time
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GENERATION_TIMEOUT_SEC = 60

def get_base_path():
    """
    環境に応じて動的にベースパスを取得
    完全に独立した実装
    """
    try:
        # 1. 環境変数から取得
        env_base_path = os.getenv("INTERPRETER_BASE_PATH")
        if env_base_path:
            # パスの正規化と存在確認
            normalized_path = os.path.normpath(env_base_path)
            if not normalized_path.endswith('/'):
                normalized_path += '/'
            
            # 親ディレクトリの存在確認
            parent_dir = os.path.dirname(normalized_path.rstrip('/'))
            if os.path.exists(parent_dir):
                return normalized_path
            
            logger.warning(f"Environment path parent not found: {parent_dir}")
        
        # 2. 現在の作業ディレクトリから推測
        current_dir = os.getcwd()
        logger.info(f"Current directory: {current_dir}")
        
        # 3. 環境タイプの検出と適切なパス設定
        if "/workspaces/" in current_dir:
            # GitHub Codespaces環境
            path = os.path.join(current_dir, "app", "Http", "controller")
            return os.path.normpath(path) + "/"
        
        elif "/home/user/app/" in current_dir or os.path.exists("/home/user/app/"):
            # Docker環境
            return "/home/user/app/app/Http/controller/"
        
        elif "fastapi_django_main_live" in current_dir:
            # ローカル開発環境
            path = os.path.join(current_dir, "app", "Http", "controller")
            return os.path.normpath(path) + "/"
        
        # 4. フォールバック
        fallback_path = os.path.join(current_dir, "temp_controller")
        return os.path.normpath(fallback_path) + "/"
        
    except Exception as e:
        logger.error(f"Error in get_base_path: {e}")
        # 最終フォールバック
        return os.path.join(os.getcwd(), "temp_controller") + "/"

# グローバル変数として初期化（遅延初期化）
_BASE_PATH = None

def get_base_path_safe():
    """
    安全なベースパス取得（遅延初期化）
    """
    global _BASE_PATH
    if _BASE_PATH is None:
        _BASE_PATH = get_base_path()
        logger.info(f"Base path initialized: {_BASE_PATH}")
    return _BASE_PATH

def ensure_base_path_exists():
    """
    ベースパスが存在することを確認し、必要に応じて作成
    """
    base_path = get_base_path_safe()
    
    try:
        os.makedirs(base_path, exist_ok=True)
        
        # 書き込み権限の確認
        test_file = os.path.join(base_path, ".write_test")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        logger.info(f"Base path verified: {base_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create/verify base path {base_path}: {e}")
        
        # フォールバックパスを試行
        fallback_path = os.path.join(os.getcwd(), "temp_controller") + "/"
        try:
            os.makedirs(fallback_path, exist_ok=True)
            
            # グローバル変数を更新
            global _BASE_PATH
            _BASE_PATH = fallback_path
            
            logger.info(f"Using fallback path: {fallback_path}")
            return True
            
        except Exception as fallback_error:
            logger.error(f"Failed to create fallback path: {fallback_error}")
            return False

def set_environment_variables():
    """
    環境変数の設定
    """
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    os.environ["OPENAI_API_KEY"] = os.getenv("api_key", "")
    os.environ["MODEL_NAME"] = "llama3-8b-8192"
    os.environ["LOCAL_MODEL"] = "true"

def create_folder_structure(foldername):
    """
    フォルダ構造の作成（安全版）
    """
    if not ensure_base_path_exists():
        raise Exception("Could not create or access base directory")
    
    base_path = get_base_path_safe()
    target_dir = os.path.join(base_path, foldername)
    
    try:
        os.makedirs(target_dir, exist_ok=True)
        logger.info(f"Created directory: {target_dir}")
        return target_dir
    except Exception as e:
        logger.error(f"Error creating directory {target_dir}: {e}")
        raise

def write_prompt_file(foldername, prompt):
    """
    プロンプトファイルの作成（安全版）
    """
    target_dir = create_folder_structure(foldername)
    prompt_file_path = os.path.join(target_dir, "prompt")
    
    try:
        with open(prompt_file_path, "w", encoding="utf-8") as prompt_file:
            prompt_file.write(prompt)
        logger.info(f"Prompt file created: {prompt_file_path}")
        return prompt_file_path
    except Exception as e:
        logger.error(f"Error writing prompt file: {e}")
        raise

# 使用例とテスト関数
def test_process_system():
    """
    プロセスシステムのテスト
    """
    print("=== Process System Test ===")
    
    try:
        # 1. パス設定のテスト
        base_path = get_base_path_safe()
        print(f"✅ Base path: {base_path}")
        
        # 2. パス作成のテスト
        success = ensure_base_path_exists()
        print(f"✅ Path creation: {success}")
        
        # 3. フォルダ作成のテスト
        test_folder = "test_folder_" + str(int(time.time()))
        folder_path = create_folder_structure(test_folder)
        print(f"✅ Folder creation: {folder_path}")
        
        # 4. ファイル作成のテスト
        test_prompt = "This is a test prompt for the system"
        prompt_file = write_prompt_file(test_folder, test_prompt)
        print(f"✅ File creation: {prompt_file}")
        
        # 5. ファイル読み込みのテスト
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ File content: '{content[:30]}...'")
        
        # 6. クリーンアップ
        shutil.rmtree(folder_path)
        print("✅ Cleanup completed")
        
        print("\n=== Test Summary ===")
        print("✅ All process system functions working correctly")
        print(f"✅ Environment: {get_environment_type()}")
        print(f"✅ Base path: {base_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_environment_type():
    """
    現在の環境タイプを取得
    """
    current_dir = os.getcwd()
    
    if "/workspaces/" in current_dir:
        return "GitHub Codespaces"
    elif "/home/user/app/" in current_dir or os.path.exists("/home/user/app/"):
        return "Docker Container"
    elif "fastapi_django_main_live" in current_dir:
        return "Local Development"
    else:
        return "Unknown/Fallback"

if __name__ == "__main__":
    test_process_system()
