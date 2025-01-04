from typing import List, Tuple, Union, Optional
from dataclasses import dataclass

# Define Record class
@dataclass
class Record:
    id: str
    fields: List[Tuple[str, str]]  # List of tuples (Text, Text)

# Define Field class
@dataclass
class Field:
    name: str
    unique: bool
    fieldType: str

# Define Result Variants
@dataclass
class Result:
    ok: Optional[bool] = None
    err: Optional[str] = None

@dataclass
class Result1:
    ok: Optional[List[Record]] = None
    err: Optional[str] = None

@dataclass
class Result2:
    ok: Optional[List[str]] = None
    err: Optional[str] = None

@dataclass
class Result3:
    ok: Optional[str] = None
    err: Optional[str] = None

@dataclass
class Result4:
    ok: Optional[Tuple[int, int]] = None
    err: Optional[str] = None

# Define Schema class
@dataclass
class Schema:
    schemaName: str
    createdAt: int
    fields: List[Field]
    indexes: List[str]

# Define Service with methods
class Service:
    def create_record_data(self, schema_name: str, record: Record) -> Result:
        # Implement the functionality
        pass

    def create_schema(self, schema_name: str, fields: List[Field], indexes: List[str]) -> Result:
        # Implement the functionality
        pass

    def delete_all_records(self, schema_name: str) -> Result:
        # Implement the functionality
        pass

    def delete_record(self, schema_name: str, record_id: str) -> Result:
        # Implement the functionality
        pass

    def delete_records_by_index(self, schema_name: str, index_name: str, value: str) -> Result:
        # Implement the functionality
        pass

    def delete_schema(self, schema_name: str) -> Result:
        # Implement the functionality
        pass

    def get_all_records(self, schema_name: str) -> Result1:
        # Implement the functionality
        pass

    def get_metrics(self, schema_name: str) -> Result4:
        # Implement the functionality
        pass

    def get_owner(self) -> str:
        # Return the owner principal
        pass

    def get_record(self, schema_name: str, record_id: str) -> Result3:
        # Implement the functionality
        pass

    def get_record_sizes(self, schema_name: str) -> Result2:
        # Implement the functionality
        pass

    def get_schema(self, schema_name: str) -> Optional[Schema]:
        # Implement the functionality
        pass

    def init_owner(self) -> bool:
        # Initialize the owner
        pass

    def list_schemas(self) -> List[str]:
        # Return a list of schemas
        pass

    def no_of_schema(self) -> int:
        # Return the number of schemas
        pass

    def search_by_index(self, schema_name: str, index_name: str, value: str) -> Result1:
        # Implement the functionality
        pass

    def search_by_multiple_fields(self, schema_name: str, fields: List[Tuple[str, str]]) -> Result1:
        # Implement the functionality
        pass

    def update_data(self, schema_name: str, record_id: str, updates: List[Tuple[str, str]]) -> Result:
        # Implement the functionality
        pass
