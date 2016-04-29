import socket
from bs4 import BeautifulSoup
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from Future import Future
from Task import Task
selector = DefaultSelector()
urls_todo = set(['/'])
seen_urls = set(['/'])

class Fetcher:
    def __init__(self, url):
        self.response = b''
        self.url = url
        urls_todo.add(url)
        self.stopped = False

    def parse_links(self):
        soup = BeautifulSoup(self.response, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            links.add(link.get('href'))
        return links

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('xkcd.com', 80))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected(sel, mask):
            f.set_result(None)

        # Register next callback.
        selector.register(sock.fileno(),
                          EVENT_WRITE,
                          on_connected)

        yield f
        print('connected!')
        selector.unregister(sock.fileno())
        request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(self.url)
        sock.send(request.encode('ascii'))

        while True:
            # Register the next callback.

            f2 = Future()
            def on_readable(sel,mask):
                f2.set_result(sock.recv(4096))


            selector.register(sock.fileno(),
                              EVENT_READ,
                              on_readable)
            chunk = yield f2
            selector.unregister(sock.fileno())  # Done reading.
            if chunk:
                self.response += chunk
            else:
                links = self.parse_links()

                print("~~~~~~~~~~~~~~~~~~~RESPONSE~~~~~~~~~~~~~~~~~~~~~~")
                print(self.response)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                # Python set-logic:
                for link in links.difference(seen_urls):
                    urls_todo.add(link)
                    Task(Fetcher(link).fetch())  # <- New Fetcher Task


                seen_urls.update(links)
                try:
                    urls_todo.remove(self.url)
                except KeyError:
                    pass
                if not urls_todo:
                    self.stopped = True
                    break

    def loop(self):
        while not self.stopped:
            events = selector.select()
            for event_key, event_mask in events:
                callback = event_key.data
                callback(event_key, event_mask)
