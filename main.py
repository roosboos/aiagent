import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Check if the prompt was provided
if len(sys.argv) == 1:
    print("Prompt not provided")
    sys.exit(1)


# Get prompt from command line argument
prompt = sys.argv[1]


# Create client
client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]


# Call the model
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages
)

if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    print("User prompt:", prompt)
    print(response.text)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
else:
# Print response
    print(response.text)

