import requests, os, yt_dlp
from files.config import API_TOKEN, app, admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from files.text import text_uz, text_kz
async def get_url(file_id,user_id, lang):
	"""
	Telegramnan kelgan media file idsi orqali yuklab olish havolasini yaratadi
	:param file_id: id raqam,
	:param user_id: foydalanuvchi ID raqami
	:param lang: foydaluvchi tili
	"""
	response = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getFile?file_id={file_id}")
	try:
		if response.status_code == 200:
			file_info = response.json()
			file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info["result"]["file_path"]}"
			print(file_url)
			await shazam(file_url, user_id, lang)
		else:
			await app.send_message(admin, response.text)
	except Exception as e:
		print(e)
		await app.send_message(admin, e)

async def shazam(media_id, user_id, lang):
	"""
	Media fayl urli orqali musiqa qidiradi
	:param media_id: media urli
	:param user_id: foydalanuvchi ID raqami
	:param lang: foydaluvchi tili
	"""
	url = "https://shazam-media-search-api.p.rapidapi.com/"
	querystring = {"url": media_id}
	headers = {
		"x-rapidapi-key": "e4ddf02ccemshb1ef6e6532851a6p1203e2jsn03b41c1597f1",
		"x-rapidapi-host": "shazam-media-search-api.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	lang = text_uz if lang == "uz" else text_kz
	try:
		if response.status_code==200:
			print(response.json())
			response_json=response.json()
			await result(f"{response_json["track"]["subtitle"]} - {response_json["track"]["title"]}", user_id)
		else:
			await app.send_message(admin, response.text)
	except KeyError:
		await app.send_message(user_id, lang["music_none"])
	except Exception as e:
		await app.send_message(admin, e)

async def result(query, user_id):
	"""
	Ushbu funksiya youtubedan musiqa qidiradi
    :param query: qidiriladigan musiqa nomi
    :param user_id: sorov yuboruvchi id raqmi
	"""
	ydl_opts = {
		'quiet': True,
		'extract_flat': True,
		'format': 'bestaudio',
	}
	mp3_name=[]
	text=""
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		result_search = ydl.extract_info(f"ytsearch{5}:{query}", download=False)
		for u in result_search["entries"]:
			try:
				mp3_name.append([u["title"], f"{int(u["duration"] // 60)}:{int(u["duration"] % 60)}", u["id"]]) if int(
					u["duration"]) <= 3600 else None
			except KeyError:
				continue
		for i, u in enumerate(mp3_name[:10], start=1):
			text += f"<b>{i}.</b>{u[0]} <b>{u[1]}</b>\n"
		await app.send_message(user_id, f"<b>🎵 {query}</b>\n\n{text}", reply_markup=InlineKeyboardMarkup([
			[InlineKeyboardButton(f"{i-1}", callback_data=f"({u[2]}){i-2}") for i, u in enumerate(mp3_name, start=2)]
		]))
