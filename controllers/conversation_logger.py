"""
会話履歴自動記録システム
=======================

GitHub Copilotとの会話を自動的にSQLiteに保存するためのフックシステム

使用方法:
1. このモジュールをインポート
2. log_conversation()を呼び出すだけで自動保存
3. セッション管理も自動化
"""

import uuid
import datetime
import json
import os
import traceback
import sqlite3
from typing import Optional, Dict, List
from controllers.conversation_history import ConversationManager

class ConversationLogger:
    def __init__(self):
        """会話ログシステムの初期化"""
        self.conversation_manager = ConversationManager()
        self.current_session_id = self.generate_session_id()
        self.session_start_time = datetime.datetime.now()
        
        print(f"🎯 会話ログシステム開始 - セッションID: {self.current_session_id[:8]}")
    
    def generate_session_id(self) -> str:
        """新しいセッションIDを生成"""
        return str(uuid.uuid4())
    
    def start_new_session(self, session_name: str = None) -> str:
        """新しいセッションを開始"""
        self.current_session_id = self.generate_session_id()
        self.session_start_time = datetime.datetime.now()
        
        if session_name:
            # セッション名を更新
            try:
                conn = sqlite3.connect(self.conversation_manager.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE sessions 
                    SET session_name = ?
                    WHERE session_id = ?
                ''', (session_name, self.current_session_id))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"⚠️ セッション名更新エラー: {e}")
        
        print(f"🆕 新しいセッション開始: {self.current_session_id[:8]}")
        return self.current_session_id
    
    def log_conversation(self,
                        user_message: str,
                        assistant_response: str,
                        context_info: str = "",
                        files_involved: List[str] = None,
                        tools_used: List[str] = None,
                        tags: List[str] = None,
                        project_name: str = "ContBK統合システム") -> Optional[int]:
        """
        会話を自動記録
        
        Args:
            user_message: ユーザーからのメッセージ
            assistant_response: アシスタントの応答
            context_info: コンテキスト情報
            files_involved: 関連ファイルのリスト
            tools_used: 使用ツールのリスト
            tags: タグのリスト
            project_name: プロジェクト名
        
        Returns:
            会話ID (保存に成功した場合)
        """
        try:
            # リストを文字列に変換
            files_str = ", ".join(files_involved) if files_involved else ""
            tools_str = ", ".join(tools_used) if tools_used else ""
            tags_str = ", ".join(tags) if tags else ""
            
            # 会話を保存
            conversation_id = self.conversation_manager.save_conversation(
                session_id=self.current_session_id,
                user_message=user_message,
                assistant_response=assistant_response,
                context_info=context_info,
                files_involved=files_str,
                tools_used=tools_str,
                tags=tags_str
            )
            
            print(f"✅ 会話を記録しました (ID: {conversation_id})")
            return conversation_id
            
        except Exception as e:
            print(f"❌ 会話記録エラー: {e}")
            print(traceback.format_exc())
            return None
    
    def log_tool_usage(self, tool_name: str, parameters: Dict, result: str):
        """ツール使用ログを記録"""
        tool_info = {
            "tool": tool_name,
            "parameters": parameters,
            "result": result[:500],  # 結果は500文字まで
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # 直前の会話にツール情報を追加
        try:
            conn = sqlite3.connect(self.conversation_manager.db_path)
            cursor = conn.cursor()
            
            # 最新の会話を取得
            cursor.execute('''
                SELECT id, tools_used FROM conversations 
                WHERE session_id = ?
                ORDER BY timestamp DESC 
                LIMIT 1
            ''', (self.current_session_id,))
            
            row = cursor.fetchone()
            if row:
                conversation_id, existing_tools = row
                
                # 既存のツール情報に追加
                updated_tools = existing_tools + f", {tool_name}" if existing_tools else tool_name
                
                cursor.execute('''
                    UPDATE conversations 
                    SET tools_used = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (updated_tools, conversation_id))
                
                conn.commit()
            
            conn.close()
            print(f"🔧 ツール使用を記録: {tool_name}")
            
        except Exception as e:
            print(f"⚠️ ツール使用記録エラー: {e}")
    
    def get_session_summary(self) -> Dict:
        """現在のセッションの要約を取得"""
        try:
            conversations = self.conversation_manager.get_conversations(
                session_id=self.current_session_id
            )
            
            return {
                "session_id": self.current_session_id,
                "start_time": self.session_start_time.isoformat(),
                "conversation_count": len(conversations),
                "duration_minutes": (datetime.datetime.now() - self.session_start_time).total_seconds() / 60,
                "latest_conversation": conversations[0] if conversations else None
            }
        except Exception as e:
            print(f"⚠️ セッション要約取得エラー: {e}")
            return {}
    
    def export_session(self, session_id: str = None) -> str:
        """セッションをJSON形式でエクスポート"""
        target_session = session_id or self.current_session_id
        
        try:
            conversations = self.conversation_manager.get_conversations(
                session_id=target_session
            )
            
            export_data = {
                "session_id": target_session,
                "export_time": datetime.datetime.now().isoformat(),
                "conversation_count": len(conversations),
                "conversations": conversations
            }
            
            filename = f"session_export_{target_session[:8]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"📥 セッションエクスポート完了: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ セッションエクスポートエラー: {e}")
            return ""

