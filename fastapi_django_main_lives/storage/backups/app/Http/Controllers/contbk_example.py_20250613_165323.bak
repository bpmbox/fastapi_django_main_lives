"""
ContBK インターフェース統合例
=========================

このファイルは、contbkフォルダーにある全てのGradioインターフェースを
タブ表示で統合する例を示しています。

使用方法:
1. このファイルを controllers フォルダーに配置
2. メインアプリケーションから gradio_interface をインポート
3. 自動的にcontbkフォルダーのインターフェースがタブ表示される
"""

import gradio as gr
import importlib
import os
import sys
import traceback
from typing import List, Tuple, Any

print("🔧 Starting contbk_example module...")

def create_demo_interfaces() -> Tuple[List[Any], List[str]]:
    """
    デモ用のシンプルなインターフェースを作成
    """
    print("📝 Creating demo interfaces...")
    interfaces = []
    names = []
    
    # 1. テキスト変換ツール
    def text_transformer(text, operation):
        if operation == "大文字変換":
            return text.upper()
        elif operation == "小文字変換":
            return text.lower()
        elif operation == "文字数カウント":
            return f"文字数: {len(text)}文字"
        elif operation == "逆順変換":
            return text[::-1]
        else:
            return text
    
    text_interface = gr.Interface(
        fn=text_transformer,
        inputs=[
            gr.Textbox(label="テキスト入力", placeholder="変換したいテキストを入力"),
            gr.Dropdown(
                ["大文字変換", "小文字変換", "文字数カウント", "逆順変換"], 
                label="変換タイプ",
                value="大文字変換"
            )
        ],
        outputs=gr.Textbox(label="変換結果"),
        title="📝 テキスト変換ツール",
        description="様々なテキスト変換を行います"
    )
    
    # 2. 簡単計算機
    def simple_calculator(a, operation, b):
        try:
            if operation == "+":
                result = a + b
            elif operation == "-":
                result = a - b
            elif operation == "×":
                result = a * b
            elif operation == "÷":
                result = a / b if b != 0 else "エラー: ゼロ除算"
            else:
                result = "不明な演算"
            
            return f"{a} {operation} {b} = {result}"
        except Exception as e:
            return f"エラー: {str(e)}"
    
    calc_interface = gr.Interface(
        fn=simple_calculator,
        inputs=[
            gr.Number(label="数値 A", value=10),
            gr.Dropdown(["+", "-", "×", "÷"], label="演算子", value="+"),
            gr.Number(label="数値 B", value=5)
        ],
        outputs=gr.Textbox(label="計算結果"),
        title="🧮 簡単計算機",
        description="基本的な四則演算を行います"
    )
    
    # 3. リスト生成ツール
    def list_generator(items_text, separator, list_type):
        if not items_text.strip():
            return "項目を入力してください"
        
        items = [item.strip() for item in items_text.split(separator) if item.strip()]
        
        if list_type == "番号付きリスト":
            result = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
        elif list_type == "ブレットリスト":
            result = "\n".join([f"• {item}" for item in items])
        elif list_type == "チェックリスト":
            result = "\n".join([f"☐ {item}" for item in items])
        else:
            result = "\n".join(items)
        
        return result
    
    list_interface = gr.Interface(
        fn=list_generator,
        inputs=[
            gr.Textbox(
                label="項目入力", 
                lines=5,
                placeholder="項目1,項目2,項目3\n（または改行区切り）"
            ),
            gr.Dropdown([",", "\n", ";", "|"], label="区切り文字", value=","),
            gr.Dropdown(
                ["番号付きリスト", "ブレットリスト", "チェックリスト", "プレーンリスト"], 
                label="リスト形式",
                value="番号付きリスト"
            )
        ],
        outputs=gr.Textbox(label="生成されたリスト", lines=10),
        title="📋 リスト生成ツール",
        description="テキストから様々な形式のリストを生成します"
    )
    
    interfaces = [text_interface, calc_interface, list_interface]
    names = ["📝 テキスト変換", "🧮 計算機", "📋 リスト生成"]
    
    return interfaces, names

def load_contbk_interfaces() -> Tuple[List[Any], List[str]]:
    """
    contbkフォルダーから動作するGradioインターフェースを読み込み
    """
    print("📂 Loading contbk interfaces...")
    interfaces = []
    names = []
    
    # contbkパスの設定
    contbk_path = "/workspaces/fastapi_django_main_live/contbk"
    main_path = "/workspaces/fastapi_django_main_live"
    
    # パスを追加
    if contbk_path not in sys.path:
        sys.path.insert(0, contbk_path)
    if main_path not in sys.path:
        sys.path.insert(0, main_path)
    
    # 動作確認済みのモジュール（依存関係の問題がないもの）
    stable_modules = [
        ("gra_09_weather.weather", "🌤️ 天気予報"),
        ("gra_10_frontend.frontend_generator", "🎨 フロントエンド生成"),
        ("gra_11_multimodal.image_to_ui", "🖼️ マルチモーダル"),
    ]
    
    for module_name, display_name in stable_modules:
        try:
            print(f"🔍 Loading {module_name}...")
            module = importlib.import_module(module_name)
            
            if hasattr(module, 'gradio_interface'):
                interfaces.append(module.gradio_interface)
                names.append(display_name)
                print(f"✅ Successfully loaded: {display_name}")
            else:
                print(f"⚠️ No gradio_interface found in {module_name}")
                
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {str(e)}")
            # エラーの詳細をログに出力（デバッグ用）
            if "mysite" not in str(e):  # mysite関連エラー以外は詳細表示
                traceback.print_exc()
    
    return interfaces, names

