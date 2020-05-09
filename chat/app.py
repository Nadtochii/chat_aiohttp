import aiohttp_jinja2
import jinja2
from aiohttp import web

from chat.db import init_pg, close_pg
from routes import setup_routes


async def create_app():
    app = web.Application()
    app['ws'] = {}

    app.router.add_static('/static/',
                          path=str('chat/static'),
                          name='static')

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('chat', 'templates')
    )

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    setup_routes(app)
    return app
