import socket
from bs4 import BeautifulSoup
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
selector = DefaultSelector()
urls_todo = set(['/'])
seen_urls = set(['/'])

class Fetcher:
    def __init__(self, url):
        self.response = b''
        self.url = url
        self.sock = None
        self.stopped = False

    def parse_links(self):
        soup = BeautifulSoup(self.response, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            links.add(link.get('href'))
        return links

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('xkcd.com', 80))
        except BlockingIOError:
            pass

        print (self.sock)
        # Register next callback.
        selector.register(self.sock.fileno(),
                          EVENT_WRITE,
                          self.connected)

    def connected(self, key, mask):
        print('connected!')
        selector.unregister(key.fd)
        request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(self.url)
        urls_todo.add(self.url)
        self.sock.send(request.encode('ascii'))

        # Register the next callback.
        selector.register(key.fd,
                          EVENT_READ,
                          self.read_response)

    # Method on Fetcher class.
    def read_response(self, key, mask):
        chunk = self.sock.recv(4096)  # 4k chunk size.
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)  # Done reading.
            links = self.parse_links()

            print("~~~~~~~~~~~~~~~~~~~RESPONSE~~~~~~~~~~~~~~~~~~~~~~")
            print(self.response)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # Python set-logic:
            for link in links.difference(seen_urls):
                urls_todo.add(link)
                Fetcher(link).fetch()  # <- New Fetcher.

            seen_urls.update(links)
            urls_todo.remove(self.url)
            if not urls_todo:
                self.stopped = True

    def loop(self):
        while not self.stopped:
            events = selector.select()
            for event_key, event_mask in events:
                callback = event_key.data
                callback(event_key, event_mask)
