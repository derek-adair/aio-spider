import asyncio
import aiohttp

async def print_page(url):
    response = await aiohttp.request('GET', url)
    body = await response.read()
    response.close()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(body)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([
    print_page('http://google.com'),
    print_page('http://derekadair.com')
    ]))
loop.close()
