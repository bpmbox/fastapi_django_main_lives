# https://colab.research.google.com/drive/1Bg84yu7H7_3-gLi_9kq7dqQUBlY2gID8#scrollTo=GN-l2igNCwjt
from interpreter import interpreter
# 環境変数でOpenAI APIキーを保存および使用
interpreter.auto_run = True
#interpreter.llm.model = "huggingface/meta-llama/Meta-Llama-3-8B-Instruct"
#interpreter.llm.api_key = os.getenv("hf_token")
interpreter.llm.api_base = "https://api.groq.com/openai/v1"
interpreter.llm.api_key = os.getenv("api_key")
interpreter.llm.model = "Llama3-70b-8192"
interpreter.chat()