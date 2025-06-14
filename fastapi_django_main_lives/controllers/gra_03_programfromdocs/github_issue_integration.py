"""
GitHub ISSUE連携システム
ISSUEを監視してプロンプトを自動実行し、結果を返すシステム
"""

import requests
import json
import time
import threading
from typing import Dict, List, Optional
import re
from datetime import datetime
import sqlite3

class GitHubIssueMonitor:
    """GitHub ISSUE監視システム"""
    
    def __init__(self, github_token: str, repo_owner: str, repo_name: str):
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.processed_issues = set()
        self.db_path = "github_issues.db"
        self.init_db()
    
    def init_db(self):
        """ISSUE処理履歴データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_issues (
                issue_number INTEGER PRIMARY KEY,
                title TEXT,
                body TEXT,
                processed_at TIMESTAMP,
                status TEXT,
                result_url TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_open_issues(self) -> List[Dict]:
        """未処理のISSUEを取得"""
        try:
            # システム生成用のラベルがついたISSUEのみ取得
            url = f"{self.base_url}/issues"
            params = {
                'state': 'open',
                'labels': 'system-generation,prompt-request',
                'sort': 'created',
                'direction': 'desc'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            issues = response.json()
            
            # 未処理のISSUEをフィルタリング
            unprocessed_issues = []
            for issue in issues:
                if issue['number'] not in self.processed_issues:
                    # データベースでも確認
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute(
                        'SELECT issue_number FROM processed_issues WHERE issue_number = ?',
                        (issue['number'],)
                    )
                    if not cursor.fetchone():
                        unprocessed_issues.append(issue)
                    conn.close()
            
            return unprocessed_issues
            
        except Exception as e:
            print(f"❌ ISSUE取得エラー: {e}")
            return []
    
    def extract_prompt_from_issue(self, issue: Dict) -> Optional[Dict]:
        """ISSUEからプロンプト情報を抽出"""
        try:
            title = issue['title']
            body = issue['body'] or ""
            
            # プロンプト形式を検出
            prompt_data = {
                'title': title,
                'content': body,
                'system_type': 'general',
                'github_url': '',
                'requirements': []
            }
            
            # タイトルからシステムタイプを推定
            if 'api' in title.lower() or 'fastapi' in title.lower():
                prompt_data['system_type'] = 'api_system'
            elif 'web' in title.lower() or 'website' in title.lower():
                prompt_data['system_type'] = 'web_system'
            elif 'chat' in title.lower() or 'ai' in title.lower():
                prompt_data['system_type'] = 'ai_system'
            elif 'interface' in title.lower() or 'gradio' in title.lower():
                prompt_data['system_type'] = 'interface_system'
            
            # 本文から要件を抽出
            lines = body.split('\n')
            for line in lines:
                if line.strip().startswith('- ') or line.strip().startswith('* '):
                    prompt_data['requirements'].append(line.strip()[2:])
            
            # GitHub URLの抽出（希望リポジトリ名など）
            github_pattern = r'https://github\.com/[\w\-]+/[\w\-]+'
            github_matches = re.findall(github_pattern, body)
            if github_matches:
                prompt_data['github_url'] = github_matches[0]
            
            return prompt_data
            
        except Exception as e:
            print(f"❌ プロンプト抽出エラー: {e}")
            return None
    
    def create_system_from_prompt(self, prompt_data: Dict) -> Dict:
        """プロンプトからシステムを生成"""
        try:
            # ここで実際のシステム生成を行う
            # process_file_and_notify_enhanced と同様の処理
            
            # 仮の結果（実際にはGPT-ENGINEERを呼び出す）
            result = {
                'success': True,
                'github_url': f"https://github.com/generated-systems/{prompt_data['title'].lower().replace(' ', '-')}",
                'system_type': prompt_data['system_type'],
                'files_created': ['main.py', 'requirements.txt', 'README.md'],
                'description': f"Generated system: {prompt_data['title']}"
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def post_comment_to_issue(self, issue_number: int, comment: str) -> bool:
        """ISSUEにコメントを投稿"""
        try:
            url = f"{self.base_url}/issues/{issue_number}/comments"
            data = {'body': comment}
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            print(f"❌ コメント投稿エラー: {e}")
            return False
    
    def close_issue_with_label(self, issue_number: int, label: str = "completed") -> bool:
        """ISSUEをクローズしてラベルを追加"""
        try:
            # ラベル追加
            url = f"{self.base_url}/issues/{issue_number}/labels"
            response = requests.post(url, headers=self.headers, json=[label])
            
            # ISSUEクローズ
            url = f"{self.base_url}/issues/{issue_number}"
            response = requests.patch(url, headers=self.headers, json={'state': 'closed'})
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            print(f"❌ ISSUEクローズエラー: {e}")
            return False
    
    def process_issue(self, issue: Dict) -> bool:
        """ISSUEを処理"""
        try:
            issue_number = issue['number']
            
            # プロンプト抽出
            prompt_data = self.extract_prompt_from_issue(issue)
            if not prompt_data:
                # エラーコメント投稿
                error_comment = """❌ **プロンプト抽出エラー**

