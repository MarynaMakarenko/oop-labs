import logging

from app.controllers.auth_controller import AuthController
from app.controllers.booking_controller import BookingController
from app.controllers.dashboard_controller import DashboardController
from app.controllers.invoice_controller import InvoiceController
from app.controllers.room_controller import RoomController
from app.core.router import router
from app.core.server import run_server

logger = logging.getLogger(__name__)


def register_routes() -> None:
    # Auth
    router.get('/login',  AuthController.login_page)
    router.post('/login', AuthController.login)
    router.get('/logout', AuthController.logout)
    router.post('/logout', AuthController.logout)

    # Dashboard
    router.get('/',          DashboardController.dashboard)
    router.get('/dashboard', DashboardController.dashboard)

    # Bookings
    router.get('/bookings',                         BookingController.list_bookings)
    router.get('/bookings/new',                     BookingController.create_booking_page)
    router.post('/bookings/new',                    BookingController.create_booking)
    router.get('/bookings/:booking_id',             BookingController.booking_detail)
    router.post('/bookings/:booking_id/approve',    BookingController.approve_booking)
    router.post('/bookings/:booking_id/reject',     BookingController.reject_booking)

    # Rooms
    router.get('/rooms',               RoomController.list_rooms)
    router.get('/rooms/new',           RoomController.create_room_page)
    router.post('/rooms/new',          RoomController.create_room)
    router.get('/rooms/:room_id/edit', RoomController.edit_room_page)
    router.post('/rooms/:room_id/edit',RoomController.edit_room)
    router.post('/rooms/:room_id/delete', RoomController.delete_room)

    # Invoices
    router.get('/invoices',                      InvoiceController.list_invoices)
    router.post('/invoices/:invoice_id/pay',     InvoiceController.pay_invoice)


if __name__ == '__main__':
    register_routes()
    logger.info("Routes registered. Starting server...")
    run_server()
