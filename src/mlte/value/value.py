"""
Indicates the outcome of measurement evaluation.
"""

from __future__ import annotations
import abc

from typing import Dict, Any, Optional

from mlte._global import global_state
from mlte.store.api import read_value, write_value
from mlte.identifier import Identifier
from mlte._private.schema import VALUE_LATEST_SCHEMA_VERSION

# NOTE(Kyle): This must remain a relative import to
# circumvent a circular import issue, until we do a
# better job of decoupling some of these dependencies
from mlte.measurement_metadata.measurement_metadata import MeasurementMetadata


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Value(metaclass=abc.ABCMeta):
    """
    The Value class serves as the base class of all
    semantically-enriched measurement evaluation values.
    The Value provides a common interface for inspecting
    the results of measurement evaluation, and also
    encapsulates the functionality required to uniquely
    associate evaluation results with the originating measurement.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all Value subclasses."""
        # All subclasses of Value must define serialize() and deserialize()
        return all(
            _has_callable(subclass, method)
            for method in ["serialize", "deserialize"]
        )

    def __init__(self, instance, measurement_metadata: MeasurementMetadata):
        """
        Initialize a Value instance.

        :param instance: The subclass instance
        :type instance: Value
        :param measurement_metadata: The generating measurement's metadata
        :type measurement: MeasurementMetadata
        """
        self.identifier: Identifier = measurement_metadata.identifier
        """The identifier for the value"""

        self.measurement_typename = measurement_metadata.typename
        """The type of the generating measurement."""

        self.typename = type(instance).__name__
        """The type of the value itself."""

    @abc.abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """TODO"""
        raise NotImplementedError("Cannot serialize abstract Value.")

    @staticmethod
    @abc.abstractmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json: Dict[str, Any]
    ) -> Any:
        """TODO"""
        raise NotImplementedError("Cannot deserialize abstract Value.")

    def save(self, tag: Optional[str] = None):
        """
        Save value data to the configured artifact store.

        :param tag: An optional tag to identify groups of results
        :type tag: str
        """
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Use API to save to artifact store
        write_value(
            artifact_store_uri,
            model_identifier,
            model_version,
            self.identifier.name,
            {
                "schema_version": VALUE_LATEST_SCHEMA_VERSION,
                "metadata": self._serialize_metadata(),
                "payload": {**self.serialize()},
            },
            tag,
        )

    @classmethod
    def load(cls, identifier: str, version: Optional[int] = None) -> Value:
        """
        Load non-semantically-enriched value data from an artifact store.
        This data may then be passed to the type-specific load() method to
        fully-reconstruct the loaded value.

        :param identifier: The identifier for the value
        :type identifier: str
        :param version: The optional version identifier; when not specified,
        the latest version of the value is read
        :type version: int

        :return: The loaded value
        :rtype: Value
        """
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Use API to load from artifact store
        json = read_value(
            artifact_store_uri,
            model_identifier,
            model_version,
            identifier,
            version,
        )

        # TODO: Validate response

        metadata = json["metadata"]
        value: Value = cls.deserialize(
            MeasurementMetadata(
                metadata["measurement"]["typename"],
                Identifier.from_json(metadata["identifier"]),
            ),
            json["payload"],
        )
        return value

    def _serialize_metadata(self) -> Dict[str, Any]:
        """Return the header for serialization."""
        return {
            "identifier": self.identifier.to_json(),
            "measurement": {"typename": self.measurement_typename},
            "value": {"typename": self.typename},
        }
