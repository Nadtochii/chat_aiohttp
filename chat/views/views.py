import aiohttp_jinja2

from chat import db


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@aiohttp_jinja2.template('chat.html')
async def chats_list(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.chat.select())
        records = await cursor.fetchall()
        chats = [dict(chat) for chat in records]
        return {'chats': chats}
