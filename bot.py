import time
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = "8515645903:AAHGepuwub9UX6kEUoaaBMVgSVc0BFRL9Ps"
OWNER_CHAT_ID = 712674739
KEYWORDS = ["arsyad", "Arsyad", "4S2"]
REMINDER_INTERVAL = 300  # 5 minit

pending_alert = {}

def reminder_loop(context: CallbackContext, user_id, message_text):
    while pending_alert.get(user_id, False):
        context.bot.send_message(
            chat_id=user_id,
            text=f"🔔 PERINGATAN: Anda ada mesej penting yang belum disahkan.\n\nMesej:\n{message_text}",
        )
        time.sleep(REMINDER_INTERVAL)

def check_message(update: Update, context: CallbackContext):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return
    text = update.message.text or ""
    if any(k in text for k in KEYWORDS):
        message_text = update.message.text
        keyboard = [[InlineKeyboardButton("✔ Selesai", callback_data="done")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=f"📌 Mesej penting dikesan:\n\n{message_text}",
            reply_markup=reply_markup
        )
        pending_alert[OWNER_CHAT_ID] = True
        threading.Thread(target=reminder_loop, args=(context, OWNER_CHAT_ID, message_text)).start()

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    if query.data == "done":
        pending_alert[user_id] = False
        query.answer("Reminder dihentikan.")
        query.edit_message_text("✔ Tugas disahkan. Reminder dihentikan.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

