import os
import shutil
import hmac
import hashlib
import base64
import subprocess
import time
from mysite.logger import logger
import async_timeout
import asyncio
from mysite.interpreter.interpreter_config import configure_interpreter
from fastapi import HTTPException
from groq import Groq

# Try to import open-interpreter, but handle if it's not available
try:
    from interpreter import interpreter
    # Configure interpreter without circular import
    interpreter = configure_interpreter()
except ImportError:
    print("Warning: open-interpreter not available. Some features may not work.")
    interpreter = None

GENERATION_TIMEOUT_SEC=60

def set_environment_variables():
    # Load environment variables first
    from dotenv import load_dotenv
    load_dotenv()
    
    # Try both possible environment variable names for Groq API key
    groq_key = os.getenv("GROQ_API_KEY") or os.getenv("api_key")
    if groq_key:
        os.environ["OPENAI_API_KEY"] = groq_key
        os.environ["GROQ_API_KEY"] = groq_key
        os.environ["api_key"] = groq_key
        # Also set for open-interpreter compatibility
        os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
        os.environ["MODEL_NAME"] = "llama3-8b-8192"
        os.environ["LOCAL_MODEL"] = "true"
        
        # Configure interpreter if it's available
        if interpreter is not None:
            try:
                interpreter.llm.api_key = groq_key
                interpreter.llm.api_base = "https://api.groq.com/openai/v1"
                interpreter.llm.model = "llama3-8b-8192"
            except Exception as e:
                print(f"Warning: Could not configure interpreter: {e}")

# Set environment variables on import
set_environment_variables()

def format_response(chunk, full_response):
    """Format the response chunk and add it to the full response"""
    if isinstance(chunk, dict):
        if 'content' in chunk:
            content = chunk['content']
            if isinstance(content, str):
                return full_response + content
    elif hasattr(chunk, 'content'):
        return full_response + str(chunk.content)
    elif isinstance(chunk, str):
        return full_response + chunk
    return full_response

# Set the environment variable.
def chat_with_interpreter(
    message, history=None, a=None, b=None, c=None, d=None
):  # , openai_api_key):
    # Check if interpreter is available
    if interpreter is None:
        yield "Error: open-interpreter is not available. Please install it with: pip install open-interpreter"
        return
        
    # Load environment variables if not already loaded
    from dotenv import load_dotenv
    load_dotenv()
    
    # Set the API key for the interpreter
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("api_key")
    if not api_key:
        yield "Error: No Groq API key found. Please set GROQ_API_KEY or api_key environment variable."
        return
        
    # Configure the interpreter with Groq settings
    try:
        interpreter.llm.api_key = api_key
        interpreter.llm.api_base = "https://api.groq.com/openai/v1"
        interpreter.llm.model = "llama3-8b-8192"
        # Also ensure environment variables are set
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["GROQ_API_KEY"] = api_key
    except Exception as e:
        yield f"Error configuring interpreter: {e}"
        return
    
    if message == "reset":
        interpreter.reset()
        return "Interpreter reset", history
    full_response = ""
    # add_conversation(history,20)
    user_entry = {"role": "user", "type": "message", "content": message}
    #messages.append(user_entry)
    # Call interpreter.chat and capture the result
    messages = []
    recent_messages = history[-20:]
    for conversation in recent_messages:
        user_message = conversation[0]
        user_entry = {"role": "user", "content": user_message}
        messages.append(user_entry)
        assistant_message = conversation[1]
        assistant_entry = {"role": "assistant", "content": assistant_message}
        messages.append(assistant_entry)

    user_entry = {"role": "user", "content": message}
    messages.append(user_entry)
    #system_prompt = {"role": "system", "content": "あなたは日本語の優秀なアシスタントです。"}
    #messages.insert(0, system_prompt)

    for chunk in interpreter.chat(messages, display=False, stream=True):
        # print(chunk)
        # output = '\n'.join(item['content'] for item in result if 'content' in item)
        full_response = format_response(chunk, full_response)
        yield full_response  # chunk.get("content", "")

    yield full_response  # , history
    return full_response, history

GENERATION_TIMEOUT_SEC = 60

def completion(message: str, history, c=None, d=None, prompt="あなたは日本語の優秀なアシスタントです。"):
    # Load environment variables if not already loaded
    from dotenv import load_dotenv
    load_dotenv()
    
    # Try both possible environment variable names for Groq API key
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("api_key")
    if not api_key:
        yield "Error: No Groq API key found. Please set GROQ_API_KEY or api_key environment variable."
        return
        
    client = Groq(api_key=api_key)
    messages = []
    recent_messages = history[-20:]
    for conversation in recent_messages:
        user_message = conversation[0]
        user_entry = {"role": "user", "content": user_message}
        messages.append(user_entry)
        assistant_message = conversation[1]
        assistant_entry = {"role": "assistant", "content": assistant_message}
        messages.append(assistant_entry)

    user_entry = {"role": "user", "content": message}
    messages.append(user_entry)
    system_prompt = {"role": "system", "content": prompt}
    messages.insert(0, system_prompt)

    #async with async_timeout.timeout(GENERATION_TIMEOUT_SEC):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        all_result = ""
        for chunk in response:
            current_content = chunk.choices[0].delta.content or ""
            all_result += current_content
            yield current_content
        yield all_result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Stream timed out")
    except StopAsyncIteration:
        return

# 例としての使用方法
if __name__ == "__main__":
    history = [
        ("user message 1", "assistant response 1"),
        ("user message 2", "assistant response 2"),
    ]

    async def main():
        async for response in completion("新しいメッセージ", history):
            print(response)

    asyncio.run(main())