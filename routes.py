from aiohttp import web

from chat.views.views import index


def setup_routes(app):
    app.add_routes([web.get('/', index)])