def create_info_tab() -> gr.Blocks:
    """情報・ヘルプタブを作成"""
    print("ℹ️ Creating info tab...")
    with gr.Blocks() as info_tab:
        gr.Markdown("""
        # 🎯 ContBK ダッシュボード
        
        ## 📖 概要
        このダッシュボードは、`contbk`フォルダーにある様々なGradioインターフェースを
        統合して表示するサンプル実装です。
        
        ## 🚀 機能紹介
        
        ### 📝 基本ツール
        - **テキスト変換**: 文字の大文字・小文字変換、文字数カウントなど
        - **計算機**: 基本的な四則演算
        - **リスト生成**: テキストから様々な形式のリストを生成
        
        ### 🔧 高度な機能（ContBKから）
        - **天気予報**: 気象情報の取得と表示
        - **フロントエンド生成**: UIコードの自動生成
        - **マルチモーダル**: 画像とテキストの統合処理
        
        ## 💡 開発者向け情報
        
        ### 新しいインターフェースの追加方法
        1. `contbk/` フォルダーに新しいディレクトリを作成
        2. Python ファイル内で `gradio_interface` 変数を定義
        3. このダッシュボードが自動的に検出・表示
        
        ### コード例
        ```python
        import gradio as gr
        
        def my_function(input_text):
            return f"処理結果: {input_text}"
        
        gradio_interface = gr.Interface(
            fn=my_function,
            inputs=gr.Textbox(label="入力"),
            outputs=gr.Textbox(label="出力"),
            title="マイ機能"
        )
        ```
        
        ## 📊 技術仕様
        - **フレームワーク**: Gradio
        - **動的読み込み**: Pythonの`importlib`を使用
        - **エラーハンドリング**: 個別モジュールの失敗が全体に影響しない設計
        """)
        
        # システム状態表示
        with gr.Accordion("🔍 システム情報", open=False):
            def get_system_info():
                import datetime
                contbk_path = "/workspaces/fastapi_django_main_live/contbk"
                folder_count = len([d for d in os.listdir(contbk_path) 
                                  if os.path.isdir(os.path.join(contbk_path, d)) 
                                  and d.startswith('gra_')])
                
                return f"""
                **現在時刻**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
                **Python バージョン**: {sys.version.split()[0]}
                **ContBK パス**: {contbk_path}
                **ContBK フォルダー数**: {folder_count}個
                **Gradio バージョン**: {gr.__version__}
                """
            
            gr.Markdown(get_system_info())
            
            # リフレッシュボタン
            refresh_btn = gr.Button("🔄 情報を更新")
            system_info_display = gr.Markdown(get_system_info())
            
            refresh_btn.click(
                fn=get_system_info,
                outputs=system_info_display
            )
    
    return info_tab

def create_unified_dashboard() -> gr.TabbedInterface:
    """
    統合ダッシュボードを作成
    """
    print("🎯 Creating unified dashboard...")
    try:
        # 各種インターフェースを読み込み
        demo_interfaces, demo_names = create_demo_interfaces()
        contbk_interfaces, contbk_names = load_contbk_interfaces()
        info_tab = create_info_tab()
        
        # 全てを統合
        all_interfaces = [info_tab] + demo_interfaces + contbk_interfaces
        all_names = ["ℹ️ 情報"] + demo_names + contbk_names
        
        # タブ付きインターフェースを作成
        dashboard = gr.TabbedInterface(
            all_interfaces,
            all_names,
            title="🎯 ContBK 統合ダッシュボード"
        )
        
        print(f"📊 ダッシュボード作成完了: {len(all_interfaces)}個のタブ")
        return dashboard
        
    except Exception as e:
        print(f"❌ ダッシュボード作成エラー: {str(e)}")
        traceback.print_exc()
        
        # フォールバック: エラー情報のみ表示
        with gr.Blocks() as error_interface:
            gr.Markdown(f"""
            # ❌ エラーが発生しました
            
            ```
            {str(e)}
            ```
            
            システム管理者にお問い合わせください。
            """)
        
        return gr.TabbedInterface(
            [error_interface],
            ["❌ エラー"],
            title="エラー"
        )

print("🚀 Creating gradio_interface...")
# このファイルのメインエクスポート - 美しいタイトル付き
# gradio_interface = create_unified_dashboard()  # 無効化：新しい統合ダッシュボードに移行
print("🚫 gradio_interface disabled - moved to contbk_unified_dashboard.py")

# 自動検出システム用のメタデータ
interface_title = "🎯 ContBK ダッシュボード (旧版)"
interface_description = "ContBKフォルダーの全インターフェースを統合表示"

# テスト実行用
if __name__ == "__main__":
    print("🚀 ContBK統合ダッシュボードを起動中...")
    gradio_interface = create_unified_dashboard()  # テスト実行時のみ
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7864,  # 新しいポート
        share=False,
        debug=True
    )
