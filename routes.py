from aiohttp import web

from chat.views.login import login


def setup_routes(app):
    app.add_routes([web.get('/', login)])
