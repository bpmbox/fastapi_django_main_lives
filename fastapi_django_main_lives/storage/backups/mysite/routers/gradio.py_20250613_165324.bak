import shutil
import gradio as gr
#from mysite.libs.utilities import chat_with_interpreter, completion, process_file
#from interpreter import interpreter
#import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import importlib
import os
import pkgutil
#from babyagi.babyagi import gradio_babyagi
#from routers.gra_02_openInterpreter.OpenInterpreter import gradio_interface
#from llamafactory.webui.interface import create_ui
import importlib
import os
import pkgutil

import importlib
import os
import pkgutil
import traceback

def include_gradio_interfaces():
    gradio_interfaces = {}  # 辞書型: { interface_name: gradio_interface }
    
    # 検索対象ディレクトリを指定（ContBKは統合ダッシュボードで表示するため除外）
    search_dirs = [
        ("controllers", "controllers"),  # メインのcontrollersディレクトリのみ
    ]
    
    package_paths = []
    
    # 各検索ディレクトリをスキャン
    for package_dir, module_prefix in search_dirs:
        if os.path.exists(package_dir):
            print(f"📂 Scanning directory: {package_dir}")
            for root, dirs, files in os.walk(package_dir):
                if "__pycache__" in root:  # `__pycache__` を除外
                    continue
                package_paths.append((root, module_prefix))

    for package_path, module_prefix in package_paths:
        # パッケージの Python モジュールを取得
        rel_path = os.path.relpath(package_path, module_prefix.split('.')[0] if '.' in module_prefix else module_prefix)
        
        if rel_path == ".":
            package_name = module_prefix
        else:
            package_name = module_prefix + "." + rel_path.replace(os.sep, ".")

        for module_info in pkgutil.iter_modules([package_path]):
            sub_module_name = f"{package_name}.{module_info.name}"
            print(f"Trying to import {sub_module_name}")

            try:
                module = importlib.import_module(sub_module_name)
                print(f"Successfully imported {sub_module_name}")

                # `gradio_interface` を持つモジュールのみ追加
                if hasattr(module, "gradio_interface"):
                    print(f"Found gradio_interface in {sub_module_name}")

                    # 美しいタイトルを生成（絵文字付き）
                    base_name = module_info.name
                    
                    # 特定のモジュールに対する美しいタイトルマッピング
                    title_mapping = {
                        'beginner_guide_system': '🚀 初心者ガイド',
                        'conversation_history': '💬 会話履歴管理',
                        'conversation_logger': '📝 会話ログ',
                        'conversation_demo': '🎯 会話履歴統合デモ',
                        'contbk_unified_dashboard': '🎯 ContBK統合ダッシュボード',
                        # 'contbk_example': '🎯 ContBK ダッシュボード',  # 無効化済み
                        # 'contbk_dashboard': '📊 ContBK 統合',  # 無効化済み
                        # 'example_gradio_interface': '🔧 サンプル',  # 無効化済み
                        'hasura': '🗄️ Hasura API',
                        'Chat': '💬 チャット',
                        'OpenInterpreter': '🤖 AI インタープリター',
                        'programfromdoc': '📄 ドキュメント生成',
                        'gradio_interface': '🚀 AI開発プラットフォーム',
                        'lavelo': '💾 プロンプト管理システム',
                        'rides': '🚗 データベース管理',
                        'files': '📁 ファイル管理',
                        'gradio': '🌐 HTML表示',
                        'rpa_automation': '🤖 RPA自動化システム',
                        'github_issue_dashboard': '🚀 GitHub ISSUE自動化',
                        'github_issue_automation': '🤖 GitHub ISSUE自動生成システム',
                        'integrated_approval_system': '🎯 統合承認システム',
                        'integrated_dashboard': '🚀 統合管理ダッシュボード',
                        'ui_verification_system': '🔧 UI検証・システム診断',
                    }
                    
                    # モジュールにtitle属性があるかチェック
                    if hasattr(module, 'interface_title'):
                        display_name = module.interface_title
                    elif base_name in title_mapping:
                        display_name = title_mapping[base_name]
                    else:
                        # デフォルトの美しいタイトル生成
                        formatted_name = base_name.replace('_', ' ').title()
                        display_name = f"✨ {formatted_name}"

                    # 名前の一意性を保証する処理
                    unique_name = display_name
                    count = 1

                    # 重複がある場合は番号を付与
                    while unique_name in gradio_interfaces:
                        unique_name = f"{display_name} ({count})"
                        count += 1

                    # Handle factory functions specifically
                    interface = module.gradio_interface
                    
                    # Check if it's a factory function by checking if it's callable but not a Gradio object
                    # Gradio objects have 'queue' method, regular functions don't
                    if callable(interface) and not hasattr(interface, 'queue'):
                        try:
                            interface = interface()
                        except Exception as call_error:
                            print(f"Failed to call factory function for {base_name}: {call_error}")
                            continue  # Skip this interface if factory function fails
                    
                    gradio_interfaces[unique_name] = interface
            except ModuleNotFoundError as e:
                print(f"ModuleNotFoundError: {sub_module_name} - {e}")
            except AttributeError as e:
                print(f"AttributeError in {sub_module_name}: {e}")
            except Exception as e:
                print(f"Failed to import {sub_module_name}: {e}")
                print(traceback.format_exc())

    # 名前とインターフェースのリストを返す
    print(f"Collected Gradio Interfaces: {list(gradio_interfaces.keys())}")
    return list(gradio_interfaces.values()), list(gradio_interfaces.keys())


