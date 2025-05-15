# framework/builder.py
import uuid
from typing import List, Type, Dict, Any, Optional, Union, TypeVar
from fastapi import FastAPI, APIRouter, HTTPException, Depends, Body, Query, status
from pydantic import BaseModel, create_model
from pydantic_core import PydanticUndefined

from .datastore import DataStore, IdType  # Use the IdType from datastore

# Define a generic type for the ID based on the datastore's ID type
BuilderIdType = TypeVar("BuilderIdType")


class CrudApiBuilder:
    """
    Builds FastAPI CRUD endpoints for a list of Pydantic models.
    """

    def __init__(
        self,
        models: List[Type[BaseModel]],
        data_store: DataStore[BuilderIdType],  # Use generic DataStore
        id_field: str = "id",
        id_type: Type[BuilderIdType] = uuid.UUID,  # Default ID type
        api_prefix: str = "/api",
        allow_id_updates: bool = False,  # Control if ID can be updated via PUT
    ):
        """
        Initializes the CrudApiBuilder.

        Args:
            models: A list of Pydantic model classes representing the entities.
            data_store: An instance of a class implementing the DataStore protocol.
            id_field: The name of the field used as the unique identifier in the models.
            id_type: The Python type of the identifier field (e.g., int, str, uuid.UUID).
            api_prefix: The prefix for all generated API routes.
            allow_id_updates: If True, allows the ID field to be present in PUT request bodies
                              (but the datastore should prevent changing it). If False, excludes
                              the ID field from the auto-generated Update model.
        """
        if not models:
            raise ValueError("At least one Pydantic model must be provided.")

        self.models = models
        self.data_store = data_store
        self.id_field = id_field
        self.id_type = id_type  # Store the actual ID type
        self.api_prefix = api_prefix
        self.allow_id_updates = allow_id_updates
        self._validate_models()

        # Initialize the data store with the models
        self.data_store.initialize(self.models, self.id_field)

        self.router = APIRouter(prefix=self.api_prefix)
        self._create_models: Dict[str, Type[BaseModel]] = {}
        self._update_models: Dict[str, Type[BaseModel]] = {}

        self._build_routes()

    def _validate_models(self):
        """Ensure all models have the specified id_field."""
        for model in self.models:
            if self.id_field not in model.model_fields:
                raise ValueError(
                    f"Model '{model.__name__}' does not have the specified "
                    f"id_field: '{self.id_field}'"
                )
            if model.model_fields[self.id_field].annotation != self.id_type:
                print(
                    f"Warning: Model '{model.__name__}' id_field '{self.id_field}' type "
                    f"({model.model_fields[self.id_field].annotation}) does not match "
                    f"specified id_type ({self.id_type}). Ensure consistency."
                )

    def _get_entity_name(self, model: Type[BaseModel]) -> str:
        """Returns the lowercase name of the model class."""
        return model.__name__.lower()

    def _generate_create_model(self, model: Type[BaseModel]) -> Type[BaseModel]:
        """Generates a Pydantic model for creation (ID might be optional or excluded)."""
        entity_name = self._get_entity_name(model)
        if entity_name in self._create_models:
            return self._create_models[entity_name]

        fields = {}
        for name, field_info in model.model_fields.items():
            if name == self.id_field:
                # Make ID optional on creation, DataStore will generate if needed
                # Use default=None and annotation=Optional[id_type]
                fields[name] = (Optional[self.id_type], None)
            else:
                # Keep original field definition (type hint and default)
                fields[name] = (field_info.annotation, field_info.default)

        create_model_name = f"{model.__name__}Create"
        created_model = create_model(
            create_model_name,
            **fields,
            __base__=None,  # No base class initially needed
            __module__=model.__module__,  # Keep the same module context
        )
        self._create_models[entity_name] = created_model
        return created_model

    def _generate_update_model(self, model: Type[BaseModel]) -> Type[BaseModel]:
        """
        Generates a Pydantic model for updates (all fields optional, ID excluded unless allowed).
        """
        entity_name = self._get_entity_name(model)
        if entity_name in self._update_models:
            return self._update_models[entity_name]

        fields = {}
        for name, field_info in model.model_fields.items():
            # Exclude the ID field unless explicitly allowed
            if name == self.id_field and not self.allow_id_updates:
                continue

            # Make all other fields optional for PATCH-like updates via PUT/PATCH
            # We use PydanticUndefined as default to distinguish between
            # a field explicitly set to None vs. a field not provided.
            # For simplicity here, we'll make them Optional[Type] with default=None
            # A more advanced version could use exclude_unset=True in the route.
            if field_info.is_required():
                fields[name] = (Optional[field_info.annotation], None)
            else:
                # If already optional or has a default, keep its nature but make sure default is None for update form
                fields[name] = (Optional[field_info.annotation], None)

        update_model_name = f"{model.__name__}Update"
        updated_model = create_model(
            update_model_name, **fields, __base__=None, __module__=model.__module__
        )
        self._update_models[entity_name] = updated_model
        return updated_model

    def _build_routes(self):
        """Generates all CRUD routes for the models and global routes."""
        print("Building API routes...")
        for model in self.models:
            entity_name = self._get_entity_name(model)
            plural_entity_name = f"{entity_name}s"  # Simple pluralization
            tags = [entity_name.capitalize()]  # Tag for Swagger UI grouping

            CreateModel = self._generate_create_model(model)
            UpdateModel = self._generate_update_model(model)

            # --- Create (POST) ---
            @self.router.post(
                f"/{plural_entity_name}",
                response_model=model,
                status_code=status.HTTP_201_CREATED,
                tags=tags,
                summary=f"Create a new {entity_name}",
            )
            async def create_item(
                item_data: CreateModel,  # Use generated CreateModel
                # Dependency injection to get specific model and entity name
                model_cls: Type[BaseModel] = model,
                current_entity_name: str = entity_name,
            ):
                try:
                    # Pass data as dict, let datastore handle ID generation/validation
                    created_item = self.data_store.create(
                        current_entity_name, item_data.model_dump(exclude_none=True)
                    )
                    return created_item
                except ValueError as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                    )
                except Exception as e:
                    # Catch unexpected errors
                    print(f"Error creating {current_entity_name}: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Internal server error during creation",
                    )

            # --- Read All (GET) ---
            @self.router.get(
                f"/{plural_entity_name}",
                response_model=List[model],
                tags=tags,
                summary=f"Get all {plural_entity_name}",
            )
            async def list_items(
                model_cls: Type[BaseModel] = model,  # DI
                current_entity_name: str = entity_name,
            ):
                try:
                    return self.data_store.get_all(current_entity_name)
                except Exception as e:
                    print(f"Error listing {current_entity_name}: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Internal server error",
                    )

            # --- Read One (GET) ---
            @self.router.get(
                f"/{plural_entity_name}/{{item_id}}",
                response_model=model,
                tags=tags,
                summary=f"Get a specific {entity_name} by ID",
            )
            async def get_item(
                item_id: self.id_type,  # Use the configured ID type
                model_cls: Type[BaseModel] = model,  # DI
                current_entity_name: str = entity_name,
            ):
                try:
                    item = self.data_store.get_by_id(current_entity_name, item_id)
                    if item is None:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{model_cls.__name__} with ID {item_id} not found",
                        )
                    return item
                except (
                    ValueError
                ) as e:  # Should not happen for get by id, but defensive
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                    )
                except HTTPException:
                    raise  # Re-raise HTTP exceptions
                except Exception as e:
                    print(f"Error getting {current_entity_name} {item_id}: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Internal server error",
                    )

            # --- Update (PUT) ---
            # Uses PUT for full replacement semantics according to generated UpdateModel
            # For partial updates (PATCH), the UpdateModel generation and route logic
            # would need adjustment (e.g., using model_dump(exclude_unset=True)).
            @self.router.put(
                f"/{plural_entity_name}/{{item_id}}",
                response_model=model,
                tags=tags,
                summary=f"Update an existing {entity_name}",
            )
            async def update_item(
                item_id: self.id_type,
                update_payload: UpdateModel,  # Use generated UpdateModel
                model_cls: Type[BaseModel] = model,  # DI
                current_entity_name: str = entity_name,
            ):
                # Get data dict, excluding fields not present in payload
                # Using exclude_none=True common for updates, but exclude_unset=True is better for PATCH
                update_data = update_payload.model_dump(exclude_unset=True)

                if not update_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No update data provided.",
                    )

                try:
                    updated_item = self.data_store.update(
                        current_entity_name, item_id, update_data
                    )
                    if updated_item is None:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{model_cls.__name__} with ID {item_id} not found",
                        )
                    return updated_item
                except ValueError as e:  # Catch validation errors from datastore
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                    )
                except HTTPException:
                    raise
                except Exception as e:
                    print(f"Error updating {current_entity_name} {item_id}: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Internal server error during update",
                    )

            # --- Delete (DELETE) ---
            @self.router.delete(
                f"/{plural_entity_name}/{{item_id}}",
                status_code=status.HTTP_204_NO_CONTENT,
                tags=tags,
                summary=f"Delete a {entity_name} by ID",
            )
            async def delete_item(
                item_id: self.id_type,
                model_cls: Type[BaseModel] = model,  # DI
                current_entity_name: str = entity_name,
            ):
                try:
                    deleted = self.data_store.delete(current_entity_name, item_id)
                    if not deleted:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{model_cls.__name__} with ID {item_id} not found",
                        )
                    # No content response on success (FastAPI handles status 204)
                    return None  # Must return None for 204
                except HTTPException:
                    raise
                except Exception as e:
                    print(f"Error deleting {current_entity_name} {item_id}: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Internal server error",
                    )

            print(f"  - Registered CRUD routes for: {entity_name}")

        # --- Global Export Route ---
        @self.router.get(
            "/export",
            response_model=Dict[str, List[Dict[str, Any]]],
            tags=["Global"],
            summary="Export all data as JSON",
        )
        async def export_data():
            try:
                return self.data_store.get_all_data()
            except Exception as e:
                print(f"Error during export: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to export data",
                )

        # --- Global Import Route ---
        @self.router.post(
            "/import",
            status_code=status.HTTP_202_ACCEPTED,  # Import might take time
            tags=["Global"],
            summary="Import data from JSON, replacing existing data",
        )
        async def import_data(
            import_payload: Dict[str, List[Dict[str, Any]]] = Body(...),
            force: bool = Query(
                False, description="Set to true to confirm data replacement."
            ),
        ):
            if not force:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Import replaces all existing data. Add '?force=true' query parameter to confirm.",
                )
            try:
                # Consider running this in background task for large imports
                self.data_store.replace_all_data(import_payload)
                return {
                    "message": "Data import started. Existing data is being replaced."
                }
            except (
                ValueError
            ) as e:  # Catch validation errors from datastore during import
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Import failed: {str(e)}",
                )
            except Exception as e:
                print(f"Error during import: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to import data: {str(e)}",
                )

        # --- Metadata Route (for UI generation) ---
        @self.router.get(
            "/metadata",
            tags=["Global"],
            summary="Get metadata about the managed entities and fields",
        )
        async def get_metadata():
            entities = {}
            for model in self.models:
                entity_name = self._get_entity_name(model)
                schema = model.model_json_schema()
                # Simplify schema slightly for easier UI consumption if needed
                entities[entity_name] = {
                    "name": model.__name__,
                    "plural_name": f"{entity_name}s",
                    "id_field": self.id_field,
                    "id_type": str(
                        self.id_type.__name__
                    ),  # String representation of type
                    "schema": schema,  # Full Pydantic schema
                }
            return {"api_prefix": self.api_prefix, "entities": entities}

        print(f"  - Registered global routes: /export, /import, /metadata")
        print("API route building complete.")

    def get_router(self) -> APIRouter:
        """Returns the configured APIRouter."""
        return self.router

    def attach_to_app(self, app: FastAPI):
        """Includes the generated router into a FastAPI application instance."""
        app.include_router(self.router)
        print(
            f"CRUD API routes included in FastAPI app with prefix '{self.api_prefix}'"
        )
