import logging
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.server import RequestContext, Response

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
_env = Environment(
    loader=FileSystemLoader(_TEMPLATE_DIR),
    autoescape=select_autoescape(['html']),
)


class BaseController:
    """
    Base class for all MVC controllers.

    Provides render(), authentication guards, and shared Jinja2 environment.
    Sub-classes inherit these helpers through standard Python class inheritance.
    """

    @staticmethod
    def render(resp: Response, template: str, ctx: RequestContext, **kwargs) -> None:
        session = ctx.session
        context = {
            'user_id': session.get('user_id') if session else None,
            'username': session.get('username') if session else None,
            'role': session.get('role') if session else None,
            **kwargs,
        }
        html = _env.get_template(template).render(**context)
        resp.send_html(html)

    @staticmethod
    def require_auth(ctx: RequestContext, resp: Response) -> bool:
        if not ctx.is_authenticated():
            resp.redirect('/login')
            return False
        return True

    @staticmethod
    def require_admin(ctx: RequestContext, resp: Response) -> bool:
        if not ctx.is_authenticated():
            resp.redirect('/login')
            return False
        if ctx.role != 'admin':
            resp.send_html('<h1>403 — Forbidden</h1>', 403)
            return False
        return True

    @staticmethod
    def require_client(ctx: RequestContext, resp: Response) -> bool:
        if not ctx.is_authenticated():
            resp.redirect('/login')
            return False
        if ctx.role != 'client':
            resp.send_html('<h1>403 — Forbidden</h1>', 403)
            return False
        return True
