import aiosqlite
import datetime

async def add_to_database(telegram_id: int, username: str):
    async with aiosqlite.connect('telegram.db') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (telegram_id BIGINT, username TEXT, date TEXT)")
        cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        data = await cursor.fetchone()
        if data is not None:
            return
        date = f'{datetime.date.today()}'
        await db.execute(
            "INSERT INTO users (telegram_id, username, date) VALUES (?, ?, ?)",
            (telegram_id, username, date)
        )
        await db.commit()
