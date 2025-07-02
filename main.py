import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions

# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Check if the prompt was provided
if len(sys.argv) == 1:
    print("Prompt not provided")
    sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files


All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

prompt = sys.argv[1]


# Create client
client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

# Call the model
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
)

if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    print("User prompt:", prompt)
    print(response.text)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

if not response.function_calls:
    print (response.text)

for function_call_part in response.function_calls:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")

