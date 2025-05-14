"""
user.py

Defines Pydantic schemas for user-related operations.

Schemas:
- UserBase: Base schema for user details.
- UserCreate: Schema for user registration.
- UserResponse: Schema for user response data.
- UserLogin: Schema for user login credentials.

Features:
- Provides standardized representation for user operations.
- Includes validation and examples for API documentation.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict


class UserBasePostgres(BaseModel):
    """
    Base schema for user details.

    Attributes:
        username (Str): The username of the user.
        full_name (str): The full name of the user.
    """

    username: str = Field(..., json_schema_extra={"example": "jane.doe"})
    full_name: str = Field(
        ..., min_length=3, max_length=100, json_schema_extra={"example": "Jane Doe"}
    )


class UserCreatePostgres(UserBasePostgres):
    """
    Schema for user registration.

    Extends:
        UserBase

    Attributes:
        password (str): The plain-text password for the user.
    """

    password: str = Field(
        ..., min_length=8, json_schema_extra={"example": "Passw0rd123!"}
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
        Validates the password field to ensure it meets security requirements.

        Raises:
            ValueError: If the password does not meet strength requirements.
        """
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number.")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter.")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "jane.doe",
                "full_name": "Jane Doe",
                "password": "Passw0rd123!",
            }
        }
    )


class UserResponsePostgres(UserBasePostgres):
    """
    Schema for user response data.

    Extends:
        UserBase

    Attributes:
        id (str): The unique identifier for the user.
    """

    id: str = Field(..., json_schema_extra={"example": "507f1f77bcf86cd799439011"})

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "username": "jane.doe",
                "full_name": "Jane Doe",
            }
        }
    )


class UserLoginPostgres(BaseModel):
    """
    Schema for user login credentials.

    Attributes:
        username (str): The username of the user.
        password (str): The plain-text password of the user.
    """

    username: str = Field(..., json_schema_extra={"username": "jane.doe"})
    password: str = Field(
        ..., min_length=8, json_schema_extra={"example": "Passw0rd123!"}
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "jane.doe",
                "password": "Passw0rd123!",
            }
        }
    )
