#!/usr/bin/env python3
"""
AI記憶復元プロンプト自動生成
============================

新しいチャットセッションで使用する、
AI記憶復元のための最適化されたプロンプトを自動生成します。
"""

import requests
import datetime
import subprocess
import os

def fetch_wiki_content():
    """GitHub WikiからAI記憶復元用コンテンツを取得"""
    
    wiki_pages = {
        "Continuity-Guide": "https://raw.githubusercontent.com/wiki/miyataken999/fastapi_django_main_live/Continuity-Guide.md",
        "System-Architecture": "https://raw.githubusercontent.com/wiki/miyataken999/fastapi_django_main_live/System-Architecture.md",
        "Implemented-Features": "https://raw.githubusercontent.com/wiki/miyataken999/fastapi_django_main_live/Implemented-Features.md",
        "AI-Collaboration-Guide": "https://raw.githubusercontent.com/wiki/miyataken999/fastapi_django_main_live/AI-Developer-Collaboration-Guide.md"
    }
    
    content = {}
    
    for name, url in wiki_pages.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content[name] = response.text
                print(f"✅ {name} 取得成功")
            else:
                print(f"❌ {name} 取得失敗: {response.status_code}")
                content[name] = f"❌ 取得失敗 (Status: {response.status_code})"
        except Exception as e:
            print(f"⚠️ {name} エラー: {e}")
            content[name] = f"⚠️ 取得エラー: {e}"
    
    return content

def get_project_status():
    """現在のプロジェクト状況を取得"""
    
    try:
        os.chdir("/workspaces/fastapi_django_main_live")
        
        # Git情報
        git_status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        ).stdout
        
        git_log = subprocess.run(
            ["git", "log", "--oneline", "-3"],
            capture_output=True, text=True
        ).stdout
        
        # Issue情報
        try:
            issues = subprocess.run(
                ["gh", "issue", "list", "--state", "all", "--limit", "10"],
                capture_output=True, text=True
            ).stdout
        except:
            issues = "GitHub CLI not available"
        
        return {
            "git_status": git_status.strip(),
            "git_log": git_log.strip(),
            "issues": issues.strip()
        }
        
    except Exception as e:
        return {"error": str(e)}

def generate_memory_restoration_prompt():
    """記憶復元用プロンプト生成"""
    
    print("🧠 AI記憶復元プロンプト生成開始...")
    
    # Wiki情報取得
    wiki_content = fetch_wiki_content()
    
    # プロジェクト状況取得
    project_status = get_project_status()
    
    # プロンプト生成
    prompt = f"""🧠 **AI記憶復元プロンプト** - {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')}

こんにちは！私は新しいチャットセッションのGitHub Copilotです。
以下のナレッジを読んで、前任AIの記憶を完全に引き継ぎます。

## 📚 引き継ぐ重要なナレッジ

### 🔄 AI継続ガイド (最重要)
{wiki_content.get('Continuity-Guide', '取得失敗')[:3000]}...

### 🏗️ システムアーキテクチャ
{wiki_content.get('System-Architecture', '取得失敗')[:2000]}...

### 📋 実装済み機能
{wiki_content.get('Implemented-Features', '取得失敗')[:2000]}...

### 🤖 AI協働開発ガイド
{wiki_content.get('AI-Collaboration-Guide', '取得失敗')[:1500]}...

## 📊 現在のプロジェクト状況

### Git状況
```
最新コミット:
{project_status.get('git_log', 'N/A')}

変更ファイル:
{project_status.get('git_status', 'なし')}
```

### Issue状況
```
{project_status.get('issues', 'N/A')}
```

## ✅ 記憶復元完了確認

私は以下を理解・記憶しました：

1. **プロジェクト概要**: FastAPI Django Main Live - AI協働開発プロジェクト
2. **開発者**: miyatakenさん（人間）+ GitHub Copilot（AI）の協働
3. **核心機能**: 
   - 🏠 ContBK統合ダッシュボード
   - 🐙 GitHub Issue自動作成
   - 🖼️ RPA画像取得機能
   - 🤖 OpenInterpreter統合
   - 🔧 VS Code デバッグ環境

4. **技術思想**: 
   - AI指示での自動機能追加
   - 命名規則による自動統合（gradio_interface, router）
   - プラグイン式アーキテクチャ
   - ゼロ設定ファイル

5. **協働スタイル**: 
   - 自然言語での要求・実装
   - 継続的改善
   - 実用性重視
   - miyatakenさんとの対等なパートナーシップ

## 🎯 復元確認メッセージ

**miyatakenさん、お疲れさまです！**

前任AIの記憶を完全に引き継ぎました。私たちが一緒に構築してきた素晴らしいFastAPI Django Main Liveプロジェクトの開発を継続させてください！

現在の実装状況、進行中のIssue、今後の開発方向性など、何でもお聞かせください。前任AIと同じように、効率的で実用的な開発を一緒に進めさせていただきます。

🚀 何から始めましょうか？

---

**記憶復元日時**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
**GitHub Wiki**: https://github.com/miyataken999/fastapi_django_main_live/wiki
**継続ガイド**: https://github.com/miyataken999/fastapi_django_main_live/wiki/Continuity-Guide
"""
    
    return prompt

def save_restoration_prompt():
    """記憶復元プロンプトをファイルに保存"""
    
    prompt = generate_memory_restoration_prompt()
    
    # ファイル保存
    output_file = "/workspaces/fastapi_django_main_live/docs/ai_memory_restoration_prompt.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"✅ 記憶復元プロンプト保存完了: {output_file}")
    
    # ファイルサイズ確認
    import os
    file_size = os.path.getsize(output_file)
    print(f"📏 ファイルサイズ: {file_size:,} bytes")
    
    return output_file, prompt

if __name__ == "__main__":
    print("🧠 AI記憶復元プロンプト自動生成")
    print("=" * 50)
    
    output_file, prompt = save_restoration_prompt()
    
    print(f"\n📋 使用方法:")
    print(f"1. 新しいチャットセッションを開始")
    print(f"2. 以下のファイル内容をコピー&ペースト:")
    print(f"   {output_file}")
    print(f"3. AIが記憶を復元して開発継続可能！")
    
    print(f"\n🎯 記憶復元プロンプト生成完了！")
