import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERATIONS, MODEL_NAME
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
    
    iteration = 0
    while True:
        iteration += 1
        if iteration > MAX_ITERATIONS:
            print(f"Stopped after maximum iterations ({MAX_ITERATIONS}).")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, args.verbose)
            if args.verbose:
                print(f"{'*' * 15} End of iteration {iteration} {'*' * 15}")
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Exception raised in generate_content(): {e}")
            sys.exit(1)

def generate_content(client, messages, verbose):
    client_response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )
    if not client_response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed.")
    
    if verbose:
        print(f"Prompt tokens: {client_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {client_response.usage_metadata.candidates_token_count}")
    
    # Check if model is finished
    if not client_response.function_calls:
        return client_response.text
    
    for candidate in client_response.candidates:
        messages.append(candidate.content)

    function_results = []
    for function_call_part in client_response.function_calls:
        function_result = call_function(function_call_part, verbose)
        if (
            not function_result.parts
            or not function_result.parts[0].function_response.response
        ):
            raise Exception("Empty function call result.")
        
        if verbose:
            print(f"-> {function_result.parts[0].function_response.response}")
        function_results.append(function_result.parts[0])

    if not function_results:
        raise Exception("No function call results to process.")
    messages.append(types.Content(role="user", parts=function_results))
    

if __name__ == "__main__":
    main()
