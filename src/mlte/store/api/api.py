"""
Generic API wrapper.
"""

from typing import Optional, Dict, Any

from mlte.store.api.uri import parse_uri_type, UriType
import mlte.store.api.local as local


def read_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_version: Optional[int] = None,
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.read_result(
            uri,
            model_identifier,
            model_version,
            result_identifier,
            result_version,
        )
    else:
        assert False, "Unreachable."


def write_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_data: Dict[str, Any],
    result_tag: Optional[str],
):
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        local.write_result(
            uri,
            model_identifier,
            model_version,
            result_identifier,
            result_data,
            result_tag,
        )
    else:
        assert False, "Unreachable."
