from dataclasses import dataclass
from typing import List, Tuple, Union, Optional
from enum import Enum

# Type Definitions
@dataclass
class Field:
    name: str
    unique: bool
    fieldType: str

@dataclass
class DBRecord:
    id: str
    fields: List[Tuple[str, str]]  # List of tuples (name, value)

@dataclass
class Schema:
    schemaName: str
    createdAt: float
    fields: List[Field]
    indexes: List[str]

# Argument Type Definitions
CreateSchemaArgs = Tuple[str, List[Field], List[str]]
DeleteDataArgs = Tuple[str, str]
DeleteSchemaArgs = Tuple[str]
GetAllRecordsArgs = Tuple[str]
UpdateDataArgs = Tuple[str, str, List[Tuple[str, str]]]
InitOwnerArgs = Tuple[str]  # Assuming Principal is represented as a string in Python
GetMetricsArgs = Tuple[str]
GetRecordSizesArgs = Tuple[str]
QueryByIndexArgs = Tuple[str, str, str]
SearchByIndexArgs = Tuple[str, str, str]
SearchByMultipleFieldsArgs = Tuple[str, List[Tuple[str, str]]]
GetOwnerArgs = Tuple[()]
ListSchemasArgs = Tuple[()]
NoOfSchemaArgs = Tuple[()]
GetSchemaArgs = Tuple[str]
CreateRecordDataArgs = Tuple[str, DBRecord]
GetRecordArgs = Tuple[str, str]

# Enum for Canister Methods
class CanisterMethod(Enum):
    CreateRecordData = 'createRecordData'
    CreateSchema = 'createSchema'
    DeleteRecord = 'deleteRecord'
    DeleteSchema = 'deleteSchema'
    GetAllRecords = 'getAllRecords'
    UpdateData = 'updateData'
    InitOwner = 'initOwner'
    GetMetrics = 'getMetrics'
    GetRecordSizes = 'getRecordSizes'
    QueryByIndex = 'queryByIndex'
    SearchByIndex = 'searchByIndex'
    SearchByMultipleFields = 'searchByMultipleFields'
    GetOwner = 'getOwner'
    ListSchemas = 'listSchemas'
    NoOfSchema = 'noOfSchema'
    GetSchema = 'getSchema'
    GetRecord = 'getRecord'
