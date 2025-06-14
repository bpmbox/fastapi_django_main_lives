"""
Laravel构造対応 Polls Models (軽量版)
=====================================

元のpolls.modelsを参照するラッパー
Django初期化問題を回避
"""

def get_polls_models():
    """
    Pollsモデルを動的にインポート
    Django初期化後に呼び出し
    """
    try:
        from polls.models import Question, Choice
        return Question, Choice
    except ImportError as e:
        print(f"❌ Pollsモデルのインポートエラー: {e}")
        return None, None

# 軽量アクセス関数
def get_question_model():
    """Questionモデルを取得"""
    Question, _ = get_polls_models()
    return Question

def get_choice_model():
    """Choiceモデルを取得"""
    _, Choice = get_polls_models()
    return Choice
