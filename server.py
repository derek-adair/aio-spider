from aiohttp import web
import aiohttp
import asyncio
from bs4 import BeautifulSoup

def swap_styles(html, domain):
    soup = BeautifulSoup(html, 'html.parser')
    style_hrefs = set()
    for link in soup.find_all('link'):
        print("must fetch resource crom {}".format(domain + link['href']))
        #code = fetch_resouce(domain + a['href'])

async def handle(request):
    domain = '//{}'.format(request.GET['domain'])
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        print("fetching from {}".format(domain))
        async with session.get(domain) as resp:
            content = await resp.text()
            swap_styles(content, domain)

            return web.Response(body=content.encode('utf-8'))

app = web.Application()
app.router.add_route('GET', '/', handle)

web.run_app(app)
