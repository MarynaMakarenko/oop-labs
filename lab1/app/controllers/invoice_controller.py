import logging

from app.controllers.base_controller import BaseController
from app.core.server import RequestContext, Response
from app.dao.booking_dao import BookingDAO
from app.dao.invoice_dao import InvoiceDAO

logger = logging.getLogger(__name__)
_invoice_dao = InvoiceDAO()
_booking_dao = BookingDAO()


class InvoiceController(BaseController):

    @classmethod
    def list_invoices(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_auth(ctx, resp):
            return
        if ctx.role == 'admin':
            invoices = _invoice_dao.find_all()
        else:
            invoices = _invoice_dao.find_by_client(ctx.user_id)
        bookings = {b.id: b for b in _booking_dao.find_all()}
        cls.render(resp, 'invoices/list.html', ctx,
                   invoices=invoices, bookings=bookings)

    @classmethod
    def pay_invoice(cls, ctx: RequestContext, resp: Response,
                    invoice_id: str, **_) -> None:
        if not cls.require_client(ctx, resp):
            return
        invoice = _invoice_dao.find_by_id(int(invoice_id))
        if not invoice:
            resp.send_html('<h1>404 — Not Found</h1>', 404)
            return
        booking = _booking_dao.find_by_id(invoice.booking_id)
        if booking.client_id != ctx.user_id:
            resp.send_html('<h1>403 — Forbidden</h1>', 403)
            return
        _invoice_dao.mark_paid(invoice.id)
        resp.redirect('/invoices')
