from aiohttp import web
import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def handle(request):
    domain = '//{}'.format(request.GET['domain'])
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        print("fetching from {}".format(domain))
        async with session.get(domain) as resp:
            content = await resp.text()

            return web.Response(body=content.encode('utf-8'))

app = web.Application()
app.router.add_route('GET', '/', handle)

web.run_app(app, port=80)