# グローバルログインスタンス
conversation_logger = ConversationLogger()

def log_this_conversation(user_msg: str, assistant_msg: str, 
                         context: str = "", files: List[str] = None, 
                         tools: List[str] = None, tags: List[str] = None):
    """
    簡単な会話ログ記録関数
    
    使用例:
    log_this_conversation(
        user_msg="ContBK統合システムについて教えて",
        assistant_msg="ContBK統合システムは...",
        files=["controllers/contbk_example.py"],
        tools=["create_file", "insert_edit_into_file"],
        tags=["contbk", "gradio"]
    )
    """
    return conversation_logger.log_conversation(
        user_message=user_msg,
        assistant_response=assistant_msg,
        context_info=context,
        files_involved=files,
        tools_used=tools,
        tags=tags
    )

def start_new_conversation_session(session_name: str = None):
    """新しい会話セッションを開始"""
    return conversation_logger.start_new_session(session_name)

def get_current_session_info():
    """現在のセッション情報を取得"""
    return conversation_logger.get_session_summary()

# 自動ログ記録のデコレーター
def auto_log_conversation(tags: List[str] = None):
    """
    関数の実行を自動的にログに記録するデコレーター
    
    使用例:
    @auto_log_conversation(tags=["gradio", "interface"])
    def create_interface():
        # 関数の処理
        pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            
            try:
                result = func(*args, **kwargs)
                
                # 成功した場合のログ
                conversation_logger.log_conversation(
                    user_message=f"関数実行: {func.__name__}",
                    assistant_response=f"関数 {func.__name__} が正常に実行されました",
                    context_info=f"実行時間: {(datetime.datetime.now() - start_time).total_seconds():.2f}秒",
                    tools_used=[func.__name__],
                    tags=tags or ["自動実行"]
                )
                
                return result
                
            except Exception as e:
                # エラーの場合のログ
                conversation_logger.log_conversation(
                    user_message=f"関数実行エラー: {func.__name__}",
                    assistant_response=f"エラーが発生しました: {str(e)}",
                    context_info=f"実行時間: {(datetime.datetime.now() - start_time).total_seconds():.2f}秒",
                    tools_used=[func.__name__],
                    tags=(tags or []) + ["エラー"]
                )
                raise
                
        return wrapper
    return decorator

if __name__ == "__main__":
    # テスト実行
    print("🧪 会話ログシステムテスト")
    
    # サンプル会話を記録
    log_this_conversation(
        user_msg="会話履歴システムのテストです",
        assistant_msg="会話履歴システムが正常に動作しています！",
        context="テスト実行",
        files=["controllers/conversation_logger.py"],
        tools=["create_file"],
        tags=["テスト", "会話履歴"]
    )
    
    # セッション情報表示
    session_info = get_current_session_info()
    print(f"📊 セッション情報: {session_info}")
    
    print("✅ テスト完了")
