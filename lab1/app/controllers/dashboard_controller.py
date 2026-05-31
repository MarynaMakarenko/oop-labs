import logging

from app.controllers.base_controller import BaseController
from app.core.server import RequestContext, Response
from app.dao.booking_dao import BookingDAO
from app.dao.invoice_dao import InvoiceDAO
from app.dao.room_dao import RoomDAO

logger = logging.getLogger(__name__)
_booking_dao = BookingDAO()
_room_dao = RoomDAO()
_invoice_dao = InvoiceDAO()


class DashboardController(BaseController):

    @classmethod
    def dashboard(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_auth(ctx, resp):
            return
        if ctx.role == 'admin':
            pending = _booking_dao.find_pending()
            total_rooms = len(_room_dao.find_all())
            cls.render(resp, 'dashboard.html', ctx,
                       pending_bookings=pending, total_rooms=total_rooms)
        else:
            bookings = _booking_dao.find_by_client(ctx.user_id)
            invoices = _invoice_dao.find_by_client(ctx.user_id)
            cls.render(resp, 'dashboard.html', ctx,
                       bookings=bookings, invoices=invoices)
