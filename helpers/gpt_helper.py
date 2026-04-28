from openai import AsyncAzureOpenAI  # <-- Swapped to AsyncAzureOpenAI
from config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, OPENAI_DEPLOYMENT
from helpers.search_helper import search_products
import json

# Initialize the async client
client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2025-04-01-preview"
)

SYSTEM_PROMPT = """You are ShopBot, an intelligent and helpful product recommendation assistant 
for ShopSmart India. 

Your goal is to recommend the best products based on the user query and the provided search results from our database.
If search results are available, use them to provide accurate information about name, price, and features.
If no search results match, try to provide general recommendations but clearly state they are from your general knowledge.

For each product provide:
- Name
- Price (in Rupees)
- 2 Key Features
- A one-sentence justification

Keep responses friendly, helpful, and concise. Rank recommendations by relevance."""

async def get_recommendation(user_query: str, history: list, clu_data: dict = None) -> str:
    # 1. Fetch context from Azure AI Search ASYNCHRONOUSLY
    search_results = await search_products(user_query)  # <-- Added await here
    
    search_context = ""
    if search_results:
        search_context = "\n\n[DATABASE CONTEXT - Use these products for recommendations]:\n"
        for p in search_results:
            search_context += f"- Product: {p['name']}, Price: {p['price']}, Features: {p['description']}\n"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    
    # 2. Enhance user query with CLU and Search Context
    enhanced_user_content = user_query
    if clu_data and clu_data.get("intent") != "None":
        intent_info = f"\n[System Note - Detected Intent: {clu_data.get('intent')}. Entities: {json.dumps(clu_data.get('entities'))}]"
        enhanced_user_content += intent_info
    
    if search_context:
        enhanced_user_content += search_context

    messages.append({"role": "user", "content": enhanced_user_content})
    
    try:
        # 3. Call Azure OpenAI ASYNCHRONOUSLY
        response = await client.chat.completions.create(  # <-- Added await here
            model=OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=0.3,
            max_completion_tokens=800  # Reverted back as the specific resource requires 'max_completion_tokens'
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Azure OpenAI: {e}")
        return "I'm having trouble fetching recommendations right now."
