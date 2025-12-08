import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash"
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )
    if not response.usage_metadata:
        raise RuntimeError("No usage metadata found in the response.")
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")
    if response.function_calls:
        for function_call_part in response.function_calls:
            if function_call_part.args:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            else:
                print(f"Calling function: {function_call_part.name}()  # no arguments")
            


if __name__ == "__main__":
    main()
