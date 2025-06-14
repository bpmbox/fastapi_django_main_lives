#!/usr/bin/env python3
"""
GitHub ISSUE リアルタイム監視システム
外部ユーザーからのシステム生成リクエストを24時間監視
"""

import os
import time
import threading
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
from system_automation import SystemAutomation

class GitHubIssueMonitor:
    """GitHub ISSUE監視クラス（リアルタイム）"""
    
    def __init__(self, github_token: str, repo_owner: str, repo_name: str):
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        
        # 監視設定
        self.monitoring = False
        self.check_interval = 30  # 30秒間隔
        self.processed_issues = set()
        self.init_processed_issues()
        
        # システム自動化
        self.automation = SystemAutomation(github_token)
        
        print(f"📡 GitHub ISSUE監視初期化")
        print(f"   リポジトリ: {repo_owner}/{repo_name}")
        print(f"   監視間隔: {self.check_interval}秒")
    
    def init_processed_issues(self):
        """既に処理済みのISSUEを初期化"""
        try:
            # データベースから処理済みISSUEを読み込み
            db_path = "/workspaces/fastapi_django_main_live/github_issues.db"
            
            if not Path(db_path).exists():
                # データベース初期化
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS processed_issues (
                        issue_number INTEGER PRIMARY KEY,
                        title TEXT,
                        body TEXT,
                        processed_at TIMESTAMP,
                        status TEXT,
                        result_url TEXT,
                        repo_url TEXT
                    )
                ''')
                conn.commit()
                conn.close()
            else:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT issue_number FROM processed_issues')
                processed = cursor.fetchall()
                self.processed_issues = {row[0] for row in processed}
                conn.close()
                print(f"📋 処理済みISSUE: {len(self.processed_issues)}件読み込み")
        
        except Exception as e:
            print(f"❌ 処理済みISSUE初期化エラー: {e}")
    
    def get_system_generation_issues(self):
        """システム生成用のISSUEを取得"""
        try:
            # システム生成ラベル付きのISSUEを検索
            url = f"{self.base_url}/issues"
            params = {
                'state': 'open',
                'labels': 'system-generation,prompt-request',
                'sort': 'created',
                'direction': 'desc',
                'per_page': 10
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
    
    def extract_system_requirements(self, issue):
        """ISSUEからシステム要件を抽出"""
        title = issue['title']
        body = issue['body'] or ""
        
        # システム要件の解析
        requirements = {
            'title': title.replace('[SYSTEM-GEN]', '').strip(),
            'content': body,
            'system_type': 'general',
            'technologies': [],
            'priority': 'medium',
            'estimated_time': '30min'
        }
        
        # 技術スタック抽出
        tech_keywords = {
            'fastapi': 'FastAPI',
            'django': 'Django',
            'flask': 'Flask',
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'nodejs': 'Node.js',
            'python': 'Python',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'postgresql': 'PostgreSQL',
            'mysql': 'MySQL',
            'mongodb': 'MongoDB',
            'docker': 'Docker',
            'kubernetes': 'Kubernetes'
        }
        
        content_lower = (title + " " + body).lower()
        for keyword, tech in tech_keywords.items():
            if keyword in content_lower:
                requirements['technologies'].append(tech)
        
        # システムタイプ判定
        if any(word in content_lower for word in ['api', 'backend', 'server']):
            requirements['system_type'] = 'api_system'
        elif any(word in content_lower for word in ['web', 'frontend', 'ui', 'interface']):
            requirements['system_type'] = 'web_system'
        elif any(word in content_lower for word in ['bot', 'chat', 'ai']):
            requirements['system_type'] = 'ai_system'
        elif any(word in content_lower for word in ['mobile', 'app', 'android', 'ios']):
            requirements['system_type'] = 'mobile_system'
        
        # 優先度判定
        if '緊急' in content_lower or 'urgent' in content_lower or '高' in content_lower:
            requirements['priority'] = 'high'
        elif '低' in content_lower or 'low' in content_lower:
            requirements['priority'] = 'low'
        
        return requirements
    
    def process_issue(self, issue):
        """ISSUE処理の実行"""
        issue_number = issue['number']
        print(f"\n🔄 ISSUE #{issue_number} 処理開始")
        print(f"   タイトル: {issue['title']}")
        print(f"   作成者: {issue['user']['login']}")
        
        try:
            # システム要件抽出
            requirements = self.extract_system_requirements(issue)
            print(f"   システムタイプ: {requirements['system_type']}")
            print(f"   技術スタック: {', '.join(requirements['technologies'])}")
            
            # データベースに記録
            db_path = "/workspaces/fastapi_django_main_live/github_issues.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO processed_issues 
                (issue_number, title, body, processed_at, status, result_url, repo_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                issue_number,
                issue['title'],
                issue['body'],
                datetime.now().isoformat(),
                'processing',
                '',
                issue['html_url']
            ))
            conn.commit()
            conn.close()
            
            # プロンプトデータベースに保存
            prompt_db_path = "/workspaces/fastapi_django_main_live/prompts.db"
            conn = sqlite3.connect(prompt_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO prompts 
                (title, github_url, repository_name, system_type, content, execution_status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                requirements['title'],
                issue['html_url'],
                f"github-issue-{issue_number}",
                requirements['system_type'],
                requirements['content'],
                'approved'  # ISSUE経由は自動承認
            ))
            conn.commit()
            conn.close()
            
            # ISSUE に処理開始コメント投稿
            self.post_issue_comment(issue_number, f"""
🤖 **システム生成開始**

お疲れ様です！システム生成リクエストを受け付けました。

📋 **処理情報**
- システムタイプ: {requirements['system_type']}
- 検出技術: {', '.join(requirements['technologies']) if requirements['technologies'] else '汎用システム'}
- 優先度: {requirements['priority']}
- 推定時間: {requirements['estimated_time']}

🚀 **次のステップ**
1. GPT-ENGINEERによるシステム生成
2. GitHubリポジトリ自動作成
3. 生成コードのプッシュ
4. Controller/Router自動統合

完了次第、このISSUEにコメントで結果をお知らせします。
            """)
            
            # 処理済みセットに追加
            self.processed_issues.add(issue_number)
            
            print(f"✅ ISSUE #{issue_number} 処理記録完了")
            return True
            
        except Exception as e:
            print(f"❌ ISSUE #{issue_number} 処理エラー: {e}")
            
            # エラーコメント投稿
            self.post_issue_comment(issue_number, f"""
❌ **処理エラー**

申し訳ございません。システム生成処理中にエラーが発生しました。

エラー詳細: {str(e)}

管理者に報告いたします。しばらく後に再度お試しください。
            """)
            return False
    
    def post_issue_comment(self, issue_number, comment):
        """ISSUEにコメントを投稿"""
        try:
            url = f"{self.base_url}/issues/{issue_number}/comments"
            data = {'body': comment}
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                print(f"✅ ISSUE #{issue_number} コメント投稿成功")
            else:
                print(f"❌ ISSUE #{issue_number} コメント投稿失敗: {response.status_code}")
        
        except Exception as e:
            print(f"❌ コメント投稿エラー: {e}")
    
    def monitor_loop(self):
        """監視ループ"""
        print(f"🚀 GitHub ISSUE監視開始")
        
        while self.monitoring:
            try:
                # 新しいISSUEをチェック
                new_issues = self.get_system_generation_issues()
                
                if new_issues:
                    print(f"\n📥 新しいISSUE: {len(new_issues)}件")
                    
                    for issue in new_issues:
                        if self.monitoring:  # 監視継続中のみ処理
                            self.process_issue(issue)
                            time.sleep(5)  # 処理間隔
                
                else:
                    # 監視中表示（10回に1回）
                    if int(time.time()) % (self.check_interval * 10) == 0:
                        print(f"👁️ 監視中... ({datetime.now().strftime('%H:%M:%S')})")
                
                # 次のチェックまで待機
                time.sleep(self.check_interval)
            
            except KeyboardInterrupt:
                print(f"\n⏹️ 監視停止（ユーザー要求）")
                break
            except Exception as e:
                print(f"❌ 監視ループエラー: {e}")
                time.sleep(self.check_interval)
        
        print(f"🔚 GitHub ISSUE監視終了")
    
    def start_monitoring(self):
        """監視開始"""
        if self.monitoring:
            print("⚠️ 監視は既に開始されています")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"✅ バックグラウンド監視開始")
    
    def stop_monitoring(self):
        """監視停止"""
        self.monitoring = False
        print(f"⏹️ 監視停止要求")
    
    def get_monitoring_status(self):
        """監視状況取得"""
        return {
            'monitoring': self.monitoring,
            'processed_count': len(self.processed_issues),
            'check_interval': self.check_interval,
            'repo': f"{self.repo_owner}/{self.repo_name}"
        }

def demo_monitoring():
    """監視デモ実行"""
    print("📡 GitHub ISSUE監視デモ")
    print("=" * 50)
    
    # GitHub設定
    github_token = os.environ.get('GITHUB_TOKEN', '')
    if not github_token or len(github_token) < 20:
        print("❌ GITHUB_TOKEN が設定されていません")
        return
    
    # デモ用設定（実際のリポジトリ名に変更してください）
    repo_owner = "miyataken999"  # あなたのGitHubユーザー名
    repo_name = "fastapi_django_main_live"  # 監視対象リポジトリ
    
    # 監視開始
    monitor = GitHubIssueMonitor(github_token, repo_owner, repo_name)
    
    try:
        print(f"\n📋 現在の設定:")
        print(f"   リポジトリ: {repo_owner}/{repo_name}")
        print(f"   監視間隔: {monitor.check_interval}秒")
        print(f"   処理済み: {len(monitor.processed_issues)}件")
        
        # デモ監視（60秒間）
        print(f"\n🕐 60秒間のデモ監視を開始...")
        print(f"   （実際の運用では24時間継続監視）")
        
        monitor.start_monitoring()
        
        # 60秒間待機
        for i in range(60):
            time.sleep(1)
            if i % 10 == 0:
                status = monitor.get_monitoring_status()
                print(f"⏱️ {i}秒経過 - 処理済み: {status['processed_count']}件")
        
        # 監視停止
        monitor.stop_monitoring()
        
        # 結果表示
        final_status = monitor.get_monitoring_status()
        print(f"\n📊 デモ監視結果:")
        print(f"   処理済みISSUE: {final_status['processed_count']}件")
        print(f"   監視状態: {'稼働中' if final_status['monitoring'] else '停止'}")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ 監視停止（ユーザー中断）")
        monitor.stop_monitoring()
    except Exception as e:
        print(f"❌ 監視エラー: {e}")

if __name__ == "__main__":
    demo_monitoring()
