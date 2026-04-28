from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    TurnContext,
    UserState,
)
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus

class ShopBot(ActivityHandler):
    """Bot that routes incoming activities to the main dialog."""

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog
        self.dialog_state = self.conversation_state.create_property("DialogState")
        self.history_property = self.conversation_state.create_property("ConversationHistory")

    async def on_turn(self, turn_context: TurnContext):
        """Process every incoming activity."""
        await super().on_turn(turn_context)

        # Persist state changes at the end of each turn
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    async def on_message_activity(self, turn_context: TurnContext):
        """Handle incoming message activities by running the dialog."""
        dialog_set = DialogSet(self.dialog_state)
        dialog_set.add(self.dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()

        if results.status == DialogTurnStatus.Empty:
            # Pass the history_property to the dialog so it can manage it
            await dialog_context.begin_dialog(self.dialog.id, options={"history_prop": self.history_property})

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        """Greet new members when they join the conversation."""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 Welcome to **ShopSmart Bot**! I can help you with:\n\n"
                    "🛒 Product search & recommendations\n"
                    "📷 Image-based product lookup\n"
                    "🎙️ Voice commands\n"
                    "💬 General shopping assistance\n\n"
                    "How can I help you today?"
                )
