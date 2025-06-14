from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import our OpenInterpreter functions
try:
    from controllers.gra_02_openInterpreter.OpenInterpreter import (
        chat_with_interpreter,
        validate_code,
        get_recent_messages,
        add_message_to_db
    )
except ImportError as e:
    print(f"Warning: Could not import OpenInterpreter functions: {e}")
    # Create dummy functions for testing
    def chat_with_interpreter(*args, **kwargs):
        yield "Test response"
    def validate_code(code):
        return True
    def get_recent_messages(limit=10):
        return []
    def add_message_to_db(role, msg_type, content):
        pass

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    password: Optional[str] = None
    temperature: Optional[float] = 0.95
    max_new_tokens: Optional[int] = 512

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

class CodeValidationRequest(BaseModel):
    code: str

class CodeValidationResponse(BaseModel):
    is_valid: bool
    error: Optional[str] = None

class HistoryResponse(BaseModel):
    messages: List[dict]
    count: int

@router.post("/api/chat", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
    """
    API endpoint for chatting with OpenInterpreter
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")
        
        # Collect all responses from the generator
        responses = []
        for response in chat_with_interpreter(
            message=request.message,
            passw=request.password,
            temperature=request.temperature,
            max_new_tokens=request.max_new_tokens
        ):
            responses.append(str(response))
        
        # Get the final response
        final_response = responses[-1] if responses else "No response generated"
        
        return ChatResponse(
            response=final_response,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in chat API: {str(e)}")
        return ChatResponse(
            response="",
            success=False,
            error=str(e)
        )

@router.post("/api/validate-code", response_model=CodeValidationResponse)
async def validate_code_api(request: CodeValidationRequest):
    """
    API endpoint for validating Python code
    """
    try:
        is_valid = validate_code(request.code)
        return CodeValidationResponse(
            is_valid=is_valid
        )
    
    except Exception as e:
        logger.error(f"Error in code validation API: {str(e)}")
        return CodeValidationResponse(
            is_valid=False,
            error=str(e)
        )

@router.get("/api/history", response_model=HistoryResponse)
async def get_chat_history(limit: int = 10):
    """
    API endpoint for getting chat history
    """
    try:
        messages = get_recent_messages(limit=limit)
        formatted_messages = [
            {
                "role": msg[0],
                "type": msg[1],
                "content": msg[2]
            }
            for msg in messages
        ]
        
        return HistoryResponse(
            messages=formatted_messages,
            count=len(formatted_messages)
        )
    
    except Exception as e:
        logger.error(f"Error in history API: {str(e)}")
        return HistoryResponse(
            messages=[],
            count=0
        )

@router.get("/api/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {
        "status": "healthy",
        "service": "openinterpreter",
        "version": "1.0.0"
    }

@router.post("/api/test-interpreter")
async def test_interpreter():
    """
    Test endpoint to verify OpenInterpreter functionality
    """
    try:
        # Test with a simple message
        test_message = "Calculate 2 + 2"
        responses = []
        
        for response in chat_with_interpreter(
            message=test_message,
            passw="12345"
        ):
            responses.append(str(response))
            # Limit responses to avoid long execution
            if len(responses) >= 5:
                break
        
        return {
            "test_message": test_message,
            "responses": responses,
            "success": True,
            "response_count": len(responses)
        }
    
    except Exception as e:
        return {
            "test_message": "Calculate 2 + 2",
            "error": str(e),
            "success": False
        }
