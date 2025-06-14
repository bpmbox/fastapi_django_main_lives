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
from mysite.interpreter.google_chat import send_google_chat_card


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