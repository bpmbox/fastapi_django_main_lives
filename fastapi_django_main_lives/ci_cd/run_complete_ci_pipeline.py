#!/usr/bin/env python3
"""
🚀 完全自動CI/CDパイプライン実行スクリプト

コントローラー作成時に実行する統合テストシステム:
1. 画面キャプチャー
2. Gradio API自動テスト  
3. GitHub Issue自動レポート
4. 結果の可視化とレポート
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# 作成したモジュールをインポート
from ci_auto_test_system import CIAutoTestSystem
from github_issue_ci_system import create_ci_github_issue, GitHubIssueCISystem
from comprehensive_controller_test import ComprehensiveControllerTester
from real_gradio_api_tester import RealGradioAPITester

class CompleteCIPipeline:
    """完全自動CI/CDパイプライン"""
    
    def __init__(self, project_name: str = "AI-Human協働システム", create_github_issue: bool = True, comprehensive_test: bool = True, real_api_test: bool = True):
        """初期化"""
        self.project_name = project_name
        self.create_github_issue = create_github_issue
        self.comprehensive_test = comprehensive_test
        self.real_api_test = real_api_test
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.codespace_url = "https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev"
        
        print(f"🚀 完全自動CI/CDパイプライン初期化")
        print(f"📋 プロジェクト: {project_name}")
        print(f"📊 GitHub Issue作成: {'有効' if create_github_issue else '無効'}")
        print(f"🔍 包括的テスト: {'有効' if comprehensive_test else '無効'}")
        print(f"� 実際のAPIテスト: {'有効' if real_api_test else '無効'}")
        print(f"�🌐 Codespace URL: {self.codespace_url}")
        print(f"📋 API一覧URL: {self.codespace_url}/?view=api")
        print(f"⏰ 実行時刻: {self.timestamp}")
        print("=" * 60)
    
    def run_complete_pipeline(self) -> bool:
        """完全なCI/CDパイプラインを実行"""
        pipeline_start_time = time.time()
        
        try:
            # ステップ1: 基本CI/CDテスト実行
            print("🔄 ステップ1: 基本CI/CDテスト実行")
            ci_system = CIAutoTestSystem(self.project_name)
            ci_success = ci_system.run_full_ci_pipeline()
            
            # ステップ2: 包括的コントローラーテスト
            comprehensive_success = True
            comprehensive_results = {}
            
            if self.comprehensive_test:
                print("\n🔄 ステップ2: 包括的コントローラーテスト実行")
                comprehensive_tester = ComprehensiveControllerTester(self.codespace_url)
                comprehensive_results = comprehensive_tester.run_comprehensive_test()
                comprehensive_success = comprehensive_results.get("summary", {}).get("overall_success", False)
                
                if comprehensive_success:
                    print("✅ 包括的コントローラーテスト成功")
                else:
                    print("⚠️ 包括的コントローラーテストで問題が発見されましたが、続行します")
            else:
                print("\n⏭️ ステップ2: 包括的コントローラーテストをスキップ")
            
            # ステップ3: 実際のGradio APIテスト
            real_api_success = True
            real_api_results = {}
            
            if self.real_api_test:
                print("\n🔄 ステップ3: 実際のGradio APIテスト実行")
                real_api_tester = RealGradioAPITester(self.codespace_url)
                real_api_results = real_api_tester.run_comprehensive_api_test()
                real_api_success = real_api_results.get("summary", {}).get("overall_success", False)
                
                if real_api_success:
                    print("✅ 実際のAPIテスト成功")
                else:
                    print("⚠️ 実際のAPIテストで問題が発見されましたが、続行します")
            else:
                print("\n⏭️ ステップ3: 実際のAPIテストをスキップ")
            
            # ステップ4: GitHub Issue自動作成
            if self.create_github_issue:
                print("\n🔄 ステップ4: GitHub Issue自動作成")
                
                # 基本CI/CDテスト結果のIssue作成
                basic_github_success = create_ci_github_issue(
                    ci_system.test_results,
                    ci_system.screenshots_dir
                )
                
                # 包括的テスト結果のIssue作成
                comprehensive_github_success = True
                if self.comprehensive_test and comprehensive_results:
                    github_ci = GitHubIssueCISystem()
                    comprehensive_github_success = github_ci.create_comprehensive_test_issue(
                        comprehensive_results, 
                        self.codespace_url
                    )
                
                # 実際のAPIテスト結果のIssue作成
                api_github_success = True
                if self.real_api_test and real_api_results:
                    api_github_success = self._create_api_test_issue(real_api_results)
                
                github_success = basic_github_success and comprehensive_github_success and api_github_success
                
                if github_success:
                    print("✅ GitHub Issue作成成功")
                else:
                    print("❌ GitHub Issue作成失敗")
            else:
                print("\n⏭️ ステップ4: GitHub Issue作成をスキップ")
                github_success = True
            
            # ステップ5: 結果サマリー表示
            print("\n🔄 ステップ5: 結果サマリー表示")
            self._display_comprehensive_summary(
                ci_system.test_results, 
                comprehensive_results, 
                real_api_results,
                ci_success, 
                comprehensive_success,
                real_api_success
            )
            
            # パイプライン完了
            pipeline_duration = time.time() - pipeline_start_time
            overall_success = ci_success and comprehensive_success and real_api_success and (github_success if self.create_github_issue else True)
            
            print("\n" + "=" * 60)
            print("🏁 完全自動CI/CDパイプライン完了")
            print(f"⏱️ 総実行時間: {pipeline_duration:.2f}秒")
            print(f"📊 最終結果: {'✅ 成功' if overall_success else '❌ 失敗'}")
            print(f"🌐 Codespace URL: {self.codespace_url}")
            print(f"📋 API一覧URL: {self.codespace_url}/?view=api")
            
            if overall_success:
                print("🎉 全システムが正常に動作しています！")
                print("👀 GitHub Issueで詳細な画面チェックを依頼済みです")
                print("📋 実際のAPIドキュメントも確認可能です")
            else:
                print("🔧 修正が必要な項目があります。詳細は上記レポートとGitHub Issueを確認してください。")
            
            print("=" * 60)
            
            return overall_success
            
        except Exception as e:
            print(f"❌ パイプライン実行エラー: {e}")
            return False
    
    def _create_api_test_issue(self, api_results: dict) -> bool:
        """実際のAPIテスト結果のGitHub Issue作成"""
        try:
            issue_title = f"🎯 実際のGradio APIテスト結果 - {self.timestamp}"
            
            summary = api_results.get("summary", {})
            overall_success = summary.get("overall_success", False)
            status_emoji = "✅" if overall_success else "❌"
            status_text = "成功" if overall_success else "失敗"
            
            issue_body = f"""# 🎯 実際のGradio APIテスト結果レポート

