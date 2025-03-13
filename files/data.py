import sqlite3

conn = sqlite3.connect("files/data.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_id INTEGER,
    users_name TEXT NOT NULL,
    users_lang TEXT NOT NULL
)
''')
async def sql(users_id, users_name, users_lang):
    """
    Malumotlar bazaiga foydalanuvchini qoshadi
    :param users_id: Foydalanuvchi ID raqmi
    :param users_name: Foydalanuvchi ismi (Telegram nickname)
    :param users_lang: Bot tili
    """
    db=0
    cursor.execute("SELECT users_id FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if (users_id,)==row:
            db+=1
    if db==0:
        cursor.execute("INSERT INTO users (users_id, users_name, users_lang) VALUES (?, ?, ?)",
                   (users_id, f"{users_name}", f"{users_lang}"))

    conn.commit()

def stat_bot():
    """
    Foydalanuvchi id raqamlarini olish
    :return: ID raqamlarni qaytaradi
    """
    cursor.execute("SELECT id FROM users")
    rows = cursor.fetchall()
    return len(rows)

async def users_id():
    cursor.execute("SELECT users_id FROM users")
    id_users = cursor.fetchall()
    id_list = [int(row[0]) for row in id_users]
    return id_list

async def get_user_by_name(user_id):
    cursor.execute("SELECT * FROM users WHERE users_id = ?", (user_id,))
    user = cursor.fetchone()
    return user

async def change_lang(lang, id):
    sql = "UPDATE users SET users_lang = ? WHERE users_id = ?"
    cursor.execute(sql, (f"{lang}", id))
    conn.commit()
