from pyrogram.errors import MessageEmpty, UserBlocked, UserIsBlocked
from files.config import app
from pyrogram import filters
from files.data import *
from files.keyboard import *
from files.text import *
from media.instagram import get_media
import requests, re
from media.music_search import get_music, get_mp3
from media.shazam import get_url
from media.tiktok import download_tiktok_video

@app.on_message(filters.command("start"))
async def start(client, message):
    get = await get_user_by_name(message.from_user.id)
    if get:
        if get[3] == "uz":
            await message.reply_text(text_uz["start"], reply_markup=button_uz["change"])
        else:
            await message.reply_text(text_kz["start"], reply_markup=button_kz["change"])
    else:
        await message.reply_text("<b>🇰🇿Тілді таңдаңыз.\n🇺🇿Tilni tanlang.</b>", reply_markup=lang_btn)

user_state = {}

@app.on_callback_query()
async def inline_query(client, callback_query):
    global button, language
    cl=callback_query
    callback = callback_query.data
    user_id = callback_query.from_user.id
    name = callback_query.from_user.first_name
    get = await get_user_by_name(user_id)
    if get:
        button = button_uz if get[3]=="uz" else button_kz
        language = text_uz if get[3]=="uz" else text_kz
    if callback == "change_lang":
        await app.edit_message_text(user_id, cl.message.id, "<b>🇰🇿Тілді таңдаңыз.\n🇺🇿Tini tanlang.</b>", reply_markup=lang_btn)
    elif callback == "uz":
        if get:
            await change_lang(callback, user_id)
        else:
            await sql(user_id, name, callback)
        await app.edit_message_text(user_id, cl.message.id, text_uz["start"], reply_markup=button_uz["change"])
    elif callback=="download_music":
        await app.edit_message_reply_markup(user_id, cl.message.id, reply_markup=None)
        await get_url(callback_query.message.video.file_id, user_id, get[3])
    elif callback == "kz":
        if get:
            await change_lang(callback, user_id)
        else:
            await sql(user_id, name, callback)
        await app.edit_message_text(user_id, cl.message.id, text_kz["start"], reply_markup=button_kz['change'])
    elif callback == "send_message":
        await app.edit_message_text(user_id, cl.message.id, language["input_message"], reply_markup=button["cancel"])
        user_state[user_id] = "waiting_for_broadcast"
    elif callback == "cancel":
        await callback_query.message.edit_text(language["admin"], reply_markup=button['send_message'])
        user_state.pop(user_id, None)
    elif callback == "send_data":
        await app.send_document(callback_query.message.chat.id, "files/data.db", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌", callback_data="x")]]))
    elif callback == "x":
        await app.delete_messages(chat_id=user_id, message_ids=callback_query.message.id)
    elif callback[0] and callback[-2] == "|":
        result_music = await get_music(callback[1:-2], user_id, language)
        await app.edit_message_text(user_id, cl.message.id, result_music[0][int(callback[-1]) - 1], reply_markup=result_music[1][int(callback[-1]) - 1])
    elif callback[0] == "(" and callback[-2]== ")":
        await callback_query.answer(language["wait"])
        if len(callback_query.message.text.split('\n'))>7:
            if callback[-1]=="9":
                await get_mp3(callback[1:-2], callback_query.message.text.split('\n')[int(callback[-1])][3:-5], user_id)
            else:
                await get_mp3(callback[1:-2], callback_query.message.text.split('\n')[int(callback[-1])][2:-5], user_id)
        else:
            await get_mp3(callback[1:-2], callback_query.message.text.split('\n')[int(callback[-1])+2][2:-5], user_id)
    elif callback=="done":
        data = user_data.get(user_id, {})
          # Bu yerda bot foydalanuvchilarining ID ro'yxatini olish kerak
        for user in id_users:
            try:
                await client.send_message(user, data['message'], reply_markup=data.get('buttons'))
            except Exception as e:
                print(f"Foydalanuvchiga xabar yuborishda xatolik: {user} - {e}")
        await callback_query.message.reply_text("Xabar muvaffaqiyatli yuborildi.")
        user_state.pop(user_id, None)
        user_data.pop(user_id, None)
    elif callback=="add_button":
        data = user_data.get(user_id, {})
        await callback_query.message.reply_text("Inline tugmalar uchun matnni quyidagi shaklda yuboring:\n\nNomi | URL, Nomi2 | URL2\nNomi3 | URL3")

@app.on_message(filters.user(admin) & filters.command("stat"))
async def admin(client, message):
    get = await get_user_by_name(message.from_user.id)
    if get:
        btn = button_uz if get[3] == "uz" else button_kz
        lang = text_uz if get[3] == "uz" else text_kz
        global delete_msg_id
        delete_msg_id = await message.reply_text(lang["admin"], reply_markup=btn["send_message"])

@app.on_message(filters.regex(r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/([a-zA-Z0-9_.]+)\/?"))
async def instagram_video_downloader(client, message):
    get = await get_user_by_name(message.from_user.id)
    txt_lang = text_uz if get[3] == "uz" else text_kz

    if await get_user_by_name(message.from_user.id):
        if not message.from_user.id in user_state:
            message_id = await app.send_message(chat_id=message.from_user.id, text=txt_lang["downloading"])
            await get_media(requests.get(message.text, allow_redirects=True).url, message.from_user.id, get[3], message_id.id)
    else:
        await app.send_message(message.chat.id, "/start")

@app.on_message(filters.regex(r"https?:\/\/(?:www\.)?tiktok\.com\/(?:@[\w.-]+\/video\/\d+|\w+\?[\w=&]+)") | filters.regex(r"https?:\/\/(?:vt|www)?\.?tiktok\.com\/[^\s]+"))
async def tiktok(client, message):
    get = await get_user_by_name(message.from_user.id)
    txt_lang = text_uz if get[3] == "uz" else text_kz
    if await get_user_by_name(message.from_user.id):
        if not message.from_user.id in user_state:
            message_id = await app.send_message(chat_id=message.from_user.id, text=txt_lang["downloading"])
            await download_tiktok_video(message.text, message.from_user.id, get[3],
                            message_id.id)
    else:
        await app.send_message(message.chat.id, "/start")

@app.on_message(filters.video | filters.audio | filters.voice | filters.text | filters.photo | filters.document)
async def media(client, message):
    get = await get_user_by_name(message.from_user.id)
    if get:
        btn = button_uz if get[3] == "uz" else button_kz
        lang = text_uz if get[3] == "uz" else text_kz
        if message.from_user.id in user_state:
            id_users = await users_id()
            i = 0
            none_button=0
            cpt=None
            msg_btn = None
            if message.caption:
                msg_btn = await create_inline_buttons(message.caption.split("/btn")[1]) if len(message.caption.split("/btn"))>1 else None
                cpt = message.caption.split("/btn")[0] if len(message.caption.split("/btn")) > 1 else message.caption
            if message.text:
                for user in id_users:
                    try:
                        await app.send_message(user, text=message.text.split("/btn")[0] if len(message.text.split("/btn"))>1 else message.text,  reply_markup=await create_inline_buttons(message.text.split("/btn")[1]) if len(message.text.split("/btn"))>1 else None)
                    except ValueError:
                        none_button+=1
                    except UserIsBlocked:
                        i+=1
                    except Exception as e:
                        print(e)
                if none_button>0:
                    await app.send_message(message.chat.id, lang["btn_error"])
                else:
                    await app.send_message(message.from_user.id, lang["suc"].format(len(id_users)-i), reply_markup=btn["resend1"])
                    none_button = 0
                    user_state.pop(message.from_user.id, None)
            elif message.photo:
                for user in id_users:
                    try:
                        await app.send_photo(user, caption=cpt, photo=message.photo.file_id, reply_markup=msg_btn)
                    except ValueError:
                        none_button+=1
                    except UserIsBlocked:
                        i+=1
                    except Exception as e:
                        print(e)
                if none_button>0:
                    await app.send_message(message.chat.id, lang["btn_error"])
                else:
                    await app.send_message(message.from_user.id, lang["suc"].format(len(id_users)-i), reply_markup=btn["resend1"])
                    none_button = 0
                    user_state.pop(message.from_user.id, None)
            elif message.video:
                for user in id_users:
                    try:
                        await app.send_video(user, caption=cpt, video=message.video.file_id, reply_markup=msg_btn)
                    except ValueError:
                        none_button+=1
                    except UserIsBlocked:
                        i+=1
                    except Exception as e:
                        print(e)
                if none_button>0:
                    await app.send_message(message.chat.id, lang["btn_error"])
                else:
                    await app.send_message(message.from_user.id, lang["suc"].format(len(id_users)-i), reply_markup=btn["resend1"])
                    none_button = 0
                    user_state.pop(message.from_user.id, None)
            elif message.audio:
                for user in id_users:
                    try:
                        await app.send_audio(user, cpt, reply_markup=msg_btn)
                    except ValueError:
                        none_button+=1
                    except UserIsBlocked:
                        i+=1
                    except Exception as e:
                        print(e)
                if none_button>0:
                    await app.send_message(message.chat.id, lang["btn_error"])
                else:
                    await app.send_message(message.from_user.id, lang["suc"].format(len(id_users)-i), reply_markup=btn["resend1"])
                    none_button = 0
                    user_state.pop(message.from_user.id, None)
            elif message.document:
                for user in id_users:
                    try:
                        await app.send_document(user, cpt, reply_markup=msg_btn)
                    except ValueError:
                        none_button+=1
                    except UserIsBlocked:
                        i+=1
                    except Exception as e:
                        print(e)
                if none_button>0:
                    await app.send_message(message.chat.id, lang["btn_error"])
                else:
                    await app.send_message(message.from_user.id, lang["suc"].format(len(id_users)-i), reply_markup=btn["resend1"])
                    none_button = 0
                    user_state.pop(message.from_user.id, None)
            elif message.voice:
                for user in id_users:
                    try:
                        await app.send_voice(user, cpt, reply_markup=msg_btn)
                    except ValueError:
                        none_button+=1
                    except UserIsBlocked:
                        i+=1
                    except Exception as e:
                        print(e)
                if none_button>0:
                    await app.send_message(message.chat.id, lang["btn_error"])
                else:
                    await app.send_message(message.from_user.id, lang["suc"].format(len(id_users)-i), reply_markup=btn["resend1"])
                    none_button = 0
                    user_state.pop(message.from_user.id, None)

        else:
            if message.text:
                music = await get_music(message.text, message.from_user.id, get[3])
                await app.send_message(message.chat.id, music[0][0], reply_markup=music[1][0])
            elif message.video:
                await get_url(message.video.file_id, message.from_user.id, get[3])
            elif message.audio:
                await get_url(message.audio.file_id, message.from_user.id, get[3])
            elif message.voice:
                await get_url(message.video.file_id, message.from_user.id, get[3])
    else:
        await app.send_message(message.chat.id, "/start")

app.run()
