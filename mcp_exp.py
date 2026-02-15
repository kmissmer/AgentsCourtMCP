from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
subscription_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"


client = AzureOpenAI(
    api_version="2025-01-01-preview",
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Paris, what should I see?",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)