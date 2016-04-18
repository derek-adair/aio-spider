import socket
from selectors import DefaultSelector, EVENT_WRITE
def fetch(url):
    selector = DefaultSelector()
    sock = socket.socket()
    sock.setblocking(True)
    try:
        sock.connect(('xkcd.com', 80))
    except BlockingIOError:
        pass

    request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(url)
    encoded = request.encode('ascii')

    while True:
        try:
            sock.send(encoded)
            break  # Done.
        except OSError as e:
            pass

    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)

    return response

def connected():
    selector.unregister(sock.fileno())
    print('connected!')

selector.register(sock.fileno(), EVENT_WRITE, connected)

def loop():
    while True:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()

loop()
