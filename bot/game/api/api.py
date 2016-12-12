import http.server
import json
import socketserver
import ssl

from tools import config

LISTEN_ADDRESS = ("", 4343)

API_PATH = "/cgbapi/"
RESPONSE_ENCODING = "utf-8"

ALLOWED_ORIGINS = ("https://rawgit.com", "https://cdn.rawgit.com")


class ApiServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    def server_bind(self):
        super().server_bind()
        self.socket = ssl.wrap_socket(self.socket, keyfile=config.Key.SSL_API_KEY.path, certfile=config.Key.SSL_API_CERT.path, server_side=True)


class ApiRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
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

    def _encode_response(self, response):
        return json.dumps(response).encode(RESPONSE_ENCODING)

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
        return {"ok": "ok"}


if __name__ == "__main__":
    server = ApiServer(LISTEN_ADDRESS, ApiRequestHandler)
    server.serve_forever()
