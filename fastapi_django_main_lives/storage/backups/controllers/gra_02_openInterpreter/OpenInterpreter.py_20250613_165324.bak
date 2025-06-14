import gradio as gr
from mysite.libs.utilities import completion, process_file, no_process_file
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb
import os
import sqlite3
from datetime import datetime
import base64
from PIL import Image
from io import BytesIO
from config.database import get_db_path

# Try to import open-interpreter, but handle if it's not available
try:
    from interpreter import interpreter
except ImportError:
    print("Warning: open-interpreter not available. Some features may not work.")
    interpreter = None
    
#from logger import logger

def validate_code(code_content):
    """Validate Python code syntax to prevent syntax errors"""
    if not code_content or not code_content.strip():
        return False
    
    # Skip if only whitespace or empty lines
    cleaned_code = '\n'.join(line for line in code_content.split('\n') if line.strip())
    if not cleaned_code:
        return False
    
    try:
        import ast
        # Try to parse the code to check for syntax errors
        ast.parse(cleaned_code)
        return True
    except SyntaxError as e:
        print(f"DEBUG: Syntax error in code: {e}")
        return False
    except Exception as e:
        print(f"DEBUG: Error validating code: {e}")
        return False

def format_response(chunk, full_response):
    print(f"DEBUG: Processing chunk type: {chunk.get('type', 'unknown')}")
    
    # Message
    if chunk["type"] == "message":
        content = chunk.get("content", "")
        if content:  # Only add non-empty content
            full_response += content
        if chunk.get("end", False):
            full_response += "\n"

    # Code - Only add code blocks if they contain valid code
    if chunk["type"] == "code":
        code_content = chunk.get("content", "").strip()
        print(f"DEBUG: Code chunk content: '{code_content}'")
        
        if chunk.get("start", False):
            # Don't add the opening ``` yet, wait to see if we have valid content
            pass
        
        # Only add valid, non-empty code content
        if code_content and not code_content.isspace():
            # Remove backticks and clean up the code
            code_content = code_content.replace("`", "").strip()
            
            # Validate code syntax
            if validate_code(code_content):
                # Add opening ``` if this is the first valid content in a code block
                if "```python\n" not in full_response[-20:]:
                    full_response += "```python\n"
                full_response += code_content
                if not code_content.endswith('\n'):
                    full_response += '\n'
            else:
                print(f"DEBUG: Invalid code syntax detected, skipping: {code_content}")
                # Don't add anything for invalid code
        
        if chunk.get("end", False):
            # Only add closing ``` if we have an opening ```
            if "```python\n" in full_response and not full_response.endswith("```\n"):
                full_response += "```\n"

    # Console output
    if chunk["type"] == "console":
        console_content = chunk.get("content", "")
        print(f"DEBUG: Console chunk content: '{console_content}'")
        
        if not isinstance(console_content, str):
            console_content = str(console_content)
        
        # Filter out unwanted content
        if console_content.strip() and not console_content.isdigit() and console_content.strip().lower() != "none":
            # Remove backticks
            console_content = console_content.replace("`", "")
            
            if chunk.get("start", False):
                full_response += "```\n"
            
            if chunk.get("format", "") == "active_line":
                full_response += console_content.rstrip("\n") + "\n"
            elif chunk.get("format", "") == "output":
                full_response += console_content.rstrip("\n") + "\n"
            
            if chunk.get("end", False):
                full_response += "```\n"

    # Output/Confirmation - handle carefully
    if chunk["type"] == "confirmation":
        code_content = chunk.get("content", {})
        if isinstance(code_content, dict):
            code = code_content.get("code", "").strip()
            if code and validate_code(code):
                if chunk.get("start", False):
                    full_response += "```python\n"
                full_response += code
                if not code.endswith('\n'):
                    full_response += '\n'
                if chunk.get("end", False):
                    full_response += "```\n"

    # Image
    if chunk["type"] == "image":
        if chunk.get("start", False) or chunk.get("end", False):
            full_response += "\n"
        else:
            image_format = chunk.get("format", "")
            if image_format == "base64.png":
                image_content = chunk.get("content", "")
                if image_content:
                    try:
                        image = Image.open(BytesIO(base64.b64decode(image_content)))
                        new_image = Image.new("RGB", image.size, "white")
                        new_image.paste(image, mask=image.split()[3])
                        buffered = BytesIO()
                        new_image.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        full_response += f"![Image](data:image/png;base64,{img_str})\n"
                    except Exception as e:
                        print(f"DEBUG: Error processing image: {e}")

    return full_response

