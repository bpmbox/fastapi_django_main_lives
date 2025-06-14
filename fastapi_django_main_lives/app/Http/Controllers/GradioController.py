"""
Gradio Controller
Laravel的なController層でGradioインターフェースのHTTPリクエストを処理
"""
import sys
import os
# パスを追加してServiceにアクセス
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from app.Services.GradioInterfaceService import GradioInterfaceService
except ImportError:
    # フォールバック用のダミークラス
    class GradioInterfaceService:
        def create_tabbed_interface(self):
            import gradio as gr
            return gr.Interface(
                fn=lambda x: "Laravel風Controller読み込み中...",
                inputs="text",
                outputs="text",
                title="🚀 Laravel風 Gradio Controller"
            )

import gradio as gr
from fastapi import FastAPI

class GradioController:
    """Gradioインターフェースのコントローラー"""
    
    def __init__(self):
        self.gradio_service = GradioInterfaceService()
        self.mounted_apps = {}  # マウントされたアプリケーションを追跡
    
    def setup_gradio_interfaces(self):
        """Gradioインターフェースをセットアップする"""
        try:
            # サービス層でインターフェースを作成
            tabbed_interface = self.gradio_service.create_tabbed_interface()
            
            print("✅ Gradio interfaces setup completed via Laravel-style Controller")
            return tabbed_interface
            
        except Exception as e:
            print(f"❌ Error setting up Gradio interfaces: {e}")
            # エラー時のフォールバック
            return gr.Interface(
                fn=lambda x: f"Error: {str(e)}",
                inputs="text",
                outputs="text",
                title="🚨 Error - Gradio Setup Failed"
            )
    
    def mount_gradio_to_fastapi(self, app: FastAPI, gradio_interfaces, mount_paths=None):
        """
        FastAPIアプリケーションに複数のGradioインターフェースをマウント
        
        Args:
            app: FastAPIアプリケーション
            gradio_interfaces: Gradioインターフェース（単体またはリスト）
            mount_paths: マウントパス（文字列またはリスト）
        """
        if mount_paths is None:
            mount_paths = ["/gradio"]
        
        # 単体の場合はリストに変換
        if not isinstance(gradio_interfaces, list):
            gradio_interfaces = [gradio_interfaces]
        if not isinstance(mount_paths, list):
            mount_paths = [mount_paths]
        
        # パスとインターフェースの数を調整
        if len(mount_paths) < len(gradio_interfaces):
            # パスが足りない場合は自動生成
            for i in range(len(mount_paths), len(gradio_interfaces)):
                mount_paths.append(f"/gradio{i+1}")
        
        mounted_count = 0
        
        for i, (interface, path) in enumerate(zip(gradio_interfaces, mount_paths)):
            try:
                # 方法1: gr.mount_gradio_app を試す (root_pathを指定)
                try:
                    # Codespacesでのポート問題を回避するため、環境変数を設定
                    import os
                    original_port = os.environ.get('PORT')
                    os.environ['PORT'] = '443'  # HTTPSポートに設定
                    
                    app = gr.mount_gradio_app(
                        app, 
                        interface, 
                        path=path,
                        app_kwargs={
                            "root_path": path,
                            "docs_url": None,  # docsを無効化
                            "redoc_url": None  # redocを無効化
                        }
                    )
                    
                    # 元のポート設定を復元
                    if original_port:
                        os.environ['PORT'] = original_port
                    elif 'PORT' in os.environ:
                        del os.environ['PORT']
                    
                    print(f"✅ Gradio interface mounted at {path} (method 1 with port fix)")
                    self.mounted_apps[path] = {"interface": interface, "method": "mount_gradio_app"}
                    mounted_count += 1
                    continue
                except Exception as e1:
                    print(f"⚠️ Method 1 failed for {path}: {e1}")
                
                # 方法2: 手動でASGIアプリとしてマウント (root_pathを指定)
                try:
                    # Codespacesでのポート問題を回避
                    import os
                    original_port = os.environ.get('PORT')
                    os.environ['PORT'] = '443'  # HTTPSポートに設定
                    
                    gradio_asgi = gr.routes.App.create_app(
                        interface, 
                        app_kwargs={
                            "root_path": path,
                            "docs_url": None,
                            "redoc_url": None
                        }
                    )
                    app.mount(path, gradio_asgi)
                    
                    # 元のポート設定を復元
                    if original_port:
                        os.environ['PORT'] = original_port
                    elif 'PORT' in os.environ:
                        del os.environ['PORT']
                    
                    print(f"✅ Gradio interface mounted at {path} (method 2 with port fix)")
                    self.mounted_apps[path] = {"interface": interface, "method": "manual_mount"}
                    mounted_count += 1
                    continue
                except Exception as e2:
                    print(f"⚠️ Method 2 failed for {path}: {e2}")
                
                # 方法3: Blocksを使った手動マウント
                try:
                    if hasattr(interface, 'app'):
                        app.mount(path, interface.app)
                        print(f"✅ Gradio interface mounted at {path} (method 3)")
                        self.mounted_apps[path] = {"interface": interface, "method": "blocks_mount"}
                        mounted_count += 1
                    else:
                        print(f"❌ Interface at {path} doesn't have app attribute")
                except Exception as e3:
                    print(f"❌ Method 3 failed for {path}: {e3}")
                    
            except Exception as general_error:
                print(f"❌ Failed to mount interface at {path}: {general_error}")
        
        print(f"🎯 Laravel風Controller: {mounted_count}/{len(gradio_interfaces)} interfaces mounted successfully")
        return app, self.mounted_apps
    
    def get_mounted_apps_info(self):
        """マウントされたアプリケーションの情報を取得"""
        return {
            "total_mounted": len(self.mounted_apps),
            "mount_points": list(self.mounted_apps.keys()),
            "details": self.mounted_apps
        }
    
    def unmount_gradio_app(self, app: FastAPI, path: str):
        """特定のパスのGradioアプリケーションをアンマウント"""
        try:
            if path in self.mounted_apps:
                # FastAPIから直接アンマウントする方法は限定的
                # 通常は再起動が必要
                del self.mounted_apps[path]
                print(f"✅ Removed {path} from tracking")
                return True
            else:
                print(f"⚠️ Path {path} not found in mounted apps")
                return False
        except Exception as e:
            print(f"❌ Error unmounting {path}: {e}")
            return False
    
    def get_interface_list(self):
        """利用可能なインターフェースの一覧を取得"""
        interfaces, names = self.gradio_service.collect_gradio_interfaces()
        return {
            "total_count": len(interfaces),
            "interface_names": names,
            "status": "success"
        }
    
    def get_categorized_interfaces(self):
        """カテゴリ別のインターフェース一覧を取得"""
        interfaces, names = self.gradio_service.collect_gradio_interfaces()
        categories = self.gradio_service.categorize_interfaces(interfaces, names)
        return categories

# Laravel風のファサードパターンでグローバルアクセスを提供
def setup_gradio_interfaces():
    """グローバル関数としてGradioインターフェースをセットアップ"""
    controller = GradioController()
    return controller.setup_gradio_interfaces()

def mount_gradio_to_fastapi(app: FastAPI, gradio_interfaces, mount_paths=None):
    """グローバル関数としてGradioをFastAPIにマウント"""
    controller = GradioController()
    return controller.mount_gradio_to_fastapi(app, gradio_interfaces, mount_paths)

def get_mounted_apps_info():
    """マウントされたアプリケーション情報を取得"""
    controller = GradioController()
    return controller.get_mounted_apps_info()
