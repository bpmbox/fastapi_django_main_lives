"""
ContBK 統合ダッシュボード
======================

ContBKフォルダーの全機能を統合した見やすいダッシュボード
サブフォルダーの機能を「Example」タブ内で整理して表示
"""

import gradio as gr
import importlib
import os
import sys
import traceback
from typing import List, Tuple, Any, Dict

def load_contbk_interfaces() -> Dict[str, List[Tuple[Any, str]]]:
    """
    ContBKフォルダーから機能をカテゴリ別に読み込み
    """
    print("📂 ContBK統合ダッシュボード: 機能を読み込み中...")
    
    # パスの設定
    contbk_path = "/workspaces/fastapi_django_main_live/contbk"
    main_path = "/workspaces/fastapi_django_main_live"
    
    if contbk_path not in sys.path:
        sys.path.insert(0, contbk_path)
    if main_path not in sys.path:
        sys.path.insert(0, main_path)
    
    # カテゴリ別の機能整理
    categories = {
        "🤖 AI・自動化": [
            ("gra_01_chat.Chat", "💬 AI チャット"),
            ("gra_02_openInterpreter.OpenInterpreter", "🤖 AI インタープリター"),
            ("gra_12_rpa.rpa_automation", "🤖 RPA自動化システム"),
        ],
        "📄 ドキュメント・開発": [
            ("gra_03_programfromdoc.programfromdoc", "📄 ドキュメント生成"),
            ("gra_03_programfromdocgas.programfromdocAI", "📄 プログラム生成AI"),
            ("gra_03_programfromdocs.lavelo", "💾 プロンプト管理"),
        ],
        "🎨 フロントエンド・UI": [
            ("gra_10_frontend.frontend_generator", "🎨 フロントエンド生成"),
            ("gra_11_multimodal.image_to_ui", "🖼️ 画像からUI生成"),
        ],
        "📊 データ・ファイル": [
            ("gra_04_database.rides", "🚗 データベース管理"),
            ("gra_05_files.files", "📁 ファイル管理"),
        ],
        "🌐 その他ツール": [
            ("gra_09_weather.weather", "🌤️ 天気予報"),
            ("gra_06_video.video", "🎥 動画処理"),
        ],
        "🐙 開発・Issue管理": [
            ("controllers.github_issue_creator", "🐙 GitHub Issue作成"),
        ],
    }
    
    loaded_categories = {}
    
    for category_name, modules in categories.items():
        loaded_interfaces = []
        
        for module_name, display_name in modules:
            try:
                print(f"🔍 Loading {module_name}...")
                module = importlib.import_module(module_name)
                
                if hasattr(module, 'gradio_interface'):
                    loaded_interfaces.append((module.gradio_interface, display_name))
                    print(f"✅ Successfully loaded: {display_name}")
                else:
                    print(f"⚠️ No gradio_interface found in {module_name}")
                    
            except Exception as e:
                print(f"❌ Failed to load {module_name}: {str(e)}")
                continue
        
        if loaded_interfaces:
            loaded_categories[category_name] = loaded_interfaces
    
    return loaded_categories

def create_category_tab(interfaces: List[Tuple[Any, str]], category_name: str) -> gr.Blocks:
    """
    カテゴリごとのタブを作成
    """
    with gr.Blocks(title=f"ContBK - {category_name}") as category_tab:
        gr.Markdown(f"# {category_name}")
        gr.Markdown(f"このカテゴリには {len(interfaces)} 個の機能があります。")
        
        if interfaces:
            # サブタブとして各機能を表示
            interface_list = [interface for interface, _ in interfaces]
            interface_names = [name for _, name in interfaces]
            
            if len(interfaces) == 1:
                # 1つの機能のみの場合、直接表示
                interface = interface_list[0]
                # Handle factory functions
                if callable(interface) and not hasattr(interface, 'queue'):
                    interface = interface()
                interface.render()
            else:
                # 複数の機能がある場合、サブタブで表示
                # Handle factory functions in the list
                processed_interfaces = []
                for interface in interface_list:
                    if callable(interface) and not hasattr(interface, 'queue'):
                        interface = interface()
                    processed_interfaces.append(interface)
                
                sub_tabs = gr.TabbedInterface(
                    processed_interfaces,
                    interface_names,
                    title=f"{category_name} 機能一覧"
                )
        else:
            gr.Markdown("⚠️ このカテゴリには利用可能な機能がありません。")
    
    return category_tab

