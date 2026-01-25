from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):
    """Schema for creating a user profile."""

    native_language: str = Field(default="Korean")
    target_language: str = Field(default="English")
    proficiency_level: str = Field(default="B1")
    interests: list[str] = Field(default_factory=list)


class UserProfileUpdate(BaseModel):
    """Schema for updating a user profile."""

    native_language: str | None = None
    target_language: str | None = None
    proficiency_level: str | None = None
    interests: list[str] | None = None

