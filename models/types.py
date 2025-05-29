from typing import Dict, List

from pydantic import BaseModel


class PageContent(BaseModel):
    upper_page: List[str]
    lower_page: List[str]


class Document(BaseModel):
    pages: Dict[int, PageContent]
