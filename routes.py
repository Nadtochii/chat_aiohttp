from aiohttp import web

from chat.views import views


def setup_routes(app):
    app.add_routes([
        web.get('/', views.index),
        web.get('/chats/', views.chats_list),
        web.get('/ws/chats/', views.ws_handler_chats)
    ])
