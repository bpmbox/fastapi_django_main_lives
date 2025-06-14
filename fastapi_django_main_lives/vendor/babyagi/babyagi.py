#!/usr/bin/env python3
from dotenv import load_dotenv

# Load default environment variables (.env)
load_dotenv()

import os
import time
import logging
from collections import deque
from typing import Dict, List
import importlib
import openai
import chromadb
import tiktoken as tiktoken
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
import re
from groq import Groq

# default opt out of chromadb telemetry.
from chromadb.config import Settings
from transformers import AutoTokenizer, AutoModel
import torch
import numpy

import psycopg2
import shutil
import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import importlib
import os
import pkgutil
import async_timeout
import asyncio
import sys
from mysite.interpreter.google_chat import send_google_chat_card_thread,send_google_chat_card

args = sys.argv


DESCRIPTION = """
<div>
<h1 style="text-align: center;">develop site</h1>
<p>🦕 共同開発 AIシステム設定 LINE開発 CHATGPTS CHATGPTアシスタント設定 AI自動開発設定 APPSHEET GAS PYTHON</p>
</div>
<!-- Start of HubSpot Embed Code -->
  <script type="text/javascript" id="hs-script-loader" async defer src="//js-na1.hs-scripts.com/46277896.js"></script>
<!-- End of HubSpot Embed Code -->
"""

LICENSE = """
<p/>
<!-- Start of HubSpot Embed Code -->
  <script type="text/javascript" id="hs-script-loader" async defer src="//js-na1.hs-scripts.com/46277896.js"></script>
<!-- End of HubSpot Embed Code -->
---
Built with Meta Llama 3
"""

PLACEHOLDER = """
<div style="padding: 30px; text-align: center; display: flex; flex-direction: column; align-items: center;">
   <img src="https://ysharma-dummy-chat-app.hf.space/file=/tmp/gradio/8e75e61cc9bab22b7ce3dec85ab0e6db1da5d107/Meta_lockup_positive%20primary_RGB.jpg" style="width: 80%; max-width: 550px; height: auto; opacity: 0.55;  ">
   <h1 style="font-size: 28px; margin-bottom: 2px; opacity: 0.55;">Meta llama3</h1>
   <p style="font-size: 18px; margin-bottom: 2px; opacity: 0.65;">Ask me anything...</p>
</div>
"""


# チャットインターフェースの関数定義
# def chat_with_interpreter(message):
#    return "Response: " + message


# カスタムCSSの定義
css = """
.gradio-container {
    height: 100vh; /* 全体の高さを100vhに設定 */
    display: flex;
    flex-direction: column;
}
.gradio-tabs {
    flex: 1; /* タブ全体の高さを最大に設定 */
    display: flex;
    flex-direction: column;
}
.gradio-tab-item {
    flex: 1; /* 各タブの高さを最大に設定 */
    display: flex;
    flex-direction: column;
    overflow: hidden; /* オーバーフローを隠す */
}
.gradio-block {
    flex: 1; /* ブロックの高さを最大に設定 */
    display: flex;
    flex-direction: column;
}
.gradio-chatbot {
    height: 100vh; /* チャットボットの高さを100vhに設定 */
    overflow-y: auto; /* 縦スクロールを有効にする */
}
"""
GENERATION_TIMEOUT_SEC = 60
# Gradio block
chatbot2 = gr.Chatbot(height=450, placeholder=PLACEHOLDER, label="Gradio ChatInterface")



