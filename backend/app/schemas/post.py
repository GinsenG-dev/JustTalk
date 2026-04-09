from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class PostCreate(BaseModel):
    title: str = Field(max_length=200)
    body: str = Field(max_length=10_000)

    @field_validator("title", "body")
    @classmethod
    def strip_nonempty(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("must not be empty")
        return s


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    body: str | None = Field(default=None, max_length=10_000)

    @field_validator("title", "body")
    @classmethod
    def strip_if_set(cls, v: str | None) -> str | None:
        if v is None:
            return None
        s = v.strip()
        if not s:
            raise ValueError("must not be empty")
        return s

    @model_validator(mode="after")
    def at_least_one_field(self) -> "PostUpdate":
        if self.title is None and self.body is None:
            raise ValueError("at least one of title, body is required")
        return self


class PostAuthorOut(BaseModel):
    id: int
    username: str
    display_name: str | None = None

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    updated_at: datetime
    author: PostAuthorOut

    class Config:
        from_attributes = True
