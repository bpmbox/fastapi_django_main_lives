#!/usr/bin/env python3
"""Test script to verify Groq API key loading fix"""

import os
import sys
sys.path.append('.')

def test_env_loading():
    print("Testing environment variable loading...")
    
    # Test 1: Direct .env loading
    from dotenv import load_dotenv
    result = load_dotenv()
    print(f"load_dotenv() result: {result}")
    
    # Test 2: Check environment variables
    groq_key = os.getenv('GROQ_API_KEY')
    api_key = os.getenv('api_key')
    
    print(f"GROQ_API_KEY found: {bool(groq_key)}")
    print(f"api_key found: {bool(api_key)}")
    
    if groq_key:
        print(f"GROQ_API_KEY starts with: {groq_key[:10]}...")
    if api_key:
        print(f"api_key starts with: {api_key[:10]}...")
    
    # Test 3: Import interpreter module
    try:
        from mysite.interpreter.interpreter import set_environment_variables
        print("Successfully imported interpreter module")
        
        # Call the function
        set_environment_variables()
        print("Environment variables set successfully")
        
        # Check if the variables are now set
        final_groq = os.getenv('GROQ_API_KEY')
        final_api = os.getenv('api_key')
        final_openai = os.getenv('OPENAI_API_KEY')
        
        print(f"Final GROQ_API_KEY: {bool(final_groq)}")
        print(f"Final api_key: {bool(final_api)}")
        print(f"Final OPENAI_API_KEY: {bool(final_openai)}")
        
        # Test 4: Test interpreter instance
        from mysite.interpreter.interpreter import interpreter
        if interpreter:
            print(f"Interpreter instance available: {type(interpreter)}")
            print(f"Interpreter has llm: {hasattr(interpreter, 'llm')}")
            if hasattr(interpreter, 'llm'):
                print(f"LLM has api_key: {hasattr(interpreter.llm, 'api_key')}")
                if hasattr(interpreter.llm, 'api_key'):
                    print(f"API key set: {bool(interpreter.llm.api_key)}")
        else:
            print("Interpreter instance not available")
        
    except Exception as e:
        print(f"Error importing interpreter module: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_env_loading()
