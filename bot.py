# وارد کردن کتابخانه‌های مورد نیاز
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import os

# ذخیره اطلاعات کاربران
user_data = {}  # در نسخه تولیدی بهتر است از دیتابیس استفاده شود
admin_chat_id = os.getenv("ADMIN_CHAT_ID")  # شناسه تلگرام مدیر از متغیر محیطی خوانده می‌شود

# تابع شروع
def start(update: Update, context: CallbackContext):
    """
    ارسال پیام خوش‌آمدگویی به کاربران و نمایش منوی اصلی.
    """
    keyboard = [[InlineKeyboardButton("ثبت فیش بانکی", callback_data='submit_receipt')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("به ربات ثبت فیش بانکی خوش آمدید. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=reply_markup)

# مدیریت دکمه‌ها
def button_handler(update: Update, context: CallbackContext):
    """
    مدیریت کلیک روی دکمه‌ها توسط کاربران.
    """
    query = update.callback_query
    query.answer()

    if query.data == "submit_receipt":
        keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            "شماره کارت: ۱۲۳۴-۵۶۷۸-۹۰۱۲-۳۴۵۶\nپس از واریز، فیش بانکی خود را در اینجا آپلود کنید.",
            reply_markup=reply_markup
        )
    elif query.data == "main_menu":
        start(update, context)

# مدیریت آپلود فایل‌ها
def document_handler(update: Update, context: CallbackContext):
    """
    ذخیره اطلاعات فیش بانکی ارسال‌شده توسط کاربران و اطلاع‌رسانی به مدیر.
    """
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "نامشخص"
    file_id = update.message.document.file_id

    # ذخیره اطلاعات در حافظه
    user_data[user_id] = {
        "username": username,
        "file_id": file_id
    }

    # ارسال پیام به مدیر
    context.bot.send_message(
        chat_id=admin_chat_id,
        text=f"فیش جدید دریافت شد:\n\nشناسه کاربر: {user_id}\nنام کاربری: @{username}\n"
             f"شناسه فایل: {file_id}\nلطفاً فیش را بررسی کنید."
    )

    update.message.reply_text("فیش شما با موفقیت ارسال شد. لطفاً منتظر بررسی باشید.")

# تابع اصلی اجرای ربات
def main():
    """
    راه‌اندازی و اجرای ربات.
    """
    bot_token = os.getenv("BOT_TOKEN")  # توکن ربات از متغیر محیطی خوانده می‌شود
    updater = Updater(bot_token)

    dp = updater.dispatcher

    # تعریف هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.document, document_handler))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
