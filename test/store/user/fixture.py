"""
test/store/user/fixture.py

Fixtures for MLTE user store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Generator

import pytest
from sqlalchemy.pool import StaticPool

from mlte.store.base import StoreURI, StoreURIPrefix
from mlte.store.user.factory import create_store
from mlte.store.user.underlying.fs import FileSystemUserStore
from mlte.store.user.underlying.memory import InMemoryUserStore
from mlte.store.user.underlying.rdbs.store import RelationalDBUserStore

_STORE_FIXTURE_NAMES = ["memory_store", "rdbs_store", "fs_store"]


def create_memory_store() -> InMemoryUserStore:
    return typing.cast(
        InMemoryUserStore, create_store(StoreURIPrefix.LOCAL_MEMORY[0])
    )


@pytest.fixture(scope="function")
def memory_store() -> InMemoryUserStore:
    """A fixture for an in-memory store."""
    return create_memory_store()


def create_rdbs_store() -> RelationalDBUserStore:
    return RelationalDBUserStore(
        StoreURI.from_string("sqlite+pysqlite:///:memory:"),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture(scope="function")
def rdbs_store() -> RelationalDBUserStore:
    """A fixture for an in-memory RDBS store."""
    return create_rdbs_store()


def create_fs_store(path: Path) -> FileSystemUserStore:
    return typing.cast(
        FileSystemUserStore,
        create_store(f"{StoreURIPrefix.LOCAL_FILESYSTEM[0]}{path}"),
    )


@pytest.fixture(scope="function")
def fs_store(tmp_path) -> FileSystemUserStore:
    """A fixture for an local FS store."""
    return create_fs_store(tmp_path)


def user_stores() -> Generator[str, None, None]:
    """
    Yield User store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name
