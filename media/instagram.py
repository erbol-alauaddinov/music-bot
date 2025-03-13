from json import JSONDecodeError
from files.delete import delete
import requests, os, re
from pyrogram.errors import MediaEmpty
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from files.config import app, admin
from files.text import text_kz, text_uz
from files.keyboard import *
from datetime import datetime
dt = datetime.now()
API_KEYS = [
    "208dec8f56msh25e7cb119fae2bdp12b479jsn7b421732bee1",#AE
    "118a192fe0msh650cdebda4d7be6p1f3fdajsnbd1653d279ef",#EA
    "1209262864mshc88c1b402e027fdp15f3aajsnfae6f09e4ac5",#WE
]

async def get_media(video_url, user_id, lang, message_id):
    """Uhbu funksiya instagram urli orqali postni yuklab uni userga yuboradi
    Parametrlar; video_url: post urli, user_id: userning telegram id raqami, langauge: user tiloi, 
    """
    button = button_uz if lang == "uz" else button_kz
    lang = text_uz if lang == "uz" else text_kz
    api_url = "https://snapinsta.app/get-data.php"
    querystring = {
        "url": video_url,
        "new": "2",
        "lang": "en",
        "app": ""
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.post(api_url, data=querystring, headers=headers)
    delete_files=[]
    jpg=[]
    jpg1=[]
    print(response.json())
    try:
        if response.status_code==200 and response.json()["files"]:
            url_video = []
            media_name=[]
            save_folder = "media/instagram"
            os.makedirs(save_folder, exist_ok=True)
            name = dt.strftime(f"{user_id}_%Y-%m-%d_%H-%M-%S_")
            search=""
            for i, u in enumerate(response.json()["files"], start=1):

                if u["__type"]=="GraphVideo":
                    delete_files.append(f"{save_folder}/{name}{i}.mp4")
                    url_video.append(u["video_url"])
                    search+=f"{save_folder}/{name}{i}.mp4"
                    media_name.append(InputMediaVideo(f"{save_folder}/{name}{i}.mp4", caption=lang["izoh"]) if i==1 or i==11 else InputMediaVideo(f"{save_folder}/{name}{i}.mp4"))
                    with open(os.path.join(save_folder, f"{name}{i}.mp4"), "wb") as f:
                        f.write(requests.get(u["video_url"]).content)
                else:
                    delete_files.append(f"{save_folder}/{name}{i}.jpg")
                    url_video.append(u["download_url"])
                    media_name.append(InputMediaPhoto(f"{save_folder}/{name}{i}.jpg", caption=lang["izoh"]) if i==1 or i == 11 else InputMediaPhoto(f"{save_folder}/{name}{i}.jpg"))
                    jpg.append(f"{save_folder}/{name}{i}.jpg")
                    with open(os.path.join(save_folder, f"{name}{i}.jpg"), "wb") as f:
                        f.write(requests.get(u["download_url"]).content)
            await app.edit_message_text(user_id, message_id, lang["sending"])
            if len(media_name)==1 and not search=="":
                await app.send_video(user_id, search, lang["izoh"], reply_markup=button["download_music"])
            elif len(media_name)>10:
                await app.send_media_group(user_id, media_name[:10])
                await app.send_media_group(user_id, media_name[10:])

            else:
                await app.send_media_group(user_id, media_name)
            await app.delete_messages(user_id, message_ids=message_id)

        else:
            await app.send_message(chat_id=admin, text=response.json()["message"])
            await app.send_message(chat_id=user_id, text=lang["xato_nomalum"], reply_markup=button["change"])
    except MediaEmpty as e:
        for i, u in enumerate(jpg):
            jpg1.append(InputMediaPhoto(u, f"{lang["izoh"]}\n\n{lang["MediaEmpty"]}") if i==0 or i==10 else InputMediaPhoto(u))
        if len(jpg1)>10:
            await app.send_media_group(user_id, jpg1[:10])
            await app.send_media_group(user_id, jpg1[10:])
        else:
            await app.send_media_group(user_id, jpg1)
        await app.delete_messages(user_id, message_ids=message_id)
    except JSONDecodeError:
        await app.delete_messages(user_id, message_ids=message_id)
        await app.send_message(user_id, lang["X_url_instagram"])
    except Exception as e:
        await app.send_message(admin, f"{response.text}\n{e}")
        await app.delete_messages(user_id, message_ids=message_id)
    await delete(delete_files)