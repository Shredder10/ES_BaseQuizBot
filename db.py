import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, answer0 INTEGER, answer1 INTEGER, answer2 INTEGER, answer3 INTEGER, answer4 INTEGER, answer5 INTEGER, answer6 INTEGER, answer7 INTEGER, answer8 INTEGER, answer9 INTEGER)''')
        await db.commit()

async def get_quiz_index(user_id):
     async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def write_quiz_results(user_id, res):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, answer0, answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9]))
        await db.commit()

async def get_quiz_result(user_id):
     async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0