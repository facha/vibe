import os
import re
import types
import logging
import hashlib
import inspect
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

CACHE_DIR = os.getenv("CACHE_DIR", ".function_cache")
API_URL = os.getenv("API_URL", "http://localhost:8080/v1/chat/completions")
API_KEY = os.getenv("API_KEY", "dummy_key")
MODEL = os.getenv("MODEL", "llama")


def get_signature(func_stub: types.FunctionType) -> str:
    signature = inspect.signature(func_stub)
    signature_str = re.sub(r"\b__\w+__\.", "", str(signature))
    return signature_str

def get_cache_filename(func_stub: types.FunctionType) -> str:
    func_name = func_stub.__name__
    docstring = inspect.getdoc(func_stub) or ""
    signature_str = get_signature(func_stub)
    key_info_str = f"{func_name}{docstring}{signature_str}"
    key_info_hash = hashlib.sha256(key_info_str.encode("utf-8")).hexdigest()
    file_name = os.path.join(CACHE_DIR, f"{func_name}_{key_info_hash}.py")
    return file_name

def load_code_from_cache(func_stub: types.FunctionType) -> str | None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    filename = get_cache_filename(func_stub)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return None

def save_code_to_cache(func_stub: types.FunctionType, generated_code: str):
    filename = get_cache_filename(func_stub)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

def get_func_custom_types(func_stub: types.FunctionType) -> str:
    sources = set()
    for _, annotation_type in func_stub.__annotations__.items(): # Changed annotation_name to _
        try:
            source = inspect.getsource(annotation_type).strip()
            sources.add(source)
        except (OSError, TypeError, AttributeError):
            continue
    return "\n\n".join(sources)

def get_source(func_stub: types.FunctionType) -> str:
    src = ""
    src_file = func_stub.__globals__.get('__file__')
    if src_file and os.path.exists(src_file): 
        with open(src_file, 'r', encoding='utf-8') as f:
            src = f.read()
    return src

def construct_prompt(func_stub: types.FunctionType) -> str:
    func_name = func_stub.__name__
    docstring = inspect.getdoc(func_stub)
    signature = get_signature(func_stub)
    custom_types = get_func_custom_types(func_stub)
    context = get_source(func_stub)
    custom_types_str = ""
    if custom_types:
        custom_types_str = f"""
The function is using the following custom types:
{custom_types}
These types are defined elsewhere. Do not include their definitions into your code.
"""
    prompt = f"""
You are a Python programmer. Write the implementation of the function which signature will be provided below.
{custom_types_str}
The function is executed ih the following context:
--------
{context}
--------
Function to implement:
def {func_name}{signature}:
    \"\"\"{docstring}\"\"\"

Provide the implementation for the function above. Include only function definition. Do not explain it.
"""
    return prompt

def request_code_from_llm(prompt: str) -> str:
    logger.debug(f"prompt:\n{prompt}\n")
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=30,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    code_match = re.search(r"```(?:python)?\s*(.*?)```", content, re.DOTALL)
    generated_code = code_match.group(1).strip() if code_match else content
    logger.debug(f"code:\n{generated_code}\n")
    return generated_code

def code(func_stub: types.FunctionType):
    def wrapper():
        generated_code = load_code_from_cache(func_stub)
        if not generated_code:
            prompt = construct_prompt(func_stub) 
            generated_code = request_code_from_llm(prompt)
            save_code_to_cache(func_stub, generated_code)
        namespace = func_stub.__globals__
        exec(generated_code, namespace)
        return namespace[func_stub.__name__]
    return wrapper()
