import requests, os
from pyrogram.types import InputMediaVideo, InputMediaPhoto
from files.config import app
from files.text import text_uz, text_kz
from files.keyboard import button_uz, button_kz
from datetime import datetime
from files.delete import delete

dt = datetime.now()

async def download_tiktok_video(video_url, user_id, lang, message_id):
    """Uhbu funksiya instagram urli orqali postni yuklab uni userga yuboradi
    Parametrlar; video_url: post urli, user_id: userning telegram id raqami, language: user tiloi,
    """
    button = button_uz if lang == "uz" else button_kz
    lang = text_uz if lang == "uz" else text_kz
    api_url = "https://savetik.net/api/action"
    params = {"url": video_url}
    try:
        response = requests.post(api_url, params=params)
        delete_files=[]
        jpg=[]
        if response.status_code==200 and "postinfo" in response.json():
            url_video = []
            media_name=[]
            save_folder = "media/tiktok"
            os.makedirs(save_folder, exist_ok=True)
            name = dt.strftime(f"{user_id}_%Y-%m-%d_%H-%M-%S_")
            r = response.json()
            print(r)
            if "video_link" in r:
                name = dt.strftime(f"{user_id}_%Y-%m-%d_%H-%M-%S")
                url_video.append(f"https://savetik.net{r["video_link"]}")
                with open(os.path.join(save_folder, f"{name}.mp4"), "wb") as f:
                    f.write(requests.get(f"https://savetik.net{r["video_link"]}").content)
                await app.edit_message_text(user_id, message_id, lang["sending"])
                await app.send_video(user_id, f"{save_folder}/{name}.mp4", caption=lang["izoh"],
                                     reply_markup=button["download_music"])
                await delete([f"{save_folder}/{name}.mp4"])
            elif "items" in r:
                for i, item in enumerate(r["items"]):
                    url_video.append(item)
                    jpg.append(f"{name}{i}.jpg")
                    media_name.append(InputMediaPhoto(f"{save_folder}/{name}{i}.jpg", caption=lang["izoh"]) if i == 1 or i == 11 else InputMediaPhoto(f"{save_folder}/{name}{i}.jpg"))
                    with open(os.path.join(save_folder, f"{name}{i}.jpg"), "wb") as f:
                        f.write(requests.get(item).content)
                await app.edit_message_text(user_id, message_id, lang["sending"])
                if 10 < len(media_name) < 21:
                    await app.send_media_group(user_id, media_name[:10])
                    await app.send_media_group(user_id, media_name[10:])
                elif 20 < len(media_name):
                    await app.send_media_group(user_id, media_name[20:30])
                    await app.send_media_group(user_id, media_name[30:])
                else:
                    await app.send_media_group(user_id, media_name)
                await delete(jpg)

        else:
            await app.send_message(user_id, lang["X_url_instagram"])
        await app.delete_messages(user_id, message_ids=message_id)
    except Exception as e:
        await app.send_message(user_id, )
        await app.send_message(admin, e)
