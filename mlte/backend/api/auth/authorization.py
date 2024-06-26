"""
mlte/backend/api/auth/authorization.py

Setup of OAuth based authorization checks.
"""

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

from mlte.backend.api import codes, dependencies
from mlte.backend.api.auth import jwt
from mlte.backend.api.auth.http_auth_exception import HTTPAuthException
from mlte.backend.api.endpoints.token import TOKEN_ENDPOINT_URL
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.user.model import BasicUser

# -----------------------------------------------------------------------------
# Helper functions.
# -----------------------------------------------------------------------------


async def get_resource(request: Request) -> str:
    """Gets a resource description for the current method and URL."""
    method = request.method
    url = request.url.path

    # TODO: define better way to encapsulate this.
    resource_url = url.replace(settings.API_PREFIX, "")
    resource = f"{resource_url}-{method}"
    print(f"Resource: {resource}")
    return resource


def get_username_from_token(token: str, key: str) -> str:
    """Obtains a user from an encoded token, if the token is valid."""
    # Decode token, checking for format and expiration.
    decoded_token = jwt.decode_user_token(token, key)
    return decoded_token.username


def is_authorized(current_user: BasicUser, resource: str) -> bool:
    """Checks if the current user is authorized to access the current resource."""
    # TODO: define resource names/actions as enum or similar
    # TODO: define where permissions will be stored
    # TODO: check that users have correct permissions, and return accordingly.
    # TODO: define if roles will be used for this.

    # For now any authenticated user is authorized to everything.
    print(
        f"Checking authorization for user {current_user.username} to resource {resource}"
    )
    return True


# -----------------------------------------------------------------------------
# Dep injection to get current authorized user.
# -----------------------------------------------------------------------------


# TODO: Add support for more than password grant type.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}{TOKEN_ENDPOINT_URL}"
)
"""Securty scheme to be used."""


async def get_authorized_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    resource: Annotated[str, Depends(get_resource)],
) -> BasicUser:
    """
    Given a token, gets the authenticated user and checks if it has access to resources.

    :param token: A JWT bearer access token with user information.
    :return: A User data structure, with a User that has access to the resources.
    """
    # Validate token and get username.
    try:
        username = get_username_from_token(token, state.token_key)
    except Exception as ex:
        raise HTTPAuthException(
            error="invalid_token",
            error_decription=f"Could not decode token: {ex}",
        )

    # Check if user in token exists.
    user = None
    with dependencies.user_store_session() as handle:
        user = handle.read_user(username)
    if user is None:
        raise HTTPAuthException(
            error="invalid_token",
            error_decription="Username in token was not found.",
        )

    # Check if user is enabled to be used.
    if user.disabled:
        raise HTTPException(
            status_code=codes.FORBIDDEN, detail="User is inactive"
        )

    # Check proper authorizations.
    if not is_authorized(user, resource):
        raise HTTPException(
            status_code=codes.FORBIDDEN,
            detail="User is not authorized to access this resource.",
        )

    # Convert to simple user version to avoid including hashed password.
    basic_user = BasicUser(**user.model_dump())
    return basic_user


AuthorizedUser = Annotated[BasicUser, Depends(get_authorized_user)]
"""Type alias to simplify use of get user."""
