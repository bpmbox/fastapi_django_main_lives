import gradio as gr
import importlib
import os
import sys
import traceback
from typing import List, Tuple, Dict, Any

def create_simple_interfaces() -> Tuple[List[Any], List[str]]:
    """
    シンプルなテスト用インターフェースを作成
    """
    interfaces = []
    names = []
    
    # 1. テキスト処理インターフェース
    def text_processor(text):
        return f"処理結果: {text.upper()}"
    
    text_interface = gr.Interface(
        fn=text_processor,
        inputs=gr.Textbox(label="テキスト入力", placeholder="何か入力してください"),
        outputs=gr.Textbox(label="処理結果"),
        title="テキスト処理",
        description="入力されたテキストを大文字に変換します"
    )
    
    # 2. 計算機インターフェース
    def calculator(num1, operation, num2):
        try:
            if operation == "足し算":
                result = num1 + num2
            elif operation == "引き算":
                result = num1 - num2
            elif operation == "掛け算":
                result = num1 * num2
            elif operation == "割り算":
                result = num1 / num2 if num2 != 0 else "エラー: ゼロ除算"
            else:
                result = "不明な演算"
            return f"{num1} {operation} {num2} = {result}"
        except Exception as e:
            return f"エラー: {str(e)}"
    
    calc_interface = gr.Interface(
        fn=calculator,
        inputs=[
            gr.Number(label="数値1", value=0),
            gr.Dropdown(["足し算", "引き算", "掛け算", "割り算"], label="演算"),
            gr.Number(label="数値2", value=0)
        ],
        outputs=gr.Textbox(label="計算結果"),
        title="簡単計算機",
        description="2つの数値で四則演算を行います"
    )
    
    # 3. ファイル情報表示インターフェース
    def file_info(file):
        if file is None:
            return "ファイルが選択されていません"
        
        file_path = file.name
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        return f"""
        ファイル名: {file_name}
        ファイルサイズ: {file_size} bytes
        ファイルパス: {file_path}
        """
    
    file_interface = gr.Interface(
        fn=file_info,
        inputs=gr.File(label="ファイルを選択"),
        outputs=gr.Textbox(label="ファイル情報"),
        title="ファイル情報表示",
        description="アップロードされたファイルの情報を表示します"
    )
    
    interfaces = [text_interface, calc_interface, file_interface]
    names = ["📝 テキスト処理", "🧮 計算機", "📁 ファイル情報"]
    
    return interfaces, names

def load_working_contbk_interfaces() -> Tuple[List[Any], List[str]]:
    """
    動作確認済みのcontbkインターフェースのみを読み込み
    """
    interfaces = []
    names = []
    
    # 動作確認済みのインターフェースリスト
    working_modules = [
        ("gra_09_weather.weather", "🌤️ 天気予報"),
        ("gra_11_multimodal.image_to_ui", "🖼️ マルチモーダル"),
        ("gra_10_frontend.frontend_generator", "🎨 フロントエンド生成"),
    ]
    
    # パスを追加
    contbk_path = "/workspaces/fastapi_django_main_live/contbk"
    main_path = "/workspaces/fastapi_django_main_live"
    
    if contbk_path not in sys.path:
        sys.path.insert(0, contbk_path)
    if main_path not in sys.path:
        sys.path.insert(0, main_path)
    
    for module_name, display_name in working_modules:
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
            continue
    
    return interfaces, names

def create_welcome_tab() -> gr.Blocks:
    """ウェルカムタブを作成"""
    with gr.Blocks() as welcome:
        gr.Markdown("""
        # 🎯 ContBK インターフェース ダッシュボード
        
        このダッシュボードでは、`contbk`フォルダーにある全ての Gradio インターフェースにアクセスできます。
        
        ## 📋 利用可能な機能:
        
        各タブには以下のような機能が含まれています：
        
        ### 🔧 基本機能:
        - **📝 テキスト処理**: テキストの変換・処理
        - **🧮 計算機**: 基本的な四則演算
        - **📁 ファイル情報**: ファイル情報の表示
        
        ### 🚀 高度な機能 (contbkから):
        - **🌤️ 天気予報**: 天気情報の取得・表示
        - **🖼️ マルチモーダル**: 画像とテキストの処理
        - **🎥 ビデオ処理**: 動画ファイルの処理
        - **🎨 フロントエンド生成**: UIコードの自動生成
        
        ## 🚀 使い方:
        1. 上部のタブから使いたい機能を選択
        2. 各タブの指示に従って操作
        3. 必要に応じて設定やパラメータを調整
        
        ## 📞 サポート:
        - 各機能の詳細は対応するタブで確認できます
        - 問題が発生した場合は、エラーメッセージを確認してください
        """)
        
        # システム情報を表示
        with gr.Accordion("🔧 システム情報", open=False):
            gr.Markdown(f"""
            **Python バージョン**: {sys.version}
            **ContBK パス**: /workspaces/fastapi_django_main_live/contbk
            **現在時刻**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """)
    
    return welcome

def create_error_tab(error_message: str) -> gr.Blocks:
    """エラータブを作成"""
    with gr.Blocks() as error_tab:
        gr.Markdown(f"""
        # ❌ エラーが発生しました
        
        ```
        {error_message}
        ```
        
        ## 🔧 トラブルシューティング:
        1. contbkフォルダーが存在することを確認
        2. 各モジュールが正しくインストールされていることを確認
        3. Pythonパスが正しく設定されていることを確認
        """)
    return error_tab

def create_tabbed_interface() -> gr.TabbedInterface:
    """
    シンプル機能とcontbkフォルダーのインターフェースを統合したタブ表示を作成
    """
    try:
        # ウェルカムタブ
        welcome_tab = create_welcome_tab()
        
        # シンプルなインターフェース
        simple_interfaces, simple_names = create_simple_interfaces()
        
        # 動作するcontbkインターフェース
        contbk_interfaces, contbk_names = load_working_contbk_interfaces()
        
        # 全て統合
        all_interfaces = [welcome_tab] + simple_interfaces + contbk_interfaces
        all_names = ["🏠 ホーム"] + simple_names + contbk_names
        
        if len(all_interfaces) == 1:  # ウェルカムタブのみの場合
            error_tab = create_error_tab("インターフェースの読み込みに失敗しました。")
            all_interfaces.append(error_tab)
            all_names.append("❌ エラー")
        
        # タブ付きインターフェースを作成
        tabs = gr.TabbedInterface(
            all_interfaces,
            all_names,
            title="🎯 ContBK ダッシュボード"
        )
        
        print(f"📊 Total tabs created: {len(all_interfaces)}")
        return tabs
        
    except Exception as e:
        print(f"❌ Failed to create tabbed interface: {str(e)}")
        traceback.print_exc()
        
        # エラーの場合、基本的なインターフェースを返す
        error_tab = create_error_tab(str(e))
        welcome_tab = create_welcome_tab()
        
        return gr.TabbedInterface(
            [welcome_tab, error_tab],
            ["🏠 ホーム", "❌ エラー"],
            title="🎯 ContBK ダッシュボード (エラー)"
        )

# メインのgradio_interfaceを作成
# gradio_interface = create_tabbed_interface()  # 無効化：重複を防ぐため

# スタンドアロン実行用（テスト用）
if __name__ == "__main__":
    print("🚀 ContBK ダッシュボードを起動中...")
    gradio_interface = create_tabbed_interface()  # テスト実行時のみ
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7863,  # 別のポートを使用
        share=False,
        debug=True
    )
