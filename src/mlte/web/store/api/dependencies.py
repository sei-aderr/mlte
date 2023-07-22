"""
mlte/web/store/api/dependencies.py

This file defines common dependencies that are used by API functions.
In practice, this ensures that the backend is initialized prior to
attempting to service any incoming requests.

Originally, I used FastAPI dependency injection to manage dependencies,
but it became so much harder to manage the fact that initialization was
occurring at import time rather than at invocation time that I removed
this in favor of slightly more brittle but eminently more workable
solution that involves manual context management with a global state object.
"""

from mlte.store.store import StoreSession
from mlte.web.store.state import state


def session() -> StoreSession:
    """
    Get a handle to underlying store session.
    :return: The session handle
    """
    return state.store.session()
