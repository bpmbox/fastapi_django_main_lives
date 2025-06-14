#!/usr/bin/env python3
"""
🚀 GitHub Issue自動作成付きCI/CDシステム

テスト結果を自動でGitHub Issueとして作成・アップロードするシステム
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class GitHubIssueCISystem:
    """GitHub Issue自動作成付きCI/CDシステム"""
    
    def __init__(self, repo_name: str = "miyataken999/fastapi_django_main_live"):
        """初期化"""
        self.repo_name = repo_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.issue_templates_dir = Path("/workspaces/fastapi_django_main_live/ci_issue_templates")
        self.issue_templates_dir.mkdir(parents=True, exist_ok=True)
        
    def create_ci_test_issue(self, test_results: Dict[str, Any], screenshots_dir: Path) -> bool:
        """CI/CDテスト結果をGitHub Issueとして作成"""
        try:
            # Issue内容生成
            issue_title, issue_body = self._generate_issue_content(test_results, screenshots_dir)
            
            # Issue本文をファイルに保存
            issue_body_file = self.issue_templates_dir / f"ci_test_issue_{self.timestamp}.md"
            with open(issue_body_file, 'w', encoding='utf-8') as f:
                f.write(issue_body)
            
            # GitHub CLI使用してIssue作成（基本ラベルのみ）
            cmd = [
                "gh", "issue", "create",
                "--title", issue_title,
                "--body-file", str(issue_body_file),
                "--label", "enhancement"
            ]
            
            print(f"🚀 GitHub Issue作成中...")
            print(f"📋 タイトル: {issue_title}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd="/workspaces/fastapi_django_main_live")
            
            if result.returncode == 0:
                issue_url = result.stdout.strip()
                print(f"✅ GitHub Issue作成成功!")
                print(f"🔗 Issue URL: {issue_url}")
                return True
            else:
                print(f"❌ GitHub Issue作成失敗:")
                print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ GitHub Issue作成エラー: {e}")
            return False
    
    def _generate_issue_content(self, test_results: Dict[str, Any], screenshots_dir: Path) -> tuple[str, str]:
        """Issue用のタイトルと本文を生成"""
        
        # 総合成功判定
        overall_success = self._calculate_overall_success(test_results)
        status_emoji = "✅" if overall_success else "❌"
        status_text = "成功" if overall_success else "失敗"
        
        # Issue タイトル
        title = f"{status_emoji} CI/CD自動テスト結果 - {self.timestamp} ({status_text})"
        
        # Issue 本文
        body = f"""# 🚀 CI/CD自動テスト結果レポート

## 📋 テスト実行概要
- **実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **テストID**: {self.timestamp}
- **総合結果**: {status_emoji} **{status_text}**
- **リポジトリ**: {self.repo_name}

## 📊 詳細テスト結果

### 📸 画面キャプチャー結果
"""
        
        # スクリーンショット結果
        if "screenshots" in test_results:
            screenshots = test_results["screenshots"]
            if "error" not in screenshots:
                total_screenshots = len(screenshots)
                successful_screenshots = sum(1 for r in screenshots.values() if r.get("success", False))
                success_rate = (successful_screenshots / total_screenshots * 100) if total_screenshots > 0 else 0
                
                body += f"""
**成功率**: {successful_screenshots}/{total_screenshots} ({success_rate:.1f}%)

| 画面 | 状態 | ファイル | 説明 |
|------|------|----------|------|
"""
                
                for name, result in screenshots.items():
                    status = "✅" if result.get("success", False) else "❌"
                    file_path = result.get("file_path", "N/A")
                    description = result.get("description", name)
                    body += f"| {name} | {status} | `{file_path}` | {description} |\n"
            else:
                body += f"❌ **エラー**: {screenshots['error']}\n"
        
        # APIテスト結果
        body += f"\n### 🤖 Gradio APIテスト結果\n"
        if "api_tests" in test_results:
            api_tests = test_results["api_tests"]
            if "error" not in api_tests:
                total_api_tests = len(api_tests)
                successful_api_tests = sum(1 for r in api_tests.values() if r.get("success", False))
                success_rate = (successful_api_tests / total_api_tests * 100) if total_api_tests > 0 else 0
                
                body += f"""
**成功率**: {successful_api_tests}/{total_api_tests} ({success_rate:.1f}%)

| APIテスト | 状態 | 説明 | エラー |
|-----------|------|------|-------|
"""
                
                for name, result in api_tests.items():
                    status = "✅" if result.get("success", False) else "❌"
                    description = result.get("description", name)
                    error = result.get("error", "-")
                    body += f"| {name} | {status} | {description} | {error} |\n"
            else:
                body += f"❌ **エラー**: {api_tests['error']}\n"
        
        # 検証依頼セクション
        body += f"""
## 🔍 検証・フィードバック依頼

以下の点について検証とフィードバックをお願いします:

