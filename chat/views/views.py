import uuid

import aiohttp_jinja2
from aiohttp import web

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


async def new_chat(request):
    name = str(uuid.uuid4())
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.chat.insert().values({'name': name}))
        chat = await cursor.fetchone()

    raise web.HTTPFound('/chats/' + str(chat.id) + '/')
