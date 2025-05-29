# vibe

**vibe** module provides `@code` decorator that dynamically implements function bodies using a language model (LLM) of your choice — just write the docstring with the description, and vibe does the rest.

### Example

```python
from vibe import code

@code
def add(a, b):
    """Returns the sum of a and b."""

print(add(3, 5))
```

###🔥 Disclaimer
> There are no safety checks or guardrails. If you instruct it to wipe your hard drive in a docstring, it will do so without hesitation. There is a chance it will wipe out your HDD even if you asked it to return the sum of a and b. You've been warned.

### How it Works
When a function decorated with @code is encountered:

1. The decorator inspects the function's signature and docstring.
2. It generates a unique hash based on the prompt used to generate the function.
3. It checks if a cached file for this function and hash exists.
  * If cached: The code from the cache file is loaded and executed.
  * If not cached:
      1. It asks the LLM (configured API endpoint) to provide the implementation.
      2. The LLM's response (the generated Python code for the function) is extracted.
      3. The generated code is then executed to re-define the function.
      4. This generated code is saved to a cache file.
4. The fully implemented function is returned and can be called as usual.

Subsequent calls to the same function (with an unchanged signature and docstring) will use the cached version directly, bypassing the LLM.

### Setup

Install the package (from GitHub or locally):

```
pip install git+https://github.com/facha/vibe.git
```
Create a .env file with your settings:

```
CACHE_DIR=.function_cache
API_URL=http://localhost:8080/v1/chat/completions
API_KEY=dummy
MODEL=llama
```
Make sure your LLM server (llama-server, ollama, etc) is running at the given API_URL (or you could use an OpenAI compatible remote endpoint):

```
brew install llama-server
llama-server -m unsloth_Devstral-Small-2505-GGUF_Devstral-Small-2505-Q8_0.gguf -fa
```

### Run example
```
$ cat examples/basic_usage.py
from vibe import code

@code
def greet(name):
    """Returns a friendly greeting for the given name."""

@code
def fib(n):
    """Return the nth Fibonacci number."""

print(greet("Alice"))
print(fib(10))
```
```
$ uv run examples/basic_usage.py 
Hello, Alice!
34
```

### License

This project is licensed under the MIT License. See `LICENSE` for details.
