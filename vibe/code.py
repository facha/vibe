import os
import re
import logging
import inspect
import hashlib
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

CACHE_DIR = os.getenv("CACHE_DIR", ".function_cache")
API_URL = os.getenv("API_URL", "http://localhost:8080/v1/chat/completions")
API_KEY = os.getenv("API_KEY", "dummy_key")
MODEL = os.getenv("MODEL", "llama")


def get_cache_filename(func_name: str, prompt: str) -> str:
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{func_name}_{prompt_hash}.py")

def load_code_from_cache(func_name: str, prompt: str) -> str | None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    filename = get_cache_filename(func_name, prompt)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return None

def save_code_to_cache(func_name: str, prompt: str, generated_code: str):
    filename = get_cache_filename(func_name, prompt)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

def get_func_custom_types(func_stub) -> str:
    sources = set()
    for annotation_name, annotation_type in func_stub.__annotations__.items():
        try:
            source = inspect.getsource(annotation_type).strip()
            sources.add(source)
        except:
           continue
    return "\n\n".join(sources)

def construct_prompt(func_stub) -> str:
    func_name = func_stub.__name__
    signature = inspect.signature(func_stub)
    signature = re.sub(r'\b__\w+__\.', '', str(signature))
    docstring = inspect.getdoc(func_stub)
    custom_types = get_func_custom_types(func_stub)
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
Function to implement:
def {func_name}{signature}:
    \"\"\"{docstring}\"\"\"

Include only the function definition. Do not explain it.
"""
    return prompt

def request_code_from_llm(prompt: str) -> str:
    logger.debug(f"prompt:\n{prompt}\n")
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        },
        timeout=30
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    code_match = re.search(r"```(?:python)?\s*(.*?)```", content, re.DOTALL)
    generated_code = code_match.group(1).strip() if code_match else content
    logger.debug(f"code:\n{generated_code}\n")
    return generated_code

def code(func_stub):
    def wrapper():
        prompt = construct_prompt(func_stub)
        generated_code = load_code_from_cache(func_stub.__name__, prompt)
        if not generated_code:
            generated_code = request_code_from_llm(prompt)
            save_code_to_cache(func_stub.__name__, prompt, generated_code)
        namespace = func_stub.__globals__
        exec(generated_code, namespace)
        return namespace[func_stub.__name__]
    return wrapper()
