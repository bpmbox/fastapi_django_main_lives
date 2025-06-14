import pytest
import asyncio
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI
import sys
import json

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the main app
from app import app
from controllers.gra_02_openInterpreter.OpenInterpreter import (
    chat_with_interpreter, 
    validate_code, 
    format_response,
    initialize_db,
    add_message_to_db,
    get_recent_messages
)

# Create test client
client = TestClient(app)

class TestOpenInterpreter:
    """Test cases for OpenInterpreter functionality"""
    
    @classmethod
    def setup_class(cls):
        """Setup test database and environment"""
        initialize_db()
        # Set test environment variables
        os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "test_key")
        os.environ["api_key"] = os.getenv("api_key", "test_key")
    
    def test_validate_code_valid(self):
        """Test code validation with valid Python code"""
        valid_code = "print('Hello, world!')"
        assert validate_code(valid_code) == True
    
    def test_validate_code_invalid(self):
        """Test code validation with invalid Python code"""
        invalid_code = "print('Hello, world!'"  # Missing closing parenthesis
        assert validate_code(invalid_code) == False
    
    def test_validate_code_empty(self):
        """Test code validation with empty code"""
        assert validate_code("") == False
        assert validate_code("   ") == False
        assert validate_code("\n\n") == False
    
    def test_validate_code_comments_only(self):
        """Test code validation with comments only"""
        comment_code = "# This is just a comment"
        assert validate_code(comment_code) == False
    
    def test_format_response_message(self):
        """Test format_response with message chunk"""
        chunk = {"type": "message", "content": "Hello, this is a test message."}
        result = format_response(chunk, "")
        assert "Hello, this is a test message." in result
    
    def test_format_response_code_valid(self):
        """Test format_response with valid code chunk"""
        chunk = {
            "type": "code", 
            "content": "print('Hello, world!')",
            "start": True,
            "end": True
        }
        result = format_response(chunk, "")
        assert "```python" in result
        assert "print('Hello, world!')" in result
        assert "```" in result
    
    def test_format_response_code_invalid(self):
        """Test format_response with invalid code chunk"""
        chunk = {
            "type": "code", 
            "content": "print('Hello, world!'",  # Invalid syntax
            "start": True,
            "end": True
        }
        result = format_response(chunk, "")
        # Should not include code block for invalid code
        assert "```python" not in result
    
    def test_database_operations(self):
        """Test database add and retrieve operations"""
        test_message = "Test message for database"
        
        # Add message to database
        add_message_to_db("user", "message", test_message)
        
        # Retrieve messages
        messages = get_recent_messages(limit=1)
        assert len(messages) >= 1
        assert test_message in str(messages)
    
    def test_fastapi_main_endpoint(self):
        """Test FastAPI main endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_chat_with_interpreter_no_password(self):
        """Test chat_with_interpreter without password"""
        messages = list(chat_with_interpreter("Hello", passw="wrong_password"))
        assert any("パスワードが正しくありません" in str(msg) for msg in messages)
    
    def test_chat_with_interpreter_correct_password(self):
        """Test chat_with_interpreter with correct password"""
        # This test requires actual API key and interpreter
        try:
            messages = list(chat_with_interpreter("What is 2+2?", passw="12345"))
            assert len(messages) > 0
            # Should not contain password error
            assert not any("パスワードが正しくありません" in str(msg) for msg in messages)
        except Exception as e:
            # If interpreter is not available, we expect an error message
            assert "open-interpreter" in str(e) or "API key" in str(e)
    
    def test_chat_with_interpreter_reset(self):
        """Test chat_with_interpreter reset functionality"""
        messages = list(chat_with_interpreter("reset", passw="12345"))
        assert any("Interpreter reset" in str(msg) for msg in messages)
    
    @pytest.mark.asyncio
    async def test_async_chat_response(self):
        """Test asynchronous chat response"""
        async def async_chat_test():
            messages = []
            for message in chat_with_interpreter("Hello", passw="12345"):
                messages.append(message)
                if len(messages) >= 5:  # Limit to avoid long running test
                    break
            return messages
        
        result = await async_chat_test()
        assert isinstance(result, list)

class TestFastAPIEndpoints:
    """Test FastAPI specific endpoints"""
    
    def test_gradio_interface_loading(self):
        """Test that Gradio interface loads properly"""
        response = client.get("/")
        assert response.status_code == 200
        # Check if the response contains Gradio content
        content = response.text
        assert "gradio" in content.lower() or "chatbot" in content.lower()
    
    def test_health_check(self):
        """Test application health"""
        # Test basic application response
        response = client.get("/")
        assert response.status_code == 200
        assert len(response.content) > 0

class TestCodeExecution:
    """Test code execution scenarios"""
    
    def test_simple_math_code(self):
        """Test simple mathematical code validation"""
        code = "result = 2 + 2\nprint(result)"
        assert validate_code(code) == True
    
    def test_import_statement_code(self):
        """Test code with import statements"""
        code = "import os\nprint(os.getcwd())"
        assert validate_code(code) == True
    
    def test_function_definition_code(self):
        """Test code with function definitions"""
        code = """
def greet(name):
    return f"Hello, {name}!"

result = greet("World")
print(result)
"""
        assert validate_code(code) == True
    
    def test_syntax_error_code(self):
        """Test various syntax error scenarios"""
        invalid_codes = [
            "if True",  # Missing colon
            "print('unclosed string",  # Unclosed string
            "def func(\n    pass",  # Invalid function definition
            "for i in",  # Incomplete for loop
        ]
        
        for code in invalid_codes:
            assert validate_code(code) == False

def test_environment_setup():
    """Test that required environment variables are set"""
    # Check if API keys are available
    groq_key = os.getenv("GROQ_API_KEY")
    api_key = os.getenv("api_key")
    
    assert groq_key is not None or api_key is not None, "At least one API key should be set"

if __name__ == "__main__":
    # Run tests manually if script is executed directly
    import subprocess
    
    print("Running OpenInterpreter tests...")
    
    # Run specific test functions
    test_instance = TestOpenInterpreter()
    test_instance.setup_class()
    
    print("✓ Testing code validation...")
    test_instance.test_validate_code_valid()
    test_instance.test_validate_code_invalid()
    test_instance.test_validate_code_empty()
    
    print("✓ Testing response formatting...")
    test_instance.test_format_response_message()
    test_instance.test_format_response_code_valid()
    test_instance.test_format_response_code_invalid()
    
    print("✓ Testing database operations...")
    test_instance.test_database_operations()
    
    print("✓ Testing FastAPI endpoints...")
    fastapi_test = TestFastAPIEndpoints()
    fastapi_test.test_gradio_interface_loading()
    fastapi_test.test_health_check()
    
    print("✓ Testing code execution scenarios...")
    code_test = TestCodeExecution()
    code_test.test_simple_math_code()
    code_test.test_import_statement_code()
    code_test.test_function_definition_code()
    code_test.test_syntax_error_code()
    
    print("✓ All tests completed successfully!")
