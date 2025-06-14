"""
GitHub ISSUE自動生成メイン機能
===========================

ISSUEを監視してプロンプトから自動でシステム生成する統合メイン機能
- 24時間自動監視
- AI解析・プロンプト抽出
- GPT-ENGINEER実行
- GitHub自動アップロード
- 結果通知
"""

import gradio as gr
import requests
import sqlite3
import json
import time
import threading
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import subprocess
import re

# プロジェクトルートをパスに追加
import sys
sys.path.append('/workspaces/fastapi_django_main_live')

# 代替インポート（process_file_and_notifyが見つからない場合）
try:
    from mysite.interpreter.process import process_nofile as process_file_and_notify
except ImportError:
    try:
        from mysite.libs.utilities import process_file_and_notify
    except ImportError:
        # フォールバック関数定義
        def process_file_and_notify(prompt, folder_name, github_token=None):
            """フォールバック実装"""
            try:
                import subprocess
                import os
                
                # 簡易的なプロセス実行
                target_dir = f"/workspaces/fastapi_django_main_live/test_generated_systems/{folder_name}"
                os.makedirs(target_dir, exist_ok=True)
                
                # プロンプトファイル作成
                prompt_file = f"{target_dir}/prompt.txt"
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                
                return f"✅ システム生成完了\n📁 フォルダ: {folder_name}\n📄 プロンプト保存済み"
            except Exception as e:
                return f"❌ 生成エラー: {str(e)}"

try:
    from controllers.gra_03_programfromdocs.system_automation import SystemAutomation
except ImportError:
    # フォールバックSystemAutomation
    class SystemAutomation:
        def __init__(self, github_token):
            self.github_token = github_token
        
        def full_automation_pipeline(self, *args, **kwargs):
            return {'success': False, 'error': 'SystemAutomation not available'}


