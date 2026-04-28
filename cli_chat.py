import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from helpers.gpt_helper import get_recommendation
from helpers.clu_helper import analyze_intent

async def chat():
    print("="*50)
    print("Welcome to ShopSmart Bot CLI Terminal! 🛒")
    print("Type your message and press ENTER to chat.")
    print("Type 'quit' or 'exit' to stop.")
    print("="*50 + "\n")
    
    history = []
    
    while True:
        try:
            user_input = input("You: ")
            if not user_input.strip():
                continue
            if user_input.lower() in ['quit', 'exit']:
                print("Bot: Goodbye! Have a great day.")
                break
            
            # Analyze intent (Note: this will display a 401 error print if your CLU keys in .env aren't fixed yet)
            clu_data = await analyze_intent(user_input)
            
            print("Bot is thinking...")
            # Query GPT for response
            response = await get_recommendation(user_input, history, clu_data)
            
            # Print response
            print(f"\nBot: {response}\n")
            print("-" * 50)
            
            # Update history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            
            # Keep history short (last 10 interactions)
            if len(history) > 10:
                history = history[-10:]
                
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(chat())
