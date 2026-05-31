import logging
from datetime import date

from app.controllers.base_controller import BaseController
from app.core.server import RequestContext, Response
from app.dao.booking_dao import BookingDAO
from app.dao.invoice_dao import InvoiceDAO
from app.dao.room_dao import RoomDAO
from app.dao.user_dao import UserDAO
from app.models.room import APARTMENT_CLASSES

logger = logging.getLogger(__name__)
_booking_dao = BookingDAO()
_room_dao = RoomDAO()
_invoice_dao = InvoiceDAO()
_user_dao = UserDAO()


class BookingController(BaseController):

    @classmethod
    def list_bookings(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_auth(ctx, resp):
            return
        if ctx.role == 'admin':
            bookings = _booking_dao.find_all()
            client_ids = {b.client_id for b in bookings}
            users = {uid: _user_dao.find_by_id(uid) for uid in client_ids}
            rooms = {r.id: r for r in _room_dao.find_all()}
            cls.render(resp, 'bookings/admin_list.html', ctx,
                       bookings=bookings, users=users, rooms=rooms)
        else:
            bookings = _booking_dao.find_by_client(ctx.user_id)
            rooms = {r.id: r for r in _room_dao.find_all()}
            cls.render(resp, 'bookings/client_list.html', ctx,
                       bookings=bookings, rooms=rooms)

    @classmethod
    def create_booking_page(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_client(ctx, resp):
            return
        cls.render(resp, 'bookings/create.html', ctx,
                   apartment_classes=APARTMENT_CLASSES, error=None)

    @classmethod
    def create_booking(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_client(ctx, resp):
            return
        data = ctx.form_data()
        try:
            guests_count = int(data.get('guests_count', 0))
            apartment_class = data.get('apartment_class', '')
            check_in = date.fromisoformat(data.get('check_in', ''))
            check_out = date.fromisoformat(data.get('check_out', ''))
            notes = data.get('notes', '')
            if guests_count < 1:
                raise ValueError('Guests count must be at least 1')
            if apartment_class not in APARTMENT_CLASSES:
                raise ValueError('Invalid apartment class')
            if check_out <= check_in:
                raise ValueError('Check-out must be after check-in')
            _booking_dao.create(ctx.user_id, guests_count, apartment_class,
                                check_in, check_out, notes)
            resp.redirect('/bookings')
        except ValueError as exc:
            cls.render(resp, 'bookings/create.html', ctx,
                       apartment_classes=APARTMENT_CLASSES, error=str(exc))

    @classmethod
    def booking_detail(cls, ctx: RequestContext, resp: Response,
                       booking_id: str, **_) -> None:
        if not cls.require_auth(ctx, resp):
            return
        booking = _booking_dao.find_by_id(int(booking_id))
        if booking is None:
            resp.send_html('<h1>404 — Not Found</h1>', 404)
            return
        if ctx.role == 'client' and booking.client_id != ctx.user_id:
            resp.send_html('<h1>403 — Forbidden</h1>', 403)
            return
        available_rooms = []
        if ctx.role == 'admin' and booking.status == 'pending':
            available_rooms = _room_dao.find_available(booking.guests_count,
                                                        booking.apartment_class)
        invoice = _invoice_dao.find_by_booking(booking.id)
        room = _room_dao.find_by_id(booking.room_id) if booking.room_id else None
        client = _user_dao.find_by_id(booking.client_id)
        cls.render(resp, 'bookings/detail.html', ctx,
                   booking=booking, room=room, client=client,
                   invoice=invoice, available_rooms=available_rooms)

    @classmethod
    def approve_booking(cls, ctx: RequestContext, resp: Response,
                        booking_id: str, **_) -> None:
        if not cls.require_admin(ctx, resp):
            return
        data = ctx.form_data()
        room_id = int(data.get('room_id', 0))
        booking = _booking_dao.find_by_id(int(booking_id))
        room = _room_dao.find_by_id(room_id)
        if not booking or not room:
            resp.send_html('<h1>404 — Not Found</h1>', 404)
            return
        _booking_dao.approve(booking.id, room_id)
        _room_dao.set_availability(room_id, False)
        amount = booking.nights * room.price_per_day
        _invoice_dao.create(booking.id, amount)
        logger.info("Booking %s approved; invoice generated for $%.2f", booking.id, amount)
        resp.redirect(f'/bookings/{booking_id}')

    @classmethod
    def reject_booking(cls, ctx: RequestContext, resp: Response,
                       booking_id: str, **_) -> None:
        if not cls.require_admin(ctx, resp):
            return
        _booking_dao.reject(int(booking_id))
        resp.redirect('/bookings')
