"""
🎨 Gradio 専用コントローラー
============================

Laravel風のGradio UIコントローラー
インタラクティブなWebインターフェースを提供
"""

from app.Http.Controllers.HybridController import HybridController
import gradio as gr
from typing import Dict, Any, List, Tuple
import json
import logging
import importlib
import os
import pkgutil

logger = logging.getLogger(__name__)

class GradioController(HybridController):
    """
    Gradio専用のLaravel風コントローラー
    インタラクティブなWebUIを提供
    """
    
    def __init__(self):
        super().__init__()
        self.interfaces = {}
        self.main_interface = None
        
    def gradio_process(self, input_text: str) -> str:
        """
        Gradio メイン処理関数
        """
        try:
            # 基本的なエコー処理（継承先で実装をオーバーライド）
            return f"処理結果: {input_text}"
        except Exception as e:
            logger.error(f"Gradio processing error: {e}")
            return f"エラーが発生しました: {e}"
    
    def create_main_interface(self) -> gr.Interface:
        """
        メインGradioインターフェースを作成
        """
        if not self.main_interface:
            self.main_interface = gr.Interface(
                fn=self.gradio_process,
                inputs=[
                    gr.Textbox(
                        label="入力テキスト",
                        placeholder="処理したいテキストを入力してください",
                        lines=3
                    )
                ],
                outputs=[
                    gr.Textbox(
                        label="処理結果",
                        lines=5
                    )
                ],
                title="🎨 Laravel風 Gradio インターフェース",
                description="FastAPI + Django + Gradio 統合システム",
                theme=gr.themes.Soft(),
                css="""
                .gradio-container {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .gr-button {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    color: white;
                }
                """
            )
        return self.main_interface
    
    def include_gradio_interfaces(self) -> Dict[str, gr.Interface]:
        """
        既存のGradioインターフェースを統合
        """
        interfaces = {}
        
        # 検索対象ディレクトリ
        search_dirs = [
            ("controllers", "controllers"),
            ("routers", "routers"),
            ("app.Http.Controllers", "app/Http/Controllers"),
        ]
        
        for package_name, package_path in search_dirs:
            if not os.path.exists(package_path):
                continue
                
            try:
                # パッケージ内のGradioインターフェースを検索
                for finder, name, ispkg in pkgutil.walk_packages([package_path]):
                    if ispkg:
                        continue
                    
                    try:
                        module_name = f"{package_name}.{name}"
                        module = importlib.import_module(module_name)
                        
                        # Gradioインターフェースを検索
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if isinstance(attr, gr.Interface):
                                interface_key = f"{name}_{attr_name}"
                                interfaces[interface_key] = attr
                                logger.info(f"Found Gradio interface: {interface_key}")
                                
                    except Exception as e:
                        logger.debug(f"Failed to import {module_name}: {e}")
                        
            except Exception as e:
                logger.error(f"Error scanning {package_path}: {e}")
        
        self.interfaces = interfaces
        return interfaces
    
    def create_tabbed_interface(self) -> gr.TabbedInterface:
        """
        タブ形式の統合インターフェースを作成
        """
        # 既存インターフェースを収集
        self.include_gradio_interfaces()
        
        # メインインターフェースを追加
        all_interfaces = [self.create_main_interface()]
        tab_names = ["メイン"]
        
        # 既存インターフェースを追加
        for name, interface in self.interfaces.items():
            all_interfaces.append(interface)
            tab_names.append(name)
        
        # タブ形式インターフェース作成
        tabbed_interface = gr.TabbedInterface(
            all_interfaces,
            tab_names,
            title="🏗️ Laravel風 統合ダッシュボード",
            css="""
            .gradio-container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .tab-nav {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            """
        )
        
        return tabbed_interface
    
    async def index(self) -> Dict[str, Any]:
        """
        Gradio インターフェース一覧
        """
        self.include_gradio_interfaces()
        
        return {
            "status": "success",
            "data": {
                "available_interfaces": list(self.interfaces.keys()),
                "total_interfaces": len(self.interfaces),
                "main_interface": "available"
            },
            "message": "Gradio interfaces retrieved successfully"
        }
    
    async def store(self, request) -> Dict[str, Any]:
        """
        新規インターフェース作成（プレースホルダー）
        """
        return {
            "status": "success",
            "message": "Interface creation not yet implemented"
        }
    
    async def show(self, id: int) -> Dict[str, Any]:
        """
        特定インターフェース情報取得
        """
        interface_list = list(self.interfaces.keys())
        if id < 1 or id > len(interface_list):
            raise HTTPException(status_code=404, detail="Interface not found")
        
        interface_name = interface_list[id - 1]
        
        return {
            "status": "success",
            "data": {
                "id": id,
                "name": interface_name,
                "type": "gradio_interface"
            },
            "message": "Interface information retrieved successfully"
        }
    
    async def update(self, id: int, request) -> Dict[str, Any]:
        """
        インターフェース更新（プレースホルダー）
        """
        return {
            "status": "success",
            "message": "Interface update not yet implemented"
        }
    
    async def destroy(self, id: int) -> Dict[str, Any]:
        """
        インターフェース削除（プレースホルダー）
        """
        return {
            "status": "success",
            "message": "Interface deletion not yet implemented"
        }

# インスタンス作成
gradio_controller = GradioController()
router = gradio_controller.router
