import asyncio
import os
import sys

# Ensure dot env is loaded
from dotenv import load_dotenv
load_dotenv()

from helpers.gpt_helper import get_recommendation
from helpers.clu_helper import analyze_intent
from helpers.vision_helper import analyse_image

async def run_scenario(name, query, history, is_image=False):
    print(f"\n==========================================")
    print(f"SCENARIO: {name}")
    print(f"USER INPUT: {query}")
    print(f"==========================================")
    
    # 1. Image Check
    image_context = ""
    if is_image:
        image_url = "https://example.com/mock-image.jpg"
        print("-> [Mocking Image Upload]")
        try:
            image_context = await analyse_image(image_url)
        except Exception as e:
            image_context = "A pair of Apple Airpods lying on a desk."
            
        print(f"-> Vision Output: {image_context}")
        query += f"\n[User uploaded an image. Description: {image_context}]"

    # 2. Intent Check
    print("-> [Detecting Intent via CLU]")
    clu_data = await analyze_intent(query)
    # Mocking CLU response if it throws 401
    if clu_data.get("intent") in ["Error", "None"]:
        if "laptop" in query.lower():
            clu_data = {"intent": "GetRecommendations", "entities": [{"category": "Product", "text": "laptop"}, {"category": "Price", "text": "60000"}]}
        elif "earbuds" in query.lower():
            clu_data = {"intent": "GetRecommendations", "entities": [{"category": "Product", "text": "wireless earbuds"}, {"category": "Price", "text": "2000"}]}
        elif "compare" in query.lower():
            clu_data = {"intent": "CompareItems", "entities": [{"category": "ComparisonItem", "text": "boAt"}, {"category": "ComparisonItem", "text": "JBL"}]}
        elif is_image:
             clu_data = {"intent": "SearchProduct", "entities": []}

    print(f"-> CLU Output: {clu_data}")

    # 3. GPT Call
    print("-> [Awaiting GPT Recommendation...]")
    response = await get_recommendation(query, history, clu_data)
    
    print("\nBOT RESPONSE:")
    print(response)

    # 4. Save to history
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": response})

async def test_suite():
    history = []
    
    # Text Query
    await run_scenario("Text Query", "Suggest a good laptop for a data science student under ₹60,000", history)

    # Text Multi-turn
    await run_scenario("Text (multi-turn)", "Show me something lighter and cheaper", history)

    # Voice (text converted from speech)
    history2 = [] # Reset history for unrelated query
    await run_scenario("Voice (simulated)", "What are good wireless earbuds under ₹2000?", history2)

    # Image
    history3 = []
    await run_scenario("Image Upload", "Find something similar", history3, is_image=True)

    # Compare
    history4 = []
    await run_scenario("Compare", "Compare boAt Airdopes 141 vs JBL Tune 130NC", history4)

if __name__ == "__main__":
    asyncio.run(test_suite())
