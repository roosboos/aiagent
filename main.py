import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

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

is_verbose = False

if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    is_verbose = True

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_call_part.args["working_directory"] = "./calculator"
    

    if function_call_part.name not in func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"}
                )
            ],
        )
    else:
        result = func[function_call_part.name](**function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result}
                )
            ],
        )
        

func = {"get_file_content": get_file_content, "get_files_info": get_files_info, "run_python_file": run_python_file, "write_file": write_file}

    
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
    result = call_function(function_call_part, is_verbose)
    if result and result.parts and hasattr(result.parts[0], 'function_response') and hasattr(result.parts[0].function_response, 'response'):
        print(f"-> {result.parts[0].function_response.response}")
    else:
        raise Exception ("function response not within")