class ProductDatabase:
    def __init__(self, database_url):
        self.database_url = database_url
        self.conn = None
    
    def connect(self):
        self.conn = psycopg2.connect(self.database_url)
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def fetch_data(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM products")
            rows = cursor.fetchall()
            return rows
    
    def update_data(self, product_id, new_price):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE products SET price = %s WHERE id = %s", (new_price, product_id))
            self.conn.commit()

# モデル名を指定
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# トークナイザーとモデルをロード
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
client = chromadb.Client(Settings(anonymized_telemetry=False))

# Engine configuration

# Model: GPT, LLAMA, HUMAN, etc.
LLM_MODEL = os.getenv("LLM_MODEL", os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo")).lower()

# API Keys
OPENAI_API_KEY = os.getenv("api_key", "")
if not (LLM_MODEL.startswith("llama") or LLM_MODEL.startswith("human")):
    assert OPENAI_API_KEY, "\033[91m\033[1m" + "OPENAI_API_KEY environment variable is missing from .env" + "\033[0m\033[0m"

# Table config
RESULTS_STORE_NAME = os.getenv("RESULTS_STORE_NAME", os.getenv("TABLE_NAME", ""))
assert RESULTS_STORE_NAME, "\033[91m\033[1m" + "RESULTS_STORE_NAME environment variable is missing from .env" + "\033[0m\033[0m"

# Run configuration
INSTANCE_NAME = os.getenv("INSTANCE_NAME", os.getenv("BABY_NAME", "BabyAGI"))
COOPERATIVE_MODE = "none"
JOIN_EXISTING_OBJECTIVE = False

# Goal configuration
#OBJECTIVE = os.getenv("OBJECTIVE", "")
OBJECTIVE = "ボットの性能をよくする方法　日本語で説明"
OBJECTIVE = f"""チャットボットでの広告展開"""
thread_name = ""
args = sys.argv
if len(args) > 1:
    print(args[1])
    thread_name = args[1]
    # ファイルを開いて内容を読み込む
    #with open('/home/user/app/babyagi/prompt.txt', 'r') as file:
    #    data = file.read()    
    #thread_name = args[2]

else:
    print("not args")

with open('/home/user/app/babyagi/prompt.txt', 'r') as file:
    OBJECTIVE = file.read()  


INITIAL_TASK = os.getenv("INITIAL_TASK", os.getenv("FIRST_TASK", ""))

# Model configuration
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.0))

