"""
schemas module

Defines Pydantic schemas for request and response validation in the JANUX Authentication Gateway.

Submodules:
- token: Defines schemas for token-related operations.
- user: Defines schemas for user-related operations (registration, login, response).
- response: Provides schemas for standardized API responses.

Features:
- Centralized schema management for API request/response validation.
- Custom validation rules for fields like passwords.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .token_schema import Token
from .user_schema_mongo import (
    UserBaseMongo,
    UserCreateMongo,
    UserResponseMongo,
    UserLoginMongo,
)
from .user_schema_postgres import (
    UserBasePostgres,
    UserCreatePostgres,
    UserResponsePostgres,
    UserLoginPostgres,
)
from .response_schema import ConflictResponse, ErrorResponse

__all__ = [
    "Token",
    "UserBaseMongo",
    "UserCreateMongo",
    "UserResponseMongo",
    "UserLoginMongo",
    "UserBasePostgres",
    "UserCreatePostgres",
    "UserResponsePostgres",
    "UserLoginPostgres",
    "ConflictResponse",
    "ErrorResponse",
]