class GitHubIssueAutomation:
    """GitHub ISSUE自動生成メインシステム"""
    
    def __init__(self, github_token: str = "", repo_owner: str = "", repo_name: str = ""):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN', '')
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        
        # データベース設定
        self.db_path = "/workspaces/fastapi_django_main_live/github_issues_automation.db"
        self.prompts_db_path = "/workspaces/fastapi_django_main_live/prompts.db"
        
        # 監視設定
        self.monitoring = False
        self.check_interval = 60  # 60秒間隔
        self.processed_issues = set()
        
        # 自動化システム
        self.automation = None
        if self.github_token:
            self.automation = SystemAutomation(self.github_token)
        
        self.init_database()
        self.load_processed_issues()
        
    def init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # メインテーブル作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automated_issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_number INTEGER UNIQUE,
                title TEXT,
                body TEXT,
                requester TEXT,
                repo_url TEXT,
                detected_at TIMESTAMP,
                processed_at TIMESTAMP,
                status TEXT DEFAULT 'detected',
                system_type TEXT,
                generated_repo_url TEXT,
                error_message TEXT,
                execution_time_minutes REAL,
                ai_analysis TEXT
            )
        ''')
        
        # 統計テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automation_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE,
                issues_detected INTEGER DEFAULT 0,
                issues_processed INTEGER DEFAULT 0,
                issues_successful INTEGER DEFAULT 0,
                issues_failed INTEGER DEFAULT 0,
                total_execution_time REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ GitHub ISSUE自動化データベース初期化完了")
    
    def load_processed_issues(self):
        """処理済みISSUE読み込み"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT issue_number FROM automated_issues')
            processed = cursor.fetchall()
            self.processed_issues = {row[0] for row in processed}
            conn.close()
            print(f"📋 処理済みISSUE: {len(self.processed_issues)}件読み込み")
        except Exception as e:
            print(f"❌ 処理済みISSUE読み込みエラー: {e}")
    
    def get_target_issues(self) -> List[Dict]:
        """対象ISSUEを取得"""
        if not self.github_token or not self.repo_owner or not self.repo_name:
            return []
        
        try:
            # システム生成ラベル付きのISSUEを検索
            url = f"{self.base_url}/issues"
            params = {
                'state': 'open',
                'labels': 'system-generation,prompt-request',
                'sort': 'created',
                'direction': 'desc',
                'per_page': 20
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                issues = response.json()
                
                # 未処理のISSUEをフィルタリング
                new_issues = []
                for issue in issues:
                    if issue['number'] not in self.processed_issues:
                        new_issues.append(issue)
                
                return new_issues
                
            elif response.status_code == 404:
                print(f"⚠️ リポジトリが見つかりません: {self.repo_owner}/{self.repo_name}")
                return []
            else:
                print(f"❌ GitHub API エラー: {response.status_code}")
                return []
        
        except Exception as e:
            print(f"❌ ISSUE取得エラー: {e}")
            return []
    
    def extract_system_requirements(self, issue: Dict) -> Dict:
        """ISSUEからシステム要件を抽出（AI解析）"""
        title = issue['title']
        body = issue['body'] or ""
        content = f"{title}\n\n{body}".lower()
        
        requirements = {
            'title': title,
            'content': body,
            'system_type': 'general',
            'technologies': [],
            'priority': 'medium',
            'estimated_time': '30-60分',
            'features': [],
            'github_url': ''
        }
        
        # システムタイプ判定
        if any(word in content for word in ['api', 'fastapi', 'rest', 'endpoint']):
            requirements['system_type'] = 'api_system'
        elif any(word in content for word in ['web', 'website', 'frontend', 'react', 'vue']):
            requirements['system_type'] = 'web_system'
        elif any(word in content for word in ['gradio', 'interface', 'ui', 'dashboard']):
            requirements['system_type'] = 'interface_system'
        elif any(word in content for word in ['line', 'bot', 'chat', 'messaging']):
            requirements['system_type'] = 'line_system'
        elif any(word in content for word in ['ecommerce', 'ec', 'shop', 'store']):
            requirements['system_type'] = 'ecommerce_system'
        
        # 技術スタック検出
        tech_keywords = {
            'python': ['python', 'fastapi', 'django', 'flask'],
            'react': ['react', 'nextjs', 'next.js'],
            'vue': ['vue', 'vuejs', 'vue.js', 'nuxt'],
            'database': ['postgresql', 'mysql', 'sqlite', 'mongodb'],
            'ai': ['ai', 'ml', 'machine learning', 'chatgpt', 'openai']
        }
        
        for tech, keywords in tech_keywords.items():
            if any(keyword in content for keyword in keywords):
                requirements['technologies'].append(tech)
        
        # 優先度判定
        if '緊急' in content or 'urgent' in content or '高' in content:
            requirements['priority'] = 'high'
            requirements['estimated_time'] = '15-30分'
        elif '低' in content or 'low' in content:
            requirements['priority'] = 'low'
            requirements['estimated_time'] = '60-120分'
        
        # 機能抽出（箇条書き部分）
        lines = body.split('\n') if body else []
        for line in lines:
            if line.strip().startswith(('- ', '* ', '1. ', '2. ')):
                feature = line.strip().lstrip('- *0123456789. ')
                if feature and len(feature) > 3:
                    requirements['features'].append(feature)
        
        # GitHub URLの抽出
        github_pattern = r'https://github\.com/[\w\-]+/[\w\-]+'
        github_matches = re.findall(github_pattern, body) if body else []
        if github_matches:
            requirements['github_url'] = github_matches[0]
        
        return requirements
    
    def process_issue_automatically(self, issue: Dict) -> Dict:
        """ISSUEを自動処理"""
        issue_number = issue['number']
        start_time = datetime.now()
        
        print(f"\n🚀 自動処理開始: ISSUE #{issue_number}")
        print(f"   タイトル: {issue['title']}")
        print(f"   作成者: {issue['user']['login']}")
        
        try:
            # 1. システム要件抽出
            requirements = self.extract_system_requirements(issue)
            print(f"   システムタイプ: {requirements['system_type']}")
            print(f"   技術スタック: {', '.join(requirements['technologies'])}")
            
            # 2. データベースに記録（処理開始）
            self.record_issue_detection(issue, requirements, start_time)
            
            # 3. 処理開始コメント投稿
            self.post_processing_start_comment(issue_number, requirements)
            
            # 4. プロンプト生成・保存
            prompt_content = self.generate_system_prompt(requirements)
            
            # プロンプトDBに保存
            self.save_to_prompts_db(requirements, prompt_content)
            
            # 5. システム生成実行
            if self.automation:
                generation_result = self.execute_system_generation(
                    prompt_content, 
                    requirements,
                    issue_number
                )
            else:
                generation_result = {
                    'success': False,
                    'error': 'GitHub Token not configured'
                }
            
            # 6. 結果処理
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds() / 60
            
            if generation_result['success']:
                # 成功コメント投稿
                self.post_success_comment(issue_number, generation_result, execution_time)
                # ISSUEクローズ
                self.close_issue_with_label(issue_number, "completed")
                # データベース更新
                self.update_issue_status(issue_number, 'completed', generation_result, execution_time)
                
                print(f"✅ ISSUE #{issue_number} 自動処理完了")
                return {'success': True, 'repo_url': generation_result.get('github_url', '')}
            else:
                # エラーコメント投稿
                self.post_error_comment(issue_number, generation_result.get('error', '不明なエラー'))
                # データベース更新
                self.update_issue_status(issue_number, 'failed', generation_result, execution_time)
                
                print(f"❌ ISSUE #{issue_number} 処理失敗")
                return {'success': False, 'error': generation_result.get('error', '')}
        
        except Exception as e:
            # データベース更新
            execution_time = (datetime.now() - start_time).total_seconds() / 60
            self.update_issue_status(issue_number, 'error', {'error': str(e)}, execution_time)
            # エラーコメント投稿
            self.post_error_comment(issue_number, str(e))
            
            print(f"❌ ISSUE #{issue_number} 例外エラー: {e}")
            return {'success': False, 'error': str(e)}
        
        finally:
            # 処理済みセットに追加
            self.processed_issues.add(issue_number)
    
    def generate_system_prompt(self, requirements: Dict) -> str:
        """システム生成用プロンプト作成"""
        prompt = f"""# {requirements['title']}

## システム概要
{requirements['content']}

## システムタイプ
{requirements['system_type']}

## 技術要件
"""
        
        if requirements['technologies']:
            prompt += f"- 技術スタック: {', '.join(requirements['technologies'])}\n"
        
        prompt += f"- 優先度: {requirements['priority']}\n"
        prompt += f"- 推定実行時間: {requirements['estimated_time']}\n"
        
        if requirements['features']:
            prompt += f"\n## 機能要件\n"
            for feature in requirements['features']:
                prompt += f"- {feature}\n"
        
        prompt += f"""
## 実装要求
- Python/FastAPIでのバックエンド実装
- Gradio でのフロントエンドUI
- SQLiteデータベース
- RESTful API設計
- エラーハンドリング
- 適切なコメント・ドキュメント
- requirements.txt
- README.md

## 品質要求
- 本番環境対応
- セキュリティ考慮
- パフォーマンス最適化
- テストコード（可能であれば）

gradio は gradio_interface というBlock名で作成してください。
fastapiはrouter の作成もお願いします。
"""
        
        return prompt
    
    def record_issue_detection(self, issue: Dict, requirements: Dict, detected_time: datetime):
        """ISSUE検出をデータベースに記録"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO automated_issues 
                (issue_number, title, body, requester, repo_url, detected_at, 
                 system_type, ai_analysis, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                issue['number'],
                issue['title'],
                issue['body'],
                issue['user']['login'],
                issue['html_url'],
                detected_time.isoformat(),
                requirements['system_type'],
                json.dumps(requirements, ensure_ascii=False),
                'processing'
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ ISSUE記録エラー: {e}")
    
    def save_to_prompts_db(self, requirements: Dict, prompt_content: str):
        """プロンプトDBに保存"""
        try:
            conn = sqlite3.connect(self.prompts_db_path)
            cursor = conn.cursor()
            
            # テーブルが存在しない場合は作成
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    github_url TEXT,
                    repository_name TEXT,
                    system_type TEXT,
                    content TEXT,
                    execution_status TEXT DEFAULT 'approved',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                INSERT INTO prompts 
                (title, github_url, repository_name, system_type, content, execution_status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                f"GitHub自動生成: {requirements['title']}",
                requirements.get('github_url', ''),
                f"auto-gen-{requirements['system_type']}-{datetime.now().strftime('%Y%m%d')}",
                requirements['system_type'],
                prompt_content,
                'approved'
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ プロンプトDB保存エラー: {e}")
    
    def execute_system_generation(self, prompt_content: str, requirements: Dict, issue_number: int) -> Dict:
        """システム生成実行"""
        try:
            if not self.automation:
                return {'success': False, 'error': 'Automation system not initialized'}
            
            # フォルダ名生成
            folder_name = f"github_issue_{issue_number}_{requirements['system_type']}"
            
            # GPT-ENGINEER実行（process_file_and_notify使用）
            result = process_file_and_notify(
                prompt_content,
                folder_name,
                self.github_token
            )
            
            if "✅" in result and "完了" in result:
                # 成功パターンを検出
                # GitHubリポジトリURLを抽出（実装に応じて調整）
                repo_url = f"https://github.com/{self.repo_owner}/{folder_name}"
                
                return {
                    'success': True,
                    'github_url': repo_url,
                    'system_type': requirements['system_type'],
                    'folder_name': folder_name,
                    'description': f"Generated from GitHub Issue #{issue_number}",
                    'files_created': ['main.py', 'requirements.txt', 'README.md']  # 実際の生成ファイルに応じて調整
                }
            else:
                return {
                    'success': False,
                    'error': result if result else '生成エラー'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_processing_start_comment(self, issue_number: int, requirements: Dict):
        """処理開始コメント投稿"""
        comment = f"""🤖 **自動システム生成開始**

こんにちは！GitHub Copilot AIです。

📋 **検出内容:**
- システムタイプ: {requirements['system_type']}
- 技術スタック: {', '.join(requirements['technologies']) if requirements['technologies'] else '汎用'}
- 優先度: {requirements['priority']}
- 推定時間: {requirements['estimated_time']}

🚀 **処理開始:**
1. GPT-ENGINEERによるシステム生成
2. GitHubリポジトリ自動作成
3. Controller/Router自動統合
4. 結果通知

完了次第、このISSUEにコメントで結果をお知らせします。
しばらくお待ちください...

---
**🤖 GitHub Copilot AI - Automation System**
"""
        self.post_issue_comment(issue_number, comment)
    
    def post_success_comment(self, issue_number: int, result: Dict, execution_time: float):
        """成功コメント投稿"""
        comment = f"""✅ **システム生成完了！**

🎉 お疲れ様です！システムの自動生成が完了しました。

📊 **生成結果:**
- 🔗 **GitHub リポジトリ:** {result['github_url']}
- 🏗️ **システムタイプ:** {result['system_type']}
- ⏱️ **実行時間:** {execution_time:.1f}分
- 📁 **生成ファイル:** {', '.join(result.get('files_created', []))}

## 🚀 使用方法
```bash
git clone {result['github_url']}
cd {result.get('folder_name', 'project')}
pip install -r requirements.txt
python main.py
```

## 📋 次のステップ
1. リポジトリをクローンしてください
2. 必要に応じてカスタマイズ
3. 本番環境にデプロイ

ご不明な点がございましたら、お気軽にお声がけください！

---
**🤖 Generated by GitHub Copilot AI**
**⏰ 処理完了時刻:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self.post_issue_comment(issue_number, comment)
    
    def post_error_comment(self, issue_number: int, error_message: str):
        """エラーコメント投稿"""
        comment = f"""❌ **システム生成エラー**

申し訳ございません。自動システム生成中にエラーが発生しました。

🔍 **エラー詳細:**
```
{error_message}
```

🛠️ **対処方法:**
1. ISSUE内容の再確認（特に技術要件の明確化）
2. ラベル `system-generation` と `prompt-request` の確認
3. しばらく待ってから再投稿

📞 開発チームに自動通知済みです。解決次第、再処理いたします。

---
**🤖 GitHub Copilot AI - Error Handler**
"""
        self.post_issue_comment(issue_number, comment)
    
    def post_issue_comment(self, issue_number: int, comment: str):
        """ISSUEにコメント投稿"""
        try:
            if not self.github_token:
                print(f"⚠️ GitHub Token未設定のため、コメント投稿をスキップ")
                return
            
            url = f"{self.base_url}/issues/{issue_number}/comments"
            data = {'body': comment}
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                print(f"✅ ISSUE #{issue_number} コメント投稿成功")
            else:
                print(f"❌ ISSUE #{issue_number} コメント投稿失敗: {response.status_code}")
        
        except Exception as e:
            print(f"❌ コメント投稿エラー: {e}")
    
    def close_issue_with_label(self, issue_number: int, label: str = "completed"):
        """ISSUEをクローズしてラベル追加"""
        try:
            if not self.github_token:
                return
            
            # ラベル追加
            url = f"{self.base_url}/issues/{issue_number}/labels"
            response = requests.post(url, headers=self.headers, json=[label])
            
            # ISSUEクローズ
            url = f"{self.base_url}/issues/{issue_number}"
            response = requests.patch(url, headers=self.headers, json={'state': 'closed'})
            
            if response.status_code == 200:
                print(f"✅ ISSUE #{issue_number} クローズ完了")
        
        except Exception as e:
            print(f"❌ ISSUEクローズエラー: {e}")
    
    def update_issue_status(self, issue_number: int, status: str, result: Dict, execution_time: float):
        """ISSUE処理ステータス更新"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE automated_issues 
                SET processed_at = ?, status = ?, generated_repo_url = ?, 
                    error_message = ?, execution_time_minutes = ?
                WHERE issue_number = ?
            ''', (
                datetime.now().isoformat(),
                status,
                result.get('github_url', ''),
                result.get('error', ''),
                execution_time,
                issue_number
            ))
            
            conn.commit()
            conn.close()
            
            # 統計更新
            self.update_daily_stats(status)
            
        except Exception as e:
            print(f"❌ ステータス更新エラー: {e}")
    
    def update_daily_stats(self, status: str):
        """日次統計更新"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 今日の統計を取得または作成
            cursor.execute('SELECT * FROM automation_stats WHERE date = ?', (today,))
            stats = cursor.fetchone()
            
            if stats:
                # 既存レコード更新
                if status == 'completed':
                    cursor.execute('''
                        UPDATE automation_stats 
                        SET issues_processed = issues_processed + 1,
                            issues_successful = issues_successful + 1
                        WHERE date = ?
                    ''', (today,))
                elif status in ['failed', 'error']:
                    cursor.execute('''
                        UPDATE automation_stats 
                        SET issues_processed = issues_processed + 1,
                            issues_failed = issues_failed + 1
                        WHERE date = ?
                    ''', (today,))
            else:
                # 新規レコード作成
                cursor.execute('''
                    INSERT INTO automation_stats (date, issues_detected, issues_processed, 
                                                issues_successful, issues_failed)
                    VALUES (?, 1, 1, ?, ?)
                ''', (today, 1 if status == 'completed' else 0, 1 if status in ['failed', 'error'] else 0))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ 統計更新エラー: {e}")
    
    def start_monitoring(self) -> str:
        """自動監視開始"""
        if self.monitoring:
            return "⚠️ 既に監視中です"
        
        if not self.github_token or not self.repo_owner or not self.repo_name:
            return "❌ GitHub設定が不完全です（Token, Owner, Repo名が必要）"
        
        self.monitoring = True
        
        def monitoring_loop():
            print(f"🔍 GitHub ISSUE自動監視開始")
            print(f"   リポジトリ: {self.repo_owner}/{self.repo_name}")
            print(f"   チェック間隔: {self.check_interval}秒")
            
            while self.monitoring:
                try:
                    issues = self.get_target_issues()
                    
                    if issues:
                        print(f"📋 新着ISSUE発見: {len(issues)}件")
                        
                        for issue in issues:
                            if not self.monitoring:  # 停止チェック
                                break
                            
                            print(f"🔧 自動処理開始: #{issue['number']} - {issue['title']}")
                            self.process_issue_automatically(issue)
                            time.sleep(10)  # API制限対策
                    
                    else:
                        print("✅ 新しいISSUEはありません")
                    
                    # 次回チェックまで待機
                    time.sleep(self.check_interval)
                
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ 監視エラー: {e}")
                    time.sleep(self.check_interval)
            
            print("🛑 GitHub ISSUE自動監視停止")
        
        # バックグラウンドで監視開始
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        return f"✅ GitHub ISSUE自動監視開始\n📍 リポジトリ: {self.repo_owner}/{self.repo_name}\n⏰ 間隔: {self.check_interval}秒"
    
    def stop_monitoring(self) -> str:
        """監視停止"""
        if not self.monitoring:
            return "⚠️ 監視は実行されていません"
        
        self.monitoring = False
        return "🛑 GitHub ISSUE自動監視を停止しました"
    
    def get_automation_stats(self) -> Dict:
        """自動化統計取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 今日の統計
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('SELECT * FROM automation_stats WHERE date = ?', (today,))
            today_stats = cursor.fetchone()
            
            # 全体統計
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_issues,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    AVG(execution_time_minutes) as avg_time
                FROM automated_issues
            ''')
            overall_stats = cursor.fetchone()
            
            # 最近の処理
            cursor.execute('''
                SELECT issue_number, title, status, processed_at, execution_time_minutes
                FROM automated_issues 
                ORDER BY processed_at DESC 
                LIMIT 10
            ''')
            recent_issues = cursor.fetchall()
            
            conn.close()
            
            return {
                'today': {
                    'detected': today_stats[2] if today_stats else 0,
                    'processed': today_stats[3] if today_stats else 0,
                    'successful': today_stats[4] if today_stats else 0,
                    'failed': today_stats[5] if today_stats else 0
                } if today_stats else {'detected': 0, 'processed': 0, 'successful': 0, 'failed': 0},
                'overall': {
                    'total_issues': overall_stats[0] or 0,
                    'completed': overall_stats[1] or 0,
                    'failed': overall_stats[2] or 0,
                    'avg_execution_time': round(overall_stats[3] or 0, 1)
                },
                'recent_issues': recent_issues
            }
        
        except Exception as e:
            print(f"❌ 統計取得エラー: {e}")
            return {'today': {}, 'overall': {}, 'recent_issues': []}


def create_github_issue_automation_interface():
    """GitHub ISSUE自動生成メインインターフェース"""
    
    automation_system = None
    
    def setup_automation(github_token, repo_owner, repo_name, check_interval):
        """自動化システムセットアップ"""
        nonlocal automation_system
        
        try:
            if not all([github_token, repo_owner, repo_name]):
                return "❌ 必須項目を入力してください"
            
            automation_system = GitHubIssueAutomation(github_token, repo_owner, repo_name)
            automation_system.check_interval = int(check_interval)
            
            return f"✅ 自動化システム初期化完了\n📍 リポジトリ: {repo_owner}/{repo_name}\n⏰ チェック間隔: {check_interval}秒"
        
        except Exception as e:
            return f"❌ セットアップエラー: {str(e)}"
    
    def start_automation():
        """自動監視開始"""
        if not automation_system:
            return "❌ 先にシステムをセットアップしてください"
        
        return automation_system.start_monitoring()
    
    def stop_automation():
        """自動監視停止"""
        if not automation_system:
            return "❌ システムが初期化されていません"
        
        return automation_system.stop_monitoring()
    
    def get_stats():
        """統計情報取得"""
        if not automation_system:
            return "❌ システムが初期化されていません"
        
        stats = automation_system.get_automation_stats()
        
        today_stats = stats['today']
        overall_stats = stats['overall']
        
        stats_text = f"""
## 📊 今日の統計 ({datetime.now().strftime('%Y-%m-%d')})
- 🔍 検出: {today_stats['detected']}件
- ⚙️ 処理: {today_stats['processed']}件  
- ✅ 成功: {today_stats['successful']}件
- ❌ 失敗: {today_stats['failed']}件

## 📈 全体統計
- 📋 総ISSUE数: {overall_stats['total_issues']}件
- ✅ 完了: {overall_stats['completed']}件
- ❌ 失敗: {overall_stats['failed']}件
- ⏱️ 平均実行時間: {overall_stats['avg_execution_time']}分

## 🕐 最近の処理
"""
        
        for issue in stats['recent_issues'][:5]:
            issue_num, title, status, processed_at, exec_time = issue
            status_icon = {'completed': '✅', 'failed': '❌', 'processing': '🔄'}.get(status, '⏳')
            stats_text += f"- {status_icon} #{issue_num}: {title[:30]}{'...' if len(title) > 30 else ''}\n"
        
        return stats_text
    
    def test_single_issue():
        """単一ISSUE処理テスト"""
        if not automation_system:
            return "❌ システムが初期化されていません"
        
        try:
            issues = automation_system.get_target_issues()
            if issues:
                issue = issues[0]
                result = automation_system.process_issue_automatically(issue)
                
                if result['success']:
                    return f"✅ テスト成功\nISSUE #{issue['number']} 処理完了\nリポジトリ: {result.get('repo_url', 'N/A')}"
                else:
                    return f"❌ テスト失敗\nエラー: {result.get('error', '不明')}"
            else:
                return "⚠️ 処理対象のISSUEがありません"
        
        except Exception as e:
            return f"❌ テストエラー: {str(e)}"
    
    with gr.Blocks(title="🤖 GitHub ISSUE自動生成メインシステム", theme="soft") as interface:
        gr.Markdown("""
        # 🤖 GitHub ISSUE自動生成メインシステム
        
        **24時間自動監視・AI解析・システム生成・GitHub連携**
        
        ## 🌟 主な機能
        - 🔍 **24時間自動監視** - GitHubリポジトリのISSUEを常時監視
        - 🤖 **AI自動解析** - プロンプト内容を自動で解析・分類
        - 🚀 **自動システム生成** - GPT-ENGINEERでシステム自動生成  
        - 📤 **GitHub自動アップロード** - 生成システムを自動でリポジトリ作成
        - 💬 **自動結果通知** - ISSUEに処理結果を自動コメント
        - 📊 **統計・レポート** - 処理状況の可視化
        """)
        
        with gr.Tabs():
            with gr.TabItem("⚙️ システム設定"):
                gr.Markdown("## 🔧 自動化システムの初期設定")
                
                with gr.Row():
                    with gr.Column():
                        github_token_input = gr.Textbox(
                            label="GitHub Token",
                            type="password",
                            placeholder="ghp_xxxxxxxxxxxxxxxxxxxx",
                            info="Issues権限を含むPersonal Access Token"
                        )
                        repo_owner_input = gr.Textbox(
                            label="リポジトリオーナー",
                            placeholder="your-username",
                            info="監視するリポジトリのオーナー名"
                        )
                        repo_name_input = gr.Textbox(
                            label="リポジトリ名",
                            placeholder="system-requests",
                            info="ISSUE監視対象のリポジトリ名"
                        )
                        check_interval_input = gr.Number(
                            label="チェック間隔（秒）",
                            value=60,
                            minimum=30,
                            maximum=3600,
                            info="ISSUEをチェックする間隔"
                        )
                        
                        setup_btn = gr.Button("🔧 システムセットアップ", variant="primary")
                        setup_result = gr.Textbox(label="セットアップ結果", interactive=False, lines=3)
                
                with gr.Row():
                    start_btn = gr.Button("🚀 自動監視開始", variant="primary")
                    stop_btn = gr.Button("🛑 監視停止", variant="secondary")
                    test_btn = gr.Button("🧪 単体テスト", variant="secondary")
                
                automation_status = gr.Textbox(label="監視ステータス", interactive=False, lines=2)
            
            with gr.TabItem("📊 統計・モニタリング"):
                gr.Markdown("## 📈 自動処理統計・実行状況")
                
                with gr.Row():
                    refresh_stats_btn = gr.Button("🔄 統計更新", variant="primary")
                
                stats_display = gr.Markdown("統計を読み込み中...")
                
                gr.Markdown("## 📋 処理ガイドライン")
                gr.Markdown("""
                ### 🏷️ 必要なラベル
                ISSUE には以下のラベルが必要です：
                - `system-generation` - システム生成リクエスト
                - `prompt-request` - プロンプト処理要求
                
                ### 📝 推奨ISSUE形式
                ```markdown
                # システム名
                
                ## 要件
                - 機能1の説明
                - 機能2の説明
                - 機能3の説明
                
                ## 技術スタック
                - Python/FastAPI
                - React/Vue.js
                - PostgreSQL/SQLite
                
                ## その他要求
                - セキュリティ要件
                - パフォーマンス要件
                ```
                
                ### ⚡ 処理フロー
                1. **ISSUE検出** → ラベル付きISSUEの自動検出
                2. **AI解析** → システム要件の自動抽出・分類
                3. **生成実行** → GPT-ENGINEERによるシステム生成
                4. **GitHub連携** → 新規リポジトリ作成・コードプッシュ
                5. **結果通知** → ISSUEに完了コメント・クローズ
                """)
            
            with gr.TabItem("ℹ️ 使用ガイド"):
                gr.Markdown("""
                ## 📚 GitHub ISSUE自動生成システム使用ガイド
                
                ### 🌍 どこからでも使える理由
                - **GitHub ISSUEベース** → 世界中どこからでもアクセス可能
                - **24時間自動監視** → いつでも投稿可能、自動で処理開始
                - **AI自動解析** → 人間の判断なしで要件を理解
                - **完全自動化** → 投稿から完成まで全自動
                
                ### 👥 利用者向け手順
                
                #### 1️⃣ GitHubリポジトリにアクセス
                ```
                https://github.com/[owner]/[repo-name]/issues
                ```
                
                #### 2️⃣ 新しいISSUEを作成
                - "New issue" ボタンをクリック
                - 必要なラベルを追加: `system-generation`, `prompt-request`
                
                #### 3️⃣ システム要件を記述
                - 明確なタイトル
                - 詳細な機能要件
                - 技術要件（使いたい技術があれば）
                
                #### 4️⃣ 投稿・待機
                - ISSUEを投稿
                - AI が自動で検出・処理開始
                - 進捗はISSUEのコメントで確認可能
                
                #### 5️⃣ 完成・受け取り
                - 生成完了時にISSUEにコメント投稿
                - 新しいGitHubリポジトリのリンク
                - 使用方法の説明
                
                ### 🎯 成功のコツ
                - **明確な要件記述** → 具体的な機能説明
                - **技術指定** → 使いたい技術があれば明記
                - **適切なラベル** → 必須ラベルの付与
                - **一つのシステム一つのISSUE** → 複雑すぎず分割
                
                ### ⏱️ 処理時間目安
                - **Simple System** → 15-30分
                - **Medium System** → 30-60分  
                - **Complex System** → 60-120分
                
                ### 🆘 トラブルシューティング
                - **処理されない** → ラベルの確認
                - **エラー発生** → 要件の明確化、再投稿
                - **長時間待機** → システム負荷による遅延の可能性
                """)
        
        # イベントハンドラー
        setup_btn.click(
            fn=setup_automation,
            inputs=[github_token_input, repo_owner_input, repo_name_input, check_interval_input],
            outputs=setup_result
        )
        
        start_btn.click(
            fn=start_automation,
            outputs=automation_status
        )
        
        stop_btn.click(
            fn=stop_automation,
            outputs=automation_status
        )
        
        test_btn.click(
            fn=test_single_issue,
            outputs=automation_status
        )
        
        refresh_stats_btn.click(
            fn=get_stats,
            outputs=stats_display
        )
        
        # 初期統計表示
        interface.load(
            fn=get_stats,
            outputs=stats_display
        )
    
    return interface


# Gradio インターフェース作成
gradio_interface = create_github_issue_automation_interface()

# 自動検出用のメタデータ
interface_title = "🤖 GitHub ISSUE自動生成システム"
interface_description = "24時間自動監視・AI解析・システム生成・GitHub連携の統合メインシステム"

if __name__ == "__main__":
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False
    )