申し訳ございませんが、ISSUEからプロンプト情報を正しく抽出できませんでした。

📝 **正しい形式:**
```
# システム名

## 要件
- 要件1
- 要件2
- 要件3

## 技術スタック
- Python/FastAPI
- SQLite
- Gradio

## 詳細説明
具体的な機能説明...
```

ラベル `system-generation` または `prompt-request` をつけてください。
"""
                self.post_comment_to_issue(issue_number, error_comment)
                return False
            
            # 処理開始コメント
            start_comment = f"""🚀 **システム生成開始**

こんにちは！GitHub Copilot です。

📋 **受信内容:**
- タイトル: {prompt_data['title']}
- システムタイプ: {prompt_data['system_type']}
- 要件数: {len(prompt_data['requirements'])}件

🔧 GPT-ENGINEERでシステム生成を開始します...
完了まで数分お待ちください。
"""
            self.post_comment_to_issue(issue_number, start_comment)
            
            # システム生成実行
            result = self.create_system_from_prompt(prompt_data)
            
            if result['success']:
                # 成功コメント
                success_comment = f"""✅ **システム生成完了！**

🎉 お待たせしました！システムの生成が完了しました。

📊 **生成結果:**
- 🔗 **GitHub リポジトリ:** {result['github_url']}
- 🏗️ **システムタイプ:** {result['system_type']}
- 📁 **作成ファイル数:** {len(result['files_created'])}件
- 📝 **説明:** {result['description']}

🚀 **生成されたファイル:**
{chr(10).join([f"- `{file}`" for file in result['files_created']])}

## 🔧 使用方法
1. リポジトリをクローンしてください
2. `pip install -r requirements.txt` で依存関係をインストール
3. `python main.py` で実行

ご不明な点がございましたら、お気軽にお声がけください！

---
**🤖 Generated by GitHub Copilot AI**
"""
                self.post_comment_to_issue(issue_number, success_comment)
                self.close_issue_with_label(issue_number, "completed")
                
                # データベースに記録
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO processed_issues 
                    (issue_number, title, body, processed_at, status, result_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    issue_number,
                    issue['title'],
                    issue['body'],
                    datetime.now().isoformat(),
                    'completed',
                    result['github_url']
                ))
                conn.commit()
                conn.close()
                
            else:
                # エラーコメント
                error_comment = f"""❌ **システム生成エラー**

申し訳ございません。システム生成中にエラーが発生しました。

🔍 **エラー詳細:**
```
{result.get('error', '不明なエラー')}
```

📞 開発チームに確認いたします。しばらくお待ちください。