def categorize_interfaces(interfaces, names):
    """インターフェースをユーザーフレンドリーなカテゴリ別に分類"""
    categories = {
        "スタート": [],             # 初心者ガイド・チュートリアル
        "チャット": [],             # 会話・質問・対話
        "AI作成": [],              # プログラム・コード生成
        "文書作成": [],             # ドキュメント・プロンプト
        "管理": [],                # システム・データ管理
        "開発": [],               # 開発ツール・テスト
        "その他": []              # その他の機能
    }
    
    # シンプルなカテゴリマッピング
    category_mapping = {
        # スタート - 初心者向け・ガイド
        "初心者ガイド": "スタート",
        "beginner_guide_system": "スタート",
        "ガイド": "スタート",
        "tutorial": "スタート",
        "guide": "スタート",
        
        # チャット - 会話・対話
        "会話": "チャット",
        "chat": "チャット",
        "conversation": "チャット",
        "話": "チャット",
        
        # AI作成 - プログラム生成・自動化
        "AI": "AI作成",
        "インタープリター": "AI作成",
        "interpreter": "AI作成",
        "RPA": "AI作成",
        "自動化": "AI作成",
        "automation": "AI作成",
        "generate": "AI作成",
        "program": "AI作成",
        "github": "AI作成",
        "issue": "AI作成",
        
        # 文書作成 - ドキュメント・プロンプト
        "ドキュメント": "文書作成",
        "document": "文書作成",
        "プロンプト": "文書作成",
        "prompt": "文書作成",
        "記録": "文書作成",
        
        # 管理 - システム・データ管理  
        "ダッシュボード": "管理",
        "dashboard": "管理",
        "統合": "管理",
        "管理": "管理",
        "承認": "管理",
        "dify": "管理",
        
        # 開発 - 開発・テスト
        "検証": "開発",
        "診断": "開発",
        "debug": "開発",
        "test": "開発",
        "memory": "開発",
        "restore": "開発",
        
        # その他 - デフォルト
        "file": "その他",
        "database": "その他",
        "データ": "その他",
        "api": "その他",
        "html": "その他",
        "webhook": "その他"
    }
    
    # インターフェースを分類 - より柔軟なマッピング
    for interface, name in zip(interfaces, names):
        # 完全一致を優先
        category = None
        
        # 部分一致で検索
        name_lower = name.lower()
        for key, cat in category_mapping.items():
            if key.lower() in name_lower:
                category = cat
                break
        
        # それでもマッチしない場合はデフォルト
        if not category:
            category = "その他"
            
        categories[category].append((interface, name))
    
    return categories

