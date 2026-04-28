#!/bin/bash

# Configuration
APP_NAME="shopsmart-bot-app"
RESOURCE_GROUP="ShopSmartBot-RG"

echo "Setting Environment Variables for Azure App Service: $APP_NAME..."

az webapp config appsettings set --name $APP_NAME --resource-group $RESOURCE_GROUP --settings \
    MicrosoftAppId="<your-app-id>" \
    MicrosoftAppPassword="<your-app-password>" \
    AZURE_OPENAI_ENDPOINT="https://shopsmart-openai.openai.azure.com/" \
    AZURE_OPENAI_KEY="<your-openai-key>" \
    OPENAI_DEPLOYMENT="gpt-5.4-nano" \
    SPEECH_KEY="<your-speech-key>" \
    SPEECH_REGION="centralindia" \
    VISION_ENDPOINT="https://shopsmart-cv.cognitiveservices.azure.com/" \
    VISION_KEY="<your-vision-key>" \
    CLU_ENDPOINT="https://shopsmart-lang.cognitiveservices.azure.com/" \
    CLU_KEY="<your-clu-key>" \
    CLU_PROJECT="ShopSmartCLU" \
    CLU_DEPLOYMENT="production" \
    AZURE_SEARCH_KEY="<your-search-key>" \
    AZURE_SEARCH_ENDPOINT="https://shopsmart-aisearch.search.windows.net" \
    AZURE_SEARCH_INDEX="search-1776424999149" \
    COSMOS_KEY="<your-cosmos-key>" \
    COSMOS_ENDPOINT="https://shopsmart-cosmos-db.documents.azure.com:443/" \
    COSMOS_DATABASE="ShopSmartDB" \
    COSMOS_CONTAINER="Products"

echo "Done! All environment variables have been set."
echo "You can now run: az webapp up --name $APP_NAME --resource-group $RESOURCE_GROUP --runtime \"PYTHON:3.11\""
