import os

async def delete(media_list):
    """
    Bu funksiya yuklab olingan media faylni ochirib yuboradi
    :param media_list: royxat korinishida ochirilib yuboriladigan media fayl manzili berilishi kerak
    """
    for media in media_list:
        try:
            os.remove(media)
            print(f"Deleted: {media}")
        except Exception as  e:
            None