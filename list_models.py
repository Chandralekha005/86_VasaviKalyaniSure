from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

print("Available Gemini models:\n")

for model in client.models.list():
    print(f"Model name: {model.name}")
    print(f"  Supported methods: {model.supported_generation_methods}")
    print("-" * 60)
