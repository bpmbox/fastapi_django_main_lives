"""
Laravel風のアーキテクチャに従ってGradioインターフェースを管理
Controller -> Service のパターンを使用
"""
import gradio as gr
import sys
import os

# Laravel風の構造のためにパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from app.Http.Controllers.GradioController import setup_gradio_interfaces
    print("✅ Laravel風Controller経由でGradioインターフェースを読み込み")
except ImportError as e:
    print(f"⚠️ Laravel風Controllerの読み込みに失敗、フォールバックします: {e}")
    # フォールバック: 従来の方法
    from mysite.routers.gradio_legacy import setup_gradio_interfaces_legacy as setup_gradio_interfaces

# 後方互換性のために既存の関数名も提供
def include_gradio_interfaces():
    """後方互換性のための関数"""
    print("⚠️ include_gradio_interfaces() は非推奨です。Laravel風のController経由でアクセスしてください。")
    try:
        from mysite.routers.gradio_legacy import include_gradio_interfaces as legacy_include
        return legacy_include()
    except Exception as e:
        print(f"レガシー関数の実行に失敗: {e}")
        return [], []
