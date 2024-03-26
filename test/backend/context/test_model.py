"""
test/backend/contex/test_model.py

Test the HTTP interface for model operations.
"""

import pytest

from mlte.context.model import Model, ModelCreate

from ..fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients,
    mem_store_and_test_http_client,
)

# -----------------------------------------------------------------------------
# Tests: Model
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("client_fixture", clients())
def test_init(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """The server can initialize."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    res = client.get("/api/healthz")
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", clients())
def test_create(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be created."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model = ModelCreate(identifier="model")

    res = client.post("/api/model", json=model.model_dump())
    assert res.status_code == 200
    _ = Model(**res.json())


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be read."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model = ModelCreate(identifier="0")
    res = client.post("/api/model", json=model.model_dump())
    assert res.status_code == 200

    created = Model(**res.json())

    res = client.get("/api/model/0")
    assert res.status_code == 200
    read = Model(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be listed."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model = ModelCreate(identifier="0")

    res = client.post("/api/model", json=model.model_dump())
    assert res.status_code == 200

    res = client.get("/api/model")
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model = ModelCreate(identifier="0")

    res = client.post("/api/model", json=model.model_dump())
    assert res.status_code == 200

    res = client.get("/api/model")
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.delete("/api/model/0")
    assert res.status_code == 200

    res = client.get("/api/model")
    assert res.status_code == 200
    assert len(res.json()) == 0
