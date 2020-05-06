from aiohttp import web

from chat.views.views import index, chats_list


def setup_routes(app):
    app.add_routes([web.get('/', index)]),
    app.add_routes([web.get('/chats/', chats_list)])
