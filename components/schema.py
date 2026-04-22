from typing import List
from pydantic import BaseModel


class Paper(BaseModel):
    title: str
    authors: List[str]
    summary: str
    link: str
