import telebot
from telebot import types
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import json
import os

TOKEN = "6634088197:AAESEnClwkHZM317yOF3KggpJQiw21OmcgM"
bot = telebot.TeleBot(TOKEN)

user_data = {}
allowed_users = set()
running_processes = set()

COMMANDS = {
    '/hsp': 'تعيين الحساب',
    '/sub': 'اضف الموضوع',
    '/text': 'اضف الكليشة',
    '/slp': 'عين السليب',
    '/snd': 'عدد الرسائل',
    '/adl': 'ايميل الدعم',
    '/add': 'عرض المعلومات',
    '/run': 'بدأ الإرسال',
    '/stop': 'إيقاف الرفع',
    '/acadd': 'عرض الحسابات'
}

def load_users():
    if os.path.exists('users2.json'):
        with open('users2.json', 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open('users2.json', 'w') as f:
        json.dump(users, f, indent=4)

def create_button(label, callback_data):
    return types.InlineKeyboardButton(label, callback_data=callback_data)

def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(create_button("بدأ الرفع", "/run"))
    keyboard.row(create_button("اضف الحساب", "/hsp"), create_button("عرض الحسابات", "/acadd"))
    keyboard.row(create_button("اضف الموضوع", "/sub"), create_button("اضف الكليشه", "/text"))
    keyboard.row(create_button("اضف السليب", "/slp"), create_button("اضف عدد الرسائل", "/snd"))
    keyboard.row(create_button("ايميل الدعم", "/adl"), create_button("معلوماتك", "/add"))
    keyboard.row(create_button("إيقاف الرفع", "/stop"))
    keyboard.row(types.InlineKeyboardButton(text="قناه الشرح", url="https://t.me/shdWLT"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
    bot.send_message(chat_id, "اهلا بك في بوت رفع خارجي", reply_markup=create_keyboard())

@bot.message_handler(commands=['id'])
def handle_id(message):
    if message.from_user.id == 1483470852:  # وضع معرف المدير هنا
        bot.send_message(message.chat.id, "حسناً، الآن أرسل المعرف لتفعيله")
        bot.register_next_step_handler(message, get_user_id)

def get_user_id(message):
    user_id = message.text
    user_ids = load_users()
    if user_id not in user_ids:
        user_ids.append(user_id)
        save_users(user_ids)
        bot.send_message(message.chat.id, "تم إضافة المعرف بنجاح")
    else:
        bot.send_message(message.chat.id, "المعرف مضاف من قبل")

@bot.callback_query_handler(func=lambda call: call.data == '/hsp')
def hsp_callback(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "يرجى إرسال الحساب بصيغة (ايميلك:الباسوورد)")
    bot.register_next_step_handler(call.message, save_account_info)

def save_account_info(message):
    chat_id = message.chat.id
    account_info = message.text.split(":")
    if len(account_info) == 2:
        email = account_info[0]
        password = account_info[1]
        user_data[chat_id]['email'] = email
        user_data[chat_id]['password'] = password
        bot.send_message(chat_id, f"تم حفظ الحساب\nايميلك: {email}\nالباسوورد: {password}")
    else:
        bot.send_message(chat_id, "يرجى إدخال البيانات بالشكل الصحيح (ايميلك:الباسوورد)")

@bot.callback_query_handler(func=lambda call: call.data == '/sub')
def sub_callback(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "الموضوع:")
    bot.register_next_step_handler(call.message, save_subject)

def save_subject(message):
    chat_id = message.chat.id
    subject = message.text
    user_data[chat_id]['sub'] = subject
    bot.send_message(chat_id, f"تم تعيين الموضوع: {subject}")

@bot.callback_query_handler(func=lambda call: call.data == '/text')
def text_callback(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "الكليشه:")
    bot.register_next_step_handler(call.message, save_message)

def save_message(message):
    chat_id = message.chat.id
    email_message = message.text
    user_data[chat_id]['text'] = email_message
    bot.send_message(chat_id, "تم تعيين الكليشه.")

@bot.callback_query_handler(func=lambda call: call.data == '/slp')
def slp_callback(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "عين السليب (بالثواني):")
    bot.register_next_step_handler(call.message, save_sleep_time)

def save_sleep_time(message):
    chat_id = message.chat.id
    sleep_time = int(message.text)
    user_data[chat_id]['slp'] = sleep_time
    bot.send_message(chat_id, f"تم تعيين السليب: {sleep_time} ثانية")

@bot.callback_query_handler(func=lambda call: call.data == '/snd')
def snd_callback(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "عدد الرسائل:")
    bot.register_next_step_handler(call.message, save_send_count)

def save_send_count(message):
    chat_id = message.chat.id
    send_count = int(message.text)
    user_data[chat_id]['snd'] = send_count
    bot.send_message(chat_id, f"تم تعيين عدد الرسائل: {send_count}")

@bot.callback_query_handler(func=lambda call: call.data == '/adl')
def adl_callback(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "ايميل الدعم:")
    bot.register_next_step_handler(call.message, save_receiver_email)

def save_receiver_email(message):
    chat_id = message.chat.id
    receiver_email = message.text
    user_data[chat_id]['adl'] = receiver_email
    bot.send_message(chat_id, f"تم تعيين ايميل الدعم: {receiver_email}")

@bot.callback_query_handler(func=lambda call: call.data == '/add')
def add_callback(call):
    add(call.message)

def add(message):
    chat_id = message.chat.id
    email_data = user_data.get(chat_id, {})
    subject = email_data.get('sub', 'ممحد')
    message_text = email_data.get('text', 'ممحد')
    sleep_time = email_data.get('slp', 'ممحد')
    send_count = email_data.get('snd', 'ممحد')
    receiver_email = email_data.get('adl', 'ممحد')

    if all([subject, message_text, sleep_time, send_count, receiver_email]):
        info_message = f"الموضوع: {subject}\nالكليشه: {message_text}\nسليب: {sleep_time}\nعدد الرسائل: {send_count}\nالدعم: {receiver_email}"
        bot.send_message(chat_id, info_message)
    else:
        bot.send_message(chat_id, "بعدك ممعين كلشي")

@bot.callback_query_handler(func=lambda call: call.data == '/run')
def run_callback(call):
    run(call.message)

def run(message):
    chat_id = message.chat.id

    if chat_id not in allowed_users:
        bot.send_message(chat_id, "روح اشترك من والتر وتعال شد @isWLT")
        return

    running_processes.add(chat_id)
    email_data = user_data.get(chat_id, {})
    subject = email_data.get('sub')
    message_text = email_data.get('text')
    sleep_time = email_data.get('slp')
    send_count = email_data.get('snd')
    receiver_email = email_data.get('adl')

    if not all([subject, message_text, sleep_time, send_count, receiver_email]):
        bot.send_message(chat_id, 
         "عين كلشي مطلوب يا زمال")
        return

    bot.send_message(chat_id, "يتم الرفع ...")
    successful_emails = 0
    failed_emails = 0
    progress_message_id = None

    for _ in range(send_count):
        if chat_id in running_processes:
            if send_email(email_data['email'], email_data['password'], receiver_email, subject, message_text):
                successful_emails += 1
            else:
                failed_emails += 1
            progress_message_id = send_upload_progress(chat_id, progress_message_id, successful_emails, failed_emails, send_count)
            time.sleep(sleep_time)
        else:
            break

    running_processes.discard(chat_id)

    if chat_id in running_processes:
        bot.send_message(chat_id, f"تم اكتمال الرفع\nتم رفع: {successful_emails}\nعدد الرسائل الخطا: {failed_emails}")
    else:
        bot.send_message(chat_id, "تم إيقاف الرفع")

@bot.callback_query_handler(func=lambda call: call.data == '/stop')
def stop_callback(call):
    stop_upload(call.message)

def stop_upload(message):
    chat_id = message.chat.id
    if chat_id in running_processes:
        running_processes.remove(chat_id)
        bot.send_message(chat_id, "تم إيقاف الرفع")
    else:
        bot.send_message(chat_id, "ماجاي ترفع شي هسه")

@bot.callback_query_handler(func=lambda call: call.data == '/acadd')
def acadd_callback(call):
    view_added_accounts(call)

def view_added_accounts(call):
    chat_id = call.message.chat.id
    email_data = user_data.get(chat_id, {})
    if email_data:
        keyboard = types.InlineKeyboardMarkup()
        for key in email_data:
            if key.startswith('email_'):
                email = email_data[key]
                keyboard.row(create_button(email, f"set_account_{email}"))
        bot.send_message(chat_id, "الحسابات المضافة:", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "ماكو حسابات مضافة")

def send_upload_progress(chat_id, message_id, successful_emails, failed_emails, send_count):
    progress_message = f"يتم الرفع بحقوق WLT\nتم الرفع: {successful_emails}/{send_count}\nعدد الرسائل الفاشلة: {failed_emails}"
    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=progress_message)
    else:
        sent_message = bot.send_message(chat_id, text=progress_message)
        message_id = sent_message.message_id
    return message_id

def send_email(sender_email, sender_password, receiver_email, subject, message_text):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_text, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("خطأ في الرفع:", str(e))
        return False

bot.infinity_polling