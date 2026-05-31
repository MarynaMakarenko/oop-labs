import logging

from app.controllers.base_controller import BaseController
from app.core.server import RequestContext, Response
from app.core.session import sessions
from app.dao.user_dao import UserDAO

logger = logging.getLogger(__name__)
_user_dao = UserDAO()


class AuthController(BaseController):
    """Handles login / logout flows."""

    @classmethod
    def login_page(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if ctx.is_authenticated():
            resp.redirect('/dashboard')
            return
        cls.render(resp, 'login.html', ctx, error=None)

    @classmethod
    def login(cls, ctx: RequestContext, resp: Response, **_) -> None:
        data = ctx.form_data()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        user = _user_dao.authenticate(username, password)
        if user is None:
            cls.render(resp, 'login.html', ctx, error='Invalid username or password')
            return

        session = sessions.create()
        session.set('user_id', user.id)
        session.set('username', user.username)
        session.set('role', user.role)

        resp.set_cookie(sessions.set_cookie(session.id))
        logger.info("User %s logged in as %s", username, user.role)
        resp.redirect('/dashboard')

    @classmethod
    def logout(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if ctx.session:
            sessions.destroy(ctx.session.id)
        resp.set_cookie(sessions.clear_cookie())
        resp.redirect('/login')
