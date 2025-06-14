import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion
import os
import importlib
import pkgutil

def get_system_features():
    """システムの機能一覧を取得"""
    features = {
        "スタート": [
            "🚀 初心者ガイド - システムの使い方を学ぶ",
            "📖 チュートリアル - ステップバイステップガイド"
        ],
        "チャット": [
            "💬 AIチャット - 汎用AI対話",
            "🤖 OpenInterpreter - コード実行付きAI",
            "💭 会話履歴 - 過去の対話を確認"
        ],
        "AI作成": [
            "🤖 プログラム生成 - 仕様からコード自動生成",
            "🔧 RPA自動化 - 作業の自動化",
            "🐙 GitHub Issue作成 - 自動でIssue生成",
            "🎨 フロントエンド生成 - React/Vue自動作成",
            "🖼️ 画像からUI生成 - 画像をコードに変換"
        ],
        "文書作成": [
            "📄 ドキュメント生成 - 技術文書の自動作成",
            "💾 プロンプト管理 - AIプロンプトの管理",
            "📝 記録システム - 作業ログの管理"
        ],
        "管理": [
            "📊 統合ダッシュボード - システム全体の管理",
            "🎯 承認システム - ワークフロー管理",
            "🚀 Dify管理 - AI環境の管理"
        ],
        "開発": [
            "🔧 システム診断 - エラーチェック",
            "✨ メモリ復元 - AI記憶の管理",
            "🧪 テストシステム - 自動テスト実行"
        ],
        "その他": [
            "📁 ファイル管理 - ファイルのアップロード・管理",
            "🗄️ データベース - データの管理・操作",
            "🌐 HTML表示 - Webページの表示",
            "🌤️ 天気予報 - 天気情報の取得"
        ]
    }
    return features

def format_features_for_chat():
    """チャット用に機能一覧をフォーマット"""
    features = get_system_features()
    formatted = "# 🚀 AI-Human協働開発システム 機能一覧\n\n"
    
    for category, items in features.items():
        formatted += f"## {category}\n"
        for item in items:
            formatted += f"- {item}\n"
        formatted += "\n"
    
    formatted += "💡 **使い方**: 上記の機能について質問したり、実行したい機能を教えてください！\n"
    formatted += "例：「プログラム生成機能の使い方を教えて」「GitHub Issueを作成したい」"
    
    return formatted

def enhanced_chat_with_system_info(message, history):
    """システム情報を含めた拡張チャット"""
    # システム機能に関する質問かチェック
    if any(keyword in message.lower() for keyword in ['機能', '使い方', '一覧', 'ヘルプ', 'help']):
        return format_features_for_chat()
    
    # 通常のAIチャット
    return completion(message, history)

# カスタムCSS
css = """
.feature-list {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    margin: 10px 0;
}
.category-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
}
"""

# Gradioインターフェースの作成
with gr.Blocks(css=css, title="🚀 システムナビゲーター") as gradio_interface:
    gr.Markdown("# 🚀 AI-Human協働開発システム ナビゲーター")
    gr.Markdown("### 💬 機能の説明・実行をチャットで簡単に！")
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                height=500,
                placeholder="🤖 システムの機能について何でも聞いてください！\n\n例：\n- 「機能一覧を教えて」\n- 「プログラム生成の使い方は？」\n- 「GitHub Issueを作成したい」",
                label="システムナビゲーター"
            )
            
            msg = gr.Textbox(
                placeholder="システムの機能について質問してください...",
                label="メッセージ",
                lines=2
            )
            
            with gr.Row():
                submit_btn = gr.Button("送信", variant="primary")
                clear_btn = gr.Button("クリア")
        
        with gr.Column(scale=1):
            gr.Markdown("### 📋 クイックガイド")
            
            features = get_system_features()
            for category, items in list(features.items())[:3]:  # 最初の3カテゴリのみ表示
                with gr.Group():
                    gr.Markdown(f"**{category}**")
                    for item in items[:2]:  # 各カテゴリから2項目
                        gr.Markdown(f"• {item}")
            
            gr.Markdown("💡 詳細は左のチャットで「機能一覧」と聞いてください")
    
    # チャット機能の設定
    def respond(message, chat_history):
        bot_message = enhanced_chat_with_system_info(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])
    
    # よく使う質問のサンプル
    gr.Examples(
        examples=[
            ["機能一覧を教えて"],
            ["プログラム生成機能の使い方は？"],
            ["GitHub Issueを作成したい"],
            ["チャット機能の種類は？"],
            ["AI作成機能について詳しく"],
            ["初心者におすすめの機能は？"]
        ],
        inputs=msg,
        label="💡 よく使う質問"
    )

# 自動検出システム用のメタデータ
interface_title = "🧭 システムナビゲーター"
interface_description = "システム機能の説明・実行をチャットで簡単に"