## 📋 テスト概要
- **実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **総合結果**: {status_emoji} **{status_text}**
- **Codespace URL**: {self.codespace_url}
- **API一覧URL**: {self.codespace_url}/?view=api

## 📊 テスト結果サマリー
- **成功率**: {summary.get('successful_apis', 0)}/{summary.get('total_apis', 0)} ({summary.get('success_rate', 0)}%)
- **平均レスポンス時間**: {summary.get('avg_response_time', 0)}秒

## 🔍 検証依頼
実際のAPIドキュメント（{self.codespace_url}/?view=api）と合わせて、以下の点を確認してください:

### 📋 APIエンドポイント確認
- [ ] APIドキュメントページが正常に表示される
- [ ] 各APIエンドポイントが適切に機能する
- [ ] レスポンス時間が許容範囲内である
- [ ] エラーハンドリングが適切である

## 💡 改善提案
APIの動作について改善提案があれば教えてください。

---
*このIssueは実際のGradio APIテストシステムによって自動生成されました。*
"""
            
            # Issue本文をファイルに保存
            issue_body_file = Path("/workspaces/fastapi_django_main_live/ci_issue_templates") / f"api_test_issue_{self.timestamp}.md"
            issue_body_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(issue_body_file, 'w', encoding='utf-8') as f:
                f.write(issue_body)
            
            # GitHub CLI使用してIssue作成
            cmd = [
                "gh", "issue", "create",
                "--title", issue_title,
                "--body-file", str(issue_body_file),
                "--label", "enhancement"
            ]
            
            import subprocess
            result = subprocess.run(cmd, capture_output=True, text=True, cwd="/workspaces/fastapi_django_main_live")
            
            if result.returncode == 0:
                issue_url = result.stdout.strip()
                print(f"✅ API テスト結果Issue作成成功: {issue_url}")
                return True
            else:
                print(f"❌ API テスト結果Issue作成失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ API テスト結果Issue作成エラー: {e}")
            return False

    def _display_comprehensive_summary(self, basic_results: dict, comprehensive_results: dict, api_results: dict, ci_success: bool, comprehensive_success: bool, api_success: bool):
        """包括的サマリー表示（APIテスト結果を含む）"""
        print("📊 最終テスト結果サマリー")
        print("-" * 40)
        
        # 基本CI/CDテスト結果
        print("### 🔧 基本CI/CDテスト")
        if "screenshots" in basic_results:
            screenshots = basic_results["screenshots"]
            if "error" not in screenshots:
                total_screenshots = len(screenshots)
                successful_screenshots = sum(1 for r in screenshots.values() if r.get("success", False))
                success_rate = (successful_screenshots / total_screenshots * 100) if total_screenshots > 0 else 0
                print(f"📸 スクリーンショット: {successful_screenshots}/{total_screenshots} ({success_rate:.1f}%)")
            else:
                print(f"📸 スクリーンショット: ❌ エラー")
        
        if "api_tests" in basic_results:
            api_tests = basic_results["api_tests"]
            if "error" not in api_tests:
                total_api_tests = len(api_tests)
                successful_api_tests = sum(1 for r in api_tests.values() if r.get("success", False))
                success_rate = (successful_api_tests / total_api_tests * 100) if total_api_tests > 0 else 0
                print(f"🤖 APIテスト: {successful_api_tests}/{total_api_tests} ({success_rate:.1f}%)")
            else:
                print(f"🤖 APIテスト: ❌ エラー")
        
        # 包括的テスト結果
        if comprehensive_results:
            print("\n### 🔍 包括的コントローラーテスト")
            summary = comprehensive_results.get("summary", {})
            
            api_summary = summary.get("api_tests", {})
            print(f"🤖 コントローラーAPI: {api_summary.get('successful', 0)}/{api_summary.get('total', 0)} ({api_summary.get('success_rate', 0)}%)")
            
            screenshot_summary = summary.get("screenshots", {})
            print(f"📸 カテゴリ画面: {screenshot_summary.get('successful', 0)}/{screenshot_summary.get('total', 0)} ({screenshot_summary.get('success_rate', 0)}%)")
        
        # 実際のAPIテスト結果
        if api_results:
            print("\n### 🎯 実際のGradio APIテスト")
            api_summary = api_results.get("summary", {})
            print(f"🎯 実際のAPI: {api_summary.get('successful_apis', 0)}/{api_summary.get('total_apis', 0)} ({api_summary.get('success_rate', 0)}%)")
            print(f"⏱️ 平均レスポンス時間: {api_summary.get('avg_response_time', 0)}秒")
        
        # 総合判定
        print(f"\n🎯 総合判定:")
        print(f"  - 基本CI/CD: {'✅ 成功' if ci_success else '❌ 失敗'}")
        if comprehensive_results:
            print(f"  - 包括的テスト: {'✅ 成功' if comprehensive_success else '❌ 失敗'}")
        if api_results:
            print(f"  - 実際のAPI: {'✅ 成功' if api_success else '❌ 失敗'}")
        
        # 推奨アクション
        overall_success = ci_success and comprehensive_success and api_success
        if overall_success:
            print("💡 推奨アクション:")
            print("  - 本番環境へのデプロイを検討")
            print("  - GitHub Issueで他の開発者からフィードバックを収集") 
            print(f"  - API一覧ページ（{self.codespace_url}/?view=api）で詳細確認")
            print("  - 定期的な監視とメンテナンス")
        else:
            print("⚠️ 必要なアクション:")
            print("  - 失敗したテストの原因調査")
            print("  - バグ修正とリファクタリング")
            print("  - 再テスト実行")
        """最終サマリー表示"""
        print("📊 最終テスト結果サマリー")
        print("-" * 40)
        
        # スクリーンショット結果
        if "screenshots" in test_results:
            screenshots = test_results["screenshots"]
            if "error" not in screenshots:
                total_screenshots = len(screenshots)
                successful_screenshots = sum(1 for r in screenshots.values() if r.get("success", False))
                success_rate = (successful_screenshots / total_screenshots * 100) if total_screenshots > 0 else 0
                print(f"📸 スクリーンショット: {successful_screenshots}/{total_screenshots} ({success_rate:.1f}%)")
            else:
                print(f"📸 スクリーンショット: ❌ エラー")
        
        # APIテスト結果
        if "api_tests" in test_results:
            api_tests = test_results["api_tests"]
            if "error" not in api_tests:
                total_api_tests = len(api_tests)
                successful_api_tests = sum(1 for r in api_tests.values() if r.get("success", False))
                success_rate = (successful_api_tests / total_api_tests * 100) if total_api_tests > 0 else 0
                print(f"🤖 APIテスト: {successful_api_tests}/{total_api_tests} ({success_rate:.1f}%)")
            else:
                print(f"🤖 APIテスト: ❌ エラー")
        
        # 総合判定
        print(f"🎯 総合判定: {'✅ 成功' if ci_success else '❌ 失敗'}")
        
        # 推奨アクション
        if ci_success:
            print("💡 推奨アクション:")
            print("  - 本番環境へのデプロイを検討")
            print("  - GitHub Issueで他の開発者からフィードバックを収集")
            print("  - ユーザーテストの実施")
        else:
            print("⚠️ 必要なアクション:")
            print("  - 失敗したテストの原因調査")
            print("  - バグ修正とリファクタリング")
            print("  - 再テスト実行")

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="🚀 完全自動CI/CDパイプライン")
    parser.add_argument("--project", "-p", default="AI-Human協働システム", help="プロジェクト名")
    parser.add_argument("--no-github-issue", action="store_true", help="GitHub Issue作成をスキップ")
    parser.add_argument("--no-comprehensive", action="store_true", help="包括的テストをスキップ")
    parser.add_argument("--no-real-api", action="store_true", help="実際のAPIテストをスキップ")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細ログ出力")
    
    args = parser.parse_args()
    
    # 詳細ログ設定
    if args.verbose:
        print("🔍 詳細ログモード: 有効")
    
    # パイプライン実行
    pipeline = CompleteCIPipeline(
        project_name=args.project,
        create_github_issue=not args.no_github_issue,
        comprehensive_test=not args.no_comprehensive,
        real_api_test=not args.no_real_api
    )
    
    success = pipeline.run_complete_pipeline()
    
    # 終了コード設定
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
