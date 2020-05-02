from aiohttp import web


async def login(request):
    return web.Response(text="Hello, world")
