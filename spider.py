import socket
def fetch(url):
    sock = socket.socket()
    sock.connect(('xkcd.com', 80))
    request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(url)
    print (request)
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        print(chunk)
        chunk = sock.recv(4096)

    return response

if __name__ == "__main__":
    fetch("http://xkcd.com/1019/")
