"""Helper for Azure AI Search to retrieve product information."""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.aio import SearchClient  # <-- Note the .aio import!
from config import AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, AZURE_SEARCH_INDEX

async def search_products(query: str, top: int = 5):
    """
    Search for products in the Azure AI Search index asynchronously.
    """
    try:
        if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_KEY:
            print("Search credentials not configured.")
            return []

        # Initialize the async client
        search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY)
        )

        # Await the search call
        results = await search_client.search(search_text=query, top=top)
        
        product_list = []
        # Use 'async for' to iterate over the async result generator
        async for result in results:
            product_list.append({
                "name": result.get("name", "Unknown Product"),
                "price": result.get("price", "N/A"),
                "features": result.get("features", ""),
                "description": result.get("description", result.get("content", ""))
            })
            
        # Close the client session when done
        await search_client.close()
            
        return product_list
        
    except Exception as e:
        print(f"Error searching products: {e}")
        return []

if __name__ == "__main__":
    # Quick test harness (requires asyncio to run)
    import asyncio
    
    async def main():
        test_results = await search_products("running shoes")
        for p in test_results:
            print(p)
            
    if __name__ == "__main__":
        asyncio.run(main())