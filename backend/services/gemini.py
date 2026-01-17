import requests
import json
import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
print(api_key)


async def prompt_gemini(prompt):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "google/gemini-3-flash-preview",
                "messages": [{"role": "user", "content": prompt}],
                "reasoning": {"enabled": True},
            },
        )
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]


# if __name__ == "__main__":
# asyncio.run(prompt_gemini("Hello who are you?"))
