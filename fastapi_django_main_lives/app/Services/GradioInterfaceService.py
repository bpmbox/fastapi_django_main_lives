"""
Gradio Interface Service
Laravel的なService層でGradioインターフェースの管理を行う
"""
import shutil
import gradio as gr
import importlib
import os
import pkgutil
import traceback

class GradioInterfaceService:
    """Gradioインターフェースの作成・管理を行うサービスクラス"""
    
    def __init__(self):
        self.gradio_interfaces = {}
        self.interface_names = []
    
    def collect_gradio_interfaces(self):
        """全てのGradioインターフェースを収集する"""
        self.gradio_interfaces = {}
        
        # 検索対象ディレクトリを指定
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

                        # 美しいタイトルを生成
                        display_name = self._generate_interface_title(module_info.name, module)
                        
                        # 名前の一意性を保証
                        unique_name = self._ensure_unique_name(display_name)

                        # インターフェースを処理
                        interface = self._process_interface(module.gradio_interface, module_info.name)
                        
                        if interface:
                            self.gradio_interfaces[unique_name] = interface
                            
                except ModuleNotFoundError as e:
                    print(f"ModuleNotFoundError: {sub_module_name} - {e}")
                except AttributeError as e:
                    print(f"AttributeError in {sub_module_name}: {e}")
                except Exception as e:
                    print(f"Failed to import {sub_module_name}: {e}")
                    print(traceback.format_exc())

        # 名前とインターフェースのリストを更新
        self.interface_names = list(self.gradio_interfaces.keys())
        print(f"Collected Gradio Interfaces: {self.interface_names}")
        
        return list(self.gradio_interfaces.values()), self.interface_names
    
    def _generate_interface_title(self, base_name, module):
        """インターフェースのタイトルを生成する"""
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
            return module.interface_title
        elif base_name in title_mapping:
            return title_mapping[base_name]
        else:
            # デフォルトの美しいタイトル生成
            formatted_name = base_name.replace('_', ' ').title()
            return f"✨ {formatted_name}"
    
    def _ensure_unique_name(self, display_name):
        """名前の一意性を保証する"""
        unique_name = display_name
        count = 1

        # 重複がある場合は番号を付与
        while unique_name in self.gradio_interfaces:
            unique_name = f"{display_name} ({count})"
            count += 1
            
        return unique_name
    
    def _process_interface(self, interface, base_name):
        """インターフェースを処理する（ファクトリ関数の場合は実行）"""
        # Check if it's a factory function by checking if it's callable but not a Gradio object
        # Gradio objects have 'queue' method, regular functions don't
        if callable(interface) and not hasattr(interface, 'queue'):
            try:
                interface = interface()
            except Exception as call_error:
                print(f"Failed to call factory function for {base_name}: {call_error}")
                return None  # Skip this interface if factory function fails
        
        return interface
    
    def categorize_interfaces(self, interfaces, names):
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
        
        # カテゴリマッピングロジックをここに実装
        # ... (元のコードから移植)
        
        return categories
    
    def create_tabbed_interface(self):
        """タブ付きGradioインターフェースを作成する"""
        interfaces, names = self.collect_gradio_interfaces()
        
        if not interfaces:
            # インターフェースが見つからない場合のデフォルト
            return gr.Interface(
                fn=lambda x: "No Gradio interfaces found",
                inputs="text",
                outputs="text",
                title="No Interfaces Available"
            )
        
        # タブ付きインターフェースを作成
        return gr.TabbedInterface(
            interface_list=interfaces,
            tab_names=names,
            title="🚀 AI Development Platform - Laravel風統合システム"
        )
