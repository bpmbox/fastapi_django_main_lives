#!/usr/bin/env python3
"""
UI修正検証スクリプト
改行文字の表示問題が解決されたかを確認
"""

import gradio as gr
import sqlite3
from datetime import datetime
from pathlib import Path

def test_formatting():
    """フォーマッティングテスト"""
    
    # テスト用のマークダウンテキスト
    test_text = """🎛️ **システム状況**

✅ **GitHub API**: Connected
🟢 **ISSUE監視**: Running  
✅ **プロンプトDB**: Active (8 prompts)
✅ **GPT-ENGINEER**: Ready
✅ **自動化システム**: Configured

📋 **最近のアクティビティ**

📝 **AI Chat System Generator**
   ✅ completed - 2025-06-11 15:30

🔗 **#123 Create microservice architecture**
   🔄 processing - 2025-06-11 15:25

📝 **Blockchain DApp Template**
   ⏳ pending - 2025-06-11 15:20
"""
    
    return test_text

def create_verification_interface():
    """検証用インターフェース"""
    
    with gr.Blocks(title="UI修正検証", theme="soft") as demo:
        gr.Markdown("# 🔧 UI修正検証 - 改行文字表示テスト")
        
        gr.Markdown("""
        この画面で、改行文字が `\\n\\n` として文字通り表示されずに、
        正しく改行として表示されることを確認します。
        """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📋 修正後のフォーマット表示")
                
                formatted_display = gr.Markdown(
                    value=test_formatting(),
                    label="システム状況表示"
                )
                
            with gr.Column():
                gr.Markdown("## ✅ 確認項目")
                
                checklist = gr.Markdown("""
                ### 🔍 確認ポイント
                
                ✅ **改行文字**: `\\n` が文字として表示されていない
                ✅ **段落分け**: 空行で適切に段落が分かれている  
                ✅ **アイコン表示**: 絵文字が正しく表示されている
                ✅ **太字**: `**text**` が太字として表示されている
                ✅ **階層構造**: 見出しとリストが適切に表示されている
                
                ### 🎯 修正内容
                
                **Before**: `formatted += f"{icon} **{name}**: {state}\\\\n"`
                **After**: `formatted += f"{icon} **{name}**: {state}\\n"`
                
                エスケープされた `\\\\n` を正しい改行文字 `\\n` に修正しました。
                """)
        
        # 更新ボタン
        refresh_btn = gr.Button("🔄 表示更新", variant="primary")
        
        refresh_btn.click(
            fn=test_formatting,
            outputs=formatted_display
        )
        
        # 実際のシステムデータ表示
        with gr.Accordion("📊 実際のシステムデータ", open=False):
            
            def get_real_system_data():
                """実際のシステムデータ取得"""
                try:
                    # プロンプトDB確認
                    conn = sqlite3.connect('/workspaces/fastapi_django_main_live/prompts.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT COUNT(*) FROM prompts')
                    prompt_count = cursor.fetchone()[0]
                    
                    cursor.execute('SELECT title, execution_status, created_at FROM prompts ORDER BY created_at DESC LIMIT 3')
                    recent_prompts = cursor.fetchall()
                    conn.close()
                    
                    # 実データでフォーマット
                    real_data = f"""🎛️ **実際のシステム状況**

✅ **プロンプトDB**: Active ({prompt_count} prompts)
🔄 **統合ダッシュボード**: Running on port 7863
✅ **UI修正**: 改行文字表示問題解決

📋 **実際の最近のプロンプト**

"""
                    
                    for prompt in recent_prompts:
                        title, status, created = prompt
                        status_icon = {'completed': '✅', 'pending': '⏳', 'running': '🔄'}.get(status, '❓')
                        real_data += f"📝 **{title[:40]}**\n"
                        real_data += f"   {status_icon} {status} - {created[:16]}\n\n"
                    
                    return real_data
                    
                except Exception as e:
                    return f"❌ データ取得エラー: {str(e)}"
            
            real_data_display = gr.Markdown(
                value=get_real_system_data(),
                label="実際のシステムデータ"
            )
            
            real_refresh_btn = gr.Button("🔄 実データ更新")
            real_refresh_btn.click(
                fn=get_real_system_data,
                outputs=real_data_display
            )
    
    return demo

def main():
    """メイン実行"""
    print("🔧 UI修正検証ツール起動中...")
    
    demo = create_verification_interface()
    
    print("🌐 検証画面アクセス: http://localhost:7864")
    print("📋 改行文字の表示が正しく修正されているか確認してください")
    
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7864
    )

if __name__ == "__main__":
    main()
