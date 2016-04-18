import socket
def fetch(url):
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