### 📸 画面表示の検証
- [ ] メインダッシュボードが正常に表示されているか
- [ ] Gradioインターフェースの階層化が適切に動作しているか
- [ ] UIのレスポンシブデザインが機能しているか

### 🤖 API機能の検証
- [ ] 各API エンドポイントが正常に応答するか
- [ ] レスポンス時間が許容範囲内（< 5秒）か
- [ ] エラーハンドリングが適切に機能するか

### 🚀 システム全体の検証
- [ ] 初心者ガイドシステムが直感的に使用できるか
- [ ] 階層化インターフェースでユーザビリティが向上したか
- [ ] CI/CDパイプラインが安定して動作するか

## 💡 改善提案
検証後、以下の項目について改善提案があれば教えてください:
- パフォーマンス改善点
- UIユーザビリティ改善点
- API設計改善点
- テスト項目追加提案

## 📝 追加情報
- **テスト環境**: GitHub Codespaces
- **実行コマンド**: `python ci_auto_test_system.py`
- **ログファイル**: `/workspaces/fastapi_django_main_live/ci_reports/`
- **スクリーンショット**: `/workspaces/fastapi_django_main_live/docs/images/screenshots/`

---
*このIssueはCI/CD自動テストシステムによって自動生成されました。*
"""
        
        return title, body
    
    def create_comprehensive_test_issue(self, test_results: Dict[str, Any], codespace_url: str) -> bool:
        """包括的テスト結果をGitHub Issueとして作成"""
        try:
            # Issue内容生成
            issue_title, issue_body = self._generate_comprehensive_issue_content(test_results, codespace_url)
            
            # Issue本文をファイルに保存
            issue_body_file = self.issue_templates_dir / f"comprehensive_test_issue_{self.timestamp}.md"
            with open(issue_body_file, 'w', encoding='utf-8') as f:
                f.write(issue_body)
            
            # GitHub CLI使用してIssue作成（基本ラベルのみ）
            cmd = [
                "gh", "issue", "create",
                "--title", issue_title,
                "--body-file", str(issue_body_file),
                "--label", "enhancement"
            ]
            
            print(f"🚀 包括的テスト結果GitHub Issue作成中...")
            print(f"📋 タイトル: {issue_title}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd="/workspaces/fastapi_django_main_live")
            
            if result.returncode == 0:
                issue_url = result.stdout.strip()
                print(f"✅ GitHub Issue作成成功!")
                print(f"🔗 Issue URL: {issue_url}")
                return True
            else:
                print(f"❌ GitHub Issue作成失敗:")
                print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ GitHub Issue作成エラー: {e}")
            return False
    
    def _generate_comprehensive_issue_content(self, test_results: Dict[str, Any], codespace_url: str) -> tuple[str, str]:
        """包括的テスト用Issue内容生成"""
        
        summary = test_results.get("summary", {})
        overall_success = summary.get("overall_success", False)
        status_emoji = "✅" if overall_success else "❌"
        status_text = "成功" if overall_success else "失敗"
        
        # Issue タイトル
        title = f"{status_emoji} 包括的コントローラーテスト結果 - {self.timestamp} ({status_text})"
        
        # Issue 本文
        body = f"""# 🚀 包括的コントローラーテスト結果レポート

## 📋 テスト実行概要
- **実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **テストID**: {self.timestamp}
- **総合結果**: {status_emoji} **{status_text}**
- **Codespace URL**: {codespace_url}
- **実行時間**: {test_results.get('test_duration', 0):.2f}秒

## 📊 テスト結果サマリー

### 🤖 APIテスト結果
**成功率**: {summary.get('api_tests', {}).get('successful', 0)}/{summary.get('api_tests', {}).get('total', 0)} ({summary.get('api_tests', {}).get('success_rate', 0)}%)

### 📸 画面キャプチャー結果  
**成功率**: {summary.get('screenshots', {}).get('successful', 0)}/{summary.get('screenshots', {}).get('total', 0)} ({summary.get('screenshots', {}).get('success_rate', 0)}%)

## 📋 詳細テスト結果

### 🤖 コントローラーAPIテスト詳細