# SQLiteの設定
db_name = get_db_path("chat_history.db")

def initialize_db():
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(db_name), exist_ok=True)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        type TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def add_message_to_db(role, message_type, content):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (role, type, content) VALUES (?, ?, ?)", (role, message_type, content))
    conn.commit()
    conn.close()

def get_recent_messages(limit=4):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT role, type, content FROM history ORDER BY timestamp DESC LIMIT ?", (limit,))
    messages = cursor.fetchall()
    conn.close()
    return messages[::-1]  # 最新の20件を取得して逆順にする

def format_responses(chunk, full_response):
    # This function will format the response from the interpreter
    return full_response + chunk.get("content", "")

def chat_with_interpreter(message, history=None,passw=None, temperature=None, max_new_tokens=None):
    import os
    
    # 🎯 ここにブレークポイントを設定してください！ (デバッグ開始点)
    print(f"DEBUG: Received message: '{message}'")
    print(f"DEBUG: Password: '{passw}'")
    
    # Check if interpreter is available
    if interpreter is None:
        error_msg = "Error: open-interpreter is not available. Please install it with: pip install open-interpreter"
        print(f"DEBUG: {error_msg}")
        yield error_msg
        return
    
    # Load environment variables if not already loaded
    from dotenv import load_dotenv
    load_dotenv()
    
    # API key configuration
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("api_key")
    if not api_key:
        error_msg = "Error: No Groq API key found. Please set GROQ_API_KEY or api_key environment variable."
        print(f"DEBUG: {error_msg}")
        yield error_msg
        return

    print(f"DEBUG: API key found: {api_key[:10]}...")

    # Configure interpreter with API key
    try:
        interpreter.llm.api_key = api_key
        interpreter.llm.api_base = "https://api.groq.com/openai/v1"
        interpreter.llm.model = "llama3-8b-8192"
        
        # Configure interpreter settings to reduce empty code blocks
        interpreter.auto_run = False  # Don't auto-run code
        interpreter.force_task_completion = False  # Don't force completion
        interpreter.safe_mode = "ask"  # Ask before running code
        
        print("DEBUG: Interpreter configured successfully")
    except Exception as e:
        error_msg = f"Error configuring interpreter: {e}"
        print(f"DEBUG: {error_msg}")
        yield error_msg
        return

    # Password check - get from environment variable
    required_password = os.getenv("OPENINTERPRETER_PASSWORD", "12345")  # fallback to 12345
    if passw != required_password:
        error_msg = "パスワードが正しくありません。正しいパスワードを入力してください。"
        print(f"DEBUG: {error_msg}")
        yield error_msg
        return

    print("DEBUG: Password check passed")

    if message == "reset":
        interpreter.reset()
        yield "Interpreter reset"
        return

    print(f"DEBUG: Processing message: '{message}'")

    full_response = ""
    recent_messages = get_recent_messages(limit=4)

    # Add current user message to database
    add_message_to_db("user", "message", message)

    # Process the chat
    try:
        # Configure interpreter messages
        interpreter.messages = []
        
        print(f"DEBUG: Adding {len(recent_messages)} recent messages to history")
        
        # Add recent history to interpreter
        for role, message_type, content in recent_messages:
            if role == "user":
                interpreter.messages.append({"role": "user", "type": "message", "content": content})
            elif role == "assistant":
                interpreter.messages.append({"role": "assistant", "type": "message", "content": content})
        
        print(f"DEBUG: Starting interpreter.chat() with message: '{message}'")
        
        # Process the current message
        chunk_count = 0
        for chunk in interpreter.chat(message, display=False, stream=True):
            chunk_count += 1
            print(f"DEBUG: Processing chunk {chunk_count}: {type(chunk)} - {chunk}")
            
            if isinstance(chunk, dict):
                old_response = full_response
                full_response = format_response(chunk, full_response)
                
                # Only yield if content was actually added
                if full_response != old_response:
                    print(f"DEBUG: Response updated from '{old_response[-50:]}' to '{full_response[-50:]}'")
                    yield full_response
            else:
                # Handle non-dict chunks
                print(f"DEBUG: Non-dict chunk: {chunk}")
                if hasattr(chunk, 'content'):
                    content = str(chunk.content)
                    if content.strip():  # Only add non-empty content
                        full_response += content
                        yield full_response
                else:
                    content = str(chunk)
                    if content.strip():  # Only add non-empty content
                        full_response += content
                        yield full_response

        print(f"DEBUG: Chat processing completed. Total chunks: {chunk_count}")
        print(f"DEBUG: Final response length: {len(full_response)}")

        # Save the final response
        if full_response.strip():
            add_message_to_db("assistant", "message", full_response)
            print("DEBUG: Response saved to database")
        else:
            print("DEBUG: No response to save (empty)")

    except Exception as e:
        error_msg = f"Error during chat processing: {e}"
        print(f"DEBUG: Exception occurred: {error_msg}")
        yield error_msg
        add_message_to_db("assistant", "error", error_msg)

    yield full_response


