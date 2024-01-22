from typing import Optional, List

from beanie import Document
from pydantic import BaseModel


class Event(Document):
    creator: Optional[str]
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Settings:
        name = "events"