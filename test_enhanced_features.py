import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from helpers.search_helper import search_products
from helpers.speech_helper import synthesize_speech

async def test_helpers():
    print("--- Testing AI Search Helper ---")
    query = "running shoes"
    results = search_products(query)
    if results:
        print(f"Success! Found {len(results)} products for '{query}':")
        for p in results:
            print(f"- {p['name']} ({p['price']})")
    else:
        print("No results found. (This is expected if the index is empty or credentials fail)")

    print("\n--- Testing Speech Helper (TTS) ---")
    # Note: This will attempt to use the default speaker, which might not work in some headless environments
    # but the function should return a status string either way.
    tts_result = synthesize_speech("Hello from Shop Smart Bot. Testing synthesis.")
    print(f"TTS result: {tts_result}")

if __name__ == "__main__":
    asyncio.run(test_helpers())
