#!/usr/bin/env python3
"""
自動システム作成デモ - 手動プロンプト登録テスト
プロンプト管理システムに新しいプロンプトを登録し、自動作成機能をテストします
"""

import sqlite3
import os
import json
from datetime import datetime

class AutoSystemCreatorDemo:
    """自動システム作成デモクラス"""
    
    def __init__(self):
        self.db_path = "/workspaces/fastapi_django_main_live/prompts.db"
    
    def get_current_prompts(self):
        """現在のプロンプト一覧を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, system_type, execution_status, created_at 
                FROM prompts 
                ORDER BY created_at DESC
            ''')
            prompts = cursor.fetchall()
            conn.close()
            return prompts
        except Exception as e:
            print(f"❌ プロンプト取得エラー: {e}")
            return []
    
    def add_test_prompt(self, title, system_type, content):
        """テスト用プロンプトを追加"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO prompts (title, system_type, content, execution_status) 
                VALUES (?, ?, ?, ?)
            ''', (title, system_type, content, 'pending'))
            
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ プロンプト追加成功: ID {new_id} - {title}")
            return new_id
            
        except Exception as e:
            print(f"❌ プロンプト追加エラー: {e}")
            return None
    
    def show_prompt_list(self):
        """プロンプト一覧を表示"""
        prompts = self.get_current_prompts()
        
        print("\n📋 現在のプロンプト一覧:")
        print("=" * 60)
        
        for prompt in prompts:
            id, title, system_type, status, created_at = prompt
            created_time = created_at[:16] if created_at else 'Unknown'
            
            status_icon = {
                'pending': '⏳',
                'running': '🔄', 
                'completed': '✅',
                'failed': '❌'
            }.get(status, '❓')
            
            print(f"{status_icon} ID:{id:2d} | {title[:30]:30s} | {system_type:15s} | {created_time}")
        
        print("=" * 60)
        print(f"合計: {len(prompts)}個のプロンプト")
    
    def create_sample_prompts(self):
        """サンプルプロンプトを作成"""
        sample_prompts = [
            {
                "title": "🧪 テスト: 簡単な計算機",
                "system_type": "test_system",
                "content": """シンプルな計算機アプリケーションを作成してください。

要件:
- 基本的な四則演算（+, -, *, /）
- Webブラウザで動作するHTML/CSS/JavaScript
- 数字ボタンと演算子ボタン
- 計算結果の表示
- クリアボタン

技術仕様:
- HTML5 + CSS3 + Vanilla JavaScript
- レスポンシブデザイン
- モダンなUIデザイン"""
            },
            {
                "title": "🧪 テスト: ToDoリスト",
                "system_type": "test_system", 
                "content": """ToDoリスト管理システムを作成してください。

機能:
- タスクの追加
- タスクの完了/未完了切り替え
- タスクの削除
- タスクの編集
- ローカルストレージでの保存

技術仕様:
- React.js または Vue.js
- CSS Modules または Styled Components
- TypeScript対応
- 状態管理（useState/Vuex）"""
            },
            {
                "title": "🧪 テスト: 天気情報API",
                "system_type": "api_system",
                "content": """天気情報を取得するAPIシステムを作成してください。

機能:
- 都市名で天気情報を取得
- 現在の天気、気温、湿度を表示
- 3日間の天気予報
- JSON形式でのレスポンス

技術仕様:
- FastAPI フレームワーク
- 外部天気APIとの連携（OpenWeatherMap等）
- Pydanticモデルでの型定義
- 自動生成されるSwagger UI"""
            }
        ]
        
        print("\n🚀 サンプルプロンプトを追加します...")
        
        added_ids = []
        for prompt in sample_prompts:
            prompt_id = self.add_test_prompt(
                prompt["title"],
                prompt["system_type"], 
                prompt["content"]
            )
            if prompt_id:
                added_ids.append(prompt_id)
        
        print(f"\n✅ {len(added_ids)}個のサンプルプロンプトを追加しました")
        return added_ids
    
    def test_prompt_execution_status(self, prompt_id):
        """プロンプトの実行状態をテスト"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # ステータスを'running'に更新
            cursor.execute('''
                UPDATE prompts 
                SET execution_status = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', ('running', prompt_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ プロンプト ID:{prompt_id} の状態を'running'に更新")
            return True
            
        except Exception as e:
            print(f"❌ ステータス更新エラー: {e}")
            return False
    
    def show_system_integration_status(self):
        """システム統合状況を表示"""
        print("\n🎯 システム統合状況:")
        print("=" * 50)
        
        # GitHub API状況
        github_token = os.environ.get('GITHUB_TOKEN', '')
        github_status = '✅ 設定済み' if github_token and len(github_token) > 10 else '❌ 未設定'
        print(f"GitHub API: {github_status}")
        
        # OpenAI API状況  
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        openai_status = '✅ 設定済み' if openai_key and len(openai_key) > 10 else '❌ 未設定'
        print(f"OpenAI API: {openai_status}")
        
        # データベース状況
        db_status = '✅ 接続可能' if os.path.exists(self.db_path) else '❌ 見つからない'
        print(f"プロンプトDB: {db_status}")
        
        # サービス稼働状況
        import subprocess
        try:
            result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
            output = result.stdout
            
            port_7861 = '🟢 稼働中' if ':7861' in output else '🔴 停止中'
            port_7863 = '🟢 稼働中' if ':7863' in output else '🔴 停止中'
            port_8000 = '🟢 稼働中' if ':8000' in output else '🔴 停止中'
            
            print(f"プロンプト管理 (7861): {port_7861}")
            print(f"統合ダッシュボード (7863): {port_7863}")
            print(f"API システム (8000): {port_8000}")
            
        except Exception as e:
            print(f"サービス状況確認エラー: {e}")

def main():
    """メイン実行"""
    print("🧪 自動システム作成デモ - 手動プロンプト登録テスト")
    print("=" * 60)
    
    demo = AutoSystemCreatorDemo()
    
    # 現在の状況表示
    demo.show_system_integration_status()
    demo.show_prompt_list()
    
    # ユーザー選択
    print("\n📝 実行したい操作を選択してください:")
    print("1. サンプルプロンプトを追加")
    print("2. プロンプト一覧のみ表示")
    print("3. 特定プロンプトの状態をテスト")
    print("4. 終了")
    
    choice = input("\n選択 (1-4): ").strip()
    
    if choice == "1":
        added_ids = demo.create_sample_prompts()
        print("\n📋 更新後のプロンプト一覧:")
        demo.show_prompt_list()
        
        if added_ids:
            print(f"\n🎯 追加されたプロンプト:")
            for prompt_id in added_ids:
                print(f"  - プロンプト ID: {prompt_id}")
            
            print("\n💡 次のステップ:")
            print("  1. ブラウザでプロンプト管理システムにアクセス: http://localhost:7861")
            print("  2. 新しく追加されたプロンプトが表示されることを確認")
            print("  3. プロンプトを選択して自動生成を実行")
    
    elif choice == "2":
        print("\n📋 現在のプロンプト一覧を表示しました")
    
    elif choice == "3":
        prompt_id = input("テストするプロンプトのID: ").strip()
        try:
            prompt_id = int(prompt_id)
            demo.test_prompt_execution_status(prompt_id)
        except ValueError:
            print("❌ 無効なID形式です")
    
    elif choice == "4":
        print("👋 デモを終了します")
    
    else:
        print("❌ 無効な選択です")

if __name__ == "__main__":
    main()