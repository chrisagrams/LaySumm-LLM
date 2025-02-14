from openai import OpenAI
from typing import Tuple
import json
import re
import argparse
from dataset import *

parser = argparse.ArgumentParser(description="Run LaySumm task on ChatGPT compatible API.")
parser.add_argument("--url", help="Base URL of API.", default="http://localhost:1234/v1")
parser.add_argument("--api_key", default="token-abc123")
parser.add_argument("--model")
parser.add_argument("--test_set", default="data/elife/test.json")
parser.add_argument("--output_prefix", default="")
args = parser.parse_args()

client = OpenAI(base_url=args.url, api_key=args.api_key)
model = args.model

def clean_response(response: str) -> str:
    """Remove <think>...</think> sections and strip newlines."""
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    return response.strip()

def submit_query(query: str) -> Tuple[str, dict]:
    completion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": query}]
    )
    message = clean_response(completion.choices[0].message.content)
    usage = completion.usage
    return message, usage

if __name__ == "__main__":
    test_set = load_test_set(args.test_set)
    output_file = f"{model}{args.output_prefix}-laysumm_results.jsonl"
    
    with open(output_file, "w") as jsonl_file:
        for i in test_set:
            query = construct_lay_sum_query(i)
            response, usage = submit_query(query)
            reference = get_reference_sum(i)
            
            result = {
                "key": i['id'],
                "candidate": response,
                "reference": reference,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }
            }
            
            jsonl_file.write(json.dumps(result) + "\n")
            print(f"Key: {i['id']} Prompt Tokens: {usage.prompt_tokens} Completion Tokens: {usage.completion_tokens} Total Tokens: {usage.total_tokens}")

    print(f"Results saved to {output_file}")
