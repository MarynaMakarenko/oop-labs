import logging

from app.controllers.base_controller import BaseController
from app.core.server import RequestContext, Response
from app.dao.room_dao import RoomDAO
from app.models.room import APARTMENT_CLASSES

logger = logging.getLogger(__name__)
_room_dao = RoomDAO()


class RoomController(BaseController):

    @classmethod
    def list_rooms(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_auth(ctx, resp):
            return
        rooms = _room_dao.find_all()
        cls.render(resp, 'rooms/list.html', ctx, rooms=rooms)

    @classmethod
    def create_room_page(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_admin(ctx, resp):
            return
        cls.render(resp, 'rooms/create.html', ctx,
                   apartment_classes=APARTMENT_CLASSES, error=None)

    @classmethod
    def create_room(cls, ctx: RequestContext, resp: Response, **_) -> None:
        if not cls.require_admin(ctx, resp):
            return
        data = ctx.form_data()
        try:
            number = data.get('number', '').strip()
            capacity = int(data.get('capacity', 0))
            apartment_class = data.get('apartment_class', '')
            price_per_day = float(data.get('price_per_day', 0))
            description = data.get('description', '')
            if not number:
                raise ValueError('Room number is required')
            if capacity < 1:
                raise ValueError('Capacity must be ≥ 1')
            if apartment_class not in APARTMENT_CLASSES:
                raise ValueError('Invalid apartment class')
            if price_per_day <= 0:
                raise ValueError('Price must be positive')
            _room_dao.create(number, capacity, apartment_class, price_per_day, description)
            resp.redirect('/rooms')
        except ValueError as exc:
            cls.render(resp, 'rooms/create.html', ctx,
                       apartment_classes=APARTMENT_CLASSES, error=str(exc))

    @classmethod
    def edit_room_page(cls, ctx: RequestContext, resp: Response,
                       room_id: str, **_) -> None:
        if not cls.require_admin(ctx, resp):
            return
        room = _room_dao.find_by_id(int(room_id))
        if not room:
            resp.send_html('<h1>404 — Not Found</h1>', 404)
            return
        cls.render(resp, 'rooms/edit.html', ctx, room=room,
                   apartment_classes=APARTMENT_CLASSES, error=None)

    @classmethod
    def edit_room(cls, ctx: RequestContext, resp: Response,
                  room_id: str, **_) -> None:
        if not cls.require_admin(ctx, resp):
            return
        data = ctx.form_data()
        try:
            _room_dao.update(
                int(room_id),
                number=data.get('number', '').strip(),
                capacity=int(data.get('capacity', 1)),
                apartment_class=data.get('apartment_class', ''),
                price_per_day=float(data.get('price_per_day', 0)),
                description=data.get('description', ''),
            )
            resp.redirect('/rooms')
        except Exception as exc:
            room = _room_dao.find_by_id(int(room_id))
            cls.render(resp, 'rooms/edit.html', ctx, room=room,
                       apartment_classes=APARTMENT_CLASSES, error=str(exc))

    @classmethod
    def delete_room(cls, ctx: RequestContext, resp: Response,
                    room_id: str, **_) -> None:
        if not cls.require_admin(ctx, resp):
            return
        _room_dao.delete(int(room_id))
        resp.redirect('/rooms')