def create_vector():
    inputs = tokenizer(result, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    # [CLS]トークンの出力を取得
    embeddings = outputs.last_hidden_state[:,0,:].squeeze().detach().cpu().numpy().tolist()   
    print(embeddings)
    import requests

    url = "https://kenken999-php.hf.space/api/v1.php"

    payload = f"""model_name={embeddings}&vector_text={result}&table=products&action=insert"""
    headers = {
    'X-Auth-Token': 'admin',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'runnerSession=muvclb78zpsdjbm7y9c3; pD1lszvk6ratOZhmmgvkp=13767810ebf0782b0b51bf72dedb63b3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)    
    return True

def insert_product():
    inputs = tokenizer(result, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    # [CLS]トークンの出力を取得
    embeddings = outputs.last_hidden_state[:,0,:].squeeze().detach().cpu().numpy().tolist()   
    print(embeddings)
    import requests

    url = "https://kenken999-php.hf.space/api/v1.php"

    payload = f"""model_name={embeddings}&vector_text={result}&table=products&action=insert"""
    headers = {
    'X-Auth-Token': 'admin',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'runnerSession=muvclb78zpsdjbm7y9c3; pD1lszvk6ratOZhmmgvkp=13767810ebf0782b0b51bf72dedb63b3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)    
    return True


# Extensions support begin

def can_import(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


DOTENV_EXTENSIONS = os.getenv("DOTENV_EXTENSIONS", "").split(" ")

# Command line arguments extension
# Can override any of the above environment variables
ENABLE_COMMAND_LINE_ARGS = (
        os.getenv("ENABLE_COMMAND_LINE_ARGS", "false").lower() == "true"
)
if ENABLE_COMMAND_LINE_ARGS:
    if can_import("extensions.argparseext"):
        from extensions.argparseext import parse_arguments

        OBJECTIVE, INITIAL_TASK, LLM_MODEL, DOTENV_EXTENSIONS, INSTANCE_NAME, COOPERATIVE_MODE, JOIN_EXISTING_OBJECTIVE = parse_arguments()

# Human mode extension
# Gives human input to babyagi
if LLM_MODEL.startswith("human"):
    if can_import("extensions.human_mode"):
        from extensions.human_mode import user_input_await

# Load additional environment variables for enabled extensions
# TODO: This might override the following command line arguments as well:
#    OBJECTIVE, INITIAL_TASK, LLM_MODEL, INSTANCE_NAME, COOPERATIVE_MODE, JOIN_EXISTING_OBJECTIVE
if DOTENV_EXTENSIONS:
    if can_import("extensions.dotenvext"):
        from extensions.dotenvext import load_dotenv_extensions

        load_dotenv_extensions(DOTENV_EXTENSIONS)

# TODO: There's still work to be done here to enable people to get
# defaults from dotenv extensions, but also provide command line
# arguments to override them

# Extensions support end

print("\033[95m\033[1m" + "\n*****CONFIGURATION*****\n" + "\033[0m\033[0m")
print(f"Name  : {INSTANCE_NAME}")
print(f"Mode  : {'alone' if COOPERATIVE_MODE in ['n', 'none'] else 'local' if COOPERATIVE_MODE in ['l', 'local'] else 'distributed' if COOPERATIVE_MODE in ['d', 'distributed'] else 'undefined'}")
print(f"LLM   : {LLM_MODEL}")


# Check if we know what we are doing
assert OBJECTIVE, "\033[91m\033[1m" + "OBJECTIVE environment variable is missing from .env" + "\033[0m\033[0m"
assert INITIAL_TASK, "\033[91m\033[1m" + "INITIAL_TASK environment variable is missing from .env" + "\033[0m\033[0m"

LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "models/llama-13B/ggml-model.bin")
if LLM_MODEL.startswith("llama"):
    if can_import("llama_cpp"):
        from llama_cpp import Llama

        print(f"LLAMA : {LLAMA_MODEL_PATH}" + "\n")
        assert os.path.exists(LLAMA_MODEL_PATH), "\033[91m\033[1m" + f"Model can't be found." + "\033[0m\033[0m"

        CTX_MAX = 1024
        LLAMA_THREADS_NUM = int(os.getenv("LLAMA_THREADS_NUM", 8))

        print('Initialize model for evaluation')
        llm = Llama(
            model_path=LLAMA_MODEL_PATH,
            n_ctx=CTX_MAX,
            n_threads=LLAMA_THREADS_NUM,
            n_batch=512,
            use_mlock=False,
        )

        print('\nInitialize model for embedding')
        llm_embed = Llama(
            model_path=LLAMA_MODEL_PATH,
            n_ctx=CTX_MAX,
            n_threads=LLAMA_THREADS_NUM,
            n_batch=512,
            embedding=True,
            use_mlock=False,
        )

        print(
            "\033[91m\033[1m"
            + "\n*****USING LLAMA.CPP. POTENTIALLY SLOW.*****"
            + "\033[0m\033[0m"
        )
    else:
        print(
            "\033[91m\033[1m"
            + "\nLlama LLM requires package llama-cpp. Falling back to GPT-3.5-turbo."
            + "\033[0m\033[0m"
        )
        LLM_MODEL = "gpt-3.5-turbo"

if LLM_MODEL.startswith("gpt-4"):
    print(
        "\033[91m\033[1m"
        + "\n*****USING GPT-4. POTENTIALLY EXPENSIVE. MONITOR YOUR COSTS*****"
        + "\033[0m\033[0m"
    )

if LLM_MODEL.startswith("human"):
    print(
        "\033[91m\033[1m"
        + "\n*****USING HUMAN INPUT*****"
        + "\033[0m\033[0m"
    )

print("\033[94m\033[1m" + "\n*****OBJECTIVE*****\n" + "\033[0m\033[0m")
print(f"{OBJECTIVE}")

if not JOIN_EXISTING_OBJECTIVE:
    print("\033[93m\033[1m" + "\nInitial task:" + "\033[0m\033[0m" + f" {INITIAL_TASK}")
else:
    print("\033[93m\033[1m" + f"\nJoining to help the objective" + "\033[0m\033[0m")

# Configure OpenAI
openai.api_key = os.getenv("api_key")


# Llama embedding function
class LlamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        return


    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = []
        for t in texts:
            #e = llm_embed.embed(t)
            inputs = tokenizer(t, return_tensors="pt")
            outputs = model(**inputs)
            # [CLS]トークンの出力を取得
            e = outputs.last_hidden_state[:,0,:].squeeze().detach().cpu().numpy().tolist()
            embeddings.append(e)
        return embeddings


# Results storage using local ChromaDB
class DefaultResultsStorage:
    def __init__(self):
        logging.getLogger('chromadb').setLevel(logging.ERROR)
        # Create Chroma collection
        chroma_persist_dir = "chroma"
        chroma_client = chromadb.PersistentClient(
            settings=chromadb.config.Settings(
                persist_directory=chroma_persist_dir,
            )
        )

        metric = "cosine"
        #if LLM_MODEL.startswith("llama"):
        embedding_function = LlamaEmbeddingFunction()
        #else:
        #    embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)
        self.collection = chroma_client.get_or_create_collection(
            name=RESULTS_STORE_NAME,
            metadata={"hnsw:space": metric},
            embedding_function=embedding_function,
        )



    def add(self, task: Dict, result: str, result_id: str):

        # Break the function if LLM_MODEL starts with "human" (case-insensitive)
        if LLM_MODEL.startswith("human"):
            return
        #return
        #from langchain_community.chat_models import ChatOpenAI    
        # Continue with the rest of the function
        #llm_embed = ChatOpenAI(model_name="lama3-70b-8192",
        #                            openai_api_key="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",
        #                            openai_api_base="https://api.groq.com/openai/v1",
        #                            )        
        #import openai
        #openai.api_key = "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"
        #openai.api_base = "https://api.groq.com/openai/v1"
        #response = openai.embeddings.create(input=result, 
        #                                    model="lama3-70b-8192",                                          
        #
        inputs = tokenizer(result, return_tensors="pt", max_length=512, truncation=True)
        outputs = model(**inputs)
        # [CLS]トークンの出力を取得
        embeddings = outputs.last_hidden_state[:,0,:].squeeze().detach().cpu().numpy().tolist()   
        #print(embeddings)
        import requests

        url = "https://kenken999-php.hf.space/api/v1.php"

        payload = f"""model_name={embeddings}&vector_text={result}&table=products&action=insert"""
        headers = {
        'X-Auth-Token': 'admin',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'runnerSession=muvclb78zpsdjbm7y9c3; pD1lszvk6ratOZhmmgvkp=13767810ebf0782b0b51bf72dedb63b3'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        #cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze()
        # テンソルが CPU 上にあることを確認し、NumPy 配列に変換
        #cls_embedding_np = cls_embedding.detach().cpu().numpy()        
                                        
        #embeddings = response['data'][0]['embedding']        
        #embeddings = llm_embed.embed(result) if LLM_MODEL.startswith("llama") else None
        if (
                len(self.collection.get(ids=[result_id], include=[])["ids"]) > 0
        ):  # Check if the result already exists
            self.collection.update(
                ids=result_id,
                embeddings=embeddings,
                documents=result,
                metadatas={"task": task["task_name"], "result": result},
            )
        else:
            self.collection.add(
                ids=result_id,
                embeddings=embeddings,
                documents=result,
                metadatas={"task": task["task_name"], "result": result},
            )

    def query(self, query: str, top_results_num: int) -> List[dict]:
        count: int = self.collection.count()
        if count == 0:
            return []
        results = self.collection.query(
            query_texts=query,
            n_results=min(top_results_num, count),
            include=["metadatas"]
        )
        return [item["task"] for item in results["metadatas"][0]]


# Initialize results storage
def try_weaviate():
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "")
    WEAVIATE_USE_EMBEDDED = os.getenv("WEAVIATE_USE_EMBEDDED", "False").lower() == "true"
    if (WEAVIATE_URL or WEAVIATE_USE_EMBEDDED) and can_import("extensions.weaviate_storage"):
        WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")
        from extensions.weaviate_storage import WeaviateResultsStorage
        print("\nUsing results storage: " + "\033[93m\033[1m" + "Weaviate" + "\033[0m\033[0m")
        return WeaviateResultsStorage(OPENAI_API_KEY, WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_USE_EMBEDDED, LLM_MODEL, LLAMA_MODEL_PATH, RESULTS_STORE_NAME, OBJECTIVE)
    return None

def try_pinecone():
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    if PINECONE_API_KEY and can_import("extensions.pinecone_storage"):
        PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
        assert (
            PINECONE_ENVIRONMENT
        ), "\033[91m\033[1m" + "PINECONE_ENVIRONMENT environment variable is missing from .env" + "\033[0m\033[0m"
        from extensions.pinecone_storage import PineconeResultsStorage
        print("\nUsing results storage: " + "\033[93m\033[1m" + "Pinecone" + "\033[0m\033[0m")
        return PineconeResultsStorage(OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENVIRONMENT, LLM_MODEL, LLAMA_MODEL_PATH, RESULTS_STORE_NAME, OBJECTIVE)
    return None

def use_chroma():
    print("\nUsing results storage: " + "\033[93m\033[1m" + "Chroma (Default)" + "\033[0m\033[0m")
    return DefaultResultsStorage()

results_storage = try_weaviate() or try_pinecone() or use_chroma()

# Task storage supporting only a single instance of BabyAGI
class SingleTaskListStorage:
    def __init__(self):
        self.tasks = deque([])
        self.task_id_counter = 0

    def append(self, task: Dict):
        self.tasks.append(task)

    def replace(self, tasks: List[Dict]):
        self.tasks = deque(tasks)

    def popleft(self):
        return self.tasks.popleft()

    def is_empty(self):
        return False if self.tasks else True

    def next_task_id(self):
        self.task_id_counter += 1
        return self.task_id_counter

    def get_task_names(self):
        return [t["task_name"] for t in self.tasks]


# Initialize tasks storage
tasks_storage = SingleTaskListStorage()
if COOPERATIVE_MODE in ['l', 'local']:
    if can_import("extensions.ray_tasks"):
        import sys
        from pathlib import Path

        sys.path.append(str(Path(__file__).resolve().parent))
        from extensions.ray_tasks import CooperativeTaskListStorage

        tasks_storage = CooperativeTaskListStorage(OBJECTIVE)
        print("\nReplacing tasks storage: " + "\033[93m\033[1m" + "Ray" + "\033[0m\033[0m")
elif COOPERATIVE_MODE in ['d', 'distributed']:
    pass


def limit_tokens_from_string(string: str, model: str, limit: int) -> str:
    """Limits the string to a number of tokens (estimated)."""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except:
        encoding = tiktoken.encoding_for_model('gpt2')  # Fallback for others.

    encoded = encoding.encode(string)

    return encoding.decode(encoded[:limit])


def openai_call(
    prompt: str,
    model: str = LLM_MODEL,
    temperature: float = OPENAI_TEMPERATURE,
    max_tokens: int = 100,
):
    while True:
        print("--------------------------------------------------------------------------------------")
        messages=[
            {
                "role": "user",
                "content": "prompt"
            }
        ],
        print(prompt)
        #return
        client = Groq(api_key=os.getenv("api_key"))
        res = ""
        print("--------------------------------------------------------------------------------------")
        print(prompt)
        completion = client.chat.completions.create(
                        model="llama3-70b-8192",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=1,
                        max_tokens=4024,
                        top_p=1,
                        stream=True,
                        stop=None,
                    )
        for chunk in completion:
            #print(chunk.choices[0].delta.content)
            #print(chunk.choices[0].delta.content or "", end="")
            res += chunk.choices[0].delta.content or ""
        return res

    while True:


        try:
            if model.lower().startswith("llama"):
                result = llm(prompt[:CTX_MAX],
                             stop=["### Human"],
                             echo=False,
                             temperature=0.2,
                             top_k=40,
                             top_p=0.95,
                             repeat_penalty=1.05,
                             max_tokens=200)
                # print('\n*****RESULT JSON DUMP*****\n')
                # print(json.dumps(result))
                # print('\n')
                for chunk in completion:
                    print(chunk.choices[0].delta.content or "", end="")
                return result['choices'][0]['text'].strip()
            elif model.lower().startswith("human"):
                return user_input_await(prompt)
            elif not model.lower().startswith("gpt-"):
                # Use completion API
                response = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                return response.choices[0].text.strip()
            else:
                # Use 4000 instead of the real limit (4097) to give a bit of wiggle room for the encoding of roles.
                # TODO: different limits for different models.

                trimmed_prompt = limit_tokens_from_string(prompt, model, 4000 - max_tokens)

                # Use chat completion API
                messages = [{"role": "system", "content": trimmed_prompt}]
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                )
                return response.choices[0].message.content.strip()
        except openai.error.RateLimitError:
            print(
                "   *** The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.Timeout:
            print(
                "   *** OpenAI API timeout occurred. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.APIError:
            print(
                "   *** OpenAI API error occurred. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.APIConnectionError:
            print(
                "   *** OpenAI API connection error occurred. Check your network settings, proxy configuration, SSL certificates, or firewall rules. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.InvalidRequestError:
            print(
                "   *** OpenAI API invalid request. Check the documentation for the specific API method you are calling and make sure you are sending valid and complete parameters. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.ServiceUnavailableError:
            print(
                "   *** OpenAI API service unavailable. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        else:
            break


def task_creation_agent(
        objective: str, result: Dict, task_description: str, task_list: List[str]
):
    prompt = f"""
You are to use the result from an execution agent to create new tasks with the following objective: {objective}.
The last completed task has the result: \n{result["data"]}
This result was based on this task description: {task_description}.\n"""

    if task_list:
        prompt += f"These are incomplete tasks: {', '.join(task_list)}\n"
    prompt += "Based on the result, return a list of tasks to be completed in order to meet the objective. "
    if task_list:
        prompt += "These new tasks must not overlap with incomplete tasks. "

    prompt += """
Return one task per line in your response. The result must be a numbered list in the format:

#. First task
#. Second task

The number of each entry must be followed by a period. If your list is empty, write "There are no tasks to add at this time."
Unless your list is empty, do not include any headers before your numbered list or follow your numbered list with any other output."""

    print(f'\n*****TASK CREATION AGENT PROMPT****\n{prompt}\n')
    response = openai_call(prompt, max_tokens=4000)
    print(f'\n****TASK CREATION AGENT RESPONSE****\n{response}\n')
    new_tasks = response.split('\n')
    new_tasks_list = []
    for task_string in new_tasks:
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = ''.join(s for s in task_parts[0] if s.isnumeric())
            task_name = re.sub(r'[^\w\s_]+', '', task_parts[1]).strip()
            if task_name.strip() and task_id.isnumeric():
                new_tasks_list.append(task_name)
            # print('New task created: ' + task_name)

    out = [{"task_name": task_name} for task_name in new_tasks_list]
    return out


def prioritization_agent():
    task_names = tasks_storage.get_task_names()
    bullet_string = '\n'

    prompt = f"""
You are tasked with prioritizing the following tasks: {bullet_string + bullet_string.join(task_names)}
Consider the ultimate objective of your team: {OBJECTIVE}.
Tasks should be sorted from highest to lowest priority, where higher-priority tasks are those that act as pre-requisites or are more essential for meeting the objective.
Do not remove any tasks. Return the ranked tasks as a numbered list in the format:

#. First task
#. Second task

The entries must be consecutively numbered, starting with 1. The number of each entry must be followed by a period.
Do not include any headers before your ranked list or follow your list with any other output."""

    print(f'\n****TASK PRIORITIZATION AGENT PROMPT****\n{prompt}\n')
    response = openai_call(prompt, max_tokens=2000)
    print(f'\n****TASK PRIORITIZATION AGENT RESPONSE****\n{response}\n')
    if not response:
        print('Received empty response from priotritization agent. Keeping task list unchanged.')
        return
    new_tasks = response.split("\n") if "\n" in response else [response]
    new_tasks_list = []
    for task_string in new_tasks:
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = ''.join(s for s in task_parts[0] if s.isnumeric())
            task_name = re.sub(r'[^\w\s_]+', '', task_parts[1]).strip()
            if task_name.strip():
                new_tasks_list.append({"task_id": task_id, "task_name": task_name})

    return new_tasks_list


# Execute a task based on the objective and five previous tasks
def execution_agent(objective: str, task: str) -> str:
    """
    Executes a task based on the given objective and previous context.

    Args:
        objective (str): The objective or goal for the AI to perform the task.
        task (str): The task to be executed by the AI.

    Returns:
        str: The response generated by the AI for the given task.

    """

    context = context_agent(query=objective, top_results_num=5)
    # print("\n****RELEVANT CONTEXT****\n")
    # print(context)
    # print('')
    prompt = f'Perform one task based on the following objective: {objective}.\n'
    if context:
        prompt += 'Take into account these previously completed tasks:' + '\n'.join(context)
    prompt += f'\nYour task: {task}\nResponse:'
    return openai_call(prompt, max_tokens=2000)


# Get the top n completed tasks for the objective
def context_agent(query: str, top_results_num: int):
    """
    Retrieves context for a given query from an index of tasks.

    Args:
        query (str): The query or objective for retrieving context.
        top_results_num (int): The number of top results to retrieve.

    Returns:
        list: A list of tasks as context for the given query, sorted by relevance.

    """
    results = results_storage.query(query=query, top_results_num=top_results_num)
    # print("****RESULTS****")
    # print(results)
    return results


# Add the initial task if starting new objective
if not JOIN_EXISTING_OBJECTIVE:
    initial_task = {
        "task_id": tasks_storage.next_task_id(),
        "task_name": INITIAL_TASK
    }
    tasks_storage.append(initial_task)

import os
def main():
    loop = True
    webhook_url = os.getenv("chat_url")
    #OBJECTIVE = message
    loop = True
    result_all = ""
    count = 0
    thread_name = send_google_chat_card(webhook_url,OBJECTIVE,OBJECTIVE+"\r\n"+result_all,"タスク定義","タスク定義")
    while loop:
        result_all = ""
        # As long as there are tasks in the storage...
        if not tasks_storage.is_empty():
        #OBJECTIVE = "ボットの性能をよくする方法　日本語で説明"
            # Print the task list
            print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
            print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
            for t in tasks_storage.get_task_names():
                print(" • " + str(t))
                #yield str(t)
                result_all += str(t)+"\r\n"
            send_google_chat_card_thread(webhook_url,OBJECTIVE,OBJECTIVE+"\r\n"+result_all,"タスク定義","タスク定義",thread_name)

            # Step 1: Pull the first incomplete task
            task = tasks_storage.popleft()
            print("\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m")
            #yield "\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m"
            print(str(task["task_name"]))
            #yield str(task["task_name"])
            result_all += str(task["task_name"])+"\r\n"
            send_google_chat_card_thread(webhook_url,OBJECTIVE,OBJECTIVE+"\r\n"+result_all,"タスク定義","タスク定義",thread_name)


            # Send to execution function to complete the task based on the context
            result = execution_agent(OBJECTIVE+" 回答は日本語でして下さい", str(task["task_name"]))
            print("\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m")
            #yield "\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m"
            print(result)
            #yield result
            result_all += result+"\r\n"
            send_google_chat_card_thread(webhook_url,OBJECTIVE,OBJECTIVE+"\r\n"+result_all,"タスク定義","タスク定義",thread_name)

            #yield result_all

            # Step 2: Enrich result and store in the results storage
            # This is where you should enrich the result if needed
            enriched_result = {
                "data": result
            }
            # extract the actual result from the dictionary
            # since we don't do enrichment currently
            vector = enriched_result["data"]

            result_id = f"result_{task['task_id']}"

            results_storage.add(task, result, result_id)

            # Step 3: Create new tasks and re-prioritize task list
            # only the main instance in cooperative mode does that
            new_tasks = task_creation_agent(
                OBJECTIVE,
                enriched_result,
                task["task_name"],
                tasks_storage.get_task_names(),
            )

            print('Adding new tasks to task_storage')
            for new_task in new_tasks:
                new_task.update({"task_id": tasks_storage.next_task_id()})
                print(str(new_task))
                tasks_storage.append(new_task)

            if not JOIN_EXISTING_OBJECTIVE:
                prioritized_tasks = prioritization_agent()
                if prioritized_tasks:
                    tasks_storage.replace(prioritized_tasks)

            # Sleep a bit before checking the task list again
            time.sleep(3)
            count += 1
            if count > 5:
                loop = False
        else:
            print('Done.')
            loop = False
    return result_all

if __name__ == "__main__":
    main()


def completion(message: str, history=None, c=None, d=None, prompt="あなたは日本語の優秀なアシスタントです。"):
    OBJECTIVE = message
    loop = True
    result_all = ""
    count = 0
    while loop:
        result_all = ""
        # As long as there are tasks in the storage...
        if not tasks_storage.is_empty():
        #OBJECTIVE = "ボットの性能をよくする方法　日本語で説明"
            # Print the task list
            print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
            for t in tasks_storage.get_task_names():
                print(" • " + str(t))
                yield str(t)
                result_all += str(t)+"\r\n"

            # Step 1: Pull the first incomplete task
            task = tasks_storage.popleft()
            print("\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m")
            yield "\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m"
            print(str(task["task_name"]))
            yield str(task["task_name"])
            result_all += str(task["task_name"])+"\r\n"

            # Send to execution function to complete the task based on the context
            result = execution_agent(OBJECTIVE, str(task["task_name"]))
            print("\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m")
            yield "\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m"
            print(result)
            yield result
            result_all += result+"\r\n"
            yield result_all

            # Step 2: Enrich result and store in the results storage
            # This is where you should enrich the result if needed
            enriched_result = {
                "data": result
            }
            # extract the actual result from the dictionary
            # since we don't do enrichment currently
            vector = enriched_result["data"]

            result_id = f"result_{task['task_id']}"

            results_storage.add(task, result, result_id)

            # Step 3: Create new tasks and re-prioritize task list
            # only the main instance in cooperative mode does that
            new_tasks = task_creation_agent(
                OBJECTIVE,
                enriched_result,
                task["task_name"],
                tasks_storage.get_task_names(),
            )

            print('Adding new tasks to task_storage')
            for new_task in new_tasks:
                new_task.update({"task_id": tasks_storage.next_task_id()})
                print(str(new_task))
                tasks_storage.append(new_task)

            if not JOIN_EXISTING_OBJECTIVE:
                prioritized_tasks = prioritization_agent()
                if prioritized_tasks:
                    try:
                        tasks_storage.replace(prioritized_tasks)
                    except Exception as e:
                        print(f"Error during replace: {e}")
                        pass
                    
            # Sleep a bit before checking the task list again
            time.sleep(1)
            count += 1
            if count > 2:
                loop = False
        else:
            print('Done.')
            loop = False
    return result_all



with gr.Blocks(fill_height=True, css=css) as gradio_babyagi:
    # gr.Markdown(DESCRIPTION)
    # gr.DuplicateButton(value="Duplicate Space for private use", elem_id="duplicate-button")
    gr.ChatInterface(
        fn=completion,
        chatbot=chatbot2,
        fill_height=True,
        additional_inputs_accordion=gr.Accordion(
            label="⚙️ Parameters", open=False, render=False
        ),
        additional_inputs=[
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
        examples=[
            ["HTMLのサンプルを作成して"],
            [
                "CUDA_VISIBLE_DEVICES=0 llamafactory-cli train examples/lora_single_gpu/llama3_lora_sft.yaml"
            ],
        ],
        cache_examples=False,
    )

    gr.Markdown(LICENSE)
   

def test_postgres():
    # データベース接続情報
    DATABASE_URL = os.getenv("postgre_url")
    
    # ProductDatabaseクラスのインスタンスを作成
    db = ProductDatabase(DATABASE_URL)
    
    # データベースに接続
    db.connect()
    
    try:
        # データを取得
        products = db.fetch_data()
        print("Fetched products:")
        for product in products:
            print(product)
        
        # データを更新（例: 価格を更新）
        for product in products:
            product_id = product[0]
            print(product_id)
            #new_price = product[2] * 1.1  # 価格を10%増加させる
            #db.update_data(product_id, new_price)
            #print(f"Updated product ID {product_id} with new price {new_price}")
    
    finally:
        # 接続を閉じる
        db.close()