def chat_with_interpreter_no_stream(message, history=None, a=None, b=None, c=None, d=None):
    if message == "reset":
        interpreter.reset()
        return "Interpreter reset", history

    full_response = ""
    recent_messages = get_recent_messages()

    for role, message_type, content in recent_messages:
        entry = {"role": role, "type": message_type, "content": content}
        interpreter.messages.append(entry)

    user_entry = {"role": "user", "type": "message", "content": message}
    interpreter.messages.append(user_entry)
    add_message_to_db("user", "message", message)

    chunks = interpreter.chat(message, display=False, stream=False)
    for chunk in chunks:
        if isinstance(chunk, dict):
            full_response = format_response(chunk, full_response)
        else:
            raise TypeError("Expected chunk to be a dictionary")
        #yield full_response
    assistant_entry = {"role": "assistant", "type": "message", "content": str(full_response)}
    interpreter.messages.append(assistant_entry)
    add_message_to_db("assistant", "message", str(full_response))

    #yield full_response
    return str(full_response), history


# 初期化
initialize_db()


PLACEHOLDER = """
<div style="padding: 30px; text-align: center; display: flex; flex-direction: column; align-items: center;">
   <img src="https://ysharma-dummy-chat-app.hf.space/file=/tmp/gradio/8e75e61cc9bab22b7ce3dec85ab0e6db1da5d107/Meta_lockup_positive%20primary_RGB.jpg" style="width: 80%; max-width: 550px; height: auto; opacity: 0.55;  ">
   <h1 style="font-size: 28px; margin-bottom: 2px; opacity: 0.55;">Meta llama3</h1>
   <p style="font-size: 18px; margin-bottom: 2px; opacity: 0.65;">Ask me anything...</p>
</div>
"""

chatbot = gr.Chatbot(height=450, placeholder=PLACEHOLDER, label="Gradio ChatInterface")



gradio_interface = gr.ChatInterface(
    fn=chat_with_interpreter,
    chatbot=chatbot,
    fill_height=True,
    additional_inputs_accordion=gr.Accordion(
        label="⚙️ Parameters", open=False, render=False
    ),
    additional_inputs=[
        gr.Textbox(
            type="password",
            label="パスワード",
            render=True
        ),        
        gr.Slider(
            minimum=0,
            maximum=1,
            step=0.1,
            value=0.95,
            label="Temperature",
            render=False,
        ),
        gr.Slider(
            minimum=128,
            maximum=4096,
            step=1,
            value=512,
            label="Max new tokens",
            render=False,
        ),
        
    ],
    # democs,
    examples=[
        ["HTMLのサンプルを作成して"],
        [
            "CUDA_VISIBLE_DEVICES=0 llamafactory-cli train examples/lora_single_gpu/llama3_lora_sft.yaml"
        ],
    ],
    cache_examples=False,
)

# 自動検出システム用のメタデータ
interface_title = "🤖 Open Interpreter"
interface_description = "コード実行・解釈AIシステム"

if __name__ == '__main__':
    message = f"""
    postgres connection is this postgresql://miyataken999:yz1wPf4KrWTm@ep-odd-mode-93794521.us-east-2.aws.neon.tech/neondb?sslmode=require
    create this tabale 
    CREATE TABLE items (
  id INT PRIMARY KEY,
  brand_name VARCHAR(255),
  model_name VARCHAR(255),
  product_number VARCHAR(255),
  purchase_store VARCHAR(255),
  purchase_date DATE,
  purchase_price INT,
  accessories TEXT,
  condition INT,
  metal_type VARCHAR(255),
  metal_weight DECIMAL(10, 2),
  diamond_certification BLOB,
  initial BOOLEAN
);
    
    """
    chat_with_interpreter(message)
