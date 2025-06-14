#!/usr/bin/env python3
"""
環境変数設定管理モジュール
.envファイルから環境変数を読み込み、アプリケーション全体で利用
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
import json

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

def load_env_file():
    """
    .envファイルから環境変数を読み込み
    """
    if not ENV_FILE.exists():
        print(f"⚠️ .envファイルが見つかりません: {ENV_FILE}")
        return
    
    try:
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # コメント行や空行をスキップ
                if not line or line.startswith('#'):
                    continue
                
                # 環境変数の解析
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 既存の環境変数を上書きしない
                    if key not in os.environ:
                        os.environ[key] = value
                        
        print(f"✅ .envファイルを読み込みました: {ENV_FILE}")
        
    except Exception as e:
        print(f"❌ .envファイル読み込みエラー: {e}")

def get_env(key: str, default: Any = None) -> Optional[str]:
    """
    環境変数を取得（デフォルト値付き）
    """
    return os.getenv(key, default)

def get_env_bool(key: str, default: bool = False) -> bool:
    """
    環境変数をbooleanとして取得
    """
    value = get_env(key, '').lower()
    return value in ('true', '1', 'yes', 'on')

def get_env_int(key: str, default: int = 0) -> int:
    """
    環境変数をintegerとして取得
    """
    try:
        return int(get_env(key, str(default)))
    except (ValueError, TypeError):
        return default

def get_env_json(key: str, default: Dict = None) -> Dict:
    """
    環境変数をJSONとして取得
    """
    if default is None:
        default = {}
    
    try:
        value = get_env(key)
        if value:
            return json.loads(value)
        return default
    except (json.JSONDecodeError, TypeError):
        return default

# 設定クラス
class Settings:
    """アプリケーション設定"""
    
    def __init__(self):
        load_env_file()
        
    # API設定
    @property
    def api_key(self) -> str:
        return get_env('api_key', '')
    
    @property
    def token(self) -> str:
        return get_env('token', '')
    
    @property
    def hf_token(self) -> str:
        return get_env('hf_token', '')
    
    @property
    def openinterpreter_secret(self) -> str:
        return get_env('openinterpreter_secret', '')
    
    # データベース設定
    @property
    def postgre_user(self) -> str:
        return get_env('postgre_user', '')
    
    @property
    def postgre_pass(self) -> str:
        return get_env('postgre_pass', '')
    
    @property
    def postgre_host(self) -> str:
        return get_env('postgre_host', '')
    
    @property
    def postgre_url(self) -> str:
        return get_env('postgre_url', '')
    
    # GitHub設定
    @property
    def github_token(self) -> str:
        return get_env('github_token', '')
    
    @property
    def github_user(self) -> str:
        return get_env('github_user', '')
    
    # LINE Bot設定
    @property
    def channel_access_token(self) -> str:
        return get_env('ChannelAccessToken', '')
    
    @property
    def channel_secret(self) -> str:
        return get_env('ChannelSecret', '')
    
    @property
    def channel_id(self) -> str:
        return get_env('ChannelID', '')
    
    # AppSheet設定
    @property
    def appsheet_app_id(self) -> str:
        return get_env('APPSHEET_APPID', '')
    
    @property
    def appsheet_key(self) -> str:
        return get_env('APPSHEET_KEY', '')
    
    # Webhook設定
    @property
    def webhook_gas(self) -> str:
        return get_env('WEBHOOK_GAS', '')
    
    @property
    def webhook_url(self) -> str:
        return get_env('WEBHOOK_URL', '')
    
    @property
    def chat_url(self) -> str:
        return get_env('chat_url', '')
    
    @property
    def n8n_hook(self) -> str:
        return get_env('n8nhook', '')
    
    # Google Cloud設定
    @property
    def google_credentials(self) -> Dict:
        return get_env_json('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
    
    # Gradio設定
    @property
    def gradio_theme(self) -> str:
        return get_env('GRADIO_THEME', 'huggingface')
    
    @property
    def gradio_server_name(self) -> str:
        return get_env('GRADIO_SERVER_NAME', '0.0.0.0')
    
    @property
    def gradio_cache_examples(self) -> bool:
        return get_env_bool('GRADIO_CACHE_EXAMPLES', True)
    
    # システム設定
    @property
    def accelerator(self) -> str:
        return get_env('ACCELERATOR', 'cpu')
    
    @property
    def cpu_cores(self) -> int:
        return get_env_int('CPU_CORES', 2)
    
    @property
    def memory(self) -> str:
        return get_env('MEMORY', '16Gi')
    
    @property
    def timezone(self) -> str:
        return get_env('TZ', 'Europe/Paris')
    
    def validate(self) -> bool:
        """
        重要な設定が存在するかチェック
        """
        required_keys = [
            'api_key',
            'postgre_url',
            'openinterpreter_secret'
        ]
        
        missing_keys = []
        for key in required_keys:
            if not getattr(self, key.lower()):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ 必須環境変数が設定されていません: {missing_keys}")
            return False
        
        print("✅ 環境変数の検証が完了しました")
        return True
    
    def print_summary(self):
        """設定の概要を表示"""
        print("🔧 アプリケーション設定:")
        print(f"  🔑 API Key: {'設定済み' if self.api_key else '未設定'}")
        print(f"  🗄️ PostgreSQL: {'設定済み' if self.postgre_url else '未設定'}")
        print(f"  🤖 OpenInterpreter: {'設定済み' if self.openinterpreter_secret else '未設定'}")
        print(f"  🐙 GitHub: {'設定済み' if self.github_token else '未設定'}")
        print(f"  📱 LINE Bot: {'設定済み' if self.channel_access_token else '未設定'}")
        print(f"  📊 AppSheet: {'設定済み' if self.appsheet_app_id else '未設定'}")
        print(f"  ☁️ Google Cloud: {'設定済み' if self.google_credentials else '未設定'}")
        print(f"  🎨 Gradio Theme: {self.gradio_theme}")
        print(f"  ⚡ Accelerator: {self.accelerator}")
        print(f"  💾 CPU Cores: {self.cpu_cores}")
        print(f"  🧠 Memory: {self.memory}")

# グローバル設定インスタンス
settings = Settings()

if __name__ == "__main__":
    print("🚀 環境設定テスト実行...")
    settings.print_summary()
    settings.validate()
