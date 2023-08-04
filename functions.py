import sqlite3
import random

async def getUser(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    data = cursor.fetchone()
    conn.close()
    return data

async def setUser(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id) VALUES (?)', (id,))
    conn.commit()
    conn.close()

async def editSex(id, sex):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET sex = ? WHERE id = ?', (sex, id))
    conn.commit()
    conn.close()

async def find(id, sex):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wait WHERE user_sex = ? AND user_id != ?', (sex, id))
    data = cursor.fetchall()
    resp = ''
    if data != []:
        user = random.choice(data)[1]
        resp = user
        cursor.execute('UPDATE users SET sobes = ? WHERE id = ?', (user, id))
        cursor.execute('UPDATE users SET sobes = ? WHERE id = ?', (id, user))
        cursor.execute('DELETE FROM wait WHERE user_id = ?', (user,))
    else:
        user = await getUser(id)
        cursor.execute('INSERT INTO wait (user_id, user_sex) VALUES (?, ?)', (id, user[1]))
    conn.commit()
    conn.close()
    return resp

async def setMsg(id, msg):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET msg = ? WHERE id = ?', (msg, id))
    conn.commit()
    conn.close()

async def stopDialog(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET sobes = ? WHERE id = ?', ("Нету", id))
    user = await getUser(id)
    cursor.execute('UPDATE users SET sobes = ? WHERE id = ?', ("Нету", user[2]))
    conn.commit()
    conn.close()
    return user[2]

async def stopFind(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM wait WHERE user_id = ?', (id,))
    conn.commit()
    conn.close()