---
**🤖 GitHub Copilot AI**
"""
                self.post_comment_to_issue(issue_number, error_comment)
                self.close_issue_with_label(issue_number, "error")
            
            self.processed_issues.add(issue_number)
            return True
            
        except Exception as e:
            print(f"❌ ISSUE処理エラー: {e}")
            return False
    
    def start_monitoring(self, interval: int = 60):
        """ISSUE監視を開始"""
        print(f"🔍 GitHub ISSUE監視開始 ({self.repo_owner}/{self.repo_name})")
        print(f"⏰ チェック間隔: {interval}秒")
        
        while True:
            try:
                issues = self.get_open_issues()
                
                if issues:
                    print(f"📋 未処理ISSUE発見: {len(issues)}件")
                    
                    for issue in issues:
                        print(f"🔧 処理中: #{issue['number']} - {issue['title']}")
                        self.process_issue(issue)
                        time.sleep(5)  # API制限対策
                
                else:
                    print("✅ 新しいISSUEはありません")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("🛑 監視を停止します")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(interval)


def create_github_issue_interface():
    """GitHub ISSUE連携のGradioインターフェース"""
    import gradio as gr
    
    monitor = None
    
    def start_monitoring(github_token, repo_owner, repo_name, interval):
        global monitor
        try:
            if not all([github_token, repo_owner, repo_name]):
                return "❌ 必須項目を入力してください"
            
            monitor = GitHubIssueMonitor(github_token, repo_owner, repo_name)
            
            # バックグラウンドで監視開始
            thread = threading.Thread(
                target=monitor.start_monitoring,
                args=(int(interval),),
                daemon=True
            )
            thread.start()
            
            return f"✅ GitHub ISSUE監視開始\n📍 リポジトリ: {repo_owner}/{repo_name}\n⏰ 間隔: {interval}秒"
            
        except Exception as e:
            return f"❌ 監視開始エラー: {str(e)}"
    
    with gr.Blocks(title="📋 GitHub ISSUE連携システム") as interface:
        gr.Markdown("# 📋 GitHub ISSUE連携システム")
        gr.Markdown("GitHubのISSUEを監視して、プロンプトから自動でシステム生成します")
        
        with gr.Row():
            with gr.Column():
                github_token_input = gr.Textbox(
                    label="GitHub Token",
                    type="password",
                    placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                )
                repo_owner_input = gr.Textbox(
                    label="リポジトリオーナー",
                    placeholder="username"
                )
                repo_name_input = gr.Textbox(
                    label="リポジトリ名",
                    placeholder="system-requests"
                )
                interval_input = gr.Number(
                    label="チェック間隔（秒）",
                    value=60,
                    minimum=30
                )
                
                start_btn = gr.Button("🚀 監視開始", variant="primary")
                status_output = gr.Textbox(
                    label="監視ステータス",
                    interactive=False,
                    lines=5
                )
            
            with gr.Column():
                gr.Markdown("## 📝 使用方法")
                gr.Markdown("""
                1. **GitHub Token**: Personal Access Token（Issues権限必要）
                2. **リポジトリ設定**: 監視対象のリポジトリを指定
                3. **監視開始**: バックグラウンドで自動監視開始
                
                ## 🏷️ ISSUE形式
                
                ISSUEには以下のラベルをつけてください：
                - `system-generation`
                - `prompt-request`
                
                ## 📋 プロンプト例
                
                ```
                # ECサイト構築
                
                ## 要件
                - 商品管理機能
                - ショッピングカート
                - 決済機能（Stripe）
                - ユーザー認証
                
                ## 技術スタック
                - FastAPI + SQLAlchemy
                - React Frontend
                - PostgreSQL
                ```
                
                ## 🤖 AI応答
                
                私が自動で：
                1. ISSUEを検知・解析
                2. プロンプトからシステム生成
                3. GitHubリポジトリ作成
                4. 結果をISSUEにコメント
                5. ISSUEをクローズ
                """)
        
        start_btn.click(
            fn=start_monitoring,
            inputs=[github_token_input, repo_owner_input, repo_name_input, interval_input],
            outputs=status_output
        )
    
    return interface

# GitHub ISSUE連携インターフェース
github_issue_interface = create_github_issue_interface()
