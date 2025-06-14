#!/usr/bin/env python3
"""
プロンプト生成ツール
===================

新しいGitHub Copilotセッション用のコンテキストプロンプトを生成

使用方法:
    python generate_prompt.py
    python generate_prompt.py --type summary --limit 10
    python generate_prompt.py --type context --sessions 5 --conversations 8
"""

import argparse
import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from controllers.conversation_history import ConversationManager

def main():
    parser = argparse.ArgumentParser(description="GitHub Copilot用コンテキストプロンプト生成")
    parser.add_argument(
        "--type", 
        choices=["summary", "context", "technical"],
        default="context",
        help="生成するプロンプトのタイプ"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=10,
        help="会話履歴の取得件数"
    )
    parser.add_argument(
        "--sessions", 
        type=int, 
        default=5,
        help="セッション履歴の取得件数"
    )
    parser.add_argument(
        "--conversations", 
        type=int, 
        default=8,
        help="詳細表示する会話数"
    )
    parser.add_argument(
        "--output", 
        help="出力ファイル名 (省略時は標準出力)"
    )
    
    args = parser.parse_args()
    
    # ConversationManager初期化
    try:
        manager = ConversationManager()
        
        # プロンプト生成
        if args.type == "summary":
            prompt = manager.generate_prompt_summary(limit=args.limit)
        elif args.type == "context":
            prompt = manager.generate_context_prompt(
                session_limit=args.sessions,
                detail_limit=args.conversations
            )
        elif args.type == "technical":
            # 技術フォーカス版
            base_prompt = manager.generate_context_prompt(args.sessions, args.conversations)
            tech_header = """<technical-context>
## TECHNICAL DEVELOPMENT CONTEXT

**FOCUS**: ContBK統合システム、SQLite会話履歴、Gradioインターフェース開発

**ACTIVE TOOLS**: 
- Gradio 4.31.5 (推奨: 4.44.1)
- SQLite3 (会話履歴管理)  
- Python 3.11
- Git (バージョン管理)
- FastAPI + Django (バックエンド)

**CURRENT ENVIRONMENT**:
- Workspace: /workspaces/fastapi_django_main_live
- Port 7860: メインアプリケーション
- Port 7870-7880: 開発用サブアプリ

</technical-context>

"""
            prompt = tech_header + base_prompt
        
        # 出力
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"✅ プロンプトを {args.output} に保存しました")
        else:
            print("=" * 80)
            print("🎯 GitHub Copilot用コンテキストプロンプト")
            print("=" * 80)
            print(prompt)
            print("=" * 80)
            print("📋 上記のテキストを新しいセッションの最初にコピー&ペーストしてください")
        
    except Exception as e:
        print(f"❌ エラー: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
