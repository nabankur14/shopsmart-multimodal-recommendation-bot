from aiohttp import web
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.core import BotFrameworkAdapterSettings
from botbuilder.integration.aiohttp import BotFrameworkHttpAdapter
from botbuilder.core import ConversationState, MemoryStorage, UserState

from bots.shop_bot import ShopBot
from dialogs.main_dialog import MainDialog
from config import APP_ID, APP_PASSWORD

SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkHttpAdapter(SETTINGS)

# State management
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

# Dialog and Bot
DIALOG = MainDialog()
BOT = ShopBot(CONVERSATION_STATE, USER_STATE, DIALOG)

from botbuilder.schema import Activity
import json
from helpers.gpt_helper import get_recommendation
from helpers.clu_helper import analyze_intent

async def messages(req: web.Request) -> web.Response:
    if "application/json" in req.headers.get("Content-Type", ""):
        body = await req.json()
    else:
        return web.Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    try:
        response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        if response:
            return web.json_response(data=response.body, status=response.status)
        return web.Response(status=201)
    except Exception as e:
        print(f"Error handling the activity: {e}")
        return web.Response(status=500)
async def direct_chat(req: web.Request) -> web.Response:
    try:
        if "application/json" in req.headers.get("Content-Type", ""):
            body = await req.json()
        else:
            return web.Response(status=415)
            
        user_message = body.get("message", "")
        history = body.get("history", [])
        image_base64 = body.get("image", None)

        if image_base64:
            import base64
            from helpers.vision_helper import analyse_image_bytes
            
            # Remove data URL prefix like "data:image/jpeg;base64,"
            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]
                
            img_bytes = base64.b64decode(image_base64)
            image_context = await analyse_image_bytes(img_bytes)
            user_message += f"\n[User uploaded an image. Description: {image_context}]"
        
        clu_data = await analyze_intent(user_message)
        response = await get_recommendation(user_message, history, clu_data)
        
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})
        
        if len(history) > 10:
            history = history[-10:]
            
        return web.json_response({"response": response, "history": history})
    except Exception as e:
        print(f"Error in direct chat: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def index(req: web.Request) -> web.Response:
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        return web.Response(text=html, content_type="text/html")
    except Exception as e:
        return web.Response(text=f"Error loading index.html: {e}", status=404)

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)
APP.router.add_get("/api/messages", index)
APP.router.add_post("/api/direct_chat", direct_chat)
APP.router.add_get("/", index)

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3978))
    web.run_app(APP, host="0.0.0.0", port=port)
