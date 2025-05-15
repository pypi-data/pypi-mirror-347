# framework/datastore.py
import uuid
from typing import Protocol, TypeVar, Type, List, Dict, Any, Optional, Generic
from pydantic import BaseModel
from collections import defaultdict
import copy

# Generic Type Variables
ModelType = TypeVar("ModelType", bound=BaseModel)
IdType = TypeVar("IdType")  # Type for the ID field (e.g., int, str, UUID)


class DataStore(Protocol[IdType]):
    """
    Protocol defining the interface for data storage operations.
    It's generic over the ID type used by the models.
    """

    def initialize(self, models: List[Type[BaseModel]], id_field: str) -> None:
        """Initialize the store with known model types."""
        ...

    def create(self, entity_type: str, item_data: Dict[str, Any]) -> BaseModel:
        """Create a new item."""
        ...

    def get_by_id(self, entity_type: str, item_id: IdType) -> Optional[BaseModel]:
        """Get an item by its ID."""
        ...

    def get_all(self, entity_type: str) -> List[BaseModel]:
        """Get all items of a specific type."""
        ...

    def update(
        self, entity_type: str, item_id: IdType, update_data: Dict[str, Any]
    ) -> Optional[BaseModel]:
        """Update an existing item."""
        ...

    def delete(self, entity_type: str, item_id: IdType) -> bool:
        """Delete an item by its ID. Returns True if deleted, False otherwise."""
        ...

    def get_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Export all data from the store."""
        ...

    def replace_all_data(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        """Replace all data in the store with the imported data."""
        ...

    def get_model_type(self, entity_type: str) -> Optional[Type[BaseModel]]:
        """Get the Pydantic model type for a given entity type name."""
        ...


# --- Default In-Memory Implementation ---


class InMemoryDataStore(DataStore[Any]):  # Use 'Any' for ID type initially
    """
    An in-memory implementation of the DataStore protocol.
    Stores data in nested dictionaries.
    """

    def __init__(self):
        self._data: Dict[str, Dict[Any, BaseModel]] = defaultdict(dict)
        self._models: Dict[str, Type[BaseModel]] = {}
        self._id_field: str = "id"  # Default, will be set during initialization

    def initialize(self, models: List[Type[BaseModel]], id_field: str) -> None:
        self._id_field = id_field
        self._models = {model.__name__.lower(): model for model in models}
        self._data = defaultdict(dict)  # Reset data on initialization
        print(
            f"InMemoryDataStore initialized for models: {list(self._models.keys())} with id_field='{id_field}'"
        )

    def get_model_type(self, entity_type: str) -> Optional[Type[BaseModel]]:
        return self._models.get(entity_type.lower())

    def _validate_entity_type(self, entity_type: str) -> None:
        if entity_type.lower() not in self._models:
            raise ValueError(f"Unknown entity type: {entity_type}")

    def _generate_id(self, model: Type[BaseModel]) -> Any:
        # Simple ID generation based on field type annotation
        # Assumes the id field is named correctly as per initialization
        id_field_type = model.model_fields[self._id_field].annotation
        if id_field_type == uuid.UUID:
            return uuid.uuid4()
        elif id_field_type == int:
            # Find the max current int ID for this type and add 1
            max_id = 0
            for item in self._data[model.__name__.lower()].values():
                current_id = getattr(item, self._id_field)
                if isinstance(current_id, int) and current_id > max_id:
                    max_id = current_id
            return max_id + 1
        elif id_field_type == str:
            return str(uuid.uuid4())  # Default to UUID string if type is str
        else:
            # Fallback or raise error if ID type is complex/unsupported for auto-generation
            raise TypeError(
                f"Automatic ID generation not supported for type {id_field_type}"
            )

    def create(self, entity_type: str, item_data: Dict[str, Any]) -> BaseModel:
        entity_type_lower = entity_type.lower()
        self._validate_entity_type(entity_type_lower)
        model = self._models[entity_type_lower]

        # Generate ID if not present and required
        if self._id_field not in item_data or item_data[self._id_field] is None:
            item_data[self._id_field] = self._generate_id(model)
        elif item_data[self._id_field] in self._data[entity_type_lower]:
            raise ValueError(
                f"{entity_type} with ID {item_data[self._id_field]} already exists."
            )

        # Validate data against the Pydantic model
        try:
            new_item = model(**item_data)
        except Exception as e:  # Catch Pydantic validation errors etc.
            raise ValueError(f"Invalid data for {entity_type}: {e}") from e

        item_id = getattr(new_item, self._id_field)
        self._data[entity_type_lower][item_id] = new_item
        print(f"Created {entity_type}: {item_id}")
        return copy.deepcopy(new_item)  # Return a copy

    def get_by_id(self, entity_type: str, item_id: Any) -> Optional[BaseModel]:
        entity_type_lower = entity_type.lower()
        self._validate_entity_type(entity_type_lower)
        item = self._data[entity_type_lower].get(item_id)
        return copy.deepcopy(item) if item else None  # Return a copy

    def get_all(self, entity_type: str) -> List[BaseModel]:
        entity_type_lower = entity_type.lower()
        self._validate_entity_type(entity_type_lower)
        # Return copies
        return [copy.deepcopy(item) for item in self._data[entity_type_lower].values()]

    def update(
        self, entity_type: str, item_id: Any, update_data: Dict[str, Any]
    ) -> Optional[BaseModel]:
        entity_type_lower = entity_type.lower()
        self._validate_entity_type(entity_type_lower)
        existing_item = self._data[entity_type_lower].get(item_id)

        if not existing_item:
            return None

        # Create a copy, update it, validate, then replace original
        updated_item_data = existing_item.model_dump()
        updated_item_data.update(update_data)

        model = self._models[entity_type_lower]
        try:
            # Validate the updated data by creating a new model instance
            validated_item = model(**updated_item_data)
        except Exception as e:  # Catch Pydantic validation errors etc.
            raise ValueError(
                f"Invalid update data for {entity_type} ID {item_id}: {e}"
            ) from e

        # Ensure ID hasn't changed if it was part of update_data
        if getattr(validated_item, self._id_field) != item_id:
            raise ValueError("Cannot change the ID of an existing item during update.")

        self._data[entity_type_lower][item_id] = validated_item
        print(f"Updated {entity_type}: {item_id}")
        return copy.deepcopy(validated_item)  # Return a copy

    def delete(self, entity_type: str, item_id: Any) -> bool:
        entity_type_lower = entity_type.lower()
        self._validate_entity_type(entity_type_lower)
        if item_id in self._data[entity_type_lower]:
            del self._data[entity_type_lower][item_id]
            print(f"Deleted {entity_type}: {item_id}")
            return True
        return False

    def get_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        export_data = {}
        for entity_type, items in self._data.items():
            export_data[entity_type] = [
                item.model_dump(mode="json") for item in items.values()
            ]
        return export_data

    def replace_all_data(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        print("Importing data...")
        new_data: Dict[str, Dict[Any, BaseModel]] = defaultdict(dict)
        errors = []

        for entity_type_lower, items_data in data.items():
            if entity_type_lower not in self._models:
                errors.append(
                    f"Import warning: Unknown entity type '{entity_type_lower}' found in import data. Skipping."
                )
                continue

            model = self._models[entity_type_lower]
            current_entity_items = {}
            for item_data in items_data:
                try:
                    # Check if ID field exists and is provided
                    if self._id_field not in item_data:
                        errors.append(
                            f"Import error: Missing ID field ('{self._id_field}') for an item of type '{entity_type_lower}'. Skipping item: {item_data}"
                        )
                        continue

                    item_id = item_data[self._id_field]
                    if item_id is None:
                        errors.append(
                            f"Import error: ID field ('{self._id_field}') cannot be null for an item of type '{entity_type_lower}'. Skipping item: {item_data}"
                        )
                        continue

                    # Attempt to parse and validate the item
                    item = model(**item_data)
                    item_id_validated = getattr(
                        item, self._id_field
                    )  # Get ID after validation

                    # Check for duplicate IDs within the import data for the same type
                    if item_id_validated in current_entity_items:
                        errors.append(
                            f"Import error: Duplicate ID '{item_id_validated}' found for entity type '{entity_type_lower}'. Skipping duplicate item: {item_data}"
                        )
                        continue

                    current_entity_items[item_id_validated] = item

                except Exception as e:  # Catch Pydantic validation errors etc.
                    errors.append(
                        f"Import validation error for {entity_type_lower}: {e}. Skipping item: {item_data}"
                    )
                    continue  # Skip this item

            new_data[entity_type_lower] = current_entity_items

        if errors:
            # Optionally raise an exception or just print warnings
            print("Import encountered issues:")
            for error in errors:
                print(f"- {error}")
            # Decide if partial import is okay or if we should abort
            # For simplicity here, we proceed with valid data but report errors.
            # raise ValueError("Import failed due to validation errors.")

        # If successful (or partially successful), replace the store's data
        self._data = new_data
        print(
            f"Import finished. Loaded {sum(len(items) for items in self._data.values())} items across {len(self._data)} entity types."
        )
