"""
chaya.core.model
----------------
base model for records
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BaseRecord(BaseModel):
    id: str
    type: str = Field(..., description="Record type, e.g. book, article")
    title: str
    authors: Optional[list[str]] = []
    tags: Optional[list[str]] = []
    notes: Optional[str] = None
    location: Optional[str] = None  # physical or digital location ref
    attachments: Optional[list[str]] = []  # paths or URLs
    created: date = Field(default_factory=date.today)


