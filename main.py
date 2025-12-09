import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MODEL_NAME
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    
    if args.verbose:
        print(f"User prompt: {args.prompt}")
    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )
    if not response.usage_metadata:
        raise RuntimeError("No usage metadata found in the response.")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        print(f"Response:\n{response.text}")
        return

    responses = []
    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response.response
        ):
            raise Exception("Empty function call result.")
        
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")

        responses.append(result.parts[0])
    if not responses:
        raise Exception("No function call responses to process.")

if __name__ == "__main__":
    main()
