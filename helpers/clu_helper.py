from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations.aio import ConversationAnalysisClient # Added .aio
from config import CLU_ENDPOINT, CLU_KEY, CLU_PROJECT, CLU_DEPLOYMENT

async def analyze_intent(query_text: str):
    """Analyze text intent and entities using Azure CLU asynchronously."""
    try:
        if not CLU_ENDPOINT or not CLU_KEY:
            return {"intent": "None", "entities": []}

        # Initialize the async client
        client = ConversationAnalysisClient(CLU_ENDPOINT, AzureKeyCredential(CLU_KEY))
        
        async with client: # Use async with
            result = await client.analyze_conversation( # Added await
                task={
                    "kind": "Conversation",
                    "analysisInput": {
                        "conversationItem": {
                            "participantId": "1",
                            "id": "1",
                            "modality": "text",
                            "language": "en",
                            "text": query_text
                        },
                        "isLoggingEnabled": False
                    },
                    "parameters": {
                        "projectName": CLU_PROJECT,
                        "deploymentName": CLU_DEPLOYMENT,
                        "verbose": True
                    }
                }
            )

        top_intent = result["result"]["prediction"]["topIntent"]
        entities = result["result"]["prediction"]["entities"]
        
        return {
            "intent": top_intent,
            "entities": [{"category": e["category"], "text": e["text"]} for e in entities]
        }
    except Exception as e:
        print(f"Error calling Azure CLU: {e}")
        return {"intent": "Error", "entities": []}