| コントローラー | カテゴリ | 状態 | 応答時間 | 説明 |
|---------------|----------|------|----------|------|
"""
        
        # APIテスト結果テーブル
        api_tests = test_results.get("api_tests", {})
        for name, result in api_tests.items():
            status = "✅" if result.get("success", False) else "❌"
            response_time = f"{result.get('response_time', 0)}秒"
            description = result.get("description", name)
            category = result.get("category", "未分類")
            
            body += f"| {name} | {category} | {status} | {response_time} | {description} |\n"
        
        # スクリーンショット結果
        body += f"\n### 📸 画面キャプチャー詳細\n\n"
        body += f"| カテゴリ | 状態 | ファイルパス | 説明 |\n"
        body += f"|----------|------|-------------|------|\n"
        
        screenshots = test_results.get("screenshots", {})
        for name, result in screenshots.items():
            status = "✅" if result.get("success", False) else "❌"
            file_path = result.get("file_path", "N/A")
            description = result.get("description", name)
            
            body += f"| {name} | {status} | `{file_path}` | {description} |\n"
        
        # 発見されたコントローラー一覧
        body += f"\n### 🔍 発見されたコントローラー\n\n"
        controllers = test_results.get("controllers", [])
        
        # カテゴリ別に整理
        categories = {}
        for controller in controllers:
            category = controller.get("category", "未分類")
            if category not in categories:
                categories[category] = []
            categories[category].append(controller)
        
        for category, controllers_in_category in categories.items():
            body += f"#### {category}\n"
            for controller in controllers_in_category:
                status = "✅" if api_tests.get(controller["name"], {}).get("success", False) else "❌"
                body += f"- {status} **{controller['name']}**: {controller['description']}\n"
            body += f"\n"
        
        # 画面チェック依頼
        body += f"""
## 👀 画面チェック依頼

**Codespace URL**: {codespace_url}

以下の画面について、実際にアクセスして動作確認をお願いします:

### 🎯 チェックポイント
- [ ] **メイン画面**: 正常に表示されるか
- [ ] **階層化インターフェース**: カテゴリ別に整理されているか
- [ ] **各コントローラー**: 期待通りに動作するか
- [ ] **レスポンス速度**: 許容範囲内（<5秒）か
- [ ] **エラーハンドリング**: 適切に処理されるか

### 📸 画面確認項目
"""
        
        # カテゴリ別画面確認項目
        for category in categories.keys():
            body += f"- [ ] **{category}**: 機能が正常に動作するか確認\n"
        
        body += f"""
## 🔍 検証・フィードバック依頼

### 🎨 UI/UX検証
- [ ] インターフェースが直感的に使えるか
- [ ] 画面遷移がスムーズか
- [ ] エラーメッセージが分かりやすいか

### ⚡ パフォーマンス検証
- [ ] 応答時間が適切か
- [ ] 大量データ処理に対応できるか
- [ ] メモリ使用量が適切か

### 🔒 セキュリティ検証
- [ ] 認証・認可が適切に機能するか
- [ ] 入力値検証が実装されているか
- [ ] セッション管理が適切か

## 💡 改善提案
以下について具体的な改善提案があれば、コメントで教えてください:

1. **UI改善点**: より使いやすくするための提案
2. **機能追加**: 必要な機能の提案
3. **パフォーマンス改善**: 速度改善の提案
4. **バグ報告**: 発見した問題の報告

## 📝 追加情報
- **テスト環境**: GitHub Codespaces
- **実行コマンド**: `python comprehensive_controller_test.py`
- **レポート**: `/workspaces/fastapi_django_main_live/ci_reports/`
- **スクリーンショット**: `/workspaces/fastapi_django_main_live/docs/images/screenshots/`

---
*このIssueは包括的コントローラーテストシステムによって自動生成されました。*
"""
        
        return title, body
        """総合成功判定"""
        success_count = 0
        total_count = 0
        
        # スクリーンショット成功率
        if "screenshots" in test_results and "error" not in test_results["screenshots"]:
            screenshots = test_results["screenshots"]
            successful_screenshots = sum(1 for r in screenshots.values() if r.get("success", False))
            if len(screenshots) > 0:
                success_count += 1 if (successful_screenshots / len(screenshots)) > 0.5 else 0
                total_count += 1
        
        # APIテスト成功率
        if "api_tests" in test_results and "error" not in test_results["api_tests"]:
            api_tests = test_results["api_tests"]
            successful_api_tests = sum(1 for r in api_tests.values() if r.get("success", False))
            if len(api_tests) > 0:
                success_count += 1 if (successful_api_tests / len(api_tests)) > 0.7 else 0
                total_count += 1
        
        return (success_count / total_count) >= 0.6 if total_count > 0 else False

def create_ci_github_issue(test_results: Dict[str, Any], screenshots_dir: Path) -> bool:
    """CI/CDテスト結果からGitHub Issueを作成"""
    github_ci = GitHubIssueCISystem()
    return github_ci.create_ci_test_issue(test_results, screenshots_dir)

if __name__ == "__main__":
    # テスト実行例
    sample_results = {
        "screenshots": {
            "main_dashboard": {"success": True, "description": "メインダッシュボード"},
            "gradio_interface": {"success": True, "description": "Gradioインターフェース"}
        },
        "api_tests": {
            "create_prompt": {"success": True, "description": "プロンプト作成テスト"},
            "save_prompt": {"success": False, "description": "プロンプト保存テスト", "error": "DB connection error"}
        }
    }
    
    screenshots_dir = Path("/workspaces/fastapi_django_main_live/docs/images/screenshots")
    success = create_ci_github_issue(sample_results, screenshots_dir)
    print(f"GitHub Issue作成: {'成功' if success else '失敗'}")
