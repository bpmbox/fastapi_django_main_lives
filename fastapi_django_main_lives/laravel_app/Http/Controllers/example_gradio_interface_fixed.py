import gradio as gr
import importlib
import os
import sys
import traceback
from typing import List, Tuple, Dict, Any

def load_contbk_interfaces() -> Tuple[List[Any], List[str]]:
    """
    contbkフォルダーから全てのgradio_interfaceを動的に読み込み
    Returns:
        Tuple[List[gradio.Interface], List[str]]: インターフェースとその名前のリスト
    """
    interfaces = []
    names = []
    contbk_path = "/workspaces/fastapi_django_main_live/contbk"
    main_path = "/workspaces/fastapi_django_main_live"
    
    # 必要なパスをsys.pathに追加
    if contbk_path not in sys.path:
        sys.path.insert(0, contbk_path)
    if main_path not in sys.path:
        sys.path.insert(0, main_path)
    
    # contbkフォルダー内の各サブディレクトリをチェック
    for item in os.listdir(contbk_path):
        item_path = os.path.join(contbk_path, item)
        
        # ディレクトリかつ特定の命名規則に従っている場合のみ処理
        if os.path.isdir(item_path) and item.startswith('gra_'):
            try:
                # Pythonファイルを探索
                for file in os.listdir(item_path):
                    if file.endswith('.py') and file != '__init__.py':
                        module_name = f"{item}.{file[:-3]}"
                        
                        try:
                            print(f"🔍 Loading {module_name}...")
                            
                            # モジュールを動的にインポート
                            module = importlib.import_module(module_name)
                            
                            # gradio_interfaceが存在するかチェック
                            if hasattr(module, 'gradio_interface'):
                                interface = module.gradio_interface
                                interface_name = f"{item.replace('gra_', '').replace('_', ' ').title()}"
                                
                                interfaces.append(interface)
                                names.append(interface_name)
                                print(f"✅ Successfully loaded: {interface_name}")
                                break  # 1つのフォルダーから1つのインターフェースのみ
                                
                        except Exception as e:
                            print(f"⚠️ Failed to load {module_name}: {str(e)}")
                            continue
                            
            except Exception as e:
                print(f"❌ Error processing {item}: {str(e)}")
                continue
    
    print(f"📊 Total interfaces loaded: {len(interfaces)}")
    return interfaces, names

def create_welcome_tab() -> gr.Blocks:
    """ウェルカムタブを作成"""
    with gr.Blocks() as welcome:
        gr.Markdown("""
        # 🎯 ContBK インターフェース ダッシュボード
        
        このダッシュボードでは、`contbk`フォルダーにある全ての Gradio インターフェースにアクセスできます。
        
        ## 📋 利用可能な機能:
        
        各タブには以下のような機能が含まれています：
        
        - **💬 Chat**: チャット機能
        - **🤖 Open Interpreter**: オープンインタープリター
        - **📄 Program From Doc**: ドキュメントからプログラム生成
        - **🗄️ Database**: データベース操作
        - **📁 Files**: ファイル管理
        - **🌐 Html**: HTML表示
        - **🌤️ Weather**: 天気予報機能
        - **🎨 Frontend**: フロントエンド生成
        - **🖼️ Multimodal**: マルチモーダル機能
        
        ## 🚀 使用方法:
        
        1. 上部のタブから使用したい機能を選択
        2. 各インターフェースの指示に従って操作
        3. 必要に応じてファイルのアップロードや設定を行う
        
        ## 📞 サポート:
        
        問題が発生した場合は、各インターフェースのドキュメントを参照するか、
        開発チームにお問い合わせください。
        """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📊 システム情報")
                
                def get_system_status():
                    return f"""
                    **Python バージョン**: {sys.version}
                    **ContBK パス**: /workspaces/fastapi_django_main_live/contbk
                    **利用可能なインターフェース数**: {len(load_contbk_interfaces()[0])}
                    """
                
                gr.Markdown(get_system_status())
                
    return welcome

def create_error_tab(error_message: str) -> gr.Blocks:
    """エラータブを作成"""
    with gr.Blocks() as error:
        gr.Markdown(f"""
        # ❌ エラーが発生しました
        
        ```
        {error_message}
        ```
        
        ## 📝 解決方法:
        
        1. **依存関係の確認**: 必要なパッケージがインストールされているか確認
        2. **ファイルパス**: contbkフォルダーのパスが正しいか確認
        3. **権限**: ファイルアクセス権限を確認
        4. **再起動**: アプリケーションを再起動してみる
        
        ## 📞 サポート:
        
        問題が解決しない場合は、開発チームにお問い合わせください。
        """)
    return error

def create_tabbed_interface() -> gr.TabbedInterface:
    """
    contbkフォルダーのインターフェースを統合したタブ表示を作成
    """
    try:
        # contbkからインターフェースを読み込み
        interfaces, names = load_contbk_interfaces()
        
        # ウェルカムタブを先頭に追加
        welcome_tab = create_welcome_tab()
        all_interfaces = [welcome_tab] + interfaces
        all_names = ["🏠 Welcome"] + names
        
        if len(interfaces) == 0:
            # インターフェースが見つからない場合
            error_tab = create_error_tab("contbkフォルダーからインターフェースが見つかりませんでした。")
            all_interfaces = [welcome_tab, error_tab]
            all_names = ["🏠 Welcome", "❌ Error"]
        
        # タブ付きインターフェースを作成
        tabs = gr.TabbedInterface(
            all_interfaces,
            all_names,
            title="🎯 ContBK ダッシュボード"
        )
        
        return tabs
        
    except Exception as e:
        print(f"❌ Failed to create tabbed interface: {str(e)}")
        traceback.print_exc()
        
        # エラーの場合、基本的なインターフェースを返す
        error_tab = create_error_tab(str(e))
        welcome_tab = create_welcome_tab()
        
        return gr.TabbedInterface(
            [welcome_tab, error_tab],
            ["🏠 Welcome", "❌ Error"],
            title="🎯 ContBK ダッシュボード (エラー)"
        )

# スタンドアロン実行用（テスト用）
if __name__ == "__main__":
    print("🚀 ContBK ダッシュボードを起動中...")
    gradio_interface = create_tabbed_interface()  # テスト実行時のみ作成
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7861,  # メインアプリと被らないポート
        share=False,
        debug=True
    )
