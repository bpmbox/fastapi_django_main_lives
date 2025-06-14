#!/usr/bin/env python3
"""
🔄 継続的インテグレーション & 自動修正システム
=============================================

Laravel風プロジェクトの継続的テスト・修正・改善システム
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import json
from datetime import datetime
import shutil

class ContinuousIntegrationSystem:
    """継続的インテグレーションシステム"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.reports_dir = project_root / "storage" / "ci_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def run_full_ci_pipeline(self) -> Dict[str, Any]:
        """完全なCI/CDパイプラインを実行"""
        print("🚀 継続的インテグレーション開始")
        print("=" * 60)
        
        pipeline_results = {
            "timestamp": datetime.now().isoformat(),
            "stages": {}
        }
        
        # Stage 1: 構造検証・修正
        print("\n📁 Stage 1: プロジェクト構造検証・修正")
        structure_result = self._fix_project_structure()
        pipeline_results["stages"]["structure"] = structure_result
        
        # Stage 2: コード品質チェック
        print("\n🔍 Stage 2: コード品質チェック")
        quality_result = self._check_code_quality()
        pipeline_results["stages"]["quality"] = quality_result
        
        # Stage 3: 機能テスト
        print("\n🧪 Stage 3: 機能テスト")
        functional_result = self._run_functional_tests()
        pipeline_results["stages"]["functional"] = functional_result
        
        # Stage 4: パフォーマンステスト
        print("\n⚡ Stage 4: パフォーマンステスト")
        performance_result = self._run_performance_tests()
        pipeline_results["stages"]["performance"] = performance_result
        
        # Stage 5: セキュリティチェック
        print("\n🔒 Stage 5: セキュリティチェック")
        security_result = self._run_security_checks()
        pipeline_results["stages"]["security"] = security_result
        
        # Stage 6: 自動修正
        print("\n🔧 Stage 6: 自動修正")
        fix_result = self._auto_fix_issues(pipeline_results)
        pipeline_results["stages"]["auto_fix"] = fix_result
        
        # レポート生成
        self._generate_ci_report(pipeline_results)
        
        return pipeline_results
    
    def _fix_project_structure(self) -> Dict[str, Any]:
        """プロジェクト構造を修正"""
        required_structure = {
            "app/Http/Controllers": "コントローラー格納",
            "app/Models": "モデル格納", 
            "app/Services": "サービス格納",
            "app/Console/Commands": "カスタムコマンド",
            "bootstrap": "アプリケーション初期化",
            "config": "設定ファイル",
            "database/migrations": "データベースマイグレーション",
            "public": "公開静的ファイル",
            "resources/views": "テンプレート",
            "routes": "ルーティング",
            "storage/logs": "ログファイル",
            "tests/Feature": "機能テスト",
            "tests/Unit": "ユニットテスト"
        }
        
        result = {"created": [], "existing": [], "errors": []}
        
        for dir_path, description in required_structure.items():
            full_path = self.project_root / dir_path
            if not full_path.exists():
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    result["created"].append(f"{dir_path} - {description}")
                    print(f"✅ 作成: {dir_path}")
                except Exception as e:
                    result["errors"].append(f"{dir_path}: {e}")
                    print(f"❌ 作成失敗: {dir_path} - {e}")
            else:
                result["existing"].append(dir_path)
        
        # 必要なファイルの作成
        self._create_essential_files()
        
        return result
    
    def _create_essential_files(self):
        """必須ファイルを作成"""
        # __init__.py ファイルを各Pythonパッケージディレクトリに作成
        python_dirs = [
            "app", "app/Http", "app/Http/Controllers", "app/Models", 
            "app/Services", "app/Console", "bootstrap", "config", "routes"
        ]
        
        for dir_path in python_dirs:
            init_file = self.project_root / dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                print(f"✅ 作成: {dir_path}/__init__.py")
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """コード品質をチェック"""
        result = {"checks": [], "errors": [], "warnings": []}
        
        # Python構文チェック
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    compile(content, str(py_file), 'exec')
                result["checks"].append(f"✅ 構文OK: {py_file.relative_to(self.project_root)}")
            except SyntaxError as e:
                error_msg = f"構文エラー in {py_file.relative_to(self.project_root)}: {e}"
                result["errors"].append(error_msg)
                print(f"❌ {error_msg}")
            except Exception as e:
                warning_msg = f"チェック警告 in {py_file.relative_to(self.project_root)}: {e}"
                result["warnings"].append(warning_msg)
        
        return result
    
    def _run_functional_tests(self) -> Dict[str, Any]:
        """機能テストを実行"""
        result = {"tests": [], "passed": 0, "failed": 0, "errors": []}
        
        # Artisanコマンドテスト
        artisan_tests = [
            (["./artisan", "--help"], "Artisan help"),
            (["./artisan", "route:list"], "Route listing"),
        ]
        
        for cmd, description in artisan_tests:
            try:
                proc = subprocess.run(cmd, cwd=self.project_root, 
                                    capture_output=True, text=True, timeout=30)
                if proc.returncode == 0:
                    result["tests"].append(f"✅ {description}")
                    result["passed"] += 1
                else:
                    result["tests"].append(f"❌ {description}: {proc.stderr}")
                    result["failed"] += 1
            except Exception as e:
                error_msg = f"{description}: {e}"
                result["errors"].append(error_msg)
                result["failed"] += 1
                print(f"❌ テストエラー: {error_msg}")
        
        return result
    
    def _run_performance_tests(self) -> Dict[str, Any]:
        """パフォーマンステストを実行"""
        result = {"metrics": [], "recommendations": []}
        
        # ファイルサイズチェック
        large_files = []
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and file_path.stat().st_size > 1024 * 1024:  # 1MB以上
                large_files.append(f"{file_path.relative_to(self.project_root)} ({file_path.stat().st_size // 1024}KB)")
        
        if large_files:
            result["recommendations"].append(f"大きなファイル発見: {', '.join(large_files)}")
        
        # ディスク使用量
        total_size = sum(f.stat().st_size for f in self.project_root.rglob("*") if f.is_file())
        result["metrics"].append(f"プロジェクト総サイズ: {total_size // 1024}KB")
        
        return result
    
    def _run_security_checks(self) -> Dict[str, Any]:
        """セキュリティチェックを実行"""
        result = {"checks": [], "issues": [], "recommendations": []}
        
        # .envファイルの存在チェック
        env_file = self.project_root / ".env"
        if env_file.exists():
            result["checks"].append("✅ .envファイル存在")
            # .envファイルがGitignoreされているかチェック
            gitignore = self.project_root / ".gitignore"
            if gitignore.exists():
                with open(gitignore, 'r') as f:
                    if ".env" in f.read():
                        result["checks"].append("✅ .envファイルがGitignoreに記載")
                    else:
                        result["issues"].append("⚠️ .envファイルをGitignoreに追加推奨")
        else:
            result["recommendations"].append("💡 .envファイルの作成を推奨")
        
        # パスワードやAPIキーの平文チェック（簡易版）
        sensitive_patterns = ["password", "api_key", "secret", "token"]
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    for pattern in sensitive_patterns:
                        if f'"{pattern}"' in content or f"'{pattern}'" in content:
                            result["issues"].append(f"⚠️ 平文の機密情報の可能性: {py_file.relative_to(self.project_root)}")
            except:
                pass
        
        return result
    
    def _auto_fix_issues(self, pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        """自動修正を実行"""
        result = {"fixes_applied": [], "manual_fixes_needed": []}
        
        # 構造の問題を修正
        structure_issues = pipeline_results["stages"]["structure"]["errors"]
        for issue in structure_issues:
            # 自動修正ロジックをここに追加
            result["manual_fixes_needed"].append(f"構造問題: {issue}")
        
        # コード品質の問題を修正
        quality_errors = pipeline_results["stages"]["quality"]["errors"]
        for error in quality_errors:
            result["manual_fixes_needed"].append(f"コード品質: {error}")
        
        return result
    
    def _generate_ci_report(self, pipeline_results: Dict[str, Any]):
        """CI/CDレポートを生成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"ci_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(pipeline_results, f, indent=2, ensure_ascii=False)
        
        # HTMLレポートも生成
        html_report = self._generate_html_report(pipeline_results)
        html_file = self.reports_dir / f"ci_report_{timestamp}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"\n📊 CI/CDレポート生成完了:")
        print(f"  JSON: {report_file}")
        print(f"  HTML: {html_file}")
    
    def _generate_html_report(self, results: Dict[str, Any]) -> str:
        """HTMLレポートを生成"""
        html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD Report - {results['timestamp']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .stage {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007acc; }}
        .success {{ border-left-color: #28a745; }}
        .warning {{ border-left-color: #ffc107; }}
        .error {{ border-left-color: #dc3545; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>🚀 CI/CD Pipeline Report</h1>
    <p><strong>実行日時:</strong> {results['timestamp']}</p>
    
    <h2>📊 サマリー</h2>
"""
        
        for stage_name, stage_data in results["stages"].items():
            html += f"""
    <div class="stage">
        <h3>📁 {stage_name.title()}</h3>
        <pre>{json.dumps(stage_data, indent=2, ensure_ascii=False)}</pre>
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html

def main():
    """メイン実行関数"""
    project_root = Path(__file__).parent
    
    ci_system = ContinuousIntegrationSystem(project_root)
    results = ci_system.run_full_ci_pipeline()
    
    # 最終サマリー
    print("\n🎯 CI/CDパイプライン完了!")
    print("=" * 60)
    
    total_issues = 0
    for stage_data in results["stages"].values():
        if "errors" in stage_data:
            total_issues += len(stage_data["errors"])
    
    if total_issues == 0:
        print("✅ すべてのチェックが通りました！")
    else:
        print(f"⚠️ {total_issues}件の問題が見つかりました。詳細はレポートを確認してください。")

if __name__ == "__main__":
    main()
