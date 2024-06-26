"""
mlte/store/user/underlying/memory.py

Implementation of in-memory user store.
"""

from __future__ import annotations

from typing import Dict, List, Union

import mlte.store.error as errors
from mlte.store.base import StoreURI
from mlte.store.user.store import UserStore, UserStoreSession
from mlte.user.model import BasicUser, User, UserCreate
from mlte.user.model_logic import convert_to_hashed_user, update_user

# -----------------------------------------------------------------------------
# Memory Store
# -----------------------------------------------------------------------------


class InMemoryUserStore(UserStore):
    """An in-memory implementation of the MLTE user store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage = MemoryUserStorage()
        """The underlying storage for the store."""

        # Initialize default user.
        self._init_default_user()

    def session(self) -> InMemoryUserStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return InMemoryUserStoreSession(storage=self.storage)


class MemoryUserStorage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.users: Dict[str, User] = {}


# -----------------------------------------------------------------------------
# InMemoryStoreSession
# -----------------------------------------------------------------------------


class InMemoryUserStoreSession(UserStoreSession):
    """An in-memory implementation of the MLTE user store."""

    def __init__(self, *, storage: MemoryUserStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        # Closing an in-memory session is a no-op.
        pass

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_user(self, user: UserCreate) -> User:
        if user.username in self.storage.users:
            raise errors.ErrorAlreadyExists(f"User {user.username}")

        # Create user with hashed passwords.
        stored_user = convert_to_hashed_user(user)
        self.storage.users[user.username] = stored_user
        return stored_user

    def edit_user(self, user: Union[UserCreate, BasicUser]) -> User:
        if user.username not in self.storage.users:
            raise errors.ErrorNotFound(f"User {user.username}")

        curr_user = self.storage.users[user.username]
        updated_user = update_user(curr_user, user)
        self.storage.users[user.username] = updated_user
        return updated_user

    def read_user(self, username: str) -> User:
        if username not in self.storage.users:
            raise errors.ErrorNotFound(f"User {username}")
        return self.storage.users[username]

    def list_users(self) -> List[str]:
        return [username for username in self.storage.users.keys()]

    def delete_user(self, username: str) -> User:
        if username not in self.storage.users:
            raise errors.ErrorNotFound(f"User {username}")

        popped = self.storage.users[username]
        del self.storage.users[username]
        return popped
