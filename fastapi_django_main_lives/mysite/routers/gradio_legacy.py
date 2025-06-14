"""
レガシーのGradio設定（フォールバック用）
"""
import shutil
import gradio as gr
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

def setup_gradio_interfaces_legacy():
    """レガシーのGradioインターフェース設定"""
    try:
        gradio_interfaces, gradio_names = include_gradio_interfaces()
        if gradio_interfaces:
            tabs = gr.TabbedInterface(gradio_interfaces, gradio_names, title="🚀 AI-Human協働開発システム (Legacy)")
            tabs.queue()
            return tabs
        else:
            return gr.Interface(
                fn=lambda x: "No interfaces found",
                inputs="text",
                outputs="text",
                title="No Interfaces"
            )
    except Exception as e:
        print(f"Legacy setup failed: {e}")
        return gr.Interface(
            fn=lambda x: f"Error: {str(e)}",
            inputs="text",
            outputs="text",
            title="Error"
        )