def create_user_friendly_interface(categories):
    """ユーザーフレンドリーな階層化インターフェースを作成"""
    
    # 優先順位付きカテゴリ（よく使われる順）
    priority_categories = [
        "スタート",
        "チャット", 
        "AI作成",
        "文書作成",
        "管理",
        "開発",
        "その他"
    ]
    
    valid_tabs = []
    
    for category_name in priority_categories:
        category_interfaces = categories.get(category_name, [])
        
        if not category_interfaces:  # 空のカテゴリはスキップ
            continue
        
        try:
            if len(category_interfaces) == 1:
                # 1つだけの場合
                interface, name = category_interfaces[0]
                valid_tabs.append((interface, category_name, name))
            else:
                # 複数の場合はサブタブで整理
                sub_interfaces = [item[0] for item in category_interfaces]
                sub_names = [item[1] for item in category_interfaces]
                
                # サブタブのタイトルを短縮
                short_names = []
                for name in sub_names:
                    # 絵文字を除去して短縮
                    clean_name = ''.join(c for c in name if not c.startswith('🎯🚀💬🤖📄📝📊🔧💾📁🌐🐙🖼️🎨✨'))
                    short_name = clean_name.strip()[:15] + "..." if len(clean_name) > 15 else clean_name.strip()
                    short_names.append(short_name or name[:10])
                
                sub_tabs = gr.TabbedInterface(sub_interfaces, short_names)
                valid_tabs.append((sub_tabs, category_name, f"{len(category_interfaces)}個の機能"))
                
        except Exception as e:
            print(f"カテゴリ {category_name} の処理でエラー: {e}")
            continue
    
    # メインタブインターフェースを作成
    if valid_tabs:
        try:
            # タブ名を短縮（スマホでも見やすく）
            main_interfaces = [tab[0] for tab in valid_tabs]
            main_names = [tab[1] for tab in valid_tabs]
            
            main_interface = gr.TabbedInterface(
                main_interfaces, 
                main_names,
                title="🚀 AI開発システム - 簡単操作で高速開発"
            )
            return main_interface
            
        except Exception as e:
            print(f"メインインターフェース作成エラー: {e}")
            # フォールバック処理
            return create_fallback_interface(valid_tabs)
    else:
        return create_empty_interface()

def create_fallback_interface(valid_tabs):
    """フォールバック用のシンプルインターフェース"""
    with gr.Blocks(title="🚀 AI開発システム") as fallback:
        gr.Markdown("# 🚀 AI-Human協働開発システム")
        gr.Markdown("### 直感的な操作で、24時間での高速開発を実現")
        
        # 重要なタブを優先表示
        important_tabs = valid_tabs[:6]  # 最初の6個まで
        
        for i, (interface, category, description) in enumerate(important_tabs):
            with gr.Tab(category):
                gr.Markdown(f"**{description}**")
                try:
                    if hasattr(interface, 'render'):
                        interface.render()
                    else:
                        # インターフェースオブジェクトを直接配置
                        interface
                except Exception as e:
                    gr.Markdown(f"⚠️ 読み込みエラー: {str(e)}")
                    
        if len(valid_tabs) > 6:
            gr.Markdown(f"**他にも {len(valid_tabs) - 6} 個の機能があります**")
            
    return fallback

def create_empty_interface():
    """空のインターフェース"""
    with gr.Blocks(title="🚀 AI開発システム") as empty:
        gr.Markdown("# 🚀 システム起動中...")
        gr.Markdown("### 機能を読み込んでいます。しばらくお待ちください。")
        gr.Markdown("問題が続く場合は、ページを再読み込みしてください。")
    return empty

