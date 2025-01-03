# banking-receipt-bot
این پروژه یک ربات تلگرام برای مدیریت و ثبت فیش‌های بانکی است. کاربران می‌توانند پس از واریز مبلغ به شماره کارت اعلام‌شده، فیش بانکی خود را در ربات آپلود کنند. ربات اطلاعات مربوط به فیش را همراه با شناسه کاربری و نام کاربر به مدیر ارسال می‌کند تا مدیر بتواند فیش‌ها را تأیید یا رد کند.

### ایجاد ربات تلگرام برای ثبت فیش بانکی

در این مستند، تمام مراحل طراحی، توسعه، و اجرای یک ربات تلگرام برای ثبت فیش بانکی توضیح داده می‌شود. ربات به کاربران امکان می‌دهد فیش بانکی خود را آپلود کنند و مدیر ربات بتواند آن را تأیید یا رد کند.

---

#### مرحله ۱: آماده‌سازی سرور

۱. یک **سرور مجازی (VPS)** خریداری کنید که منابع کافی برای اجرای یک اسکریپت ساده Python داشته باشد.
[خرید سرور مجازی از ایران سون](https://iran7.net)
2. سیستم‌عامل پیشنهادی **Ubuntu 22.04** است.
3. از طریق SSH به سرور متصل شوید و بسته‌های سیستم را به‌روزرسانی کنید:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

4. نصب Python:
   ```bash
   sudo apt install python3 python3-pip -y
   ```

5. نصب کتابخانه‌های مورد نیاز:
   ```bash
   pip install python-telegram-bot
   ```

---

#### مرحله ۲: ایجاد ربات در BotFather

1. به **BotFather** در تلگرام مراجعه کنید و دستور `/newbot` را وارد کنید.
2. نام و نام کاربری (username) ربات را مشخص کنید.
3. توکن دسترسی (API Token) تولیدشده را کپی کنید.

---

#### مرحله ۳: کدنویسی ربات

کد کامل ربات را در ادامه مشاهده می‌کنید. این کد شامل تمام قابلیت‌های ثبت فیش بانکی و ارسال اطلاعات به مدیر است:

```python
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
```

---

#### مرحله ۴: امنیت و بهینه‌سازی

1. توکن ربات و شناسه مدیر را در متغیرهای محیطی ذخیره کنید:
   ```bash
   export BOT_TOKEN='توکن ربات'
   export ADMIN_CHAT_ID='شناسه مدیر'
   ```

2. از HTTPS یا روش‌های رمزگذاری‌شده برای امنیت ارتباط استفاده کنید.

3. در نسخه تولیدی، اطلاعات کاربران و فیش‌ها را در یک دیتابیس مانند MySQL یا SQLite ذخیره کنید.

---

#### مرحله ۵: اجرای ربات

1. فایل کد (`bot.py`) را ذخیره کنید.
2. اسکریپت را اجرا کنید:
   ```bash
   python3 bot.py
   ```

3. ربات اکنون آماده استفاده است.

---

#### ویژگی‌های قابل توسعه

1. **تأیید یا رد فیش توسط مدیر:** اضافه کردن دکمه‌هایی برای تأیید یا رد فیش‌ها.
2. **ذخیره‌سازی پیشرفته:** ذخیره اطلاعات در دیتابیس به جای حافظه موقت.
3. **پشتیبانی چندزبانه:** افزودن زبان‌های دیگر برای کاربران مختلف.
4. **نمایش گزارش:** قابلیت مشاهده لیست فیش‌ها و وضعیت آن‌ها.

اسپانسر ما سایت ایران سون می باشد و میتوانید برای خرید سرور مجازی از این سایت اقدام کنید : https://iran7.net
همچنین در صورت نیاز به طراحی ربات تلگرامی میتوانید با ما به شماره 09306143517 تماس بگیرید.
