from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from webbrowser import open_new
import keyring


class HTTPServerHandler(BaseHTTPRequestHandler):

    def __init__(self, request, address, server):
        super().__init__(request, address, server)

    def do_GET(self):
        if self.path.startswith('/auth?access_token='):
            self.server.access_token = parse_qs(self.path[6:])["access_token"][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(
                "<html><head></head><h1>You may now close this window."
                + "</h1></html>", "utf-8"))
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("<html><head><script>window.location.href = '/auth?access_token=' + window.location.href.split('#')[1].split('&').filter(function(c) { return c.startsWith('access_token=')})[0].substring(13);</script></head><h1>You may now close this window."
                               + "</h1></html>", "utf-8"))
        return


class Token:

    def __init__(self, a_id, a_uri, a_base):
        self._id = a_id
        self._uri = a_uri
        self._base = a_base

    def open_browser(self):
        httpServer = HTTPServer(('localhost', 8080),
                                lambda req, address, server: HTTPServerHandler(req, address, server))

        open_new(self._base + '?client_id=' + self._id + '&redirect_uri=' + self._uri + '&response_type=token')

        httpServer.handle_request()
        httpServer.handle_request()

        return httpServer.access_token

    def chunks(self, s, n):
        for index, start in enumerate(range(0, len(s), n)):
            yield (index, s[start:start + n])

    def store_token(self, token):
        last_index = 0
        for chunk in self.chunks(token, 256):
            keyring.set_password("realnet", "access_token_{0}".format(chunk[0]), chunk[1])
            last_index = chunk[0]
        keyring.set_password("realnet", "access_token_count", last_index)

    def retrieve_token(self):
        count = keyring.get_password("realnet", "access_token_count")
        access_token = ''
        for index in range(0, int(count) + 1):
            access_token += keyring.get_password("realnet", "access_token_{0}".format(index))
        return access_token