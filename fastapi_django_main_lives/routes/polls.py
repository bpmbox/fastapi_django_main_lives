"""
Polls Router Integration for Laravel Structure
=============================================

FastAPIからDjangoモデルを使用するためのPollsルーター統合
"""

from fastapi import FastAPI

# Laravel構造からPollsコントローラーをインポート
try:
    from laravel_app.Http.Controllers.Api.Polls.QuestionController import router as questions_router
    from laravel_app.Http.Controllers.Api.Polls.ChoiceController import router as choices_router
    
    __all__ = ("register_polls_routers",)
    
    def register_polls_routers(app: FastAPI):
        """
        Polls関連のルーターをFastAPIアプリに登録
        
        Args:
            app: FastAPIアプリケーションインスタンス
        """
        app.include_router(questions_router, prefix="/api/polls", tags=["polls-questions"])
        app.include_router(choices_router, prefix="/api/polls", tags=["polls-choices"])
        print("✅ Polls ルーター統合完了 (Laravel構造)")
        
except ImportError as e:
    print(f"⚠️  Pollsルーター統合エラー: {e}")
    
    def register_polls_routers(app: FastAPI):
        """フォールバック: 元のpolls構造を使用"""
        try:
            from polls.routers import register_routers
            register_routers(app)
            print("⚠️  フォールバック: 元のpolls構造を使用")
        except ImportError:
            print("❌ Pollsルーターが見つかりません")
