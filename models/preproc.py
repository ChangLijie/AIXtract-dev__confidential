from typing import Dict, List

from pydantic import BaseModel


class PageContent(BaseModel):
    data: Dict[int, List[str]]


class PreProcData(BaseModel):
    pages: Dict[int, PageContent]
