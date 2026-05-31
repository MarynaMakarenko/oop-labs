import logging
import re
from typing import Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class Route:
    """A single URL pattern bound to an HTTP method and a handler function."""

    def __init__(self, method: str, pattern: str, handler: Callable):
        self.method = method.upper()
        self.pattern = pattern
        self.handler = handler
        # Convert :param segments to named regex groups
        self._regex = re.compile(
            '^' + re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern) + '$'
        )

    def match(self, method: str, path: str) -> Optional[Dict]:
        """Return captured path params if this route matches, else None."""
        if self.method != method.upper():
            return None
        m = self._regex.match(path.split('?')[0])
        return m.groupdict() if m else None


class Router:
    """
    Front-Controller router.

    Stores a list of Route objects and dispatches incoming requests
    to the first matching handler.
    """

    def __init__(self):
        self._routes: List[Route] = []

    def add_route(self, method: str, pattern: str, handler: Callable) -> None:
        self._routes.append(Route(method, pattern, handler))
        logger.debug("Registered %s %s -> %s", method, pattern, handler.__name__)

    def get(self, pattern: str, handler: Callable) -> None:
        self.add_route('GET', pattern, handler)

    def post(self, pattern: str, handler: Callable) -> None:
        self.add_route('POST', pattern, handler)

    def dispatch(self, method: str, path: str) -> Tuple[Optional[Callable], Dict]:
        for route in self._routes:
            params = route.match(method, path)
            if params is not None:
                logger.debug("Matched %s %s -> %s", method, path, route.handler.__name__)
                return route.handler, params
        logger.warning("No route for %s %s", method, path)
        return None, {}


router = Router()
