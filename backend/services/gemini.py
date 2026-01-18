import os
import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

timeout = httpx.Timeout(
    connect=10.0,
    read=60.0,
    write=10.0,
    pool=10.0,
)


async def prompt_gemini(prompt):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
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
    except httpx.ReadTimeout:
        print("gemini timed out")
        return None


# if __name__ == "__main__":
# asyncio.run(prompt_gemini("Hello who are you?"))
