import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pathlib import Path

async def test():
    load_dotenv(Path(__file__).parent.parent / "day08" / "lab" / ".env")
    key = os.getenv("OPENAI_API_KEY")
    print(f"Key exists: {bool(key)}")
    if not key: return
    
    client = AsyncOpenAI(api_key=key)
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in Vietnamese"}],
            max_tokens=10
        )
        print(f"Response: {resp.choices[0].message.content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
