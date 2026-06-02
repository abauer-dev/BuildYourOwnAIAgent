import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

#Parsing additional arguments in cli
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

#API-key from env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("No API-Key provided")

#Connecting client and generate response
client = genai.Client(api_key=api_key)
## saves chat history
messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
    if response.candidates:
        messages.append(response.candidates[0].content)

    #MetaData tracking and printing   
    metadata = response.usage_metadata
    if metadata is None:
        raise RuntimeError("API request failed; no metadata")
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")
        
    print(response.text)

    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if not function_call_result.parts:
                raise Exception("Parts have to be non-empty")
            if not function_call_result.parts[0].function_response:
                raise Exception('"Parts[0].function_response" have to be non-empty')
            if not function_call_result.parts[0].function_response.response:
                raise Exception('".parts[0].function_response.response" have to be non_empty')
            function_results.append(function_call_result.parts[0])
            print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
    else:
        print(response.text)
        sys.exit(0)

print(f"Error: model did not produce a final response after 20 iterations.") 
sys.exit(1)