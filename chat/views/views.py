import json
import uuid

import aiohttp
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


async def ws_handler_chats(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    if request.app['ws'].get('chats'):
        conns = request.app['ws']['chats']
    else:
        conns = []
    conns.append(ws)
    request.app['ws']['chats'] = conns

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                data = json.loads(msg.data)
                name = data['name']

                async with request.app['db'].acquire() as conn:
                    cursor = await conn.execute(db.chat.insert().values({'name': name}))
                    chat = await cursor.fetchone()

                for ws in request.app['ws']['chats']:
                    await ws.send_str(json.dumps({'chat_id': str(chat.id), 'chat_name': name}))

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws
