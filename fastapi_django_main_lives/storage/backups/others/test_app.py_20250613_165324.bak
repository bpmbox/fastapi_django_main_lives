#!/usr/bin/env python3
"""
独立したテスト用FastAPIアプリケーション
OpenInterpreterの機能をテストするためのAPI
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# パスを追加
sys.path.append(os.path.dirname(__file__))

# Import our OpenInterpreter functions
try:
    from controllers.gra_02_openInterpreter.OpenInterpreter import (
        chat_with_interpreter,
        validate_code,
        get_recent_messages,
        add_message_to_db,
        initialize_db
    )
    OPENINTERPRETER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import OpenInterpreter functions: {e}")
    OPENINTERPRETER_AVAILABLE = False

# FastAPIアプリケーションを作成
app = FastAPI(
    title="OpenInterpreter Test API",
    description="Testing API for OpenInterpreter functionality",
    version="1.0.0"
)

# データモデル
class ChatRequest(BaseModel):
    message: str
    password: Optional[str] = "12345"
    temperature: Optional[float] = 0.95
    max_new_tokens: Optional[int] = 512

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None
    message_count: int = 0

class CodeValidationRequest(BaseModel):
    code: str

class CodeValidationResponse(BaseModel):
    is_valid: bool
    error: Optional[str] = None
    code: str

class TestResult(BaseModel):
    test_name: str
    success: bool
    result: Any
    error: Optional[str] = None

# ヘルスチェックエンドポイント
@app.get("/health")
async def health_check():
    """APIのヘルスチェック"""
    return {
        "status": "healthy",
        "service": "openinterpreter-test-api",
        "version": "1.0.0",
        "openinterpreter_available": OPENINTERPRETER_AVAILABLE
    }

# チャット機能テスト
@app.post("/test/chat", response_model=ChatResponse)
async def test_chat(request: ChatRequest):
    """チャット機能をテスト"""
    if not OPENINTERPRETER_AVAILABLE:
        return ChatResponse(
            response="",
            success=False,
            error="OpenInterpreter is not available"
        )
    
    try:
        responses = []
        for response in chat_with_interpreter(
            message=request.message,
            passw=request.password,
            temperature=request.temperature,
            max_new_tokens=request.max_new_tokens
        ):
            responses.append(str(response))
            # 長時間実行を避けるため、5つの応答で制限
            if len(responses) >= 5:
                break
        
        final_response = responses[-1] if responses else "No response generated"
        
        return ChatResponse(
            response=final_response,
            success=True,
            message_count=len(responses)
        )
    
    except Exception as e:
        return ChatResponse(
            response="",
            success=False,
            error=str(e)
        )

# コード検証機能テスト
@app.post("/test/validate-code", response_model=CodeValidationResponse)
async def test_validate_code(request: CodeValidationRequest):
    """コード検証機能をテスト"""
    if not OPENINTERPRETER_AVAILABLE:
        return CodeValidationResponse(
            is_valid=False,
            code=request.code,
            error="OpenInterpreter is not available"
        )
    
    try:
        is_valid = validate_code(request.code)
        return CodeValidationResponse(
            is_valid=is_valid,
            code=request.code
        )
    
    except Exception as e:
        return CodeValidationResponse(
            is_valid=False,
            code=request.code,
            error=str(e)
        )

# データベース機能テスト
@app.get("/test/database")
async def test_database():
    """データベース機能をテスト"""
    if not OPENINTERPRETER_AVAILABLE:
        return {"success": False, "error": "OpenInterpreter is not available"}
    
    try:
        # データベースを初期化
        initialize_db()
        
        # テストメッセージを追加
        test_message = "This is a test message for database functionality"
        add_message_to_db("user", "message", test_message)
        
        # メッセージを取得
        messages = get_recent_messages(limit=5)
        
        return {
            "success": True,
            "message_added": test_message,
            "recent_messages_count": len(messages),
            "recent_messages": [
                {"role": msg[0], "type": msg[1], "content": msg[2][:100]}
                for msg in messages[-3:]  # 最新の3つのメッセージ
            ]
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}

# 包括的テストスイート
@app.get("/test/suite")
async def run_test_suite():
    """包括的なテストスイートを実行"""
    results = []
    
    # テスト1: コード検証
    try:
        valid_code = "print('Hello, World!')"
        invalid_code = "print('Hello, World!'"
        
        if OPENINTERPRETER_AVAILABLE:
            valid_result = validate_code(valid_code)
            invalid_result = validate_code(invalid_code)
            success = valid_result and not invalid_result
        else:
            success = False
            
        results.append(TestResult(
            test_name="code_validation",
            success=success,
            result={
                "valid_code_check": valid_result if OPENINTERPRETER_AVAILABLE else "N/A",
                "invalid_code_check": invalid_result if OPENINTERPRETER_AVAILABLE else "N/A"
            }
        ))
    except Exception as e:
        results.append(TestResult(
            test_name="code_validation",
            success=False,
            result=None,
            error=str(e)
        ))
    
    # テスト2: 基本的なチャット
    try:
        if OPENINTERPRETER_AVAILABLE:
            chat_responses = list(chat_with_interpreter("What is 2+2?", passw="12345"))
            success = len(chat_responses) > 0
            result = {
                "response_count": len(chat_responses),
                "first_response": chat_responses[0][:100] if chat_responses else ""
            }
        else:
            success = False
            result = {"error": "OpenInterpreter not available"}
            
        results.append(TestResult(
            test_name="basic_chat",
            success=success,
            result=result
        ))
    except Exception as e:
        results.append(TestResult(
            test_name="basic_chat",
            success=False,
            result=None,
            error=str(e)
        ))
    
    # テスト3: 環境変数チェック
    try:
        groq_key = os.getenv("GROQ_API_KEY")
        api_key = os.getenv("api_key")
        
        results.append(TestResult(
            test_name="environment_variables",
            success=bool(groq_key or api_key),
            result={
                "groq_key_set": bool(groq_key),
                "api_key_set": bool(api_key),
                "groq_key_format": groq_key.startswith("gsk_") if groq_key else False
            }
        ))
    except Exception as e:
        results.append(TestResult(
            test_name="environment_variables",
            success=False,
            result=None,
            error=str(e)
        ))
    
    # 全体的な成功率を計算
    successful_tests = sum(1 for result in results if result.success)
    total_tests = len(results)
    success_rate = successful_tests / total_tests if total_tests > 0 else 0
    
    return {
        "test_suite_results": results,
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": success_rate,
            "overall_success": success_rate >= 0.5
        }
    }

if __name__ == "__main__":
    print("🚀 Starting OpenInterpreter Test API...")
    print(f"OpenInterpreter Available: {OPENINTERPRETER_AVAILABLE}")
    
    uvicorn.run(
        "test_app:app",
        host="0.0.0.0",
        port=7861,  # 異なるポートを使用
        reload=True
    )
