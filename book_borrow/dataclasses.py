from dataclasses import dataclass
from datetime import datetime


@dataclass
class BlockStatus:
    blocked: bool
    unblock_time: datetime


@dataclass
class BookNextAvailability:
    name: str
    current_booked_by: str
    available_at: datetime


@dataclass
class Book:
    id: int
    name: str
    author: str
    type: str
    available: bool

    @classmethod
    def get_from_model_object(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            author=model.author.name,
            type=model.type,
            available=model.available
        )


@dataclass
class User:
    id: int
    username: str
    email: str

    @classmethod
    def get_from_model_object(cls, model):
        return cls(
            id=model.id,
            username=model.username,
            email=model.email
        )