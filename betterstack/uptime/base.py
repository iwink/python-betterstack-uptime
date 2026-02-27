"""Base classes for BetterStack API objects."""

from __future__ import annotations

import sys
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from .exceptions import ValidationError
from .helpers import filter_on_attribute

if TYPE_CHECKING:
    from .api import RESTAPI, PaginatedAPI


@dataclass
class BaseAPIObject:
    """Base class for all API objects using dataclasses.

    This class provides common functionality for all BetterStack API objects:
    - Automatic attribute assignment from API responses
    - Change tracking for efficient updates (only modified fields are sent)
    - CRUD operations (fetch, save, delete)
    - Class methods for querying and creating objects

    The hybrid approach stores known fields as dataclass fields with proper types,
    while unknown fields from the API are stored in the `_extras` dictionary.

    Attributes:
        id: The unique identifier for this object.
        _api: Reference to the API client (excluded from repr/compare).
        _extras: Dictionary for storing unknown API attributes.
        _original_values: Snapshot of values when object was loaded/saved.
    """

    # Instance fields
    id: int
    _api: RESTAPI = field(repr=False, compare=False)
    _extras: dict[str, Any] = field(default_factory=dict, repr=False, compare=False)
    _original_values: dict[str, Any] = field(default_factory=dict, repr=False, compare=False)

    # Class-level configuration (not dataclass fields)
    _url_endpoint: ClassVar[str]
    _allowed_query_parameters: ClassVar[list[str]] = []
    _known_fields: ClassVar[set[str]] = set()

    def __post_init__(self) -> None:
        """Initialize tracking after dataclass __init__."""
        self._snapshot_original()

    def _snapshot_original(self) -> None:
        """Capture current state for dirty tracking."""
        self._original_values = self._get_all_attribute_values()

    def _get_all_attribute_values(self) -> dict[str, Any]:
        """Get all attribute values (declared fields + extras).

        Returns:
            Dictionary of all current attribute values.
        """
        values = {}

        # Get values from known fields (defined in subclasses)
        for field_name in self._get_known_fields():
            if hasattr(self, field_name):
                values[field_name] = getattr(self, field_name)

        # Include extras
        values.update(self._extras)

        return values

    @classmethod
    def _get_known_fields(cls) -> set[str]:
        """Get set of known field names for this class.

        Returns:
            Set of field names that are explicitly defined.
        """
        if cls._known_fields:
            return cls._known_fields

        # Get field names from dataclass, excluding private/internal fields
        from dataclasses import fields as dataclass_fields

        known = set()
        for f in dataclass_fields(cls):
            if not f.name.startswith("_") and f.name != "id":
                known.add(f.name)
        return known

    def _set_attribute(self, name: str, value: Any) -> None:
        """Set an attribute, using extras for unknown fields.

        Args:
            name: Attribute name.
            value: Attribute value.
        """
        known_fields = self._get_known_fields()
        if name in known_fields or hasattr(self.__class__, name):
            setattr(self, name, value)
        else:
            self._extras[name] = value

    def _get_attribute(self, name: str) -> Any:
        """Get an attribute, checking extras for unknown fields.

        Args:
            name: Attribute name.

        Returns:
            The attribute value, or None if not found.
        """
        if hasattr(self, name) and not name.startswith("_"):
            return getattr(self, name)
        return self._extras.get(name)

    def get_modified_properties(self) -> list[str]:
        """Return list of modified property names since last save/fetch.

        Returns:
            List of attribute names that have been modified.
        """
        current = self._get_all_attribute_values()
        modified = []

        for key, value in current.items():
            original = self._original_values.get(key)
            if value != original:
                modified.append(key)

        return modified

    def reset_variable_tracking(self) -> None:
        """Reset change tracking to current state."""
        self._snapshot_original()

    def generate_url(self) -> str:
        """Create the URL for this specific instance.

        Returns:
            Full instance URL path.
        """
        return f"{self._url_endpoint}/{self.id}"

    @classmethod
    def generate_global_url(cls) -> str:
        """Get the collection URL for this object type.

        Returns:
            Collection URL path.
        """
        return cls._url_endpoint

    def fetch_data(self, **kwargs: Any) -> None:
        r"""Fetch all attributes from the API.

        Args:
            \*\*kwargs: Additional parameters for the API request.
        """
        data = next(self._api.get(self.generate_url(), parameters=kwargs))
        for key, value in data.get("attributes", {}).items():
            self._set_attribute(key, value)
        self.reset_variable_tracking()

    def save(self) -> None:
        """Update all changed attributes on the API.

        Only sends modified attributes to minimize API payload.
        """
        modified = self.get_modified_properties()
        if not modified:
            return

        data = {}
        for var in modified:
            data[var] = self._get_attribute(var)

        response = self._api.patch(self.generate_url(), body=data)
        response_data = response.json()

        # Update local state with response
        for key, value in response_data.get("data", {}).get("attributes", {}).items():
            self._set_attribute(key, value)

        self.reset_variable_tracking()

    def delete(self) -> None:
        """Delete this object from the API."""
        self._api.delete(url=self.generate_url())

    @classmethod
    def get_or_create(cls, api: RESTAPI, **kwargs: Any) -> tuple[bool, Self]:
        r"""Get an existing object or create a new one.

        Attempts to find an object matching the given attributes. If no match
        is found, creates a new object with those attributes.

        Args:
            api: API instance.
            \*\*kwargs: Attributes to search for or use when creating.

        Returns:
            Tuple of (created: bool, object: BaseAPIObject).
            created is True if a new object was created.

        Raises:
            ValueError: If multiple objects match the criteria.
        """
        try:
            instances = list(cls.filter(api, **kwargs))
        except (ValueError, ValidationError):
            # Filter not supported, fall back to get all and filter locally
            instances = list(cls.get_all_instances(api))
            for key, value in kwargs.items():
                instances = filter_on_attribute(instances, key, value)

        if len(instances) > 1:
            raise ValueError(
                f"Multiple matches on get_or_create for {cls.__name__}, expected unique match"
            )
        elif len(instances) == 0:
            return True, cls.new(api, **kwargs)
        else:
            return False, instances[0]

    @classmethod
    def new(cls, api: RESTAPI, **kwargs: Any) -> Self:
        r"""Create a new object on the API.

        Args:
            api: API instance.
            \*\*kwargs: Attributes for the new object.

        Returns:
            The newly created object.
        """
        response = api.post(cls.generate_global_url(), body=kwargs)
        response_data = response.json()
        return cls._from_api_response(api, response_data["data"])

    @classmethod
    def filter(cls, api: RESTAPI, **kwargs: Any) -> Generator[Self, None, None]:
        r"""Filter objects using URL query parameters.

        Args:
            api: API instance.
            \*\*kwargs: Query parameters to filter by.

        Yields:
            Objects matching the filter criteria.

        Raises:
            ValidationError: If a filter parameter is not allowed.
        """
        cls._validate_query_options(**kwargs)
        data = api.get(cls.generate_global_url(), parameters=kwargs)
        for item in data:
            yield cls._from_api_response(api, item)

    @classmethod
    def get_all_instances(cls, api: PaginatedAPI) -> Generator[Self, None, None]:
        """Fetch all objects of this type from the API.

        Args:
            api: API instance with pagination support.

        Yields:
            All objects of this type.
        """
        for item in api.get(cls.generate_global_url()):
            yield cls._from_api_response(api, item)

    @classmethod
    def _from_api_response(cls, api: RESTAPI, data: dict[str, Any]) -> Self:
        """Create an instance from API response data.

        This factory method handles the conversion from API JSON to
        a properly initialized object with all attributes set.

        Args:
            api: API instance.
            data: API response data with 'id' and 'attributes'.

        Returns:
            A new instance with all attributes populated.
        """
        obj = cls(id=data["id"], _api=api)
        for key, value in data.get("attributes", {}).items():
            obj._set_attribute(key, value)
        obj.reset_variable_tracking()
        return obj

    @classmethod
    def _validate_query_options(cls, **kwargs: Any) -> None:
        """Validate that query parameters are allowed for this object type.

        Args:
            **kwargs: Query parameters to validate.

        Raises:
            NotImplementedError: If _allowed_query_parameters is not defined.
            ValidationError: If class cannot be filtered or parameter not allowed.
        """
        if not hasattr(cls, "_allowed_query_parameters"):
            raise NotImplementedError(
                f"{cls.__name__}._allowed_query_parameters must be defined before filtering"
            )

        if not cls._allowed_query_parameters:
            raise ValidationError(f"{cls.__name__} does not support filtering")

        for key in kwargs.keys():
            if key not in cls._allowed_query_parameters:
                raise ValidationError(
                    f"'{key}' is not a valid query parameter for {cls.__name__}. "
                    f"Allowed: {cls._allowed_query_parameters}"
                )

    def __getattr__(self, name: str) -> Any:
        """Allow attribute access to extras for unknown fields.

        Args:
            name: Attribute name.

        Returns:
            Value from extras if it exists.

        Raises:
            AttributeError: If attribute not found.
        """
        # Avoid recursion for private attributes
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Check extras
        try:
            extras = object.__getattribute__(self, "_extras")
            if name in extras:
                return extras[name]
        except AttributeError:
            pass

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Allow setting unknown attributes to extras.

        Args:
            name: Attribute name.
            value: Attribute value.
        """
        # Check if this is a property with a setter - must use object.__getattribute__
        # to avoid recursion
        cls = type(self)
        class_attr = getattr(cls, name, None)
        if isinstance(class_attr, property) and class_attr.fset is not None:
            class_attr.fset(self, value)
            return

        # Let dataclass handle known fields and private attributes
        known_fields = {"id", "_api", "_extras", "_original_values"}
        known_fields.update(self._get_known_fields())

        if name in known_fields or name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            # Store in extras
            try:
                extras = object.__getattribute__(self, "_extras")
                extras[name] = value
            except AttributeError:
                # During initialization, extras may not exist yet
                object.__setattr__(self, name, value)