def create_overview_tab() -> gr.Blocks:
    """
    概要・ヘルプタブを作成
    """
    with gr.Blocks() as overview_tab:
        gr.Markdown("""
        # 🎯 ContBK 統合ダッシュボード
        
        ## 📋 概要
        このダッシュボードは、ContBKフォルダーにある全ての機能を整理して表示します。
        
        ## 🗂️ カテゴリ構成
        
        ### 🤖 AI・自動化
        - **AI チャット**: 対話型AIインターフェース
        - **AI インタープリター**: コード実行・解析
        - **RPA自動化システム**: Webブラウザ自動化
        
        ### 📄 ドキュメント・開発
        - **ドキュメント生成**: 仕様書からコード生成
        - **プログラム生成AI**: AI支援開発
        - **プロンプト管理**: プロンプトライブラリ
        
        ### 🎨 フロントエンド・UI
        - **フロントエンド生成**: UI自動生成
        - **画像からUI生成**: 画像ベースUI作成
        
        ### 📊 データ・ファイル
        - **データベース管理**: CRUD操作
        - **ファイル管理**: ファイル操作・編集
        
        ### 🌐 その他ツール
        - **天気予報**: 気象情報取得
        - **動画処理**: 動画編集・変換
        
        ### 🐙 開発・Issue管理
        - **GitHub Issue作成**: 会話履歴からIssue自動生成
        
        ## 🚀 使用方法
        1. 上部のタブから興味のあるカテゴリを選択
        2. カテゴリ内の機能を探索
        3. 各機能の詳細な操作は個別のインターフェースで実行
        
        ## 💡 ヒント
        - 各カテゴリは関連する機能でグループ化されています
        - 機能に問題がある場合は、ログを確認してください
        - 新しい機能は随時追加されます
        """)
        
        # システム情報表示
        with gr.Row():
            with gr.Column():
                def get_system_info():
                    import datetime
                    contbk_path = "/workspaces/fastapi_django_main_live/contbk"
                    folder_count = len([d for d in os.listdir(contbk_path) 
                                      if os.path.isdir(os.path.join(contbk_path, d)) 
                                      and d.startswith('gra_')])
                    
                    return f"""
                    **現在時刻**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
                    **ContBK パス**: {contbk_path}
                    **利用可能フォルダー数**: {folder_count}個
                    **Gradio バージョン**: {gr.__version__}
                    """
                
                system_info = gr.Textbox(
                    label="💻 システム情報",
                    value=get_system_info(),
                    lines=6,
                    interactive=False
                )
                
                refresh_btn = gr.Button("🔄 情報更新", variant="secondary")
                refresh_btn.click(fn=get_system_info, outputs=system_info)
    
    return overview_tab

def create_unified_dashboard() -> gr.TabbedInterface:
    """
    統合ダッシュボードを作成
    """
    print("🚀 ContBK統合ダッシュボードを作成中...")
    
    try:
        # ContBK機能をカテゴリ別に読み込み
        categories = load_contbk_interfaces()
        
        # タブリストを作成
        all_tabs = []
        all_names = []
        
        # 概要タブを最初に追加
        overview_tab = create_overview_tab()
        all_tabs.append(overview_tab)
        all_names.append("🏠 概要")
        
        # カテゴリ別タブを追加
        for category_name, interfaces in categories.items():
            category_tab = create_category_tab(interfaces, category_name)
            all_tabs.append(category_tab)
            all_names.append(category_name)
        
        # 統合タブ付きインターフェースを作成
        if len(all_tabs) > 1:
            dashboard = gr.TabbedInterface(
                all_tabs,
                all_names,
                title="🎯 ContBK 統合ダッシュボード"
            )
        else:
            # フォールバック：概要タブのみ
            dashboard = overview_tab
        
        print(f"✅ ダッシュボード作成完了: {len(all_tabs)} タブ")
        return dashboard
        
    except Exception as e:
        print(f"❌ ダッシュボード作成エラー: {str(e)}")
        traceback.print_exc()
        
        # エラー時のフォールバック
        with gr.Blocks() as error_tab:
            gr.Markdown(f"""
            # ❌ エラーが発生しました
            
            ContBK統合ダッシュボードの作成中にエラーが発生しました。
            
            **エラー詳細**: {str(e)}
            
            ## 🔧 対処方法
            1. アプリケーションを再起動してください
            2. ログを確認してください
            3. 個別の機能が正常に動作するかテストしてください
            """)
        
        return gr.TabbedInterface([error_tab], ["❌ エラー"])

# メインのgradio_interfaceを作成
print("🚀 Creating unified ContBK dashboard...")
gradio_interface = create_unified_dashboard()

# 自動検出システム用のメタデータ
interface_title = "🎯 ContBK統合ダッシュボード"
interface_description = "ContBKフォルダーの全機能を整理したダッシュボード"

# テスト実行用
if __name__ == "__main__":
    print("🚀 ContBK統合ダッシュボードを起動中...")
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7865,  # 専用ポート
        share=False,
        debug=True
    )
