import json
import logging
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

import config
from app.core.router import router
from app.core.session import sessions

logger = logging.getLogger(__name__)


class RequestContext:
    """Wraps a raw BaseHTTPRequestHandler into a convenient request object."""

    def __init__(self, handler: 'FrontController'):
        self.method: str = handler.command
        self.path: str = handler.path
        self.headers = handler.headers
        self.session = sessions.from_request(handler.headers)
        self._handler = handler
        self._body: Optional[bytes] = None

    def get_body(self) -> bytes:
        if self._body is None:
            length = int(self.headers.get('Content-Length', 0))
            self._body = self._handler.rfile.read(length) if length else b''
        return self._body

    def form_data(self) -> dict:
        body = self.get_body().decode('utf-8', errors='replace')
        return dict(urllib.parse.parse_qsl(body))

    def query_params(self) -> dict:
        parsed = urllib.parse.urlparse(self.path)
        return dict(urllib.parse.parse_qsl(parsed.query))

    @property
    def user_id(self) -> Optional[int]:
        return self.session.get('user_id') if self.session else None

    @property
    def role(self) -> Optional[str]:
        return self.session.get('role') if self.session else None

    def is_authenticated(self) -> bool:
        return self.user_id is not None


class Response:
    """Helper for sending HTTP responses."""

    def __init__(self, handler: 'FrontController'):
        self._handler = handler

    def send_html(self, body: str, status: int = 200) -> None:
        self._write(body.encode(), 'text/html; charset=utf-8', status)

    def redirect(self, location: str, status: int = 302) -> None:
        h = self._handler
        h.send_response(status)
        h.send_header('Location', location)
        cookie = getattr(h, '_pending_cookie', None)
        if cookie:
            h.send_header('Set-Cookie', cookie)
        h.end_headers()

    def set_cookie(self, value: str) -> None:
        self._handler._pending_cookie = value

    def _write(self, body: bytes, content_type: str, status: int) -> None:
        h = self._handler
        h.send_response(status)
        h.send_header('Content-Type', content_type)
        h.send_header('Content-Length', str(len(body)))
        cookie = getattr(h, '_pending_cookie', None)
        if cookie:
            h.send_header('Set-Cookie', cookie)
        h.end_headers()
        h.wfile.write(body)


class FrontController(BaseHTTPRequestHandler):
    """
    Single HTTP entry point (Front Controller pattern).

    All GET and POST requests pass through here; the Router
    dispatches each request to the appropriate controller method.
    """

    def _dispatch(self) -> None:
        self._pending_cookie = None
        ctx = RequestContext(self)
        resp = Response(self)

        handler_fn, params = router.dispatch(ctx.method, ctx.path)

        if handler_fn is None:
            if not self._try_static(ctx):
                resp.send_html('<h1>404 — Page Not Found</h1>', 404)
            return

        logger.info("%s %s  user=%s role=%s", ctx.method, ctx.path, ctx.user_id, ctx.role)
        try:
            handler_fn(ctx, resp, **params)
        except Exception as exc:
            logger.exception("Unhandled error in %s: %s", handler_fn.__name__, exc)
            resp.send_html('<h1>500 — Internal Server Error</h1>', 500)

    def _try_static(self, ctx: RequestContext) -> bool:
        path = ctx.path.split('?')[0]
        if not path.startswith('/static/'):
            return False
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', path[1:])
        if not os.path.isfile(file_path):
            return False
        ext = os.path.splitext(file_path)[1]
        mime = {'.css': 'text/css', '.js': 'application/javascript'}.get(
            ext, 'application/octet-stream'
        )
        with open(file_path, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        return True

    def do_GET(self):
        self._dispatch()

    def do_POST(self):
        self._dispatch()

    def log_message(self, fmt, *args):
        pass  # suppress default stderr output; we use our own logger


def run_server() -> None:
    server = HTTPServer((config.SERVER_HOST, config.SERVER_PORT), FrontController)
    logger.info("Server running on http://%s:%s", config.SERVER_HOST, config.SERVER_PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped")
        server.server_close()
