import os

MAX_CONCURRENT_TASKS = 10
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

TOKEN_COSTS = {
    "gpt-4-1106-preview": {"input": 0.01 / 1000, "output": 0.03 / 1000},
    "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
    "gpt-3.5-turbo-1106": {"input": 0.0010 / 1000, "output": 0.0020 / 1000}
}
