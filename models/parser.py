from typing import Dict, List

from pydantic import BaseModel


class PageSize(BaseModel):
    top: float
    left: float
    height: float
    width: float


class PageData(BaseModel):
    size: PageSize
    data: List[str]


class ParserData(BaseModel):
    pages: Dict[int, PageData]
