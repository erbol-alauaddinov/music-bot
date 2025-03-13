from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from files.text import *

def create_button(information):
    btn = []
    for info in information:
        btn.append([
            InlineKeyboardButton(i[0], url=i[1]) for i in info
        ])
    return InlineKeyboardMarkup(btn)

async def create_inline_buttons(text):
    buttons = []
    lines = text.strip().split("\n")
    for line in lines:
        row_buttons = []
        items = line.split(',')
        for item in items:
            label, url = item.split('|')
            row_buttons.append(InlineKeyboardButton(text=label.strip(), url=url.strip()))
        buttons.append(row_buttons)
    return InlineKeyboardMarkup(buttons)

# print(create_button([
#     [["Erbol", "https://erbol.com"], ["eofaf", "https://telegram.org"]], [["Erbol", "https://erbol.com"]]
# ]))

button_uz = {
    "change": InlineKeyboardMarkup([[InlineKeyboardButton("🇺🇿Tilni o'zgartirish", callback_data="change_lang")]]),
    "send_message": InlineKeyboardMarkup([
        [InlineKeyboardButton("🔜Xabar yuborish", callback_data="send_message")],
        [InlineKeyboardButton("💾Data", callback_data="send_data")]
    ]),
    "resend1": InlineKeyboardMarkup([
        [InlineKeyboardButton("🆕Yangi xabar yuborish", callback_data="send_message")],
        [InlineKeyboardButton("🔙Ortga", callback_data="cancel")]
    ]),
    "cancel": InlineKeyboardMarkup([[InlineKeyboardButton("❌Bekor qilish", callback_data="cancel")]]),
    "download_music": InlineKeyboardMarkup([[InlineKeyboardButton("📥Qo'shiqni yuklab olish", callback_data="download_music")]]),
    "add_button": InlineKeyboardMarkup([
        [InlineKeyboardButton("➕Tugma qo'shish", callback_data="add_button")],
        [InlineKeyboardButton("🔜Xabarni yuborish", callback_data="done")],
        [InlineKeyboardButton("❌Bekor qilish", callback_data="cancel")]
    ]),
}
button_kz = {
    "change": InlineKeyboardMarkup([[InlineKeyboardButton("🇰🇿Тілді өзгерту", callback_data="change_lang")]]),
    "send_message": InlineKeyboardMarkup([
        [InlineKeyboardButton("🔜Хабар жіберу", callback_data="send_message")],
        [InlineKeyboardButton("💾Data", callback_data="send_data")]
    ]),
    "resend1": InlineKeyboardMarkup([
        [InlineKeyboardButton("🆕Жаңа хабар жіберу", callback_data="send_message")],
        [InlineKeyboardButton("Malumotlar bazasi", callback_data="send_data")],
        [InlineKeyboardButton("🔙Артқа", callback_data="cancel")]
    ]),
    "cancel": InlineKeyboardMarkup([[InlineKeyboardButton("❌Болдырмау", callback_data="cancel")]]),
    "download_music": InlineKeyboardMarkup([[InlineKeyboardButton("📥Әнді жүктеп алу", callback_data="download_music")]]),
    "add_button": InlineKeyboardMarkup([
        [InlineKeyboardButton("➕Батырма қосу", callback_data="add_button")],
        [InlineKeyboardButton("🔜Хабарды жіберу", callback_data="done")],
        [InlineKeyboardButton("❌Болдырмау", callback_data="cancel")],
    ]),
}
async def admin_msg_btn(text, url):
    btn=[]
    if text:
        for i in range(len(text)):
            btn.append([InlineKeyboardButton(text[i], url=url[i])])
        return InlineKeyboardMarkup(btn)
    else:
        return None
lang_btn = InlineKeyboardMarkup([
    [InlineKeyboardButton("🇰🇿KZ", callback_data="kz"), InlineKeyboardButton("🇺🇿UZ", callback_data="uz")]
])
