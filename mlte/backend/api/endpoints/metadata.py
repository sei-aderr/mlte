"""
mlte/backend/api/endpoints/metadata.py

Endpoints for artifact organization.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte.backend.api import dependencies
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.context.model import Model, ModelCreate, Version, VersionCreate

# The router exported by this submodule
router = APIRouter()


@router.post("/model")
def create_model(
    *,
    model: ModelCreate,
    current_user: AuthorizedUser,
) -> Model:
    """
    Create a MLTE model.
    :param model: The model create model
    :return: The created model
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.create_model(model)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/model/{model_id}")
def read_model(
    *,
    model_id: str,
    current_user: AuthorizedUser,
) -> Model:
    """
    Read a MLTE model.
    :param model_id: The model identifier
    :return: The read model
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.read_model(model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/model")
def list_models(
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE models.
    :return: A collection of model identifiers
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.list_models()
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/model/{model_id}")
def delete_model(
    *,
    model_id: str,
    current_user: AuthorizedUser,
) -> Model:
    """
    Delete a MLTE model.
    :param model_id: The model identifier
    :return: The deleted model
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.delete_model(model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.post("/model/{model_id}/version")
def create_version(
    *,
    model_id: str,
    version: VersionCreate,
    current_user: AuthorizedUser,
) -> Version:
    """
    Create a MLTE version.
    :param model_id: The model identifier
    :param version: The version create model
    :return: The created version
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.create_version(model_id, version)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/model/{model_id}/version/{version_id}")
def read_version(
    *,
    model_id: str,
    version_id,
    current_user: AuthorizedUser,
) -> Version:
    """
    Read a MLTE version.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The read version
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.read_version(model_id, version_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/model/{model_id}/version")
def list_versions(
    model_id: str,
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE versions for the provided model.
    :param model_id: The model identifier
    :return: A collection of version identifiers
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.list_versions(model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/model/{model_id}/version/{version_id}")
def delete_version(
    *,
    model_id: str,
    version_id,
    current_user: AuthorizedUser,
) -> Version:
    """
    Delete a MLTE version.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The deleted version
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.delete_version(model_id, version_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )
