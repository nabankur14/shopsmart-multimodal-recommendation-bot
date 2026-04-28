"""Main dialog for the ShopSmart bot orchestrating GPT, Vision, Search, and CLU."""

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt
from botbuilder.core import MessageFactory

from helpers.gpt_helper import get_recommendation
from helpers.vision_helper import analyse_image
from helpers.clu_helper import analyze_intent
from helpers.speech_helper import synthesize_speech

class MainDialog(ComponentDialog):
    """Main waterfall dialog to handle the conversation flow with enhanced search and speech logic."""

    def __init__(self):
        super().__init__(MainDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.detect_modality_step,
                    self.call_gpt_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def detect_modality_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Step 1: Process multimodal inputs (Text, Images, potentially Voice hints)."""
        activity = step_context.context.activity
        history_prop = step_context.options.get("history_prop")
        
        # Load conversation history
        history = await history_prop.get(step_context.context, [])
        step_context.values["history"] = history
        step_context.values["history_prop"] = history_prop
        
        user_text = activity.text or ""
        modality_notes = []

        # 1. Handle Images
        if activity.attachments:
            for attachment in activity.attachments:
                if "image" in attachment.content_type:
                    image_url = attachment.content_url
                    image_context = await analyse_image(image_url)
                    modality_notes.append(f"[Visual Context: {image_context}]")

        # 2. Join text and modality context
        if modality_notes:
            user_text = f"{user_text}\n" + "\n".join(modality_notes)

        # 3. Analyze Intent via CLU
        clu_data = None
        if user_text:
            clu_data = await analyze_intent(user_text)

        step_context.values["user_text"] = user_text
        step_context.values["clu_data"] = clu_data

        return await step_context.next(None)

    async def call_gpt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Step 2: Generate response via gpt_helper (which now includes Search) and return to user."""
        user_text = step_context.values["user_text"]
        clu_data = step_context.values["clu_data"]
        history = step_context.values["history"]
        history_prop = step_context.values["history_prop"]

        # Ensure we have something to process
        if not user_text and not clu_data:
            await step_context.context.send_activity("I'm sorry, I didn't catch that. How can I help you?")
            return await step_context.end_dialog()

        # Generate recommendation (now uses search internally)
        response = await get_recommendation(user_text, history, clu_data)

        # Update history
        history.append({"role": "user", "content": user_text})
        history.append({"role": "assistant", "content": response})
        if len(history) > 10:
            history = history[-10:]
        await history_prop.set(step_context.context, history)

        # Send activity (Text and potentially fallback to TTS if desired)
        await step_context.context.send_activity(MessageFactory.text(response))
        
        # Optional: Auto-synthesize speech for short responses if configured
        # synthesize_speech(response) 

        return await step_context.end_dialog()
