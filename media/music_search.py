import requests, os, re, yt_dlp
from pyrogram.errors import MessageEmpty
from files.config import app, bot, admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from files.delete import delete
from files.text import text_uz, text_kz

msg_id=None

async def get_music(query, user_id, language):
    '''
    Ushbu funksiya youtubedan musiqa qidiradi
    :param query: qidiriladigan musiqa nomi
    :param user_id: sorov yuboruvchi id raqmi
    :return:
    '''
    text=""
    language = text_uz if language=="uz" else text_kz
    mp3_name=[]
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'format': 'bestaudio',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch{50}:{query}", download=False)
            for u, i in enumerate(result["entries"], start=1):
                try:
                    mp3_name.append([i["title"], f"{int(i["duration"]//60)}:{int(i["duration"]%60)}", i["id"]]) if int(i["duration"])<=3600 else None
                except KeyError:
                    continue
        for i , u in enumerate(mp3_name[:10], start=1):
            text += f"<b>{i}.</b>{u[0]} <b>{u[1]}</b>\n"
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{i + 1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[:5])],
            [InlineKeyboardButton(f"{i + 1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[5:10], start=5)],
            [InlineKeyboardButton("⬅️", callback_data=f"|{query}|5"), InlineKeyboardButton("❌", callback_data="x"),
             InlineKeyboardButton("➡️", callback_data=f"|{query}|2")]
        ])
        text1=""
        btn1=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[10:15])],
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[15:20], start=5)],
            [InlineKeyboardButton("⬅️", callback_data=f"|{query}|1"), InlineKeyboardButton("❌", callback_data="x"),
             InlineKeyboardButton("➡️", callback_data=f"|{query}|3")]
             ])
        for i , u in enumerate(mp3_name[10:20], start=1):
            text1 += f"<b>{i}.</b>{u[0]} <b>{u[1]}</b>\n"
        text2=""
        btn2=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[20:25])],
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[25:30], start=5)],
            [InlineKeyboardButton("⬅️", callback_data=f"|{query}|2"), InlineKeyboardButton("❌", callback_data="x"),
             InlineKeyboardButton("➡️", callback_data=f"|{query}|4")]
             ])
        for i , u in enumerate(mp3_name[20:30], start=1):
            text2 += f"<b>{i}.</b>{u[0]} <b>{u[1]}</b>\n"
        text3=""
        btn3=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[30:35])],
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[35:40], start=5)],
            [InlineKeyboardButton("⬅️", callback_data=f"|{query}|3"), InlineKeyboardButton("❌", callback_data="x"),
             InlineKeyboardButton("➡️", callback_data=f"|{query}|5")]
             ])
        for i , u in enumerate(mp3_name[30:40], start=1):
            text3 += f"<b>{i}.</b>{u[0]} <b>{u[1]}</b>\n"
        text4=""
        btn4=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[40:45])],
            [InlineKeyboardButton(f"{i+1}", callback_data=f"({u[2]}){i}") for i, u in enumerate(mp3_name[45:50], start=5)],
            [InlineKeyboardButton("⬅️", callback_data=f"|{query}|4"), InlineKeyboardButton("❌", callback_data="x"),
             InlineKeyboardButton("➡️", callback_data=f"|{query}|1")]
             ])
        for i , u in enumerate(mp3_name[40:50], start=1):
            text4 += f"<b>{i}.</b>{u[0]} <b>{u[1]}</b>\n"

        texts=[text, text1, text2, text3, text4]
        btns=[btn, btn1, btn2, btn3, btn4]
        return texts, btns, query
    except MessageEmpty:
        await app.send_message(user_id, language["music_none"])
    except Exception as e:
        print(e)
        await app.send_message(admin, e)




async def get_mp3(id, name, userid):
    """
    Ushbu youtube videoning mp3 faylini yuklab foydalanuvchiga yuboradi,
    :param id: videoning id raqami,
    :param name: mp3 fileni saqlash nomi,
    :param userid: mp3 file yuborilishi kerak bolgan foydalanuvchi id raqami,
    """
    save_folder = "media/mp3"
    os.makedirs(save_folder, exist_ok=True)
    API_URL = "https://youtube-api-4lkx.onrender.com/api/youtube/download"
    params = {"videoId": id}

    response = requests.get(API_URL, params=params)
    try:
        print(response.json())
        if response.status_code == 200:
            data = response.json()["data"]["adaptiveFormats"]
            mp3_url = data[len(data) - 1]["url"]
            print(mp3_url+' '+data[len(data) - 1]["audioQuality"])
            name = re.sub(r'[\\/*?:"<>|]', "_", name)
            with open(os.path.join(save_folder, f"{name}.mp3"), "wb") as f:
                print(f"{name} - {mp3_url}")
                f.write(requests.get(mp3_url).content)
            await app.send_audio(chat_id=userid, performer=name, title=f"@{bot}", audio=f"{save_folder}/{name}.mp3")
            await delete([f"{save_folder}/{name}.mp3"])
    except Exception as e:
        print(e)
        await app.send_message(admin, e)

