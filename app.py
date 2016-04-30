import asyncio
from bs4 import BeautifulSoup
from asyncio import Queue
import aiohttp

class Crawler:
    def __init__(self, root_url, max_redirect):
        self.max_tasks = 10
        self.max_redirect = max_redirect
        self.q = Queue()
        self.seen_urls = set()

        # aiohttp's ClientSession does connection pooling and
        # HTTP keep-alives for us.
        self.session = aiohttp.ClientSession(loop=loop)

        self.q.put_nowait((root_url, self.max_redirect))

    def parse_links(response):
        print ('parsing links')
        print(response)
        soup = BeautifulSoup(response, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            links.add(link.get('href'))
        return links

    @asyncio.coroutine
    def crawl(self):
        """Run the crawler until all work is done."""
        workers = [asyncio.Task(self.work()) for _ in range(self.max_tasks)]

        # When all work is done, exit.
        yield from self.q.join()
        print ('joined')
        for w in workers:
            print ('cancelling worker')
            w.cancel()

    @asyncio.coroutine
    def work(self):
        print("doing work")
        while True:
            url, max_redirect = yield from self.q.get()

            # Download page and add new links to self.q.
            yield from self.fetch(url, max_redirect)
            self.q.task_done()

    @asyncio.coroutine
    def fetch(self, url, max_redirect):
        # Handle redirects ourselves.
        print('fetch called')
        response = yield from self.session.get(url, allow_redirects=False)

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print( response )
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print (response.read())
        if response.status_code is 302:
            print("it is a redirect")
            if max_redirect > 0:
                next_url = response.headers['location']
                if next_url in self.seen_urls:
                    # We have been down this path before.
                    return

                # Remember we have seen this URL.
                self.seen_urls.add(next_url)

                # Follow the redirect. One less redirect remains.
                self.q.put_nowait((next_url, max_redirect - 1))
        else:
            print("calling parse links")
            links = self.parse_links(response)
            # Python set-logic:
            for link in links.difference(self.seen_urls):
                self.q.put_nowait((link, self.max_redirect))
            self.seen_urls.update(links)


loop = asyncio.get_event_loop()
crawler = Crawler("http://xkcd.com", 10)
loop.run_until_complete(crawler.crawl())