def setup_gradio_interfaces():
    """階層化されたGradioインターフェースを設定 - シンプル版"""
    print("🔍 setup_gradio_interfaces() 開始 - シンプル階層化")
    
    try:
        # インターフェースを取得
        gradio_interfaces, gradio_names = include_gradio_interfaces()
        print(f"🔍 取得したインターフェース数: {len(gradio_interfaces)}")
        
        if not gradio_interfaces:
            print("⚠️ インターフェースが見つかりません")
            with gr.Blocks(title="🚀 AI-Human協働開発システム") as minimal_interface:
                gr.Markdown("# 🚀 システムが起動中です...")
                gr.Markdown("利用可能なインターフェースがありません。")
            return minimal_interface
        
        # カテゴリ別に整理（シンプル版）
        startup_interfaces = []
        startup_names = []
        main_interfaces = []
        main_names = []
        
        for interface, name in zip(gradio_interfaces, gradio_names):
            if "初心者" in name or "ガイド" in name or "スタート" in name or "guide" in name.lower():
                startup_interfaces.append(interface)
                startup_names.append(name)
            else:
                main_interfaces.append(interface)
                main_names.append(name)
        
        # 階層化されたインターフェースを作成（シンプル版）
        print("🔍 シンプル階層化インターフェース作成")
        
        with gr.Blocks(title="🚀 AI-Human協働開発システム") as main_interface:
            gr.Markdown("# 🚀 AI-Human協働開発システム")
            gr.Markdown("**24時間での高速開発を実現する、genuineなAI-Human協働システム**")
            
            # スタートガイド
            if startup_interfaces:
                with gr.Tab("🚀 はじめる"):
                    gr.Markdown("### 初心者向けガイドと使い方")
                    if len(startup_interfaces) == 1:
                        startup_interfaces[0].render()
                    else:
                        startup_tabs = gr.TabbedInterface(startup_interfaces, startup_names)
            
            # その他の機能（最大10個まで）
            display_interfaces = main_interfaces[:10]
            display_names = main_names[:10]
            
            if display_interfaces:
                with gr.Tab("🛠️ すべての機能"):
                    gr.Markdown(f"### システムの主要機能 ({len(display_interfaces)}個)")
                    if len(display_interfaces) == 1:
                        display_interfaces[0].render()
                    else:
                        main_tabs = gr.TabbedInterface(display_interfaces, display_names)
            
            # 残りの機能（もしあれば）
            if len(main_interfaces) > 10:
                remaining_interfaces = main_interfaces[10:]
                remaining_names = main_names[10:]
                with gr.Tab("➕ その他の機能"):
                    gr.Markdown(f"### その他の機能 ({len(remaining_interfaces)}個)")
                    if len(remaining_interfaces) == 1:
                        remaining_interfaces[0].render()
                    else:
                        remaining_tabs = gr.TabbedInterface(remaining_interfaces, remaining_names)
        
        print("✅ シンプル階層化インターフェース作成完了")
        main_interface.queue()
        return main_interface
        
    except Exception as e:
        print(f"❌ シンプル階層化でもエラー: {e}")
        import traceback
        traceback.print_exc()
        
        # 最終フォールバック: 従来のフラット形式
        print("🔄 従来形式にフォールバック")
        try:
            gradio_interfaces, gradio_names = include_gradio_interfaces()
            if gradio_interfaces:
                # 最大8個に制限
                safe_interfaces = gradio_interfaces[:8]
                safe_names = gradio_names[:8]
                print(f"🔍 フォールバック表示: {safe_names}")
                tabs = gr.TabbedInterface(safe_interfaces, safe_names, title="🚀 AI-Human協働開発システム")
                tabs.queue()
                return tabs
        except Exception as final_error:
            print(f"❌ 最終フォールバックもエラー: {final_error}")
            
        # 緊急フォールバック
        with gr.Blocks(title="🚀 AI-Human協働開発システム") as emergency_interface:
            gr.Markdown("# 🚀 システムが起動中です...")
            gr.Markdown("インターフェースの読み込みでエラーが発生しました。ページを再読み込みしてください。")
        return emergency_interface
if __name__ == "__main__":
    interfaces, names = include_gradio_interfaces()