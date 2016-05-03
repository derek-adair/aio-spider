from aiohttp import web
import aiohttp
import asyncio

async def handle(request):
    domain = request.match_info.get('domain', "Anonymous")
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        print("fetching from {}".format(domain))
        async with session.get('//{}'.format(domain)) as resp:
            content = await resp.text()
            return web.Response(body=content.encode('utf-8'))

app = web.Application()
app.router.add_route('GET', '/{domain}', handle)

web.run_app(app)
