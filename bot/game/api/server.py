import http.server
import json
import socketserver
import ssl
import threading

from game.api.api import DummyApi
from tools import config

LISTEN_ADDRESS = ("", 4343)

API_PATH = "/cgbapi/"
CONTENT_ENCODING = "utf-8"

ALLOWED_ORIGINS = ("https://rawgit.com", "https://cdn.rawgit.com")


class SslMixIn:
    def server_bind(self):
        super().server_bind()
        self.socket = ssl.wrap_socket(self.socket,
                                      keyfile=config.Key.SSL_API_KEY.path,
                                      certfile=config.Key.SSL_API_CERT.path,
                                      server_side=True)


class ApiServer(SslMixIn, socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

    def start(self, api, background):
        self.api = api
        if background:
            threading.Thread(target=self.serve_forever, daemon=True).start()
        else:
            self.serve_forever()


class ApiRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if not self.path.startswith(API_PATH):
            self.send_error(404)
        else:
            self._handle_api_request()

    def _handle_api_request(self):
        api_call_name = self._get_api_call_from_path()
        if not hasattr(self, api_call_name):
            response_code = 404
            response = self._api_call_not_found()
        else:
            response_code = 200
            api_call = getattr(self, api_call_name)
            response = api_call()
        encoded_response = self._encode_response(response)
        self._send_api_response(response_code, encoded_response)

    def _get_api_call_from_path(self):
        return "api_call_" + self.path[len(API_PATH):]

    @staticmethod
    def _encode_response(response):
        return json.dumps(response).encode(CONTENT_ENCODING)

    def _send_api_response(self, response_code, encoded_response):
        self.send_response(response_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(encoded_response)))
        origin = self.headers["Origin"]
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
        self.end_headers()
        self.wfile.write(encoded_response)

    def _api_call_not_found(self):
        return {"error": "Not found"}

    def api_call_set_score(self):
        self.server.api.set_score(self._read_body())
        return {"ok": "ok"}

    def _read_body(self):
        try:
            length = int(self.headers["Content-Length"])
            return self.rfile.read(length).decode(CONTENT_ENCODING)
        except:
            return ""


def start_api_server(api, background=True):
    server = ApiServer(LISTEN_ADDRESS, ApiRequestHandler)
    server.start(api, background)


if __name__ == "__main__":
    start_api_server(DummyApi(), background=False)
