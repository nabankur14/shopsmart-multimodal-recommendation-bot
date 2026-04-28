import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("MicrosoftAppId", "")
APP_PASSWORD = os.getenv("MicrosoftAppPassword", "")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT", "gpt-5.4-nano")

SPEECH_KEY = os.getenv("SPEECH_KEY", "")
SPEECH_REGION = os.getenv("SPEECH_REGION", "centralindia")

VISION_ENDPOINT = os.getenv("VISION_ENDPOINT", "")
VISION_KEY = os.getenv("VISION_KEY", "")

CLU_ENDPOINT = os.getenv("CLU_ENDPOINT", "")
CLU_KEY = os.getenv("CLU_KEY", "")
CLU_PROJECT = os.getenv("CLU_PROJECT", "ShopSmartCLU")
CLU_DEPLOYMENT = os.getenv("CLU_DEPLOYMENT", "production")

AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "search-1776424999149")

COSMOS_KEY = os.getenv("COSMOS_KEY", "")
COSMOS_URI = os.getenv("COSMOS_ENDPOINT", "")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE", "ShopSmartDB")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "Products")
